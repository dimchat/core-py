# -*- coding: utf-8 -*-
#
#   Ming-Ke-Ming : Decentralized User Identity Authentication
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

from abc import ABC
from typing import Optional, Union, Any, Dict

from mkm.crypto import base64_encode, base64_decode
from mkm.crypto import VerifyKey, PublicKey
from mkm.types import Dictionary
from mkm.protocol import meta_has_seed
from mkm import Meta, MetaType


class BaseMeta(Dictionary, Meta, ABC):

    def __init__(self, meta: Optional[Dict[str, Any]] = None,
                 version: Union[MetaType, int] = 0, key: Optional[VerifyKey] = None,
                 seed: Optional[str] = None, fingerprint: Union[bytes, str, None] = None):
        # check parameters
        if isinstance(version, MetaType):
            version = version.value
        if fingerprint is None:
            base64 = None
        elif isinstance(fingerprint, bytes):
            base64 = base64_encode(data=fingerprint)
        else:
            # assert isinstance(fingerprint, str), 'meta.fingerprint error: %s' % fingerprint
            base64 = fingerprint
            fingerprint = base64_decode(string=base64)
        if meta is None:
            assert version > 0 and key is not None, 'meta error: %d, %s, %s, %s' % (version, key, seed, fingerprint)
            # build meta info
            if seed is None or base64 is None:
                meta = {
                    'type': version,
                    'key': key.dictionary,
                }
            else:
                meta = {
                    'type': version,
                    'key': key.dictionary,
                    'seed': seed,
                    'fingerprint': base64,
                }
        # initialize with meta info
        super().__init__(dictionary=meta)
        # lazy load
        self.__type = version
        self.__key = key
        self.__seed = seed
        self.__fingerprint = fingerprint

    @property  # Override
    def type(self) -> int:
        if self.__type == 0:
            self.__type = self.get_int(key='type')
        return self.__type

    @property  # Override
    def key(self) -> VerifyKey:
        if self.__key is None:
            key = self.get(key='key')
            self.__key = PublicKey.parse(key=key)
        return self.__key

    @property  # Override
    def seed(self) -> Optional[str]:
        if self.__seed is None and meta_has_seed(version=self.type):
            self.__seed = self.get_str(key='seed')
        return self.__seed

    @property  # Override
    def fingerprint(self) -> Optional[bytes]:
        if self.__fingerprint is None and meta_has_seed(version=self.type):
            fingerprint = self.get_str(key='fingerprint')
            if fingerprint is not None:
                self.__fingerprint = base64_decode(string=fingerprint)
        return self.__fingerprint
