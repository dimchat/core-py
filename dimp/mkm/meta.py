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

from abc import ABC
from typing import Optional, Any, Dict

from mkm.format import utf8_encode
from mkm.format import TransportableData
from mkm.crypto import VerifyKey, PublicKey
from mkm.types import Dictionary
from mkm.factory import AccountFactoryManager
from mkm import ID, Address
from mkm import Meta, MetaType


"""
    User/Group Meta data
    ~~~~~~~~~~~~~~~~~~~~
    This class is used to generate entity ID

        data format: {
            type: 1,             // meta version
            seed: "moKy",        // user/group name
            key: "{public key}", // PK = secp256k1(SK);
            fingerprint: "..."   // CT = sign(seed, SK);
        }

        algorithm:
            fingerprint = sign(seed, SK);

    abstractmethod:
        - generate_address(network)
"""


# noinspection PyAbstractClass
class BaseMeta(Dictionary, Meta, ABC):

    def __init__(self, meta: Dict[str, Any] = None,
                 version: int = None, public_key: VerifyKey = None,
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
            assert version is not None and version > 0 and public_key is not None and not MetaType.has_seed(version), \
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
            assert version is not None and version > 0 and public_key is not None and MetaType.has_seed(version), \
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
    def type(self) -> int:
        version = self.__type
        if version is None:
            gf = AccountFactoryManager.general_factory
            version = gf.get_meta_type(meta=self.dictionary, default=0)
            self.__type = version
            # self.__type = self.get_int(key='type', default=0)
        return version

    @property  # Override
    def public_key(self) -> VerifyKey:
        if self.__key is None:
            info = self.get('key')
            pub = PublicKey.parse(key=info)
            self.__key = pub
            assert pub is not None, 'meta key error: %s' % info
        return self.__key

    @property  # Override
    def seed(self) -> Optional[str]:
        if self.__seed is None and MetaType.has_seed(self.type):
            self.__seed = self.get_str(key='seed', default=None)
            assert self.__seed is not None, 'meta.seed empty: %s' % self
        return self.__seed

    @property  # Override
    def fingerprint(self) -> Optional[bytes]:
        ted = self.__fingerprint
        if ted is None and MetaType.has_seed(self.type):
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
            if MetaHelper.check_meta(meta=self):
                # correct
                self.__status = 1
            else:
                # error
                self.__status = -1
        return self.__status > 0

    # Override
    def match_identifier(self, identifier: ID) -> bool:
        return MetaHelper.match_identifier(identifier=identifier, meta=self)

    # Override
    def match_public_key(self, key: VerifyKey) -> bool:
        return MetaHelper.match_public_key(key=key, meta=self)


class MetaHelper:

    @classmethod
    def check_meta(cls, meta: Meta) -> bool:
        key = meta.public_key
        # assert key is not None, 'meta.key should not be empty: %s' % meta
        seed = meta.seed
        fingerprint = meta.fingerprint
        no_seed = seed is None or len(seed) == 0
        no_sig = fingerprint is None or len(fingerprint) == 0
        # check meta version
        if not MetaType.has_seed(meta.type):
            # this meta has no seed, so no fingerprint too
            return no_seed and no_sig
        elif no_seed or no_sig:
            # seed and fingerprint should not be empty
            return False
        # verify fingerprint
        return key.verify(data=utf8_encode(string=seed), signature=fingerprint)

    @classmethod
    def match_identifier(cls, identifier: ID, meta: Meta) -> bool:
        assert meta.valid, 'meta not valid: %s' % meta
        # check ID.name
        seed = meta.seed
        name = identifier.name
        if name is None or len(name) == 0:
            if seed is not None and len(seed) > 0:
                return False
        elif name != seed:
            return False
        # check ID.address
        old = identifier.address
        gen = Address.generate(meta=meta, network=old.type)
        return old == gen

    @classmethod
    def match_public_key(cls, key: VerifyKey, meta: Meta) -> bool:
        assert meta.valid, 'meta not valid: %s' % meta
        # check whether the public key equals to meta.key
        if key == meta.public_key:
            return True
        # check with seed & fingerprint
        if MetaType.has_seed(meta.type):
            # check whether keys equal by verifying signature
            seed = meta.seed
            fingerprint = meta.fingerprint
            assert seed is not None and fingerprint is not None, 'meta error: %s' % meta
            return key.verify(data=utf8_encode(string=seed), signature=fingerprint)
        # NOTICE: ID with BTC/ETH address has no username, so
        #         just compare the key.data to check matching
        # return False
