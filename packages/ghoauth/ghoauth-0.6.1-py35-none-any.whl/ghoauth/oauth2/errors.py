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

from webob.response import Response

from ghoauth.uriutils import extend_uri_with_params


OAuth2Error = type('OAuth2Error', (Exception, ), {})


class OAuth2ErrorResponse(Response, OAuth2Error):
    o2_error = None
    o2_code = 400
    o2_error_description = None

    def __init__(self, request, error_uri=None):
        Response.__init__(self)
        OAuth2Error.__init__(self)
        self.o2_error_uri = error_uri

        self.o2_redirect_uri = request.o2_redirect_uri
        self.o2_response_mode = request.o2_response_mode
        self.o2_prepared = False

        dct = {'error': self.o2_error}
        if self.o2_error_description:
            dct['error_description'] = self.o2_error_description
        if self.o2_error_uri:
            dct['error_uri'] = self.o2_error_uri
        if request.o2_state:
            dct['state'] = request.o2_state
        self.o2_errdct = dct

    def o2_use_redirect(self):
        if self.o2_prepared:
            return
        self.status_code = 302
        self.location = extend_uri_with_params(self.o2_redirect_uri,
                                               self.o2_errdct,
                                               self.o2_response_mode)
        self.o2_prepared = True

    def o2_use_json(self):
        if self.o2_prepared:
            return
        self.status_code = self.o2_code
        self.content_type = 'application/json'
        body = json.dumps(self.o2_errdct, ensure_ascii=True, indent=2)
        self.app_iter = [body]
        self.text = body
        self.o2_prepared = True

    def o2_ensure_prepared(self):
        self.o2_use_json()

    def __call__(self, environ, start_response):
        self.o2_ensure_prepared()
        return Response.__call__(self, environ, start_response)


class InvalidRequestError(OAuth2ErrorResponse):
    o2_error = 'invalid_request'


class UnauthorizedClientError(OAuth2ErrorResponse):
    o2_error = 'unauthorized_client'


class AccessDeniedError(OAuth2ErrorResponse):
    o2_error = 'access_denied'


class UnsupportedResponseTypeError(OAuth2ErrorResponse):
    o2_error = 'unsupported_response_type'


class InvalidScopeError(OAuth2ErrorResponse):
    o2_error = 'invalid_scope'


class ServerError(OAuth2ErrorResponse):
    code = 500
    o2_error = 'server_error'


class TemporarilyUnavailableError(OAuth2ErrorResponse):
    code = 503
    o2_error = 'temporarily_unavailable'


class UnsupportedGrantTypeError(OAuth2ErrorResponse):
    o2_error = 'unsupported_grant_type'


class InvalidClientError(OAuth2ErrorResponse):
    o2_error = 'invalid_client'


class InvalidGrantError(OAuth2ErrorResponse):
    o2_error = 'invalid_grant'


FatalOAuth2Error = type('FatalOAuth2Error', (OAuth2Error, ), {})
