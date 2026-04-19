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
from typing import List, Dict

from dkd.protocol import Content
from dkd.protocol import InstantMessage, ReliableMessage

from .types import ContentType
from .base import BaseContent


class ForwardContent(Content, ABC):
    """
        Top-Secret Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            "type" : i2s(0xFF),
            "sn"   : 67890,

            "forward" : {...}  // reliable (secure + certified) message
            "secrets" : [...]  // reliable (secure + certified) messages
        }
    """

    @property
    @abstractmethod
    def secrets(self) -> List[ReliableMessage]:
        raise NotImplemented

    #
    #   Factory methods
    #
    @classmethod
    def create(cls, messages: List[ReliableMessage]):
        return SecretContent(messages=messages)


class CombineContent(Content, ABC):
    """
        Combine Forward message
        ~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            "type" : i2s(0xCF),
            "sn"   : 67890,

            "title"    : "...",  // chat title
            "messages" : [...]   // chat history
        }
    """

    @property
    @abstractmethod
    def title(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def messages(self) -> List[InstantMessage]:
        raise NotImplemented

    #
    #   Factory methods
    #
    @classmethod
    def create(cls, title: str, messages: List[InstantMessage]):
        return CombineForwardContent(title=title, messages=messages)


class ArrayContent(Content, ABC):
    """
        Content Array message
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            "type" : i2s(0xCA),
            "sn"   : 12345,

            "contents" : [...]  // content array
        }
    """

    @property
    @abstractmethod
    def contents(self) -> List[Content]:
        raise NotImplemented

    #
    #   Factory
    #
    @classmethod
    def create(cls, contents: List[Content]):
        return ListContent(contents=contents)


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class SecretContent(BaseContent, ForwardContent):

    def __init__(self, content: Dict = None,
                 messages: List[ReliableMessage] = None):
        if content is None:
            # 1. new content with message(s)
            msg_type = ContentType.FORWARD
            super().__init__(None, msg_type)
            # if messages is not None:
            #     self['secrets'] = ReliableMessage.revert(messages=messages)
        else:
            # 2. content info from network
            assert messages is None, 'params error: %s, %s' % (content, messages)
            super().__init__(content)
        # lazy
        self.__secrets = messages

    # Override
    def to_dict(self) -> Dict:
        # serialize secret messages
        messages = self.__secrets
        if messages is not None and self.get('secrets') is None:
            self['secrets'] = ReliableMessage.revert(messages=messages)
        # OK
        return super().to_dict()

    @property  # Override
    def secrets(self) -> List[ReliableMessage]:
        messages = self.__secrets
        if messages is None:
            info = self.get('secrets')
            if isinstance(info, List):
                # get from 'secrets'
                messages = ReliableMessage.convert(array=info)
            else:
                assert info is None, 'secret messages error: %s' % info
                # get from 'forward'
                forward = self.get('forward')
                msg = ReliableMessage.parse(msg=forward)
                if msg is None:
                    messages = []
                else:
                    messages = [msg]
            self.__secrets = messages
        return messages


class CombineForwardContent(BaseContent, CombineContent):

    def __init__(self, content: Dict = None,
                 title: str = None, messages: List[InstantMessage] = None):
        if content is None:
            # 1. new content with message(s)
            assert not (title is None or messages is None), 'params error: %s, %s' % (title, messages)
            msg_type = ContentType.COMBINE_FORWARD
            super().__init__(None, msg_type)
            self['title'] = title
            self['messages'] = InstantMessage.revert(messages=messages)
        else:
            # 2. content info from network
            assert title is None and messages is None, 'params error: %s, %s' % (title, messages)
            super().__init__(content)
        # lazy
        self.__history = messages

    @property  # Override
    def title(self) -> str:
        return self.get_str(key='title', default='')

    @property  # Override
    def messages(self) -> List[InstantMessage]:
        array = self.__history
        if array is None:
            info = self.get('messages')
            if isinstance(info, List):
                array = InstantMessage.convert(array=info)
            else:
                assert info is None, 'combined messages error: %s' % info
                array = []
            self.__history = array
        return array


class ListContent(BaseContent, ArrayContent):

    def __init__(self, content: Dict = None,
                 contents: List[Content] = None):
        if content is None:
            # 1. new content with a list
            assert contents is not None, 'content list should no be None'
            msg_type = ContentType.ARRAY
            super().__init__(None, msg_type)
            self['contents'] = Content.revert(contents=contents)
        else:
            # 2. content info from network
            assert contents is None, 'params error: %s, %s' % (content, contents)
            super().__init__(content)
        # lazy
        self.__list = contents

    @property  # Override
    def contents(self) -> List[Content]:
        array = self.__list
        if array is None:
            info = self.get('contents')
            if isinstance(info, List):
                array = Content.convert(array=info)
            else:
                array = []
            self.__list = array
        return array
