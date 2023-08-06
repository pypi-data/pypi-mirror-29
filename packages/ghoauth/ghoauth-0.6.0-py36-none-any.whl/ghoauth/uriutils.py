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

from urllib.parse import (
    parse_qsl,
    urlencode,
)

from rfc3986 import (
    uri_reference,
    urlparse,
    URIReference,
)


__all__ = [
    'compare_uri',
    'extend_uri_with_params',
    'is_absolute_uri',
    'uri_reference',
    'urlparse',

    'URIReference',
]


def is_absolute_uri(uri):
    if isinstance(uri, URIReference):
        parsed = uri
    else:
        try:
            parsed = uri_reference(uri)
        except BaseException:
            return False

    return parsed.is_absolute() and parsed.scheme and parsed.host


def extend_uri_with_params(redirect_uri, paramdict, response_mode):
    parsed = urlparse(redirect_uri)
    if response_mode == 'fragment':
        fragment = urlencode(list(paramdict.items()))
        parsed = parsed.copy_with(fragment=fragment)
    else:
        qsl = parse_qsl(parsed.query, keep_blank_values=True)
        qsl.extend(paramdict.items())
        query = urlencode(qsl)
        parsed = parsed.copy_with(query=query)
    return parsed.geturl()


def compare_uri(x, y):
    try:
        if isinstance(x, URIReference):
            x_uri = x
        else:
            x_uri = uri_reference(x)
        if isinstance(y, URIReference):
            y_uri = y
        else:
            y_uri = uri_reference(y)
    except BaseException:
        return False
    else:
        return x_uri.normalized_equality(y_uri)
