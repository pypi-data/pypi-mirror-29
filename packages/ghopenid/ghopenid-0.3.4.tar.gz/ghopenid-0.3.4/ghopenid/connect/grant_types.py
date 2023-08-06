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

import hashlib
from typing import (
    Any,
    Callable,
    List,
)

from ghoauth.oauth2.request import OAuth2RequestMixin
from ghoauth.oauth2.grant_types.abc import (
    AbstractBaseGrantTypeHandler,
    AbstractBaseResponseTypeHandler,
)
from ghoauth.oauth2.errors import (
    FatalOAuth2Error,
    InvalidGrantError,
    InvalidRequestError,
    InvalidScopeError,
    ServerError,
)
from ghoauth.oauth2.token import (
    authorization_code_factory,
    bearer_token_factory,
)
from ghoauth.uriutils import extend_uri_with_params
from jwt import JWT
from jwt.utils import b64encode

from .repository import AbstractOpenIDRepository
from .request import OpenIDConnectRequestMixin
from .validator import AbstractOpenIDRequestValidator


def _std_hash_by_alg(alg) -> Callable[[bytes], Any]:
    if alg.endswith('S256'):
        return hashlib.sha256
    if alg.endswith('S384'):
        return hashlib.sha384
    if alg.endswith('S512'):
        return hashlib.sha512
    raise ValueError('{} is not supported'.format(alg))


