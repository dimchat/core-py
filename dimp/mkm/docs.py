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

from typing import Optional, Dict

from mkm.types import Converter
from mkm.crypto import PublicKey, EncryptKey
from mkm.format import TransportableData
from mkm.protocol import ID

from ..format import TransportableFile
from ..protocol import DocumentType
from ..protocol import Visa, Bulletin

from .document import BaseDocument


class BaseVisa(BaseDocument, Visa):

    def __init__(self, document: Optional[Dict] = None,
                 data: Optional[str] = None, signature: Optional[TransportableData] = None):
        if document is not None:
            # 0. document from network
            assert data is None and signature is None,  'params error: %s, %s, %s' % (document, data, signature)
            super().__init__(document)
        else:
            # 1. document from local
            doc_type = DocumentType.VISA
            super().__init__(None, doc_type, data=data, signature=signature)
        # lazy load
        self.__key: Optional[EncryptKey] = None
        self.__avatar: Optional[TransportableFile] = None

    @property  # Override
    def name(self) -> Optional[str]:
        nickname = self.get_property(name='name')
        return Converter.get_str(value=nickname)

    @name.setter  # Override
    def name(self, nickname: str):
        self.set_property(name='name', value=nickname)

    """
        Public Key for encryption
        ~~~~~~~~~~~~~~~~~~~~~~~~~
        For safety considerations, the visa.key which used to encrypt message data
        should be different with meta.key
    """

    @property  # Override
    def public_key(self) -> Optional[EncryptKey]:
        visa_key = self.__key
        if visa_key is None:
            info = self.get_property(name='key')
            # assert info is not None, 'visa key not found: %s' % self.to_dict()
            pub = PublicKey.parse(key=info)
            if isinstance(pub, EncryptKey):
                visa_key = pub
                self.__key = visa_key
            else:
                assert info is None, 'visa key error: %s' % info
        return visa_key

    @public_key.setter  # Override
    def public_key(self, key: EncryptKey):
        info = None if key is None else key.to_dict()
        self.set_property(name='key', value=info)
        self.__key = key

    """
        Avatar
        ~~~~~~
    """

    @property  # Override
    def avatar(self) -> Optional[TransportableFile]:
        img = self.__avatar
        if img is None:
            url = self.get_property(name='avatar')
            if isinstance(url, str) and len(url) == 0:
                # ignore empty URL
                # FIXME: handle it in PNF parser?
                return None
            img = TransportableFile.parse(url)
            self.__avatar = img
        return img

    @avatar.setter  # Override
    def avatar(self, img: TransportableFile):
        info = None if img is None else img.serialize()
        self.set_property(name='avatar', value=info)
        self.__avatar = img


class BaseBulletin(BaseDocument, Bulletin):

    def __init__(self, document: Optional[Dict] = None,
                 data: Optional[str] = None, signature: Optional[TransportableData] = None):
        if document is not None:
            # 0. document from network
            assert data is None and signature is None, 'params error: %s, %s, %s' % (document, data, signature)
            super().__init__(document)
        else:
            # 1. document from local
            doc_type = DocumentType.BULLETIN
            super().__init__(None, doc_type, data=data, signature=signature)

    @property  # Override
    def name(self) -> Optional[str]:
        title = self.get_property(name='name')
        return Converter.get_str(value=title)

    @name.setter  # Override
    def name(self, title: str):
        self.set_property(name='name', value=title)

    @property  # Override
    def founder(self) -> Optional[ID]:
        uid = self.get_property(name='founder')
        return ID.parse(identifier=uid)
