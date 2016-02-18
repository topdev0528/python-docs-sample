# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from compose_objects import main
from testing import CloudTest


class TestComposeObjects(CloudTest):
    def test_main(self):
        main(
            self.config.CLOUD_STORAGE_BUCKET,
            'dest.txt',
            [self.resource_path('file1.txt'),
             self.resource_path('file2.txt')]
        )
