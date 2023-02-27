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

"""
    Document Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    1. contains 'ID' only, means query document for ID
    2. contains 'document' and 'signature' (must match), means reply
"""

from abc import ABC, abstractmethod
from typing import Optional

from mkm import ID, Meta, Document

from .meta import MetaCommand


class DocumentCommand(MetaCommand, ABC):
    """
        Document Command
        ~~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command   : "document", // command name
            ID        : "{ID}",     // entity ID
            meta      : {...},      // only for handshaking with new friend
            document  : {...},      // when document is empty, means query for ID
            signature : "..."       // old document's signature for querying
        }

    """

    #
    #   document
    #
    @property
    @abstractmethod
    def document(self) -> Optional[Document]:
        raise NotImplemented

    @property
    @abstractmethod
    def signature(self) -> Optional[str]:
        """
        signature for checking new document

        :return: part of signature in current document (base64)
        """
        raise NotImplemented

    #
    #   Factory methods
    #

    @classmethod
    def query(cls, identifier: ID, signature: Optional[str] = None):
        from ..dkd import BaseDocumentCommand
        return BaseDocumentCommand(identifier=identifier, signature=signature)

    @classmethod
    def response(cls, document: Document, meta: Optional[Meta] = None, identifier: Optional[ID] = None):
        from ..dkd import BaseDocumentCommand
        return BaseDocumentCommand(identifier=identifier, meta=meta, document=document)
