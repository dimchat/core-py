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
    Meta Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~

    1. contains 'ID' only, means query meta for ID
    2. contains 'meta' (must match), means reply
"""

from typing import Optional, Any, Dict

from mkm import ID, Meta, Document

from ..protocol import MetaCommand, DocumentCommand

from .base import Command, BaseCommand


class BaseMetaCommand(BaseCommand, MetaCommand):
    """
        Meta Command
        ~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command : "meta", // command name
            ID      : "{ID}", // contact's ID
            meta    : {...}   // When meta is empty, means query meta for ID
        }
    """

    def __init__(self, content: Dict[str, Any] = None,
                 cmd: str = None,
                 identifier: ID = None,
                 meta: Optional[Meta] = None):
        if content is None:
            # 1. new command with name, ID & meta
            assert identifier is not None, 'meta command error: %s, %s, %s' % (cmd, identifier, meta)
            if cmd is None:
                cmd = Command.META
            super().__init__(cmd=cmd)
            self.set_string(key='ID', value=identifier)
            if meta is not None:
                self.set_map(key='meta', value=meta)
        else:
            # 2. command info from network
            assert cmd is None and identifier is None and meta is None, \
                'params error: %s, %s, %s, %s' % (content, cmd, identifier, meta)
            super().__init__(content)
        # lazy load
        self.__id = identifier
        self.__meta = meta

    #
    #   ID
    #
    @property  # Override
    def identifier(self) -> ID:
        if self.__id is None:
            self.__id = ID.parse(identifier=self.get('ID'))
        return self.__id

    #
    #   Meta
    #
    @property  # Override
    def meta(self) -> Optional[Meta]:
        if self.__meta is None:
            self.__meta = Meta.parse(meta=self.get('meta'))
        return self.__meta


class BaseDocumentCommand(BaseMetaCommand, DocumentCommand):
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

    def __init__(self, content: Dict[str, Any] = None,
                 identifier: ID = None,
                 meta: Optional[Meta] = None,
                 document: Optional[Document] = None,
                 signature: Optional[str] = None):
        if content is None:
            # 1. new command with ID, meta, document & signature
            if identifier is None:
                assert document is not None, 'document command error: %s, %s' % (meta, signature)
                identifier = document.identifier
            assert identifier is not None, 'document command error: %s, %s, %s' % (meta, document, signature)
            cmd = Command.DOCUMENT
            super().__init__(cmd=cmd, identifier=identifier, meta=meta)
            if document is not None:
                self['document'] = document.dictionary
            if signature is not None:
                self['signature'] = signature
        else:
            # 2. command info from network
            assert identifier is None and meta is None and document is None and signature is None, \
                'params error: %s, %s, %s, %s, %s' % (content, identifier, meta, document, signature)
            super().__init__(content)
        # lazy load
        self.__doc = document

    #
    #   document
    #
    @property  # Override
    def document(self) -> Optional[Document]:
        if self.__doc is None:
            self.__doc = Document.parse(document=self.get('document'))
        return self.__doc

    @property  # Override
    def signature(self) -> Optional[str]:
        """
        signature for checking new document

        :return: part of signature in current document (base64)
        """
        return self.get_str(key='signature', default=None)
