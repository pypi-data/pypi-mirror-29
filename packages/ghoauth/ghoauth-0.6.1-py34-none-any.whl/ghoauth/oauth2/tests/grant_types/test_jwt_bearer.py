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

from datetime import (
    datetime,
    timezone,
)
from unittest import TestCase

from ghoauth.oauth2.errors import (
    InvalidGrantError,
    InvalidRequestError,
    InvalidScopeError,
)
from ghoauth.oauth2.grant_types.jwt_bearer import JWTBearerGrant
from ghoauth.oauth2.repository import (
    AbstractBaseRepository,
    JWTBearerGrantRepositoryMixin,
)
from ghoauth.oauth2.request import OAuth2Request
from ghoauth.oauth2.validator import (
    AbstractBaseValidator,
    JWTBearerGrantValidatorMixin,
)
from ghoauth.uriutils import compare_uri


class Repository(AbstractBaseRepository, JWTBearerGrantRepositoryMixin):

    def get_default_scope(self, request):
        return 'email'

    def get_key_by_jwt_headers(self, headers, client_id, request):
        return 'secretstring'

    def get_subject_by_jwt_claims(self, claims, request):
        return 'yosida95'

    def save_access_token(self, token, request):
        assert token['scope'] == 'email'


class Validator(AbstractBaseValidator, JWTBearerGrantValidatorMixin):

    def validate_scope(self, scope, request):
        return scope == 'email'

    def validate_iss(self, iss, request):
        return compare_uri(iss, 'https://jwt-idp.example.com')

    def validate_sub(self, sub, request):
        return True

    def validate_aud(self, aud, request):
        return compare_uri(aud, 'https://jwt-rp.example.net')


