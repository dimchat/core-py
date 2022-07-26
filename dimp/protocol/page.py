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

from abc import ABC
from typing import Optional

from dkd import Content


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
    def url(self) -> str:
        """ Web Page URL """
        raise NotImplemented

    @url.setter
    def url(self, string: str):
        raise NotImplemented

    @property
    def title(self) -> Optional[str]:
        """ Document Title """
        raise NotImplemented

    @title.setter
    def title(self, string: str):
        raise NotImplemented

    @property
    def desc(self) -> Optional[str]:
        """ Description """
        raise NotImplemented

    @desc.setter
    def desc(self, string: str):
        raise NotImplemented

    @property
    def icon(self) -> Optional[bytes]:
        """ Image data """
        raise NotImplemented

    @icon.setter
    def icon(self, image: bytes):
        raise NotImplemented
