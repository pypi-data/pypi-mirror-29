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

from typing import (
    Any,
    Dict,
    Tuple,
)

from ghoauth.oauth2 import AbstractBaseRepository
from jwt.jwk import AbstractJWKBase

from .request import OpenIDConnectRequestMixin


class AbstractOpenIDRepository(AbstractBaseRepository):

    def get_id_token_by_subject(
            self, subject: Any,
            code: Dict[str, Any], token: Dict[str, Any],
            request: OpenIDConnectRequestMixin) -> Dict[str, Any]:
        raise NotImplementedError('must implement get_id_token_by_subject')

    def get_userinfo_by_subject(
            self, subject: Any, scope: str,
            request: OpenIDConnectRequestMixin) -> Dict[str, Any]:
        raise NotImplementedError('must implement get_userinfo_by_subject')

    def get_key_alg_by_client_id(
            self, client_id: str,
            request: OpenIDConnectRequestMixin) -> Tuple[AbstractJWKBase, str]:
        raise NotImplementedError('must implement get_key_alg_by_client_id')