class JWTBearerGrantTeset(TestCase):

    def setUp(self):
        self.repository = Repository()
        self.validator = Validator()
        self.current_dt = datetime(2011, 3, 22, 17, 43, tzinfo=timezone.utc)

    def test_supported_grant_types(self):
        inst = JWTBearerGrant(datetime_factory=lambda: self.current_dt)
        self.assertEqual(inst.supported_grant_types(),
                         ['urn:ietf:params:oauth:grant-type:jwt-bearer'])

    def test_validate_token_request(self):
        request = OAuth2Request.blank(
            'https://example.com/oauth2/token',
            POST={'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                  'assertion': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYWlsdG86bWlrZUBleGFtcGxlLmNvbSIsImV4cCI6MTMwMDgxOTM4MCwibmJmIjoxMzAwODE1NzgwLCJhdWQiOiJodHRwczovL2p3dC1ycC5leGFtcGxlLm5ldCIsImlzcyI6Imh0dHBzOi8vand0LWlkcC5leGFtcGxlLmNvbSIsImh0dHA6Ly9jbGFpbXMuZXhhbXBsZS5jb20vbWVtYmVyIjp0cnVlfQ.fTxrgzdzh-sgE1in4OFbGMGTlHMd9idBLL4ezkyBcGw'})  # noqa

        inst = JWTBearerGrant(datetime_factory=lambda: self.current_dt)
        inst.validate_token_request(request, self.repository, self.validator)
        self.assertEqual(
            request._o2_jwt_claims,
            {'iss': 'https://jwt-idp.example.com',
             'sub': 'mailto:mike@example.com',
             'aud': 'https://jwt-rp.example.net',
             'nbf': 1300815780,
             'exp': 1300819380,
             'http://claims.example.com/member': True})

        before = datetime(2011, 3, 22, 17, 42, tzinfo=timezone.utc)
        inst = JWTBearerGrant(datetime_factory=lambda: before)
        with self.assertRaises(InvalidGrantError):
            inst.validate_token_request(request,
                                        self.repository, self.validator)

        expired = datetime(2011, 3, 22, 18, 44, tzinfo=timezone.utc)
        inst = JWTBearerGrant(datetime_factory=lambda: expired)
        with self.assertRaises(InvalidGrantError):
            inst.validate_token_request(request,
                                        self.repository, self.validator)

    def test_validate_token_request_missing_assertion(self):
        request = OAuth2Request.blank(
            'https://example.com/oauth2/token',
            POST={'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer'})  # noqa
        inst = JWTBearerGrant(datetime_factory=lambda: self.current_dt)
        with self.assertRaises(InvalidRequestError):
            inst.validate_token_request(request,
                                        self.repository, self.validator)

    def test_validate_token_request_with_scope(self):
        request = OAuth2Request.blank(
            'https://example.com/oauth2/token',
            POST={'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                  'assertion': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYWlsdG86bWlrZUBleGFtcGxlLmNvbSIsImV4cCI6MTMwMDgxOTM4MCwibmJmIjoxMzAwODE1NzgwLCJhdWQiOiJodHRwczovL2p3dC1ycC5leGFtcGxlLm5ldCIsImlzcyI6Imh0dHBzOi8vand0LWlkcC5leGFtcGxlLmNvbSIsImh0dHA6Ly9jbGFpbXMuZXhhbXBsZS5jb20vbWVtYmVyIjp0cnVlfQ.fTxrgzdzh-sgE1in4OFbGMGTlHMd9idBLL4ezkyBcGw',  # noqa
                  'scope': 'email'})

        inst = JWTBearerGrant(datetime_factory=lambda: self.current_dt)
        inst.validate_token_request(request, self.repository, self.validator)

    def test_validate_token_request_with_invalid_scope(self):
        request = OAuth2Request.blank(
            'https://example.com/oauth2/token',
            POST={'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                  'assertion': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYWlsdG86bWlrZUBleGFtcGxlLmNvbSIsImV4cCI6MTMwMDgxOTM4MCwibmJmIjoxMzAwODE1NzgwLCJhdWQiOiJodHRwczovL2p3dC1ycC5leGFtcGxlLm5ldCIsImlzcyI6Imh0dHBzOi8vand0LWlkcC5leGFtcGxlLmNvbSIsImh0dHA6Ly9jbGFpbXMuZXhhbXBsZS5jb20vbWVtYmVyIjp0cnVlfQ.fTxrgzdzh-sgE1in4OFbGMGTlHMd9idBLL4ezkyBcGw',  # noqa
                  'scope': 'phone'})

        inst = JWTBearerGrant(datetime_factory=lambda: self.current_dt)
        with self.assertRaises(InvalidScopeError):
            inst.validate_token_request(request,
                                        self.repository, self.validator)

    def test_validate_token_request_iss_mismatch(self):
        request = OAuth2Request.blank(
            'https://example.com/oauth2/token',
            POST={'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                  'assertion': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL21hbGljaW91cy1pZHAuZXhhbXBsZS5jb20iLCJuYmYiOjEzMDA4MTU3ODAsInN1YiI6Im1haWx0bzptaWtlQGV4YW1wbGUuY29tIiwiZXhwIjoxMzAwODE5MzgwLCJhdWQiOiJodHRwczovL2p3dC1ycC5leGFtcGxlLm5ldCIsImh0dHA6Ly9jbGFpbXMuZXhhbXBsZS5jb20vbWVtYmVyIjp0cnVlfQ.EY9ygpJP6kbmakVED226wY6bbaNsKyxZg5lrD7vkaYQ'})  # noqa

        inst = JWTBearerGrant(datetime_factory=lambda: self.current_dt)
        with self.assertRaises(InvalidGrantError):
            inst.validate_token_request(request,
                                        self.repository, self.validator)

    def test_validate_token_request_aud_mismatch(self):
        request = OAuth2Request.blank(
            'https://example.com/oauth2/token',
            POST={'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                  'assertion': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2p3dC1pZHAuZXhhbXBsZS5jb20iLCJuYmYiOjEzMDA4MTU3ODAsInN1YiI6Im1haWx0bzptaWtlQGV4YW1wbGUuY29tIiwiZXhwIjoxMzAwODE5MzgwLCJhdWQiOiJodHRwczovL21hbGljaW91cy1ycC5leGFtcGxlLmNvbSIsImh0dHA6Ly9jbGFpbXMuZXhhbXBsZS5jb20vbWVtYmVyIjp0cnVlfQ.9ioNkxKlnJapTLBRL9zhiyRdIDOY-TzoA0pSLrF0YXY'})  # noqa

        inst = JWTBearerGrant(datetime_factory=lambda: self.current_dt)
        with self.assertRaises(InvalidGrantError):
            inst.validate_token_request(request,
                                        self.repository, self.validator)

    def test_validate_token_secret_mismatch(self):
        request = OAuth2Request.blank(
            'https://example.com/oauth2/token',
            POST={'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                  'assertion': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYWlsdG86bWlrZUBleGFtcGxlLmNvbSIsImlzcyI6Imh0dHBzOi8vand0LWlkcC5leGFtcGxlLmNvbSIsImh0dHA6Ly9jbGFpbXMuZXhhbXBsZS5jb20vbWVtYmVyIjp0cnVlLCJleHAiOjEzMDA4MTkzODAsImF1ZCI6Imh0dHBzOi8vand0LXJwLmV4YW1wbGUubmV0IiwibmJmIjoxMzAwODE1NzgwfQ.mtAeY_YoHe-JNK_pzo_KQDE4TAuNTI0TSoKTzQJCp0Q'})  # noqa

        inst = JWTBearerGrant(datetime_factory=lambda: self.current_dt)
        with self.assertRaises(InvalidGrantError):
            inst.validate_token_request(request,
                                        self.repository, self.validator)

    def test_handle_token_request(self):
        request = OAuth2Request.blank(
            'https://example.com/oauth2/token',
            POST={'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                  'assertion': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYWlsdG86bWlrZUBleGFtcGxlLmNvbSIsImV4cCI6MTMwMDgxOTM4MCwibmJmIjoxMzAwODE1NzgwLCJhdWQiOiJodHRwczovL2p3dC1ycC5leGFtcGxlLm5ldCIsImlzcyI6Imh0dHBzOi8vand0LWlkcC5leGFtcGxlLmNvbSIsImh0dHA6Ly9jbGFpbXMuZXhhbXBsZS5jb20vbWVtYmVyIjp0cnVlfQ.fTxrgzdzh-sgE1in4OFbGMGTlHMd9idBLL4ezkyBcGw'})  # noqa
        request.response = response = OAuth2Request.ResponseClass()

        inst = JWTBearerGrant(datetime_factory=lambda: self.current_dt)
        inst.validate_token_request(request, self.repository, self.validator)
        inst.handle_token_request(request, self.repository)

        self.assertEqual(response.status, '200 OK')
