#!/bin/bash
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# `-e` enables the script to automatically fail when a command fails
# `-o pipefail` sets the exit code to the rightmost comment to exit with a non-zero
set -eo pipefail
# Enables `**` to include files nested inside sub-folders
shopt -s globstar

DIFF_FROM=""

# `--only-diff-master` will only run tests on project changes on the
# last common commit from the master branch.
if [[ $* == *--only-diff-master* ]]; then
    set +e
    git diff --quiet "origin/master..." .kokoro/tests .kokoro/docker \
	.kokoro/trampoline_v2.sh
    CHANGED=$?
    set -e
    if [[ "${CHANGED}" -eq 0 ]]; then
	DIFF_FROM="origin/master..."
    else
	echo "Changes to test driver files detected. Running full tests."
    fi
fi

# `--only-diff-head` will only run tests on project changes from the
# previous commit.
if [[ $* == *--only-diff-head* ]]; then
    set +e
    git diff --quiet "HEAD~.." .kokoro/tests .kokoro/docker \
	.kokoro/trampoline_v2.sh
    CHANGED=$?
    set -e
    if [[ "${CHANGED}" -eq 0 ]]; then
	DIFF_FROM="HEAD~.."
    else
	echo "Changes to test driver files detected. Running full tests."
    fi
fi

# Because Kokoro runs presubmit builds simalteneously, we often see
# quota related errors. I think we can avoid this by changing the
# order of tests to execute (e.g. reverse order for py-3.8
# build). Currently there's no easy way to do that with btlr, so we
# temporarily wait few minutes to avoid quota issue for py-3.8
# presubmit build.
if [[ "${RUN_TESTS_SESSION}" == "py-3.8" ]] \
       && [[ "${KOKORO_JOB_NAME}" == *presubmit ]]; then
    echo -n "Detected py-3.8 presubmit build,"
    echo "Wait few minutes to avoid quota issues."
    sleep 5m
fi

if [[ -z "${PROJECT_ROOT:-}" ]]; then
    PROJECT_ROOT="github/python-docs-samples"
fi

cd "${PROJECT_ROOT}"

# add user's pip binary path to PATH
export PATH="${HOME}/.local/bin:${PATH}"

# install nox for testing
pip install --user -q nox

# Use secrets acessor service account to get secrets.
if [[ -f "${KOKORO_GFILE_DIR}/secrets_viewer_service_account.json" ]]; then
    gcloud auth activate-service-account \
	   --key-file="${KOKORO_GFILE_DIR}/secrets_viewer_service_account.json" \
	   --project="cloud-devrel-kokoro-resources"
    # This script will create 3 files:
    # - testing/test-env.sh
    # - testing/service-account.json
    # - testing/client-secrets.json
    ./scripts/decrypt-secrets.sh
fi

source ./testing/test-env.sh
export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/testing/service-account.json

# For cloud-run session, we activate the service account for gcloud sdk.
gcloud auth activate-service-account \
       --key-file "${GOOGLE_APPLICATION_CREDENTIALS}"

export GOOGLE_CLIENT_SECRETS=$(pwd)/testing/client-secrets.json

# For Datalabeling samples to hit the testing endpoint
export DATALABELING_ENDPOINT="test-datalabeling.sandbox.googleapis.com:443"

# Run Cloud SQL proxy (background process exit when script does)
wget --quiet https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 \
     -O ${HOME}/cloud_sql_proxy && chmod +x ${HOME}/cloud_sql_proxy
${HOME}/cloud_sql_proxy -instances="${MYSQL_INSTANCE}"=tcp:3306 &>> \
       ${HOME}/cloud_sql_proxy.log &
${HOME}/cloud_sql_proxy -instances="${POSTGRES_INSTANCE}"=tcp:5432 &>> \
       ${HOME}/cloud_sql_proxy-postgres.log &
echo -e "\nCloud SQL proxy started."

echo -e "\n******************** TESTING PROJECTS ********************"
# Switch to 'fail at end' to allow all tests to complete before exiting.
set +e
# Use RTN to return a non-zero value if the test fails.
RTN=0
ROOT=$(pwd)

test_prog="${PROJECT_ROOT}/.kokoro/tests/run_single_test.sh"

btlr_args=(
    "run"
    "**/requirements.txt"
)

if [[ -n "${NUM_TEST_WORKERS:-}" ]]; then
    btlr_args+=(
	"--max-concurrency"
	"${NUM_TEST_WORKERS}"
    )
fi

if [[ -n "${DIFF_FROM:-}"  ]]; then
    btlr_args+=(
	"--git-diff"
	"${DIFF_FROM} ."
    )
fi

btlr_args+=(
    "--"
    "${test_prog}"
)

echo "testing/btlr" "${btlr_args[@]}"

testing/btlr "${btlr_args[@]}"

RTN=$?
cd "$ROOT"

# Remove secrets if we used decrypt-secrets.sh.
if [[ -f "${KOKORO_GFILE_DIR}/secrets_viewer_service_account.json" ]]; then
    rm testing/{test-env.sh,client-secrets.json,service-account.json}
fi

exit "$RTN"
