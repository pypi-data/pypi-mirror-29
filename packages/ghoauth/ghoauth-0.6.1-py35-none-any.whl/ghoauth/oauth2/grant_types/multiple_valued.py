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

from ghoauth.oauth2.errors import ServerError
from ghoauth.oauth2.token import (
    authorization_code_factory,
    bearer_token_factory,
)
from ghoauth.uriutils import extend_uri_with_params

from .abc import AbstractBaseResponseTypeHandler


class MultipleValuedResponseType(AbstractBaseResponseTypeHandler):
    """
    http://openid.net/specs/oauth-v2-multiple-response-types-1_0.html#ResponseModes
    """
    __slots__ = ['code_factory', 'token_factory']

    def __init__(self, code_factory=authorization_code_factory,
                 token_factory=bearer_token_factory):
        self.code_factory = code_factory
        self.token_factory = token_factory

    def supported_response_types(self):
        return ['code token']

    def get_default_response_mode(self, request):
        return 'fragment'

    def is_response_mode_allowed(self, response_mode, request):
        return response_mode == 'fragment'

    def handle_authorization_request(self, request, repository, subject):
        try:
            code = self.code_factory(subject, request.o2_scope,
                                     request.o2_client_id, request)
            if request.o2_state:
                code['state'] = request.o2_state
            repository.save_authorization_code(code, request.o2_redirect_uri,
                                               request.o2_client_id, request)

            token = self.token_factory(subject, request.o2_scope, False,
                                       request)
            repository.save_access_token(token, request)
        except BaseException as why:
            raise ServerError(request) from why
        resp = code.copy()
        resp.update(token.copy())

        redirect_uri = extend_uri_with_params(request.o2_redirect_uri, resp,
                                              request.o2_response_mode)
        request.response.status = 302
        request.response.location = redirect_uri
        return None
