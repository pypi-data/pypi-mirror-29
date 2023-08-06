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

from .client_authenticator import JWTClientAuthenticator
from .grant_types import (
    AuthorizationCodeGrant,
    ImplicitGrant,
    JWTBearerGrant,
    MultipleValuedResponseType,
    RefreshTokenGrant,
)
from .repository import (
    AbstractBaseRepository,
    AuthorizationCodeGrantRepositoryMixin,
    JWTBearerGrantRepositoryMixin,
    RefreshTokenGrantRepositoryMixin,
)
from .request import (
    OAuth2Request,
    OAuth2RequestMixin,
)
from .token import (
    authorization_code_factory,
    bearer_token_factory,
)
from .validator import (
    AbstractBaseValidator,
    AuthorizationCodeGrantValidatorMixin,
    JWTBearerGrantValidatorMixin,
    RefreshTokenGrantValidatorMixin,
)
from .server import AuthorizationServer


__all__ = ['AbstractBaseRepository',
           'AbstractBaseValidator',
           'AuthorizationServer',

           'OAuth2Request',
           'OAuth2RequestMixin',

           'authorization_code_factory',
           'bearer_token_factory',

           'AuthorizationCodeGrant',
           'AuthorizationCodeGrantRepositoryMixin',
           'AuthorizationCodeGrantValidatorMixin',

           'ImplicitGrant',

           'JWTBearerGrant',
           'JWTBearerGrantRepositoryMixin',
           'JWTBearerGrantValidatorMixin',

           'MultipleValuedResponseType',

           'RefreshTokenGrant',
           'RefreshTokenGrantRepositoryMixin',
           'RefreshTokenGrantValidatorMixin',

           'JWTClientAuthenticator']
