# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2026 Albert Moky
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

from typing import Optional, Dict

from mkm.format import base64_decode, utf8_encode


"""
    RFC 2397
    ~~~~~~~~
    https://www.rfc-editor.org/rfc/rfc2397

        data:[<mime type>][;charset=<charset>][;<encoding>],<encoded data>
"""


class Header:

    def __init__(self, mime_type: str, encoding: str = None, extra: Dict[str, str] = None):
        super().__init__()
        self.__mime_type = mime_type
        self.__encoding = encoding
        self.__extra = extra
        #  lazy load
        self.__head_string = None

    @property
    def mime_type(self) -> str:
        """ default is "text/plain" """
        return self.__mime_type

    @property
    def encoding(self) -> Optional[str]:
        """ default is "base64" """
        return self.__encoding

    @property
    def extra(self) -> Optional[Dict[str, str]]:
        """ extra parameters """
        return self.__extra

    @property
    def charset(self) -> Optional[str]:
        return self.extra_value(name='charset')

    def extra_value(self, name: str) -> Optional[str]:
        # charset: default is "us-ascii"
        # filename: "avatar.png"
        extra = self.__extra
        if extra is None:
            return None
        elif name is None or len(name) == 0:
            # assert False, 'header name should not be empty'
            return None
        else:
            name = name.lower()
        # get value by name in lowercase
        return extra[name]

    # Override
    def __str__(self) -> str:
        return self.to_str()

    # Override
    def __repr__(self) -> str:
        return self.to_str()

    def to_str(self) -> str:
        text = self.__head_string
        if text is None:
            items = []
            mime_type = self.__mime_type
            encoding = self.__encoding
            extra = self.__extra
            #
            #  1. 'mime-type'
            #
            if len(mime_type) > 0:
                items.append(mime_type)
            elif encoding is not None and len(encoding) > 0:
                # make sure 'mime-type' is the first header
                items.append('text/plain')
            elif extra is not None and len(extra) > 0:
                # make sure 'mime-type' is the first header
                items.append('text/plain')
            #
            #  2. extra info: 'charset' & 'filename'
            #
            if extra is not None:
                for key in extra:
                    value = extra[key]
                    pair = '%s=%s' % (key, value)
                    items.append(pair)
            #
            #  3. 'encoding'
            #
            if encoding is not None and len(encoding) > 0:
                items.append(encoding)
            # build header
            if len(items) > 0:
                text = ';'.join(items)
            else:
                text = ''
            self.__head_string = text
        return text

    # samples:
    #     "data:,A%20simple%20text"
    #     "data:text/html,<p>Hello, World!</p>"
    #     "data:text/plain;charset=iso-8859-7,%be%fg%be"
    #     "data:image/png;base64,{BASE64_ENCODE}"
    #     "data:text/plain;charset=utf-8;base64,SGVsbG8sIHdvcmxkIQ=="

    @classmethod
    def split_header(cls, uri: str, end: int):
        if end < 6:
            # header empty
            return Header(mime_type='')
        assert end < len(uri) - 1, 'data URI error: %s' % uri
        array = uri[5:end].split(';')
        # split main info
        mime_type: str = None
        encoding: str = None
        # split extra info
        extra: Dict[str, str] = None
        for item in array:
            if len(item) == 0:
                # assert False, 'header error: %s' % uri
                continue
            #
            #  2. extra info: 'charset' or 'filename'
            #
            pos = item.find('=')
            if pos >= 0:
                assert 0 < pos < len(item) - 1, 'header error: %s' % item
                if extra is None:
                    extra = {}
                name = item[:pos].lower()
                value = item[pos+1:]
                extra[name] = value
                continue
            #
            #  1. 'mime-type'
            #
            pos = item.find('/')
            if pos >= 0:
                assert 0 < pos < len(item) - 1, 'header error: %s' % item
                assert mime_type is None, 'duplicate mime-type: %s' % uri
                mime_type = item
                continue
            #
            #  3. 'encoding'
            #
            assert encoding is None, 'duplicate encoding: %s' % uri
            encoding = item
        # OK
        if mime_type is None:
            mime_type = ''
        return Header(mime_type=mime_type, encoding=encoding, extra=extra)


class DataURI:

    def __init__(self, head: Header, body: str):
        super().__init__()
        self.__head = head
        self.__body = body
        # lazy load
        self.__uri_string = None

    @property
    def head(self) -> Header:
        """ data head """
        return self.__head

    @property
    def body(self) -> str:
        """ data body """
        return self.__body

    @property
    def parameters(self) -> Optional[Dict[str, str]]:
        """ extra parameters """
        return self.head.extra

    @property
    def content(self) -> bytes:
        """ body content in bytes """
        if self.is_base64:
            return base64_decode(string=self.body)
        else:
            return utf8_encode(string=self.body)

    @property
    def is_empty(self) -> bool:
        return len(self.body) == 0

    @property
    def mime_type(self) -> str:
        return self.head.mime_type

    @property
    def charset(self) -> str:
        return self.head.charset

    @property
    def is_base64(self) -> bool:
        return self.head.encoding == 'base64'

    def header_value(self, name: str) -> Optional[str]:
        head = self.head
        value = head.extra_value(name=name)
        if value is not None:
            # charset
            # filename
            return value
        lo = name.lower()
        if lo == 'encoding':
            return head.encoding
        elif lo == 'mime-type':
            return head.mime_type
        elif lo == 'content-type':
            return head.mime_type

    # Override
    def __str__(self) -> str:
        return self.to_str()

    # Override
    def __repr__(self) -> str:
        return self.to_str()

    def to_str(self) -> str:
        text = self.__uri_string
        if text is None:
            header = self.head.to_str()
            if len(header) == 0:
                text = 'data:,%s' % self.body
            else:
                text = 'data:%s,%s' % (header, self.body)
            self.__uri_string = text
        return text

    #
    #   Factory
    #

    @classmethod
    def parse(cls, uri: str):
        """ Split text string for data URI """
        if uri is None or len(uri) == 0:
            return None
        elif not uri.startswith('data:'):
            return None
        pos = uri.find(',')
        if pos < 0:
            # assert False, 'data URI error: %s' % uri
            return None
        head = Header.split_header(uri=uri, end=pos)
        body = uri[pos+1:]
        return DataURI(head=head, body=body)
