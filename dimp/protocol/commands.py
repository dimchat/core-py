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

from mkm import ID, Meta, Document
from dkd import Content


class Command(Content, ABC):
    """
        Command Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command : "...", // command name
            extra   : info   // command parameters
        }
    """

    # -------- command names begin --------
    META = 'meta'
    DOCUMENT = 'document'
    RECEIPT = 'receipt'
    # -------- command names end --------

    @property
    @abstractmethod
    def cmd(self) -> str:
        """ get command name """
        raise NotImplemented

    #
    #   Factory method
    #

    @classmethod
    def parse(cls, content: Any):  # -> Optional[Command]:
        gf = general_factory()
        return gf.parse_command(content=content)

    @classmethod
    def factory(cls, cmd: str):  # -> Optional[CommandFactory]:
        gf = general_factory()
        return gf.get_command_factory(cmd=cmd)

    @classmethod
    def register(cls, cmd: str, factory):
        gf = general_factory()
        gf.set_command_factory(cmd=cmd, factory=factory)


def general_factory():
    from ..dkd.factory import CommandFactoryManager
    return CommandFactoryManager.general_factory


class CommandFactory:

    @abstractmethod
    def parse_command(self, content: Dict[str, Any]) -> Optional[Command]:
        """
        Parse map object to command

        :param content: command content
        :return: Command
        """
        raise NotImplemented


class MetaCommand(Command, ABC):
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

    #
    #   ID
    #
    @property
    @abstractmethod
    def identifier(self) -> ID:
        raise NotImplemented

    #
    #   Meta
    #
    @property
    @abstractmethod
    def meta(self) -> Optional[Meta]:
        raise NotImplemented

    #
    #   Factory methods
    #

    @classmethod
    def query(cls, identifier: ID):  # -> MetaCommand:
        """
        Query meta

        :param identifier: entity ID
        :return: MetaCommand
        """
        from ..dkd import BaseMetaCommand
        return BaseMetaCommand(identifier=identifier)

    @classmethod
    def response(cls, identifier: ID, meta: Meta):  # -> MetaCommand:
        """
        Response Meta

        :param identifier: entity ID
        :param meta: entity meta
        :return: MetaCommand
        """
        from ..dkd import BaseMetaCommand
        return BaseMetaCommand(identifier=identifier, meta=meta)


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
        Document's signature (just for querying new document)

        :return: part of signature in current document (base64)
        """
        raise NotImplemented

    #
    #   Factory methods
    #

    @classmethod
    def query(cls, identifier: ID, signature: str = None):  # -> DocumentCommand:
        """
        1. Query Entity Document
        2. Query Entity Document for updating with current signature

        :param identifier: entity ID
        :param signature:  document signature
        :return: DocumentCommand
        """
        from ..dkd import BaseDocumentCommand
        return BaseDocumentCommand(identifier=identifier, signature=signature)

    @classmethod
    def response(cls, document: Document, meta: Optional[Meta] = None, identifier: ID = None):
        """
        1. Send Meta and Document to new friend
        2. Response Entity Document

        :param identifier: entity ID
        :param meta:       entity meta
        :param document:   entity document
        :return: DocumentCommand
        """
        from ..dkd import BaseDocumentCommand
        return BaseDocumentCommand(identifier=identifier, meta=meta, document=document)
