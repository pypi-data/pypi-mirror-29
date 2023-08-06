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

from webob import BaseRequest

from .validator import (
    normalize_response_type,
    validate_redirect_uri,
)


class o2_property:

    def __init__(self, name):
        self.__name__ = name

    def __get__(self, obj, type_=None):
        if obj is None:  # pragma: no cover
            return self
        paramdct = obj.environ.setdefault('oauth2.params', {})
        if self.__name__ in paramdct:
            return paramdct[self.__name__]
        return None

    def __set__(self, obj, value):
        paramdct = obj.environ.setdefault('oauth2.params', {})
        paramdct[self.__name__] = value

    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')


class request_parameter(o2_property):

    def __init__(self, name, normalizer=None):
        super().__init__(name)
        self._normalizer = normalizer or (lambda v: v)

    def __get__(self, obj, type_=None):
        value = super().__get__(obj, type_)
        paramdct = obj.environ['oauth2.params']
        if value is not None or self.__name__ in paramdct:
            return value

        values = obj.params.getall(self.__name__)
        if len(values) == 1 and values[0]:
            value = self._normalizer(values[0])
            paramdct[self.__name__] = value
            return value
        paramdct[self.__name__] = None
        return None

    def __set__(self, obj, value):
        value = self._normalizer(value)
        super().__set__(obj, value)


class OAuth2RequestMixin:
    o2_client_id = request_parameter('client_id')
    o2_client_secret = request_parameter('client_secret')
    o2_code = request_parameter('code')
    o2_grant_type = request_parameter('grant_type')
    o2_redirect_uri = request_parameter('redirect_uri')
    o2_refresh_token = request_parameter('refresh_token')
    o2_response_type = request_parameter('response_type',
                                         normalize_response_type)
    o2_scope = request_parameter('scope')
    o2_state = request_parameter('state')
    # Multiple Values Response Types
    o2_response_mode = request_parameter('response_mode')
    # Assertion Framework for OAuth 2.0 Client Authentication
    # and Authorization Grants
    o2_assertion = request_parameter('assertion')
    _o2_jwt_claims = o2_property('_o2_jwt_claims')

    def o2_validate(self, requireds=None, optionals=None):
        if requireds:
            for parameter in requireds:
                if parameter not in self.params or\
                        len(self.params.getall(parameter)) != 1 or\
                        not self.params[parameter]:
                    return False
        if optionals:
            for parameter in optionals:
                if parameter in self.params and\
                        len(self.params.getall(parameter)) != 1:
                    return False
        return True

    def o2_validate_redirect_uri(self, repository, validator, exactly=False):
        if self.o2_redirect_uri:
            if not validate_redirect_uri(self.o2_redirect_uri):
                return False
            return validator.validate_redirect_uri(
                self.o2_redirect_uri, self.o2_client_id, self, exactly)
        self.o2_redirect_uri = repository.get_primary_redirect_uri(
            self.o2_client_id, self)
        return validate_redirect_uri(self.o2_redirect_uri)


OAuth2Request = type('OAuth2Request', (OAuth2RequestMixin, BaseRequest), {})
