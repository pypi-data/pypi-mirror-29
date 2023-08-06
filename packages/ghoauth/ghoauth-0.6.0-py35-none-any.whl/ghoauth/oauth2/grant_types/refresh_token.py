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
    InvalidScopeError,
    ServerError,
)
from ghoauth.oauth2.token import bearer_token_factory

from .abc import AbstractBaseGrantTypeHandler


class RefreshTokenGrant(AbstractBaseGrantTypeHandler):
    """
    https://tools.ietf.org/html/rfc6749#section-6
    """
    __slots__ = ['issue_refresh_token', 'token_factory']

    def __init__(self, issue_refresh_token=True,
                 token_factory=bearer_token_factory):
        self.issue_refresh_token = issue_refresh_token
        self.token_factory = token_factory

    def supported_grant_types(self):
        return ['refresh_token']

    def validate_token_request(self, request, repository, validator):
        if not request.o2_validate(requireds={'refresh_token'},
                                   optionals={'scope'}):
            raise InvalidRequestError(request)
        if not validator.validate_refresh_token(request.o2_refresh_token,
                                                request.o2_client_id, request):
            raise InvalidGrantError(request)

        granted_scope = repository.get_scope_by_refresh_token(
            request.o2_refresh_token,
            request)
        if request.o2_scope:
            if not validator.validate_scope(request.o2_scope, request):
                raise InvalidScopeError(request)
            if not validator.is_scope_subset_of(request.o2_scope,
                                                granted_scope):
                raise InvalidScopeError(request)
        else:
            request.o2_scope = granted_scope

    def handle_token_request(self, request, repository):
        try:
            subject = repository.get_subject_by_refresh_token(
                request.o2_refresh_token)
            token = self.token_factory(subject, request.o2_scope,
                                       self.issue_refresh_token, request)
            repository.save_access_token(token, request)
        except BaseException as why:
            raise ServerError(request) from why

        return token
