# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2022 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
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

from typing import Optional, Union, Any, Dict

from mkm.crypto import base64_encode, base64_decode
from dkd import ContentType, BaseContent

from ..protocol import PageContent


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
        return self.get('URL')

    @url.setter  # Override
    def url(self, string: str):
        self['URL'] = string

    @property  # Override
    def title(self) -> Optional[str]:
        return self.get('title')

    @title.setter  # Override
    def title(self, string: Optional[str]):
        if string is None:
            self.pop('title', None)
        else:
            self['title'] = string

    @property  # Override
    def desc(self) -> Optional[str]:
        return self.get('desc')

    @desc.setter  # Override
    def desc(self, string: Optional[str]):
        if string is None:
            self.pop('desc', None)
        else:
            self['desc'] = string

    @property  # Override
    def icon(self) -> Optional[bytes]:
        if self.__icon is None:
            base64 = self.get('icon')
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
