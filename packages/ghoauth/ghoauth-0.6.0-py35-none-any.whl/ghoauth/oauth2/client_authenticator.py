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
    jwt,
    JWTError,
)

from .grant_types.jwt_bearer import decode_jwt_assertion


class JWTClientAuthenticator:

    __slots__ = ['repository', 'validator', 'datetime_factory']

    def __init__(self, repository, validator, datetime_factory=datetime.now):
        self.repository = repository
        self.validator = validator
        self.datetime_factory = datetime_factory

    def __call__(self, request):
        if not request.o2_validate(requireds={'client_assertion_type',
                                              'client_assertion_type'}):
            return False
        if request.o2_client_assertion_type !=\
                'urn:ietf:params:oauth:client-assertion-type:jwt-bearer':
            return False

        try:
            headers = jwt.get_unverified_headers(request.o2_assertion)
            jwt_claims = jwt.get_unverified_claims(request.o2_client_assertion)
            client_id = jwt_claims['sub']
            if not self.repository.is_client_available(client_id, request):
                return False
            decode_key = self.repository.get_key_by_jwt_headers(
                headers, client_id,
                request)
        except JWTError:
            return False
        else:
            jwt_claims = decode_jwt_assertion(
                request.o2_client_assertion, decode_key, request,
                self.validator, self.datetime_factory().timestamp(), False)
            if not jwt_claims:
                return False

        return client_id
