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

import os
from base64 import b64encode


def generate_token():
    """
    The probability of an attacker guessing generated tokens (and other
    credentials not intended for handling by end-users) MUST be less than
    or equal to 2^(-128) and SHOULD be less than or equal to 2^(-160).
    https://tools.ietf.org/html/rfc6749#section-10.10
    """
    return b64encode(os.urandom(20)).decode('ascii')


def authorization_code_factory(subject, scope, client_id, request):
    """
    The authorization code MUST expire shortly after it is issued
    to mitigate the risk of leaks.  A maximum authorization code
    lifetime of 10 minutes is RECOMMENDED
    https://tools.ietf.org/html/rfc6749#section-4.1.2
    """
    return {'code': generate_token()}


def bearer_token_factory(subject, scope, with_refresh_token, request):
    dct = {'token_type': 'Bearer',
           'scope': scope,
           'access_token': generate_token(),
           'expires_in': 3600}
    if with_refresh_token:
        dct['refresh_token'] = generate_token()
    return dct
