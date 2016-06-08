# Testing

The tests in this repository are system tests and run against live services, therefore, it takes a bit of configuration to run all of the tests locally.

Before you can run tests locally you must have:

* The latest [nox](https://nox.readthedocs.org/en/latest/),
  [pip](https://pypi.python.org/pypi/pip), and [gcp-python-repo-tools](https://pypi.python.org/pypi/gcp-python-repo-tools) installed.

        $ sudo pip install --upgrade nox-automation

* The [Google Cloud SDK](https://cloud.google.com/sdk/) installed. You
  can do so with the following command:

        $ curl https://sdk.cloud.google.com | bash

## Preparing a project for testing

Most tests require you to have an active, billing-enabled project on the
[Google Cloud Console](https://console.cloud.google.com).

### Creating resources

Some resources need to be created in a project ahead of time before testing. We have a script that can create everything needed:

    gcloud config set project <your-project-id>
    scripts/prepare-testing-project.sh

The script will also instruct you to follow a URL to enable APIs. You will need to do that.

### Getting a service account key

From the Cloud Console, create a new Service Account and download its json key. Place this file in `testing/resources/service-account.json`.

Create a new OAuth client ID. Create a file `testing/resources/client-secrets.json` and write the `client_id` and `client_secret` to the file in the [Client Secrets JSON format](https://developers.google.com/api-client-library/python/guide/aaa_client_secrets).

## Environment variables

* Copy `testing/resources/test-env.tmpl.sh` to `testing/resources/test-env.sh`, and updated it with your configuration.
* Run `source testing/resources/test-env.sh`.
* Run `export GOOGLE_APPLICATION_CREDENTIALS=testing/resources/service-account.json`.
* Run `export GOOGLE_CLIENT_SECRETS=testing/resources/client-secrets.json`.

### Test environments

We use [nox](https://nox.readthedocs.org/en/latest/) to configure
multiple python sessions:

* ``tests`` contains tests for samples that run in a normal Python 2.7 or 3.4
  environment. This is everything outside of the ``appengine`` directory. It's
  parameterized to run all the tests using the 2.7 and 3.4 interpreters.
* ``gae`` contains tests for samples that run only in Google App Engine. This is
  (mostly) everything in the ``appengine`` directory.
* ``lint`` just runs the linter.

To see a list of the available sessions:

    nox -l

To run tests for a particular session, with a particular parameter, invoke nox
with the ``-s`` flag:

    nox -s "tests(interpreter='python2.7')"

To run one particular session or provide additional parameters to ``py.test``,
invoke nox like this:

    nox -s tests -- storage/api

### Adding new tests
When adding a new top-level directory, be sure to edit ``.coveragerc`` to
include it in coverage reporting.

To add new tests that require Google App Engine, you must place them in
the ``appengine`` directory so that the py.test fixtures needed for App
Engine are available.
