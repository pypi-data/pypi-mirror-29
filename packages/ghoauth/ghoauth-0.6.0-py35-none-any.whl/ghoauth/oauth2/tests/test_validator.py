# -*- coding: utf-8 -*-
#
# Copyright 2017 Gehirn Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import TestCase

from ghoauth.oauth2.validator import (
    normalize_response_type,
    validate_redirect_uri,
)


class normalize_response_type_test(TestCase):

    def test_it(self):
        self.assertEqual(normalize_response_type('code'),
                         'code')
        self.assertEqual(normalize_response_type('code token'),
                         'code token')
        self.assertEqual(normalize_response_type('token code'),
                         'code token')


class validate_redirect_uri_test(TestCase):

    def test_it(self):
        self.assertTrue(validate_redirect_uri('https://example.com/cb'))
        self.assertFalse(
            validate_redirect_uri('urn:example:animal:ferret:nose'))

        # with fragment
        self.assertFalse(validate_redirect_uri('https://example.com/cb#k=v'))
        # relative uri
        self.assertFalse(validate_redirect_uri('/cb'))
