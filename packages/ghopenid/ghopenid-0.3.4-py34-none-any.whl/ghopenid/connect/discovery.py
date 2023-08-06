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

from collections import (
    OrderedDict,
    UserDict,
)


class OpenIDConnectProviderMetadata(UserDict):
    _attributes = [
        ('issuer', None, True),
        ('authorization_endpoint', None, True),
        ('token_endpoint', None, False),
        ('userinfo_endpoint', None, False),
        ('jwks_uri', None, True),
        ('registration_endpoint', None, False),
        ('scopes_supported', None, False),
        ('response_types_supported', None, True),
        ('response_modes_supported', ['query', 'fragment'], False),
        ('grant_types_supported', ['authorization_code', 'implicit'], False),
        ('acr_values_supported', None, False),
        ('subject_types_supported', None, True),
        ('id_token_signing_alg_values_supported', None, True),
        ('id_token_encryption_alg_values_supported', None, False),
        ('id_token_encryption_enc_values_supported', None, False),
        ('userinfo_signing_alg_values_supported', None, False),
        ('userinfo_encryption_alg_values_supported', None, False),
        ('userinfo_encryption_enc_values_supported', None, False),
        ('request_object_signing_alg_values_supported', None, False),
        ('request_object_encryption_alg_values_supported', None, False),
        ('request_object_encryption_enc_values_supported', None, False),
        ('token_endpoint_auth_methods_supported', ['client_secret_basic'],
         False),
        ('token_endpoint_auth_signing_alg_values_supported', None, False),
        ('display_values_supported', None, False),
        ('claim_types_supported', ['normal'], False),
        ('claims_supported', None, False),
        ('service_documentation', None, False),
        ('claims_locales_supported', None, False),
        ('ui_locales_supported', None, False),
        ('claims_parameter_supported', False, False),
        ('request_parameter_supported', False, False),
        ('request_uri_parameter_supported', True, False),
        ('require_request_uri_registration', False, False),
        ('op_policy_uri', None, False),
        ('op_tos_uri', None, False),
    ]

    def __init__(self, issuer):
        UserDict.__init__(self)
        self.data['issuer'] = issuer

    def set_authorization_endpoint(self, value):
        self.data['authorization_endpoint'] = value

    def set_token_endpoint(self, value):
        self.data['token_endpoint'] = value

    def set_userinfo_endpoint(self, value):
        self.data['userinfo_endpoint'] = value

    def set_jwks_uri(self, value):
        self.data['jwks_uri'] = value

    def set_registration_endpoint(self, value):
        self.data['registration_endpoint'] = value

    def set_scopes_supported(self, value):
        self.data['scopes_supported'] = value

    def set_response_types_supported(self, value):
        self.data['response_types_supported'] = value

    def set_response_modes_supported(self, value):
        self.data['response_modes_supported'] = value

    def set_grant_types_supported(self, value):
        self.data['grant_types_supported'] = value

    def set_acr_values_supported(self, value):
        self.data['acr_values_supported'] = value

    def set_subject_types_supported(self, value):
        self.data['subject_types_supported'] = value

    def set_id_token_signing_alg_values_supported(self, value):
        self.data['id_token_signing_alg_values_supported'] = value

    def set_id_token_encryption_alg_values_supported(self, value):
        self.data['id_token_encryption_alg_values_supported'] = value

    def set_id_token_encryption_enc_values_supported(self, value):
        self.data['id_token_encryption_enc_values_supported'] = value

    def set_userinfo_signing_alg_values_supported(self, value):
        self.data['userinfo_signing_alg_values_supported'] = value

    def set_userinfo_encryption_alg_values_supported(self, value):
        self.data['userinfo_encryption_alg_values_supported'] = value

    def set_userinfo_encryption_enc_values_supported(self, value):
        self.data['userinfo_encryption_enc_values_supported'] = value

    def set_request_object_signing_alg_values_supported(self, value):
        self.data['request_object_signing_alg_values_supported'] = value

    def set_request_object_encryption_alg_values_supported(self, value):
        self.data['request_object_encryption_alg_values_supported'] = value

    def set_request_object_encryption_enc_values_supported(self, value):
        self.data['request_object_encryption_enc_values_supported'] = value

    def set_token_endpoint_auth_methods_supported(self, value):
        self.data['token_endpoint_auth_methods_supported'] = value

    def set_token_endpoint_auth_signing_alg_values_supported(self, value):
        self.data['token_endpoint_auth_signing_alg_values_supported'] = value

    def set_display_values_supported(self, value):
        self.data['display_values_supported'] = value

    def set_claim_types_supported(self, value):
        self.data['claim_types_supported'] = value

    def set_claims_supported(self, value):
        self.data['claims_supported'] = value

    def set_service_documentation(self, value):
        self.data['service_documentation'] = value

    def set_claims_locales_supported(self, value):
        self.data['claims_locales_supported'] = value

    def set_ui_locales_supported(self, value):
        self.data['ui_locales_supported'] = value

    def set_claims_parameter_supported(self, value):
        self.data['claims_parameter_supported'] = value

    def set_request_parameter_supported(self, value):
        self.data['request_parameter_supported'] = value

    def set_request_uri_parameter_supported(self, value):
        self.data['request_uri_parameter_supported'] = value

    def set_require_request_uri_registration(self, value):
        self.data['require_request_uri_registration'] = value

    def set_op_policy_uri(self, value):
        self.data['op_policy_uri'] = value

    def set_op_tos_uri(self, value):
        self.data['op_tos_uri'] = value

    def validate(self):
        for name, _default, required in self._attributes:
            if not required:
                continue
            if name not in self.data:
                raise ValueError('{} is required'.format(name))

        # token_endpoint is REQUIRED unless only the Implicit Flow is used.
        grant_types = self.data.get('grant_types_supported', [])
        if (len(grant_types) != 1 or grant_types[0] != 'implicit') and \
                'token_endpoint' not in self.data:
            raise ValueError('token_endpoint is required')

    def to_dict(self, with_defaults=False):
        ret = OrderedDict()
        for name, default, required in self._attributes:
            if name in self.data:
                ret[name] = self.data[name]
                continue
            if with_defaults and default is not None:
                ret[name] = default

        additionals = set(self.data.keys()) - set(ret.keys())
        for name in additionals:
            ret[name] = self.data[name]

        return ret
