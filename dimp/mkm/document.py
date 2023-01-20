# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2022 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
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

from typing import Dict, Any, Optional, Union

from mkm import ID, Document, DocumentFactory
from mkm.core.factory import FactoryManager

from .profile import BaseDocument, BaseVisa, BaseBulletin


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
            gf = FactoryManager.general_factory
            doc_type = gf.get_document_type(identifier=document)
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
