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
from typing import Optional, Union, List, Dict, Any

from mkm.types import URI
from mkm.format import PortableNetworkFile
from mkm import ID
from dkd import Content, ReliableMessage


class TextContent(Content, ABC):
    """
        Text Message Content
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x01,
            sn   : 123,

            text : "..."
        }
    """

    #
    #   text
    #
    @property
    @abstractmethod
    def text(self) -> str:
        raise NotImplemented

    #
    #   Factory method
    #
    @classmethod
    def create(cls, text: str):
        from ..dkd import BaseTextContent
        return BaseTextContent(text=text)


class ArrayContent(Content, ABC):
    """
        Content Array message
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0xCA,
            sn   : 123,

            contents : [...]  // content array
        }
    """

    @property
    @abstractmethod
    def contents(self) -> List[Content]:
        raise NotImplemented

    #
    #   Factory methods
    #
    @classmethod
    def create(cls, contents: List[Content]):
        from ..dkd import ListContent
        return ListContent(contents=contents)

    @classmethod
    def convert(cls, contents: List[Dict[str, Any]]) -> List[Content]:
        array = []
        for item in contents:
            msg = Content.parse(content=item)
            if msg is None:
                continue
            array.append(msg)
        return array

    @classmethod
    def revert(cls, contents: List[Content]) -> List[Dict[str, Any]]:
        array = []
        for msg in contents:
            info = msg.dictionary
            array.append(info)
        return array


class ForwardContent(Content, ABC):
    """
        Top-Secret Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0xFF,
            sn   : 456,

            forward : {...}  // reliable (secure + certified) message
            secrets : [...]  // reliable (secure + certified) messages
        }
    """

    #
    #   forward (top-secret message)
    #
    @property
    @abstractmethod
    def forward(self) -> Optional[ReliableMessage]:
        raise NotImplemented

    @property
    @abstractmethod
    def secrets(self) -> List[ReliableMessage]:
        raise NotImplemented

    #
    #   Factory methods
    #
    @classmethod
    def create(cls, message: ReliableMessage = None, messages: List[ReliableMessage] = None):
        from ..dkd import SecretContent
        return SecretContent(message=message, messages=messages)

    @classmethod
    def convert(cls, messages: List[Dict[str, Any]]) -> List[ReliableMessage]:
        array = []
        for item in messages:
            msg = ReliableMessage.parse(msg=item)
            if msg is None:
                continue
            array.append(msg)
        return array

    @classmethod
    def revert(cls, messages: List[ReliableMessage]) -> List[Dict[str, Any]]:
        array = []
        for msg in messages:
            info = msg.dictionary
            array.append(info)
        return array


class PageContent(Content, ABC):
    """
        Web Page message
        ~~~~~~~~~~~~~~~~

        data format: {
            type : 0x20,
            sn   : 123,

            URL   : "https://github.com/moky/dimp",  // Page URL
            icon  : "...",                           // base64_encode(icon)
            title : "...",
            desc  : "..."
        }
    """

    @property
    @abstractmethod
    def url(self) -> URI:
        """ Web Page URL """
        raise NotImplemented

    @url.setter
    @abstractmethod
    def url(self, string: URI):
        raise NotImplemented

    @property
    @abstractmethod
    def title(self) -> str:
        """ Document Title """
        raise NotImplemented

    @title.setter
    @abstractmethod
    def title(self, string: str):
        raise NotImplemented

    @property
    @abstractmethod
    def desc(self) -> Optional[str]:
        """ Description """
        raise NotImplemented

    @desc.setter
    @abstractmethod
    def desc(self, string: str):
        raise NotImplemented

    @property
    @abstractmethod
    def icon(self) -> Optional[bytes]:
        """ Image data """
        raise NotImplemented

    @icon.setter
    @abstractmethod
    def icon(self, image: bytes):
        raise NotImplemented

    #
    #   Factory method
    #
    @classmethod
    def create(cls, url: URI, title: str, desc: Optional[str], icon: Union[bytes, str, None]):
        from ..dkd import WebPageContent
        return WebPageContent(url=url, title=title, desc=desc, icon=icon)


class NameCard(Content, ABC):
    """
        Name Card Content
        ~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x33,
            sn   : 123,

            ID     : "{ID}",        // contact's ID
            name   : "{nickname}}", // contact's name
            avatar : "{URL}"        // avatar - PNF(URL)
        }
    """

    @property
    @abstractmethod
    def identifier(self) -> ID:
        raise NotImplemented

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def avatar(self) -> Optional[PortableNetworkFile]:
        raise NotImplemented

    #
    #   Factory method
    #
    @classmethod
    def create(cls, identifier: ID, name: str, avatar: Optional[PortableNetworkFile]):
        from ..dkd import NameCardContent
        return NameCardContent(identifier=identifier, name=name, avatar=avatar)
