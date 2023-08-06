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

from datetime import datetime

from jose import (
    JWTError,
    jwt,
)

from ghoauth.oauth2.errors import (
    InvalidGrantError,
    InvalidRequestError,
    InvalidScopeError,
    ServerError,
)
from ghoauth.oauth2.token import bearer_token_factory

from .abc import AbstractBaseGrantTypeHandler


def decode_jwt_assertion(jwt_message, decode_key, request,
                         validator, current_ts, is_authorization_grant):
    try:
        options = {'verify_signature': True,
                   'verify_iss': False,
                   'verify_sub': False,
                   'verify_aud': False,
                   'verify_exp': False,
                   'verify_nbf': False,
                   'verify_iat': False,
                   'verify_jti': False}
        jwt_claims = jwt.decode(jwt_message, decode_key, options=options)
    except JWTError:
        return None

    iss = jwt_claims.get('iss')
    if not isinstance(iss, str) or\
            not validator.validate_iss(iss, request):
        return None
    sub = jwt_claims.get('sub')
    if not isinstance(sub, str) or\
            is_authorization_grant and\
            not validator.validate_sub(sub, request):
        return None
    aud = jwt_claims.get('aud')
    if not isinstance(aud, str) or\
            not validator.validate_aud(aud, request):
        return None
    exp = jwt_claims.get('exp')
    if not isinstance(exp, int) or exp < current_ts:
        return None
    if 'nbf' in jwt_claims:
        nbf = jwt_claims['nbf']
        if not isinstance(nbf, int) or nbf > current_ts:
            return None
    if 'iat' in jwt_claims and not isinstance(jwt_claims['iat'], int):
        return None
    if 'jti' in jwt_claims and\
            not validator.validate_jti(jwt_claims['jti'], request):
        return None

    return jwt_claims


class JWTBearerGrant(AbstractBaseGrantTypeHandler):
    """
    https://tools.ietf.org/html/rfc7523
    """
    __slots__ = ['token_factory', 'datetime_factory']

    def __init__(self, token_factory=bearer_token_factory,
                 datetime_factory=datetime.now):
        self.token_factory = token_factory
        self.datetime_factory = datetime_factory

    def supported_grant_types(self):
        return ['urn:ietf:params:oauth:grant-type:jwt-bearer']

    def validate_token_request(self, request, repository, validator):
        if not request.o2_validate(requireds={'assertion'},
                                   optionals={'scope'}):
            raise InvalidRequestError(request)

        try:
            headers = jwt.get_unverified_headers(request.o2_assertion)
            decode_key = repository.get_key_by_jwt_headers(
                headers, request.o2_client_id, request)
        except JWTError as why:
            raise InvalidGrantError(request) from why
        else:
            request._o2_jwt_claims = decode_jwt_assertion(
                request.o2_assertion, decode_key, request,
                validator, self.datetime_factory().timestamp(), True)
            if not request._o2_jwt_claims:
                raise InvalidGrantError(request)

        if request.o2_scope:
            if not validator.validate_scope(request.o2_scope, request):
                raise InvalidScopeError(request)
        else:
            request.o2_scope = repository.get_default_scope(request)

    def handle_token_request(self, request, repository):
        try:
            subject = repository.get_subject_by_jwt_claims(
                request._o2_jwt_claims, request)
            token = self.token_factory(subject, request.o2_scope,
                                       False, request)
            repository.save_access_token(token, request)
        except BaseException as why:  # pragma: no cover
            raise ServerError(request) from why

        request.response.status = 200
        return token
