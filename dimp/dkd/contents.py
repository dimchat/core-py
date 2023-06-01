# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
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

from mkm.crypto import base64_encode, base64_decode
from mkm import ID
from dkd import ContentType, Content
from dkd import ReliableMessage

from ..protocol import TextContent, ArrayContent, ForwardContent, CustomizedContent
from ..protocol import PageContent, MoneyContent, TransferContent

from .base import BaseContent


class BaseTextContent(BaseContent, TextContent):
    """
        Text Message Content
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x01,
            sn   : 123,

            text : "..."
        }
    """

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 text: Optional[str] = None):
        if content is None:
            super().__init__(msg_type=ContentType.TEXT)
        else:
            super().__init__(content=content)
        if text is not None:
            self.text = text

    #
    #   text
    #
    @property  # Override
    def text(self) -> Optional[str]:
        return self.get_str(key='text')

    @text.setter  # Override
    def text(self, value: Optional[str]):
        if value is None:
            self.pop('text', None)
        else:
            self['text'] = value


class ListContent(BaseContent, ArrayContent):
    """
        Content Array message
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0xCA,
            sn   : 123,

            contents : [...]  // content list
        }
    """

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 contents: Optional[List[Content]] = None):
        if content is None:
            super().__init__(msg_type=ContentType.ARRAY)
        else:
            super().__init__(content=content)
        self.__contents = contents
        if contents is not None:
            self['contents'] = ArrayContent.revert(contents=contents)

    @property  # Override
    def contents(self) -> Optional[List[Content]]:
        if self.__contents is None:
            array = self.get(key='contents')
            if array is None:
                self.__contents = []
            else:
                self.__contents = ArrayContent.convert(contents=array)
        return self.__contents


class AppCustomizedContent(BaseContent, CustomizedContent):
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

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 msg_type: Union[int, ContentType] = 0,
                 app: Optional[str] = None, mod: Optional[str] = None, act: Optional[str] = None):
        if content is None:
            if msg_type == 0:
                msg_type = ContentType.CUSTOMIZED
            super().__init__(msg_type=msg_type)
        else:
            super().__init__(content=content)
        if app is not None:
            self['app'] = app
        if mod is not None:
            self['mod'] = mod
        if act is not None:
            self['act'] = act

    @property  # Override
    def application(self) -> str:
        return self.get_str(key='app')

    @property  # Override
    def module(self) -> str:
        return self.get_str(key='mod')

    @property  # Override
    def action(self) -> str:
        return self.get_str(key='act')


class SecretContent(BaseContent, ForwardContent):
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

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 message: Optional[ReliableMessage] = None,
                 messages: Optional[List[ReliableMessage]] = None):
        if content is None:
            super().__init__(msg_type=ContentType.FORWARD)
        else:
            super().__init__(content=content)
        self.__forward = message
        self.__secrets = messages
        if message is not None:
            self['forward'] = message.dictionary
        if messages is not None:
            self['secrets'] = ForwardContent.revert(messages=messages)

    #
    #   forward (top-secret message)
    #
    @property  # Override
    def forward(self) -> ReliableMessage:
        if self.__forward is None:
            msg = self.get(key='forward')
            self.__forward = ReliableMessage.parse(msg=msg)
            # assert msg is not None, 'forward message not found: %s' % self.dictionary
        return self.__forward

    @property  # Override
    def secrets(self) -> List[ReliableMessage]:
        if self.__secrets is None:
            messages = self.get(key='secrets')
            if messages is None:
                # get from 'forward'
                msg = self.forward
                if msg is None:
                    self.__secrets = []
                else:
                    self.__secrets = [msg]
            else:
                # get from 'secrets'
                self.__secrets = ForwardContent.convert(messages=messages)
        return self.__secrets


class WebPageContent(BaseContent, PageContent):
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

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 url: Optional[str] = None, title: Optional[str] = None,
                 desc: Optional[str] = None, icon: Union[bytes, str, None] = None):
        if content is None:
            super().__init__(msg_type=ContentType.PAGE)
        else:
            super().__init__(content=content)
        if url is not None:
            self['URL'] = url
        if title is not None:
            self['title'] = title
        if desc is not None:
            self['desc'] = desc
        if icon is None:
            self.__icon = None
        elif isinstance(icon, bytes):
            self['icon'] = base64_encode(data=icon)
            self.__icon = icon
        else:
            assert isinstance(icon, str), 'Page icon error: %s' % icon
            self['icon'] = icon
            self.__icon = None

    @property  # Override
    def url(self) -> str:
        return self.get_str(key='URL')

    @url.setter  # Override
    def url(self, string: str):
        self['URL'] = string

    @property  # Override
    def title(self) -> Optional[str]:
        return self.get_str(key='title')

    @title.setter  # Override
    def title(self, string: Optional[str]):
        if string is None:
            self.pop('title', None)
        else:
            self['title'] = string

    @property  # Override
    def desc(self) -> Optional[str]:
        return self.get_str(key='desc')

    @desc.setter  # Override
    def desc(self, string: Optional[str]):
        if string is None:
            self.pop('desc', None)
        else:
            self['desc'] = string

    @property  # Override
    def icon(self) -> Optional[bytes]:
        if self.__icon is None:
            base64 = self.get_str(key='icon')
            if base64 is not None:
                self.__icon = base64_decode(string=base64)
        return self.__icon

    @icon.setter
    def icon(self, image: Optional[bytes]):
        if image is None:
            self.pop('icon', None)
        else:
            self['icon'] = base64_encode(data=image)
        self.__icon = image


class BaseMoneyContent(BaseContent, MoneyContent):
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

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 msg_type: Union[int, ContentType] = 0,
                 currency: Optional[str] = None, amount: Optional[float] = 0.0):
        if content is None and msg_type == 0:
            msg_type = ContentType.MONEY
        super().__init__(content=content, msg_type=msg_type)
        # set values to inner dictionary
        if currency is not None:
            self['currency'] = currency
        if amount > 0:
            self['amount'] = amount

    @property  # Override
    def currency(self) -> str:
        return self.get_str(key='currency')

    @property  # Override
    def amount(self) -> float:
        value = self.get_float(key='amount')
        return 0 if value is None else float(value)

    @amount.setter  # Override
    def amount(self, value: float):
        self['amount'] = value


class TransferMoneyContent(BaseMoneyContent, TransferContent):
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

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 currency: Optional[str] = None, amount: Optional[float] = 0.0):
        super().__init__(content=content, msg_type=ContentType.TRANSFER, currency=currency, amount=amount)

    @property  # Override
    def remitter(self) -> Optional[ID]:
        sender = self.get(key='remitter')
        return ID.parse(identifier=sender)

    @remitter.setter  # Override
    def remitter(self, sender: Optional[ID]):
        if sender is None:
            self.pop('remitter', None)
        else:
            self['remitter'] = str(sender)

    @property  # Override
    def remittee(self) -> Optional[ID]:
        receiver = self.get(key='remittee')
        return ID.parse(identifier=receiver)

    @remittee.setter  # Override
    def remittee(self, receiver: Optional[ID]):
        if receiver is None:
            self.pop('remittee', None)
        else:
            self['remittee'] = str(receiver)
