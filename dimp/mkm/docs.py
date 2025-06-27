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

from typing import Optional, Any, Dict, List

from mkm.crypto import PublicKey, EncryptKey
from mkm.format import TransportableData
from mkm.format import PortableNetworkFile
from mkm import ID

from ..protocol import DocumentType
from ..protocol import Visa, Bulletin

from .document import BaseDocument


class BaseVisa(BaseDocument, Visa):

    def __init__(self, document: Optional[Dict[str, Any]] = None,
                 identifier: ID = None, data: Optional[str] = None, signature: Optional[TransportableData] = None):
        if document is None:
            # 1. document from local
            assert identifier is not None, 'visa info error: %s, %s' % (data, signature)
            doc_type = DocumentType.VISA
            super().__init__(None, doc_type, identifier=identifier, data=data, signature=signature)
        else:
            # 2. document from network
            assert identifier is None and data is None and signature is None, \
                'params error: %s, %s, %s, %s' % (document, identifier, data, signature)
            super().__init__(document)
        # lazy
        self.__key: Optional[EncryptKey] = None
        self.__avatar: Optional[PortableNetworkFile] = None

    """
        Public Key for encryption
        ~~~~~~~~~~~~~~~~~~~~~~~~~
        For safety considerations, the visa.key which used to encrypt message data
        should be different with meta.key
    """

    @property  # Override
    def public_key(self) -> Optional[EncryptKey]:
        if self.__key is None:
            info = self.get_property(name='key')
            # assert info is not None, 'visa key not found: %s' % self.dictionary
            pub = PublicKey.parse(key=info)
            if isinstance(pub, EncryptKey):
                self.__key = pub
            else:
                assert info is None, 'visa key error: %s' % info
        return self.__key

    @public_key.setter  # Override
    def public_key(self, key: EncryptKey):
        info = None if key is None else key.dictionary
        self.set_property(name='key', value=info)
        self.__key = key

    """
        Avatar
        ~~~~~~
    """

    @property  # Override
    def avatar(self) -> Optional[PortableNetworkFile]:
        if self.__avatar is None:
            url = self.get_property(name='avatar')
            if isinstance(url, str) and len(url) == 0:
                # ignore empty URL
                pass
            else:
                self.__avatar = PortableNetworkFile.parse(url)
        return self.__avatar

    @avatar.setter  # Override
    def avatar(self, url: PortableNetworkFile):
        info = None if url is None else url.object
        self.set_property(name='avatar', value=info)
        self.__avatar = url


class BaseBulletin(BaseDocument, Bulletin):

    def __init__(self, document: Optional[Dict[str, Any]] = None,
                 identifier: ID = None,
                 data: Optional[str] = None, signature: Optional[TransportableData] = None):
        if document is None:
            # 1. document from local
            assert identifier is not None, 'bulletin info error: %s, %s' % (data, signature)
            doc_type = DocumentType.BULLETIN
            super().__init__(None, doc_type, identifier=identifier, data=data, signature=signature)
        else:
            # 2. document from network
            assert identifier is None and data is None and signature is None, \
                'params error: %s, %s, %s, %s' % (document, identifier, data, signature)
            super().__init__(document)
        # lazy
        self.__bots: Optional[List[ID]] = None

    @property  # Override
    def founder(self) -> Optional[ID]:
        identifier = self.get_property(name='founder')
        return ID.parse(identifier=identifier)

    @property  # Override
    def assistants(self) -> Optional[List[ID]]:
        if self.__bots is None:
            bots = self.get_property(name='assistants')
            if bots is None:
                # get from 'assistant'
                single = self.get_property(name='assistant')
                single = ID.parse(identifier=single)
                self.__bots = [] if single is None else [single]
            else:
                self.__bots = ID.convert(array=bots)
        return self.__bots

    @assistants.setter  # Override
    def assistants(self, bots: List[ID]):
        array = None if bots is None else ID.revert(identifiers=bots)
        self.set_property(name='assistants', value=array)
        self.set_property(name='assistant', value=None)
        self.__bots = bots
