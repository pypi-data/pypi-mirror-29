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

from ghoauth.uriutils import (
    is_absolute_uri,
    urlparse,
)


def normalize_response_type(response_type):
    """
    Extension response types MAY contain a space-delimited (%x20) list of
    values, where the order of values does not matter (e.g., response
    type "a b" is the same as "b a").  The meaning of such composite
    response types is defined by their respective specifications.

    https://tools.ietf.org/html/rfc6749#section-3.1.1
    """
    return ' '.join(sorted(response_type.split()))


def validate_redirect_uri(redirect_uri):
    """
    The redirection endpoint URI MUST be an absolute URI as defined by
    [RFC3986] Section 4.3.  The endpoint URI MAY include an
    "application/x-www-form-urlencoded" formatted (per Appendix B) query
    component ([RFC3986] Section 3.4), which MUST be retained when adding
    additional query parameters.  The endpoint URI MUST NOT include a
    fragment component.

    https://tools.ietf.org/html/rfc6749#section-3.1.2
    """
    parsed = urlparse(redirect_uri)
    if not is_absolute_uri(parsed.geturl()):
        return False
    if parsed.fragment:
        return False
    return True


class AbstractBaseValidator:

    def authenticate_client(self, request):
        raise NotImplementedError('must implement authenticate_client')

    def authenticate_client_as(self, client_id, request):
        raise NotImplementedError('must implement authenticate_client_as')

    def authorize_response_type(self, response_type, client_id, request):
        raise NotImplementedError('must implement authorize_response_type')

    def authorize_grant_type(self, grant_type, client_id, request):
        raise NotImplementedError('must implement authorize_grant_type')

    def validate_redirect_uri(self, redirect_uri, client_id, request,
                              exactly=False):
        """
        The authorization server MUST require the following clients to
        register their redirection endpoint:
            o  Public clients.
            o  Confidential clients utilizing the implicit grant type.
        The authorization server SHOULD require all clients to register their
        redirection endpoint prior to utilizing the authorization endpoint.

        The authorization server SHOULD require the client to provide the
        complete redirection URI (the client MAY use the "state" request
        parameter to achieve per-request customization).  If requiring the
        registration of the complete redirection URI is not possible, the
        authorization server SHOULD require the registration of the URI
        scheme, authority, and path (allowing the client to dynamically vary
        only the query component of the redirection URI when requesting
        authorization).
        The authorization server MAY allow the client to register multiple
        redirection endpoints.

        https://tools.ietf.org/html/rfc6749#section-3.1.2.2
        """
        raise NotImplementedError('must implement validate_redirect_uri')

    def validate_scope(self, scope, client_id, request):
        raise NotImplementedError('must implement validate_scope')


class AuthorizationCodeGrantValidatorMixin:

    def validate_authorization_code(self, code, redirect_uri,
                                    client_id, request):
        """
        REQUIRED, if the "redirect_uri" parameter was included in the
        authorization request as described in Section 4.1.1, and their
        values MUST be identical.

        https://tools.ietf.org/html/rfc6749#section-4.1.3
        """
        raise NotImplementedError('must implement validate_authorization_code')


class RefreshTokenGrantValidatorMixin:

    def validate_refresh_token(self, refresh_token, clieht_id, request):
        raise NotImplementedError('must implement validate_refresh_token')

    def is_scope_subset_of(self, subset, superset):
        """
        The requested scope MUST NOT include any scope
        not originally granted by the resource owner

        https://tools.ietf.org/html/rfc6749#section-6
        """
        raise NotImplementedError('must implement is_scope_subset_of')


class JWTBearerGrantValidatorMixin:

    def validate_iss(self, iss, request):
        """
        The JWT MUST contain an "iss" (issuer) claim that contains a
        unique identifier for the entity that issued the JWT.  In the
        absence of an application profile specifying otherwise,
        compliant applications MUST compare issuer values using the
        Simple String Comparison method defined in Section 6.2.1 of RFC
        3986
        """
        raise NotImplementedError('must implement validate_iss')

    def validate_sub(self, sub, request, is_authorization_grant):
        """
        The JWT MUST contain a "sub" (subject) claim identifying the
        principal that is the subject of the JWT.  The subject typically
        identifies an authorized accessor for which the access token
        is being requested (i.e., the resource owner or an
        authorized delegate), but in some cases, may be a
        pseudonymous identifier or other value denoting an anonymous
        user.
        """
        raise NotImplementedError('must implement validate_sub')

    def validate_aud(self, aud, request):
        """
        The JWT MUST contain an "aud" (audience) claim containing a
        value that identifies the authorization server as an intended
        audience.
        The authorization server MUST reject any JWT that does not contain
        its own identity as the intended audience.  In the absence of an
        application profile specifying otherwise, compliant applications
        MUST compare the audience values using the Simple String
        Comparison method defined in Section 6.2.1 of RFC 3986.
        """
        raise NotImplementedError('must implement validate_aud')

    def validate_jti(self, jti, request):
        """
        The JWT MAY contain a "jti" (JWT ID) claim that provides a
        unique identifier for the token.  The authorization server MAY
        ensure that JWTs are not replayed by maintaining the set of used
        "jti" values for the length of time for which the JWT would be
        considered valid based on the applicable "exp" instant.
        """
