# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

"""
    Certificate Authority
    ~~~~~~~~~~~~~~~~~~~~~

    Certificates for Stations and Service Providers
"""

import json

from dkd.utils import base64_decode

from mkm import PublicKey


class CASubject(dict):

    # def __new__(cls, subject: dict):
    #     return super().__new__(cls, subject)

    def __init__(self, subject: dict):
        super().__init__(subject)
        if 'C' in subject:
            self.country = subject['C']   # C:  CN, US, ...
        else:
            self['C'] = 'CN'
            self.country = 'CN'
        if 'ST' in subject:
            self.state = subject['ST']    # ST: province
        else:
            self.state = None
        if 'L' in subject:
            self.locality = subject['L']  # L:  city
        else:
            self.locality = None

        self.organization = subject['O']  # O:  Co., Ltd.
        self.unit = subject['OU']         # OU: Department
        self.name = subject['CN']         # CN: domain/ip


class CAValidity(dict):

    def __init__(self, validity: dict):
        super().__init__(validity)
        self.begin = int(validity['NotBefore'])  # notBefore
        self.end = int(validity['NotAfter'])     # notAfter


class CAData(dict):

    def __init__(self, data: dict):
        super().__init__(data)
        self.issuer = CASubject(data['Issuer'])       # issuer DN
        self.validity = CAValidity(data['Validity'])  # validity
        self.subject = CASubject(data['Subject'])     # the CA owner
        if 'PublicKey' in data:
            self.key = PublicKey(data['PublicKey'])   # owner's PK
        elif 'Key' in data:
            self.key = PublicKey(data['Key'])


class CertificateAuthority(dict):

    def __init__(self, ca: dict):
        super().__init__(ca)
        # version
        self.version = int(ca['version'])
        # serial number
        if 'serialNumber' in ca:
            self.sn = ca['serialNumber']
        else:
            self.sn = ca['sn']
        # info (JsON string)
        self.info = CAData(json.loads(ca['info']))
        # signature of info with Issuer's Public Key
        self.signature = base64_decode(ca['signature'])
        # extensions (dict)
        if 'extensions' in ca:
            self.extensions = ca['extensions']

    def verify(self, key: PublicKey) -> bool:
        """
        Verify the CA info with the Issuer's Public Key

        :param key: Issuer's Public Key
        :return: True/False
        """

        # TODO: check validity

        data = self['info']
        return key.verify(data, self.signature)
