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
    AccessDeniedError,
    InvalidRequestError,
    UnsupportedResponseTypeError,
)
from ghoauth.oauth2.validator import normalize_response_type

from .abc import AbstractBaseEndpoint


class AuthorizationEndpoint(AbstractBaseEndpoint):
    __slots__ = ['repository', 'validator', '_handlers']

    def _get_handler(self, request):
        """
        If an authorization request is missing the "response_type" parameter,
        or if the response type is not understood, the authorization server
        MUST return an error response as described in Section 4.1.2.1.
        https://tools.ietf.org/html/rfc6749#section-3.1.1
        """
        try:
            return super()._get_handler(request.o2_response_type)
        except KeyError as why:
            # NOTE(yosida95): When this method is called, the client which was
            # used to send the request and the redirect_uri which is specified
            # in the request should had been authenticated via
            # self.validate_request.
            raise UnsupportedResponseTypeError(request) from why

    def register_handler(self, handler):
        # TODO(yosida95): validate the response_type
        response_types = (normalize_response_type(v)
                          for v in handler.supported_response_types())
        super().register_handler(handler, response_types)

    def validate_request(self, request):
        handler = self._get_handler(request)

        if not request.o2_response_mode:
            request.o2_response_mode =\
                handler.get_default_response_mode(request)
        if not handler.is_response_mode_allowed(
                request.o2_response_mode, request):
            raise InvalidRequestError(request)

        handler.validate_authorization_request(
            request, self.repository, self.validator)

    def handle_request(self, request, subject, is_authorized):
        self.validate_request(request)
        if not is_authorized:
            raise AccessDeniedError(request)

        handler = self._get_handler(request)
        handler.handle_authorization_request(request, self.repository, subject)
        request.response.cache_control.no_store = True
        request.response.pragma = 'no-cache'
        return request.response
