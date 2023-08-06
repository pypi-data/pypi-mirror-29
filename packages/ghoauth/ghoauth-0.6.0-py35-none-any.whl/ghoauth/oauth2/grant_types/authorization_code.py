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

from ghoauth.oauth2.errors import (
    InvalidGrantError,
    InvalidRequestError,
    ServerError,
)
from ghoauth.oauth2.token import (
    authorization_code_factory,
    bearer_token_factory,
)
from ghoauth.uriutils import extend_uri_with_params

from .abc import (
    AbstractBaseGrantTypeHandler,
    AbstractBaseResponseTypeHandler,
)


class AuthorizationCodeGrant(AbstractBaseResponseTypeHandler,
                             AbstractBaseGrantTypeHandler):
    """
    https://tools.ietf.org/html/rfc6749#section-4.1
    """
    __slots__ = ['code_factory', 'token_factory']

    def __init__(self,
                 code_factory=authorization_code_factory,
                 token_factory=bearer_token_factory):
        self.code_factory = code_factory
        self.token_factory = token_factory

    def supported_response_types(self):
        return ['code']

    def get_default_response_mode(self, request):
        return 'query'

    def is_response_mode_allowed(self, response_mode, request):
        return response_mode == 'query'

    def handle_authorization_request(self, request, repository, subject):
        try:
            code = self.code_factory(subject, request.o2_scope,
                                     request.o2_client_id, request)
            if request.o2_state:
                code['state'] = request.o2_state
            repository.save_authorization_code(code, request.o2_redirect_uri,
                                               request.o2_client_id, request)
        except BaseException as why:
            raise ServerError(request) from why

        redirect_uri = extend_uri_with_params(request.o2_redirect_uri, code,
                                              request.o2_response_mode)
        request.response.status_code = 302
        request.response.location = redirect_uri
        return None

    def validate_token_request(self, request, repository, validator):
        super().validate_token_request(request, repository, validator)

        if not request.o2_validate(requireds={'code'},
                                   optionals={'redirect_uri'}):
            raise InvalidRequestError(request)

        if not request.o2_validate_redirect_uri(repository, validator):
            raise InvalidGrantError(request)

        if not validator.validate_authorization_code(
                request.o2_code, request.o2_redirect_uri,
                request.o2_client_id, request):
            raise InvalidGrantError(request)

    def supported_grant_types(self):
        return ['authorization_code']

    def handle_token_request(self, request, repository):
        try:
            subject = repository.get_subject_by_authorization_code(
                request.o2_code, request)
            scope = repository.get_scope_by_authorization_code(
                request.o2_code, request)

            token = self.token_factory(subject, scope, True, request)
            repository.save_access_token(token, request)
        except BaseException as why:
            raise ServerError(request) from why

        return token
