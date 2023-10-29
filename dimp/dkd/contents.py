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

from mkm.format import TransportableData, PortableNetworkFile
from mkm.types import URI
from mkm import ID
from dkd import ContentType, Content
from dkd import ReliableMessage

from ..protocol import TextContent, ArrayContent, ForwardContent
from ..protocol import PageContent, NameCard

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

    def __init__(self, content: Dict[str, Any] = None, text: str = None):
        if content is None:
            # 1. new content with text string
            assert text is not None, 'text should not be None'
            msg_type = ContentType.TEXT.value
            super().__init__(None, msg_type)
            self['text'] = text
        else:
            # 2. content info from network
            assert text is None, 'params error: %s, %s' % (content, text)
            super().__init__(content)

    #
    #   text
    #
    @property  # Override
    def text(self) -> str:
        return self.get_str(key='text', default='')


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

    def __init__(self, content: Dict[str, Any] = None,
                 contents: List[Content] = None):
        if content is None:
            # 1. new content with a list
            assert contents is not None, 'content list should no be None'
            msg_type = ContentType.ARRAY.value
            super().__init__(None, msg_type)
            self['contents'] = ArrayContent.revert(contents=contents)
        else:
            # 2. content info from network
            assert contents is None, 'params error: %s, %s' % (content, contents)
            super().__init__(content)
        # lazy
        self.__list = contents

    @property  # Override
    def contents(self) -> List[Content]:
        if self.__list is None:
            array = self.get('contents')
            if array is None:
                self.__list = []
            else:
                self.__list = ArrayContent.convert(contents=array)
        return self.__list


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

    def __init__(self, content: Dict[str, Any] = None,
                 message: ReliableMessage = None,
                 messages: List[ReliableMessage] = None):
        if content is None:
            # 1. new content with message(s)
            msg_type = ContentType.FORWARD.value
            super().__init__(None, msg_type)
            if message is not None:
                self['forward'] = message.dictionary
            if messages is not None:
                self['secrets'] = ForwardContent.revert(messages=messages)
        else:
            # 2. content info from network
            assert message is None and messages is None, 'params error: %s, %s, %s' % (content, message, messages)
            super().__init__(content)
        # lazy
        self.__forward = message
        self.__secrets = messages

    #
    #   forward (top-secret message)
    #
    @property  # Override
    def forward(self) -> ReliableMessage:
        if self.__forward is None:
            msg = self.get('forward')
            self.__forward = ReliableMessage.parse(msg=msg)
            # assert msg is not None, 'forward message not found: %s' % self.dictionary
        return self.__forward

    @property  # Override
    def secrets(self) -> List[ReliableMessage]:
        if self.__secrets is None:
            messages = self.get('secrets')
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

    def __init__(self, content: Dict[str, Any] = None,
                 url: URI = None, title: str = None,
                 desc: Optional[str] = None, icon: Optional[TransportableData] = None):
        if content is None:
            # 1. new content with url, title, desc & icon
            assert url is not None and title is not None, 'page info error: %s, %s, %s, %s' % (url, title, desc, icon)
            msg_type = ContentType.PAGE.value
            super().__init__(None, msg_type)
            self['URL'] = url
            self['title'] = title
            if desc is not None:
                self['desc'] = desc
            if icon is not None:
                self.set_icon(icon)
        else:
            # 2. content info from network
            assert url is None and title is None and desc is None and icon is None, \
                'params error: %s, %s, %s, %s, %s' % (content, url, title, desc, icon)
            super().__init__(content)
        # lazy
        self.__icon = icon

    @property  # Override
    def url(self) -> URI:
        # TODO: convert str to URI
        return self.get_str(key='URL', default=None)

    @url.setter  # Override
    def url(self, string: URI):
        # TODO: convert URI to str
        self['URL'] = string

    @property  # Override
    def title(self) -> str:
        return self.get_str(key='title', default='')

    @title.setter  # Override
    def title(self, string: str):
        self['title'] = string

    @property  # Override
    def desc(self) -> Optional[str]:
        return self.get_str(key='desc', default=None)

    @desc.setter  # Override
    def desc(self, string: Optional[str]):
        if string is None:
            self.pop('desc', None)
        else:
            self['desc'] = string

    @property  # Override
    def icon(self) -> Optional[bytes]:
        ted = self.__icon
        if ted is None:
            base64 = self.get('icon')
            self.__icon = ted = TransportableData.parse(base64)
        if ted is not None:
            return ted.data

    @icon.setter
    def icon(self, image: Optional[bytes]):
        if image is None or len(image) == 0:
            ted = None
        else:
            ted = TransportableData.create(data=image)
        self.set_icon(ted)

    def set_icon(self, ted: Optional[TransportableData]):
        if ted is None:
            self.pop('icon')
        else:
            self['icon'] = ted.object
        self.__icon = ted


class NameCardContent(BaseContent, NameCard):
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

    def __init__(self, content: Dict[str, Any] = None,
                 identifier: ID = None,
                 name: str = None, avatar: Optional[PortableNetworkFile] = None):
        if content is None:
            # 1. new content with ID, name & avatar
            assert identifier is not None and name is not None, \
                'name card info error: %s, %s, %s' % (identifier, name, avatar)
            msg_type = ContentType.NAME_CARD.value
            super().__init__(None, msg_type)
            self.set_string(key='ID', value=identifier)
            self['name'] = name
            if avatar is not None:
                self['avatar'] = avatar.object
        else:
            # 2. content info from network
            assert identifier is None and name is None and avatar is None, \
                'params error: %s, %s, %s, %s' % (content, identifier, name, avatar)
            super().__init__(content=content)
        # lazy load
        self.__id = identifier
        self.__avatar = avatar

    @property  # Override
    def identifier(self) -> ID:
        if self.__id is None:
            self.__id = ID.parse(identifier=self.get('ID'))
        return self.__id

    @property  # Override
    def name(self) -> str:
        return self.get_str(key='name', default='')

    @property  # Override
    def avatar(self) -> Optional[PortableNetworkFile]:
        if self.__avatar is None:
            url = self.get('avatar')
            if isinstance(url, str) and len(url) == 0:
                # ignore empty URL
                pass
            else:
                self.__avatar = PortableNetworkFile.parse(url)
        return self.__avatar
