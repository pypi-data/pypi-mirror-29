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

import json
from collections import Mapping

from ghoauth.oauth2.errors import (
    InvalidClientError,
    InvalidRequestError,
    UnauthorizedClientError,
    UnsupportedGrantTypeError,
)

from .abc import AbstractBaseEndpoint


class TokenEndpoint(AbstractBaseEndpoint):
    __slots__ = ['repository', 'validator', '_handlers']

    def _get_handler(self, request):
        try:
            return super()._get_handler(request.o2_grant_type)
        except KeyError as why:
            raise UnsupportedGrantTypeError(request) from why

    def register_handler(self, handler):
        # TODO(yosida95): validate the grant_type
        grant_types = handler.supported_grant_types()
        super().register_handler(handler, grant_types)

    def validate_request(self, request):
        """
        A client MAY use the "client_id" request parameter to identify itself
        when sending requests to the token endpoint.  In the
        "authorization_code" "grant_type" request to the token endpoint, an
        unauthenticated client MUST send its "client_id" to prevent itself
        from inadvertently accepting a code intended for a client with a
        different "client_id".
        https://tools.ietf.org/html/rfc6749#section-3.2.1
        """
        if not request.o2_validate(requireds={'grant_type'},
                                   optionals={'client_id'}):
            raise InvalidRequestError(request)
        if request.o2_client_id:
            if not self.validator.authenticate_client_as(
                    request.o2_client_id, request):
                raise InvalidClientError(request)
        else:
            request.o2_client_id = self.validator.authenticate_client(request)
            if not request.o2_client_id:
                raise InvalidClientError(request)
        if not self.validator.authorize_grant_type(request.o2_grant_type,
                                                   request.o2_client_id,
                                                   request):
            raise UnauthorizedClientError(request)

        handler = self._get_handler(request)
        handler.validate_token_request(request,
                                       self.repository, self.validator)

    def handle_request(self, request):
        self.validate_request(request)

        handler = self._get_handler(request)
        body = handler.handle_token_request(request, self.repository)

        response = request.response
        if isinstance(body, Mapping):
            response.text = json.dumps(body, ensure_ascii=True, indent=2)
        response.cache_control.no_store = True
        response.pragma = 'no-cache'
        return response
