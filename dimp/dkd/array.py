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

from typing import Optional, Any, Dict, List

from dkd import ContentType, Content, BaseContent

from ..protocol import ArrayContent


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
            self['contents'] = revert_contents(contents=contents)

    @property  # Override
    def contents(self) -> Optional[List[Content]]:
        if self.__contents is None:
            array = self.get('contents')
            if array is not None:
                self.__contents = convert_contents(contents=array)
        return self.__contents


def convert_contents(contents: List[Dict[str, Any]]) -> List[Content]:
    array = []
    for item in contents:
        msg = Content.parse(content=item)
        if msg is None:
            continue
        array.append(msg)
    return array


def revert_contents(contents: List[Content]) -> List[Dict[str, Any]]:
    array = []
    for msg in contents:
        info = msg.dictionary
        array.append(info)
    return array
