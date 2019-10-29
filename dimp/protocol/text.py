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

from dkd import Content, ContentType


class TextContent(Content):
    """
        Text Message Content
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x01,
            sn   : 123,

            text : "..."
        }
    """

    def __new__(cls, content: dict):
        """
        Create text content

        :param content: content info
        :return: TextContent object
        """
        if content is None:
            return None
        elif cls is TextContent:
            if isinstance(content, TextContent):
                # return TextContent object directly
                return content
        # new TextContent(dict)
        return super().__new__(cls, content)

    #
    #   text
    #
    @property
    def text(self) -> str:
        return self.get('text')

    @text.setter
    def text(self, value: str):
        if value is None:
            self.pop('text', None)
        else:
            self['text'] = value

    #
    #   Factory
    #
    @classmethod
    def new(cls, content: dict=None, text: str=None):
        if content is None:
            # create empty content
            content = {}
        # set text
        if text is not None:
            content['text'] = text
        # new
        return super().new(content=content, content_type=ContentType.Text)


# register content class with type
Content.register(content_type=ContentType.Text, content_class=TextContent)
