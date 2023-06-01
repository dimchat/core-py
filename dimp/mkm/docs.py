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

from typing import Optional, Union, Any, Dict, List

from mkm.crypto import PublicKey, EncryptKey, VerifyKey
from mkm.factory import AccountFactoryManager
from mkm import ID
from mkm import Document, DocumentFactory
from mkm import Visa, Bulletin

from .document import BaseDocument


class BaseVisa(BaseDocument, Visa):

    def __init__(self, document: Optional[Dict[str, Any]] = None,
                 identifier: Optional[ID] = None,
                 data: Optional[str] = None, signature: Union[bytes, str, None] = None):
        super().__init__(document, doc_type=Document.VISA, identifier=identifier, data=data, signature=signature)
        self.__key = None

    """
        Public Key for encryption
        ~~~~~~~~~~~~~~~~~~~~~~~~~
        For safety considerations, the visa.key which used to encrypt message data
        should be different with meta.key
    """

    @property  # Override
    def key(self) -> Union[EncryptKey, VerifyKey, None]:
        if self.__key is None:
            info = self.get_property(key='key')
            if info is not None:
                self.__key = PublicKey.parse(key=info)
        return self.__key

    @key.setter  # Override
    def key(self, value: Union[EncryptKey, VerifyKey]):
        self.set_property(key='key', value=value.dictionary)
        self.__key = value

    """
        Avatar
        ~~~~~~
    """

    @property  # Override
    def avatar(self) -> Optional[str]:
        return self.get_property(key='avatar')

    @avatar.setter  # Override
    def avatar(self, value: str):
        self.set_property(key='avatar', value=value)


class BaseBulletin(BaseDocument, Bulletin):

    def __init__(self, document: Optional[Dict[str, Any]] = None,
                 identifier: Optional[ID] = None,
                 data: Optional[str] = None, signature: Union[bytes, str, None] = None):
        super().__init__(document, doc_type=Document.BULLETIN, identifier=identifier, data=data, signature=signature)
        self.__assistants = None

    @property  # Override
    def assistants(self) -> Optional[List[ID]]:
        if self.__assistants is None:
            assistants = self.get_property(key='assistants')
            if assistants is None:
                self.__assistants = []
            else:
                self.__assistants = ID.convert(array=assistants)
        return self.__assistants

    @assistants.setter  # Override
    def assistants(self, bots: List[ID]):
        if bots is not None and len(bots) > 0:
            bots = ID.revert(array=bots)
        self.set_property(key='assistants', value=bots)
        self.__assistants = bots


class BaseDocumentFactory(DocumentFactory):

    def __init__(self, doc_type: str):
        super().__init__()
        self.__type = doc_type

    # Override
    def create_document(self, identifier: ID, data: Optional[str], signature: Union[bytes, str, None]) -> Document:
        doc_type = get_type(doc_type=self.__type, identifier=identifier)
        if doc_type == Document.BULLETIN:
            return BaseBulletin(identifier=identifier, data=data, signature=signature)
        elif doc_type == Document.VISA:
            return BaseVisa(identifier=identifier, data=data, signature=signature)
        else:
            return BaseDocument(doc_type=doc_type, identifier=identifier, data=data, signature=signature)

    # Override
    def parse_document(self, document: Dict[str, Any]) -> Optional[Document]:
        identifier = ID.parse(identifier=document.get('ID'))
        if identifier is not None:
            # check document type
            gf = AccountFactoryManager.general_factory
            doc_type = gf.get_document_type(document=document)
            if doc_type is None:
                doc_type = get_type(doc_type='*', identifier=identifier)
            # create with document type
            if doc_type == Document.BULLETIN:
                return BaseBulletin(document=document)
            elif doc_type == Document.VISA:
                return BaseVisa(document=document)
            else:
                return BaseDocument(document=document)


def get_type(doc_type: str, identifier: ID) -> str:
    if doc_type == '*':
        if identifier.is_group:
            return Document.BULLETIN
        elif identifier.is_user:
            return Document.VISA
        else:
            return Document.PROFILE
    else:
        return doc_type
