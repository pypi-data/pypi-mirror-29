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

from webob import BaseRequest

from ghoauth.oauth2.repository import AbstractBaseRepository
from ghoauth.oauth2.request import (
    OAuth2Request,
    request_parameter,
)
from ghoauth.oauth2.validator import AbstractBaseValidator


class RequestParameterTest(TestCase):

    class Request(BaseRequest):
        o2_param = request_parameter('param')
        o2_dup = request_parameter('dup')

    def test_it(self):
        req = self.Request.blank('https://example.com/?param=value&dup=1&dup=2')  # noqa
        self.assertNotIn('oauth2.params', req.environ)

        self.assertEqual(req.o2_param, 'value')
        self.assertIsNone(req.o2_dup)

        self.assertIn('oauth2.params', req.environ)
        self.assertEqual(req.environ['oauth2.params'],
                         {'param': 'value',
                          'dup': None})

        req.o2_param = 'new_value'
        self.assertEqual(req.o2_param, 'new_value')
        self.assertIsNone(req.o2_dup)
        self.assertEqual(req.environ['oauth2.params'],
                         {'param': 'new_value',
                          'dup': None})

        with self.assertRaises(AttributeError):
            del req.o2_dup


class OAuth2RequestTest(TestCase):

    class StubRepository(AbstractBaseRepository):

        def is_client_available(self, client_id, request):
            return client_id == 'yosida95'

        def get_primary_redirect_uri(self, client_id, request):
            if client_id == 'yosida95':
                return 'https://yosida95.com/cb'
            return '/cb'

    class StubValidator(AbstractBaseValidator):

        def authenticate_client(self, request):
            return 'yosida95'

        def authenticate_client_as(self, client_id, request):
            return client_id == 'yosida95'

        def validate_redirect_uri(self, redirect_uri, client_id, request):
            return redirect_uri == 'https://yosida95.com/cb'

    def test_o2_validate(self):
        req = OAuth2Request.blank('https://example.com/?client_id=yosida95&response_type=code&scope=abc&scope=def')  # noqa

        self.assertEqual(req.o2_client_id, 'yosida95')
        self.assertEqual(req.o2_response_type, 'code')

        # requireds
        self.assertTrue(req.o2_validate(requireds={'client_id',
                                                   'response_type'}))
        # optionals
        self.assertTrue(req.o2_validate(optionals={'redirect_uri'}))
        # mix
        self.assertTrue(req.o2_validate(requireds={'client_id',
                                                   'response_type'},
                                        optionals={'redirect_uri'}))

        # a missing parameter
        self.assertFalse(req.o2_validate(requireds={'redirect_uri'}))
        # a duplicated parameter
        self.assertFalse(req.o2_validate(requireds={'scope'}))
        self.assertFalse(req.o2_validate(optionals={'scope'}))

    def test_o2_validate_redirect_uri(self):
        repo = self.StubRepository()
        valid = self.StubValidator()

        # use valid primary
        req = OAuth2Request.blank('https://example.com/?client_id=yosida95')
        self.assertTrue(req.o2_validate_redirect_uri(repo, valid))
        self.assertEqual(req.o2_redirect_uri, 'https://yosida95.com/cb')

        # use invalid primary
        req = OAuth2Request.blank('https://example.com/?client_id=yoshida95')
        self.assertFalse(req.o2_validate_redirect_uri(repo, valid))
        self.assertEqual(req.o2_redirect_uri, '/cb')

        # use query parameters with a valid value
        req = OAuth2Request.blank('https://example.com/?client_id=yosida95&redirect_uri=https://yosida95.com/cb')  # noqa
        self.assertTrue(req.o2_validate_redirect_uri(repo, valid))
        self.assertEqual(req.o2_redirect_uri, 'https://yosida95.com/cb')

        # use query parameters with a invalid value
        req = OAuth2Request.blank('https://example.com/?client_id=yosida95&redirect_uri=/cb')  # noqa
        self.assertFalse(req.o2_validate_redirect_uri(repo, valid))
        self.assertEqual(req.o2_redirect_uri, '/cb')
