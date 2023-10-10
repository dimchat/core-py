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
from mkm import Document
from mkm import Visa, Bulletin

from .document import BaseDocument


class BaseVisa(BaseDocument, Visa):

    def __init__(self, document: Optional[Dict[str, Any]] = None,
                 identifier: Optional[ID] = None,
                 data: Optional[str] = None, signature: Optional[TransportableData] = None):
        super().__init__(document, doc_type=Document.VISA, identifier=identifier, data=data, signature=signature)
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
            info = self.get_property(key='key')
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
        self.set_property(key='key', value=info)
        self.__key = key

    """
        Avatar
        ~~~~~~
    """

    @property  # Override
    def avatar(self) -> Optional[PortableNetworkFile]:
        if self.__avatar is None:
            url = self.get_property(key='avatar')
            self.__avatar = PortableNetworkFile.parse(url)
        return self.__avatar

    @avatar.setter  # Override
    def avatar(self, url: PortableNetworkFile):
        info = None if url is None else url.object
        self.set_property(key='avatar', value=info)
        self.__avatar = url


class BaseBulletin(BaseDocument, Bulletin):

    def __init__(self, document: Optional[Dict[str, Any]] = None,
                 identifier: Optional[ID] = None,
                 data: Optional[str] = None, signature: Optional[TransportableData] = None):
        super().__init__(document, doc_type=Document.BULLETIN, identifier=identifier, data=data, signature=signature)
        # lazy
        self.__bots: Optional[List[ID]] = None

    @property  # Override
    def founder(self) -> Optional[ID]:
        return ID.parse(identifier=self.get_property(key='founder'))

    @property  # Override
    def assistants(self) -> Optional[List[ID]]:
        if self.__bots is None:
            bots = self.get_property(key='assistants')
            if bots is None:
                # get from 'assistant'
                ass = self.get_property(key='assistant')
                bot = ID.parse(identifier=ass)
                self.__bots = [] if bot is None else [bot]
            else:
                self.__bots = ID.convert(bots)
        return self.__bots

    @assistants.setter  # Override
    def assistants(self, bots: List[ID]):
        array = None if bots is None else ID.revert(bots)
        self.set_property(key='assistants', value=array)
        self.set_property(key='assistant', value=None)
        self.__bots = bots
