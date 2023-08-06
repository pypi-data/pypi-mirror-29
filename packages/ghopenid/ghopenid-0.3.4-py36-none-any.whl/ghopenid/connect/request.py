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

from ghoauth.oauth2.request import (
    BaseRequest,
    OAuth2RequestMixin,
    request_parameter,
)


class OpenIDConnectRequestMixin(OAuth2RequestMixin):
    # § 3.1.2.1
    o2_nonce = request_parameter('nonce')
    o2_display = request_parameter('display')
    o2_prompt = request_parameter('prompt')
    o2_max_age = request_parameter('max_age')
    o2_ui_locales = request_parameter('ui_locales')
    o2_id_token_hint = request_parameter('id_token_hint')
    o2_login_hint = request_parameter('login_hint')
    o2_acr_values = request_parameter('acr_values')
    # § 5.2
    o2_claims_locales = request_parameter('claims_locales')
    # § 5.5
    o2_claims = request_parameter('claims')
    # § 6
    o2_request = request_parameter('request')
    o2_request_uri = request_parameter('request_uri')


OpenIDConnectRequest = type(
    'OpenIDConnectRequest', (OpenIDConnectRequestMixin, BaseRequest), {})
