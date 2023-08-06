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

from .endpoints import (
    AuthorizationEndpoint,
    TokenEndpoint,
)
from .errors import OAuth2ErrorResponse
from .grant_types import (
    AbstractBaseGrantTypeHandler,
    AbstractBaseResponseTypeHandler,
)


class AuthorizationServer:

    def __init__(self, repository, validator):
        self._authz_endpoint = AuthorizationEndpoint(repository, validator)
        self._token_endpoint = TokenEndpoint(repository, validator)

    def register_handler(self, handler):
        if isinstance(handler, AbstractBaseResponseTypeHandler):
            self._authz_endpoint.register_handler(handler)
        if isinstance(handler, AbstractBaseGrantTypeHandler):
            self._token_endpoint.register_handler(handler)

    def validate_authorization_request(self, request):
        try:
            self._authz_endpoint.validate_request(request)
        except OAuth2ErrorResponse as why:
            why.o2_use_redirect()
            raise

    def validate_token_request(self, request):
        try:
            self._token_endpoint.validate_request(request)
        except OAuth2ErrorResponse as why:
            why.o2_use_json()
            raise

    def handle_authorization_request(self, request, subject, is_authorized):
        try:
            return self._authz_endpoint.handle_request(
                request, subject, is_authorized)
        except OAuth2ErrorResponse as why:
            why.o2_use_redirect()
            raise

    def handle_token_request(self, request):
        try:
            return self._token_endpoint.handle_request(request)
        except OAuth2ErrorResponse as why:
            why.o2_use_json()
            raise
