# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2020 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2020 Albert Moky
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
from typing import List

from dkd import Content, InstantMessage, SecureMessage, ReliableMessage


#
#   Message Processor
#
class Processor(ABC):

    @abstractmethod
    def process_package(self, data: bytes) -> List[bytes]:
        """
        Process data package

        :param data: data to be processed
        :return: responses
        """
        raise NotImplemented

    @abstractmethod
    def process_reliable_message(self, msg: ReliableMessage) -> List[ReliableMessage]:
        """
        Process network message

        :param msg: message to be processed
        :return: response messages
        """
        raise NotImplemented

    @abstractmethod
    def process_secure_message(self, msg: SecureMessage, r_msg: ReliableMessage) -> List[SecureMessage]:
        """
        Process encrypted message

        :param msg:   message to be processed
        :param r_msg: message received
        :return: response messages
        """
        raise NotImplemented

    @abstractmethod
    def process_instant_message(self, msg: InstantMessage, r_msg: ReliableMessage) -> List[InstantMessage]:
        """
        Process plain message

        :param msg:   message to be processed
        :param r_msg: message received
        :return: response messages
        """
        raise NotImplemented

    @abstractmethod
    def process_content(self, content: Content, r_msg: ReliableMessage) -> List[Content]:
        """
        Process message content

        :param content: content to be processed
        :param r_msg: message received
        :return: response contents
        """
        raise NotImplemented
