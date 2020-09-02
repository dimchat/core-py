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

from typing import Union
import time as time_lib
import random

from dkd import ContentType
from dkd import Content as DKDContent


def random_positive_integer():
    """
    :return: random integer greater than 0
    """
    return random.randint(1, 2**32-1)


class Content(DKDContent):
    """This class is for creating message content

        Message Content
        ~~~~~~~~~~~~~~~

        data format: {
            'type'    : 0x00,            // message type
            'sn'      : 0,               // serial number

            'group'   : 'Group ID',      // for group message

            //-- message info
            'text'    : 'text',          // for text message
            'command' : 'Command Name',  // for system command
            //...
        }
    """

    # noinspection PyTypeChecker
    def __new__(cls, content: dict):
        """
        Create message content

        :param content: content info
        :return: Content object
        """
        if content is None:
            return None
        elif cls is Content:
            if isinstance(content, Content):
                # return Content object directly
                return content
            # get subclass by message content type
            c_type = int(content['type'])
            clazz = cls.__content_classes.get(c_type)
            if clazz is not None:
                return clazz.__new__(clazz, content)
        # subclass or default Content(dict)
        return super().__new__(cls, content)

    #
    #   Factory
    #
    @classmethod
    def new(cls, content: dict=None, content_type: Union[ContentType, int, None]=0, time: int=0):
        """
        Create message content with 'type' & 'sn' (serial number)

        :param content:      content info, if empty then create a new one with 'type'
        :param content_type: content type, if not empty then set into content
        :param time:         message time
        :return: Content object
        """
        if content is None:
            # create content with 'sn'
            content = {
                'sn': random_positive_integer(),
            }
        elif 'sn' not in content:
            # generate 'sn'
            content['sn'] = random_positive_integer()
        # set content type
        if isinstance(content_type, ContentType):
            content['type'] = content_type.value
        elif content_type > 0:
            content['type'] = content_type
        # set message time
        if time > 0:
            content['time'] = time
        elif 'time' not in content:
            content['time'] = int(time_lib.time())
        # new Content(dict)
        return cls(content)

    #
    #   Runtime
    #
    __content_classes = {}  # class map

    @classmethod
    def register(cls, content_type: Union[ContentType, int], content_class=None) -> bool:
        """
        Register content class with type

        :param content_type:  message content type
        :param content_class: if content class is None, then remove with type
        :return: False on error
        """
        if isinstance(content_type, ContentType):
            content_type = content_type.value
        if content_class is None:
            cls.__content_classes.pop(content_type, None)
        elif issubclass(content_class, Content):
            cls.__content_classes[content_type] = content_class
        else:
            raise TypeError('%s must be subclass of Content' % content_class)
        return True
