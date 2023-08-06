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
    FatalOAuth2Error,
    InvalidRequestError,
    InvalidScopeError,
)


class AbstractBaseResponseTypeHandler:

    def supported_response_types(self):
        return []

    def get_default_response_mode(self, request):
        raise NotImplementedError('must implement get_default_response_mode')

    def is_response_mode_allowed(self, response_mode, request):
        raise NotImplementedError('must implement is_response_mode_allowed')

    def validate_authorization_request(self, request, repository, validator):
        if not request.o2_validate(requireds={'client_id'},
                                   optionals={'redirect_uri'}):
            raise FatalOAuth2Error()
        if not repository.is_client_available(request.o2_client_id, request):
            raise FatalOAuth2Error()
        if not request.o2_validate_redirect_uri(repository, validator):
            raise FatalOAuth2Error()

        if not request.o2_validate(requireds={'response_type'},
                                   optionals={'scope', 'state',
                                              'response_mode'}):
            raise InvalidRequestError(request)

        if request.o2_scope:
            if not validator.validate_scope(
                    request.o2_scope, request.o2_client_id, request):
                raise InvalidScopeError(request)
        else:
            request.o2_scope = repository.get_default_scope(request)

    def handle_authorization_request(self, request, repository, subject):
        raise NotImplementedError('must implement handle_authorization_request')  # noqa


class AbstractBaseGrantTypeHandler:

    def supported_grant_types(self):
        return []

    def validate_token_request(self, request, repository, validator):
        return

    def handle_token_request(self, request, repository):
        raise NotImplementedError('must implement handle_token_request')
