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

from collections import OrderedDict
from unittest import TestCase

from ghoauth.uriutils import (
    extend_uri_with_params,
    is_absolute_uri,
)


class extend_uri_with_params_test(TestCase):

    def test_it(self):
        d = OrderedDict()
        d['param_1'] = 'value_1'
        d['param_2'] = 'value_2'

        # query mode
        self.assertEqual(
            extend_uri_with_params('https://example.com/cb', d, 'query'),
            'https://example.com/cb?param_1=value_1&param_2=value_2')
        # redirect_uri with queries
        self.assertEqual(
            extend_uri_with_params('https://example.com/cb?k=v', d, 'query'),
            'https://example.com/cb?k=v&param_1=value_1&param_2=value_2')

        # fragment mode
        self.assertEqual(
            extend_uri_with_params('https://example.com/cb', d, 'fragment'),
            'https://example.com/cb#param_1=value_1&param_2=value_2')


class is_absolute_uri_test(TestCase):

    def test_it(self):
        self.assertTrue(is_absolute_uri('https://example.com/cb'))
        self.assertFalse(is_absolute_uri('urn:example:animal:ferret:nose'))
        self.assertFalse(is_absolute_uri('/cb'))
