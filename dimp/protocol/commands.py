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
from typing import Optional, Any, List, Dict

from mkm.types import DateTime
from mkm import ID, Meta, Document
from dkd import Content

from .helpers import CommandExtensions


class Command(Content, ABC):
    """
        Command Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x88),
            sn   : 123,

            command : "...", // command name
            extra   : info   // command parameters
        }
    """

    # -------- command names begin --------
    META = 'meta'
    DOCUMENTS = 'documents'
    RECEIPT = 'receipt'
    # -------- command names end --------

    @property
    @abstractmethod
    def cmd(self) -> str:
        """ command/method/declaration """
        raise NotImplemented

    #
    #   Factory method
    #

    @classmethod
    def parse(cls, content: Any):  # -> Optional[Command]:
        helper = CommandExtensions.cmd_helper
        assert isinstance(helper, CommandHelper), 'command helper error: %s' % helper
        return helper.parse_command(content=content)

    @classmethod
    def get_factory(cls, cmd: str):  # -> Optional[CommandFactory]:
        helper = CommandExtensions.cmd_helper
        assert isinstance(helper, CommandHelper), 'command helper error: %s' % helper
        return helper.get_command_factory(cmd=cmd)

    @classmethod
    def set_factory(cls, cmd: str, factory):
        helper = CommandExtensions.cmd_helper
        assert isinstance(helper, CommandHelper), 'command helper error: %s' % helper
        helper.set_command_factory(cmd=cmd, factory=factory)


class CommandFactory(ABC):
    """ Command Factory """

    @abstractmethod
    def parse_command(self, content: Dict[str, Any]) -> Optional[Command]:
        """
        Parse map object to command

        :param content: command content
        :return: Command
        """
        raise NotImplemented


class CommandHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_command_factory(self, cmd: str, factory: CommandFactory):
        raise NotImplemented

    @abstractmethod
    def get_command_factory(self, cmd: str) -> Optional[CommandFactory]:
        raise NotImplemented

    @abstractmethod
    def parse_command(self, content: Any) -> Optional[Command]:
        raise NotImplemented


#############################
#                           #
#       Core Commands       #
#                           #
#############################


class MetaCommand(Command, ABC):
    """
        Meta Command
        ~~~~~~~~~~~~

        data format: {
            type : i2s(0x88),
            sn   : 123,

            command : "meta", // command name
            did     : "{ID}", // contact's ID
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
            type : i2s(0x88),
            sn   : 123,

            command   : "document", // command name
            did       : "{ID}",     // entity ID
            meta      : {...},      // only for handshaking with new friend
            documents : [...],      // when document is empty, means query for ID
            last_time : 12345       // old document time for querying
        }

    """

    #
    #   documents
    #
    @property
    @abstractmethod
    def documents(self) -> Optional[List[Document]]:
        raise NotImplemented

    @property
    @abstractmethod
    def last_time(self) -> Optional[DateTime]:
        """ Last document time for querying """
        raise NotImplemented

    #
    #   Factory methods
    #

    @classmethod
    def query(cls, identifier: ID, last_time: str = None):  # -> DocumentCommand:
        """
        1. Query Entity Document
        2. Query Entity Document for updating with last time

        :param identifier: entity ID
        :param last_time:  last document time
        :return: DocumentCommand
        """
        from ..dkd import BaseDocumentCommand
        return BaseDocumentCommand(identifier=identifier, last_time=last_time)

    @classmethod
    def response(cls, documents: List[Document], meta: Optional[Meta] = None, identifier: ID = None):
        """
        1. Send Meta and Document to new friend
        2. Response Entity Document

        :param identifier: entity ID
        :param meta:       entity meta
        :param documents:  entity documents
        :return: DocumentCommand
        """
        from ..dkd import BaseDocumentCommand
        return BaseDocumentCommand(identifier=identifier, meta=meta, documents=documents)