def _left_half_hash(data: str, alg: str) -> str:
    hashfun = _std_hash_by_alg(alg)
    hashobj = hashfun(data.encode('ascii'))
    digest = hashobj.digest()[:hashobj.digest_size // 2]
    return b64encode(digest)


class OpenIDConnectGrant(AbstractBaseResponseTypeHandler,
                         AbstractBaseGrantTypeHandler):
    """
    http://openid.net/specs/openid-connect-core-1_0.html
    """
    __slots__ = ['code_factory', 'token_factory', 'jwt_encoder']
    jwt_encoder_cls = JWT

    def __init__(
            self,
            code_factory: Callable[
                [object, str, str, OAuth2RequestMixin], dict
            ]=authorization_code_factory,
            token_factory: Callable[
                [object, str, bool, OAuth2RequestMixin], dict
            ]=bearer_token_factory) -> None:
        self.code_factory = code_factory
        self.token_factory = token_factory
        self.jwt_encoder = self.jwt_encoder_cls()

    def supported_response_types(self) -> List[str]:
        return ['code', 'id_token', 'token', 'none',
                'code token', 'code id_token', 'id_token token',
                'code id_token token']

    def get_default_response_mode(
            self, request: OpenIDConnectRequestMixin) -> str:
        if request.o2_response_type in ('code', 'none'):
            return 'query'
        return 'fragment'

    def is_response_mode_allowed(
            self, response_mode: str,
            request: OpenIDConnectRequestMixin) -> bool:
        """
        http://openid.net/specs/oauth-v2-multiple-response-types-1_0.html#Combinations
        """
        if request.o2_response_type in ('code', 'none'):
            return response_mode in ('query', 'fragment')
        return response_mode == 'fragment'

    def validate_authorization_request(
            self, request: OpenIDConnectRequestMixin,
            repository: AbstractOpenIDRepository,
            validator: AbstractOpenIDRequestValidator) -> None:
        if not request.o2_validate(requireds={'scope'}) or \
                'openid' not in request.o2_scope.split():
            # the request is not for Open ID Connect.
            AbstractBaseResponseTypeHandler.validate_authorization_request(
                self, request, repository, validator)
            return

        if not request.o2_validate(requireds={'client_id', 'redirect_uri'}):
            raise FatalOAuth2Error()
        if not repository.is_client_available(request.o2_client_id, request):
            raise FatalOAuth2Error()
        # NOTE(yosida95): 'response_type' parameter was eventually validated by
        # the AuthorizationEndpoint to dispatch this method, the value would be
        # one of the self.supported_response_types(), so the value can be used
        # safely here.
        resp_type = request.o2_response_type.split()
        if not request.o2_validate_redirect_uri(
                repository, validator, exactly='code' not in resp_type):
            raise FatalOAuth2Error()

        if not request.o2_validate(
                optionals={'state', 'nonce', 'display', 'prompt', 'max_age',
                           'ui_locales', 'id_token_hint', 'login_hint',
                           'acr_values'}):
            raise InvalidRequestError(request)
        if 'code' not in resp_type and not request.o2_nonce:
            # In implicit flow, use of nonce is REQUIRED.
            raise InvalidRequestError(request)

        if not validator.validate_scope(
                request.o2_scope, request.o2_client_id, request):
            raise InvalidScopeError(request)

    def handle_authorization_request(
            self,
            request: OpenIDConnectRequestMixin,
            repository: AbstractOpenIDRepository,
            subject: Any) -> None:
        resp = dict()
        if request.o2_state:
            resp['state'] = request.o2_state

        try:
            resp_type = request.o2_response_type.split()

            code = None
            if 'code' in resp_type:
                code = self.code_factory(subject, request.o2_scope,
                                         request.o2_client_id, request)
                repository.save_authorization_code(
                    code, request.o2_redirect_uri, request.o2_client_id,
                    request)
                resp.update(code.copy())

            token = None
            if 'token' in resp_type:
                with_refresh_token = False
                token = self.token_factory(subject, request.o2_scope,
                                           with_refresh_token, request)
                repository.save_access_token(token, request)
                resp.update(token.copy())

            if 'id_token' in resp_type:
                key, alg = repository.get_key_alg_by_client_id(
                    request.o2_client_id, request)

                jwt_dict = repository.get_id_token_by_subject(
                    subject, code, token, request)
                if request.o2_nonce:
                    jwt_dict['nonce'] = request.o2_nonce
                if code:
                    jwt_dict['c_hash'] = _left_half_hash(code['code'], alg)
                if token:
                    jwt_dict['at_hash'] = _left_half_hash(
                        token['access_token'], alg)
                if code is None and token is None:
                    userinfo = repository.get_userinfo_by_subject(
                        subject, request.o2_scope, request)
                    jwt_dict = jwt_dict.copy()
                    if jwt_dict['sub'] != userinfo['sub']:
                        raise ServerError(request)
                    jwt_dict.update(userinfo)
                resp['id_token'] = self.jwt_encoder.encode(
                    jwt_dict, key=key, alg=alg)
        except BaseException as why:
            raise ServerError(request) from why

        redirect_uri = extend_uri_with_params(request.o2_redirect_uri, resp,
                                              request.o2_response_mode)
        request.response.state = 302
        request.response.location = redirect_uri
        return None

    def supported_grant_types(self) -> List[str]:
        return ['authorization_code']

    def validate_token_request(
            self, request: OpenIDConnectRequestMixin,
            repository: AbstractOpenIDRepository,
            validator: AbstractOpenIDRequestValidator) -> None:
        super().validate_token_request(request, repository, validator)

        if not request.o2_validate(requireds={'code'},
                                   optionals={'redirect_uri'}):
            raise InvalidRequestError(request)

        if not request.o2_validate_redirect_uri(repository, validator):
            raise InvalidGrantError(request)

        if not validator.validate_authorization_code(
                request.o2_code, request.o2_redirect_uri,
                request.o2_client_id, request):
            raise InvalidGrantError(request)

    def handle_token_request(
            self, request: OpenIDConnectRequestMixin,
            repository: AbstractOpenIDRepository) -> dict:
        resp = {}
        try:
            subject = repository.get_subject_by_authorization_code(
                request.o2_code, request)
            scope = repository.get_scope_by_authorization_code(
                request.o2_code, request)
            token = self.token_factory(subject, scope, True, request)
            repository.save_access_token(token, request)
            resp.update(token.copy())

            key, alg = repository.get_key_alg_by_client_id(
                request.o2_client_id, request)
            jwt_dict = repository.get_id_token_by_subject(
                subject, {'code': request.o2_code}, token, request)
            jwt_dict['at_hash'] = _left_half_hash(token['access_token'], alg)
            resp['id_token'] = self.jwt_encoder.encode(
                jwt_dict, key=key, alg=alg)
        except BaseException as why:
            raise ServerError(request) from why

        return resp
