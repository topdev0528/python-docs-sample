# Copyright 2014 Google Inc. All Rights Reserved.
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

"""Test classes for code snippet for modeling article."""

import contact_with_group_models as models
from google.appengine.ext import ndb
from testing import AppEngineTest


class ContactTestCase(AppEngineTest):
    """A test case for the Contact model with groups."""
    def setUp(self):
        """Creates 3 contacts and 1 group.

        Assuming the group and contacts are private and belong to tmatsuo's
        addressbook.
        """
        super(ContactTestCase, self).setUp()
        self.myaddressbook_key = ndb.Key('AddressBook', 'tmatsuo')

        friends = models.Group(parent=self.myaddressbook_key, name='friends')
        friends.put()
        self.friends_key = friends.key
        mary = models.Contact(parent=self.myaddressbook_key, name='Mary')
        mary.put()
        self.mary_key = mary.key

    def test_groups(self):
        # Add Mary to your 'friends' group
        mary = self.mary_key.get()
        friends = self.friends_key.get()
        if friends.key not in mary.groups:
            mary.groups.append(friends.key)
            mary.put()

        # Now Mary is your friend
        mary = self.mary_key.get()
        self.assertTrue(friends.key in mary.groups)

        # How about 'members' property?
        friend_list = friends.members.fetch()
        self.assertEqual(len(friend_list), 1)
