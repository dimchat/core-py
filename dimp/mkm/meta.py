# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
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

from abc import ABC, abstractmethod
from typing import Optional, Any, Dict

from mkm.format import utf8_encode
from mkm.format import TransportableData
from mkm.crypto import VerifyKey, PublicKey
from mkm.types import Dictionary
from mkm.plugins import SharedAccountExtensions
from mkm import Meta


"""
    User/Group Meta data
    ~~~~~~~~~~~~~~~~~~~~
    This class is used to generate entity ID

    data format: {
        type       : 1,              // meta version
        seed       : "moKy",         // user/group name
        key        : "{public key}", // PK = secp256k1(SK);
        fingerprint: "..."           // CT = sign(seed, SK);
    }

    algorithm:
        fingerprint = sign(seed, SK);

    abstractmethod:
        - generate_address(network)
"""


# noinspection PyAbstractClass
class BaseMeta(Dictionary, Meta, ABC):

    def __init__(self, meta: Dict[str, Any] = None,
                 version: str = None, public_key: VerifyKey = None,
                 seed: Optional[str] = None, fingerprint: Optional[TransportableData] = None):
        # check parameters
        if meta is not None:
            # 0. meta info from network
            assert version is None and public_key is None and seed is None and fingerprint is None, \
                'params error: %s, %s, %s, %s, %s' % (meta, version, public_key, seed, fingerprint)
            # waiting to verify
            # all metas must be verified before saving into local storage
            status = 0
        elif seed is None or fingerprint is None:
            # 1. new meta with type & public key only
            assert version is not None and public_key is not None, \
                'meta info error: %s, %s, %s, %s' % (version, public_key, seed, fingerprint)
            assert seed is None and fingerprint is None, 'meta seed/fingerprint error'
            meta = {
                'type': version,
                'key': public_key.dictionary,
            }
            # generated meta, or loaded from local storage,
            # no need to verify again.
            status = 1
        else:
            # 2. new meta with type, public key, seed & fingerprint
            assert version is not None and public_key is not None, \
                'meta info error: %s, %s, %s, %s' % (version, public_key, seed, fingerprint)
            meta = {
                'type': version,
                'key': public_key.dictionary,
                'seed': seed,
                'fingerprint': fingerprint.object,
            }
            # generated meta, or loaded from local storage,
            # no need to verify again.
            status = 1
        # initialize with meta info
        super().__init__(dictionary=meta)
        # lazy load
        self.__type = version
        self.__key = public_key
        self.__seed = seed
        self.__fingerprint = fingerprint
        self.__status = status

    @property  # Override
    def type(self) -> str:
        if self.__type is None:
            ext = SharedAccountExtensions()
            self.__type = ext.helper.get_meta_type(meta=self.dictionary, default='')
            # self.__type = self.get_int(key='type', default=0)
        return self.__type

    @property  # Override
    def public_key(self) -> VerifyKey:
        if self.__key is None:
            info = self.get('key')
            self.__key = PublicKey.parse(key=info)
            assert self.__key is not None, 'meta key error: %s' % info
        return self.__key

    # protected
    @property
    @abstractmethod
    def has_seed(self) -> bool:
        # version = self.type
        # return version == 'MKM' or version == '1'
        raise NotImplemented

    @property  # Override
    def seed(self) -> Optional[str]:
        if self.__seed is None and self.has_seed:
            self.__seed = self.get_str(key='seed', default='')
            assert self.__seed is not None, 'meta.seed empty: %s' % self
        return self.__seed

    @property  # Override
    def fingerprint(self) -> Optional[bytes]:
        ted = self.__fingerprint
        if ted is None and self.has_seed:
            base64 = self.get('fingerprint')
            assert base64 is not None, 'meta.fingerprint should not be empty: %s' % self
            self.__fingerprint = ted = TransportableData.parse(base64)
            assert ted is not None, 'meta.fingerprint error: %s' % base64
        if ted is not None:
            return ted.data

    #
    #   Validation
    #

    @property
    def valid(self) -> bool:
        if self.__status == 0:
            # meta from network, try to verify
            if self._check_valid():
                # correct
                self.__status = 1
            else:
                # error
                self.__status = -1
        return self.__status > 0

    # private
    def _check_valid(self) -> bool:
        key = self.public_key
        if key is None:
            return False
        elif self.has_seed:
            # check 'seed' & 'fingerprint'
            pass
        elif 'seed' in self.dictionary or 'fingerprint' in self.dictionary:
            # this meta has no seed, so
            # it should not contains 'seed' or 'fingerprint'
            return False
        else:
            # this meta has no seed, so it's always valid
            # when the public key exists
            return True
        seed = self.seed
        fingerprint = self.fingerprint
        # check meta seed & signature
        if fingerprint is None or len(fingerprint) == 0:
            # meta error
            return False
        elif seed is None or len(seed) == 0:
            # meta error
            return False
        # verify fingerprint
        data = utf8_encode(string=seed)
        return key.verify(data=data, signature=fingerprint)
