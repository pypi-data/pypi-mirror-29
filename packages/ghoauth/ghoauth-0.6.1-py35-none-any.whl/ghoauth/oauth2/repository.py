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


class AbstractBaseRepository:

    def is_client_available(self, client_id, request):
        raise NotImplementedError('must implement is_client_available')

    def get_primary_redirect_uri(self, client_id, request):
        raise NotImplementedError('must implement get_primary_redirect_uri')

    def get_default_scope(self, request):
        raise NotImplementedError('must implement get_default_scope')

    def save_access_token(self, token, request):
        raise NotImplementedError('must implement save_access_token')


class AuthorizationCodeGrantRepositoryMixin:

    def get_subject_by_authorization_code(self, code, request):
        raise NotImplementedError('must implement get_subject_by_authorization_code')  # noqa

    def get_scope_by_authorization_code(self, code, request):
        raise NotImplementedError('must implement get_scope_by_authorization_code')  # noqa

    def save_authorization_code(self, code, redirect_uri, client_id, request):
        raise NotImplementedError('must implement save_authorization_code')


class RefreshTokenGrantRepositoryMixin:

    def get_subject_by_refresh_token(self, refresh_token, request):
        raise NotImplementedError('must implement get_subject_by_refresh_token')  # noqa

    def get_scope_by_refresh_token(self, refresh_token, request):
        raise NotImplementedError('must implement get_scope_by_refresh_token')


class JWTBearerGrantRepositoryMixin:

    def get_key_by_jwt_headers(self, headers, client_id, request):
        raise NotImplementedError('must implement get_key_by_jwt_headers')

    def get_subject_by_jwt_claims(self, jwt_claims, request):
        raise NotImplementedError('must implement get_subject_by_jwt_claims')


class OpenIDRepositoryMixin:

    def get_id_token_by_subject(self, subject, code, token, request):
        raise NotImplementedError('must implement get_id_token_by_subject')
