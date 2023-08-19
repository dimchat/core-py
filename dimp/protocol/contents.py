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

from dkd import ContentType
from dkd import Content, ReliableMessage
from mkm import ID


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


class CustomizedContent(Content, ABC):
    """
        Application Customized message
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0xCC,
            sn   : 123,

            app   : "{APP_ID}",  // application (e.g.: "chat.dim.sechat")
            mod   : "{MODULE}",  // module name (e.g.: "drift_bottle")
            act   : "{ACTION}",  // action name (e.g.: "throw")
            extra : info         // action parameters
        }
    """

    @property
    @abstractmethod
    def application(self) -> str:
        """ App ID """
        raise NotImplemented

    @property
    @abstractmethod
    def module(self) -> str:
        """ Module Name """
        raise NotImplemented

    @property
    @abstractmethod
    def action(self) -> str:
        """ Action Name """
        raise NotImplemented

    #
    #   Factory method
    #
    @classmethod
    def create(cls, app: str, mod: str, act: str):
        from ..dkd import AppCustomizedContent
        return AppCustomizedContent(app=app, mod=mod, act=act)


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
    def url(self) -> str:
        """ Web Page URL """
        raise NotImplemented

    @url.setter
    @abstractmethod
    def url(self, string: str):
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
    def create(cls, url: str, title: str, desc: Optional[str], icon: Union[bytes, str, None]):
        from ..dkd import WebPageContent
        return WebPageContent(url=url, title=title, desc=desc, icon=icon)


class MoneyContent(Content, ABC):
    """
        Money Message Content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x40,
            sn   : 123,

            currency : "RMB", // USD, USDT, ...
            amount   : 100.00
        }
    """

    @property
    @abstractmethod
    def currency(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def amount(self) -> float:
        raise NotImplemented

    @amount.setter
    @abstractmethod
    def amount(self, value: float):
        raise NotImplemented

    #
    #   Factory method
    #
    @classmethod
    def create(cls, msg_type: Union[int, ContentType], currency: str, amount: float):
        from ..dkd import BaseMoneyContent
        return BaseMoneyContent(msg_type=msg_type, currency=currency, amount=amount)


class TransferContent(MoneyContent, ABC):
    """
        Transfer Money Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x41,
            sn   : 123,

            currency : "RMB",    // USD, USDT, ...
            amount   : 100.00,
            remitter : "{FROM}", // sender ID
            remittee : "{TO}"    // receiver ID
        }
    """

    @property
    @abstractmethod
    def remitter(self) -> ID:
        raise NotImplemented

    @remitter.setter
    @abstractmethod
    def remitter(self, sender: ID):
        raise NotImplemented

    @property
    @abstractmethod
    def remittee(self) -> ID:
        raise NotImplemented

    @remittee.setter
    @abstractmethod
    def remittee(self, receiver: ID):
        raise NotImplemented

    #
    #   Factory method
    #
    @classmethod
    def transfer(cls, currency: str, amount: float):
        from ..dkd import TransferMoneyContent
        return TransferMoneyContent(currency=currency, amount=amount)
