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

from mkm.format import base64_encode

from .base import EncodeAlgorithms
from .base import BaseData
from .duri import DataURI


class EmbedData(BaseData):
    """
        RFC 2397
        ~~~~~~~~
        https://www.rfc-editor.org/rfc/rfc2397

            data:[<mime type>][;charset=<charset>][;<encoding>],<encoded data>
    """

    def __init__(self, string: Optional[str], binary: Optional[bytes]):
        super().__init__(string=string, binary=binary)
        # lazy load
        self.__data_uri: Optional[DataURI] = None
        self.__mime_type: Optional[str] = None     # default is "text/plain"
        self.__parameters: Optional[Dict[str, str]] = None

    @property
    def encoding(self) -> Optional[str]:
        uri = self.data_uri
        if uri is not None and uri.is_base64:
            return EncodeAlgorithms.BASE_64
        assert uri is not None, 'data uri error'
        # plaintext
        return ''

    @property
    def binary(self) -> Optional[bytes]:
        data = self._binary
        if data is None:
            uri = self.data_uri
            if uri is not None:
                data = uri.content
                self._binary = data
        return data

    @property
    def string(self) -> str:
        txt = self._string
        if txt is None or len(txt) == 0:
            uri = self.data_uri
            if uri is not None:
                txt = uri.string
                self._string = txt
        return txt

    #
    #   URI Headers
    #

    def header_value(self, name: str) -> Optional[str]:
        extra = self.parameters
        if extra is not None:
            value = extra[name]
            if value is not None:
                # charset
                # filename
                return value
        lo = name.lower()
        if lo == 'mime-type':
            return self.mime_type
        elif lo == 'content-type':
            return self.mime_type
        # elif lo == 'encoding':
        #     return self.encoding

    @property
    def parameters(self) -> Optional[Dict[str, str]]:
        extra = self.__parameters
        if extra is not None:
            return extra
        uri = self.data_uri
        if uri is not None:
            return uri.parameters

    @property
    def mime_type(self) -> Optional[str]:
        content_type = self.__mime_type
        if content_type is not None:
            return content_type
        uri = self.data_uri
        if uri is not None:
            return uri.mime_type

    @property
    def charset(self) -> Optional[str]:
        extra = self.parameters
        if extra is not None:
            value = extra.get('charset')
            if value is not None:
                return value
        uri = self.data_uri
        if uri is not None:
            return uri.charset

    @property
    def filename(self) -> Optional[str]:
        extra = self.parameters
        if extra is not None:
            return extra.get('filename')

    #
    #  Build Data URI: "data:.../...;base64,..."
    #

    @property
    def data_uri(self) -> Optional[DataURI]:
        uri = self.__data_uri
        if uri is not None:
            return uri
        # check encoded data uri
        txt = self._string
        if txt is None or len(txt) == 0:
            # encode data to build uri
            data = self._binary
            if data is None:  # or len(data) == 0:
                return None
            assert len(data) > 0, 'embed data empty'
            # encode body
            body = base64_encode(data=data)
            # build header
            mime_type = self.__mime_type
            header = 'text/plain' if mime_type is None else mime_type
            extra = self.__parameters
            if extra is not None:
                for key in extra:
                    value = extra[key]
                    header += ';%s=%s' % (key, value)
            txt = 'data:%s;base64,%s' % (header, body)
            # self._string = txt
        # parse for data URI
        uri = DataURI.parse(uri=txt)
        self.__data_uri = uri
        return uri

    #
    #  Factories
    #

    @classmethod
    def new(cls, string: Optional[str], binary: Optional[bytes],
            uri: DataURI = None, mime_type: str = None, parameters: Dict[str, str] = None):
        if parameters is None and uri is not None:
            parameters = uri.parameters
        embed = EmbedData(string=string, binary=binary)
        embed.__data_uri = uri
        embed.__mime_type = mime_type
        embed.__parameters = parameters
        return embed

    @classmethod
    def create(cls, string: Optional[str], binary: Optional[bytes], uri: DataURI = None):
        if uri is None:
            mime_type = None
            parameters = None
        else:
            mime_type = uri.mime_type
            parameters = uri.parameters
        return cls.new(string=string, binary=binary, uri=uri, mime_type=mime_type, parameters=parameters)

    @classmethod
    def create_with_uri(cls, uri: DataURI):
        return cls.new(string=uri.string, binary=None, uri=uri, mime_type=uri.mime_type, parameters=uri.parameters)

    @classmethod
    def create_with_string(cls, string: str):
        return cls.new(string=string, binary=None)

    @classmethod
    def create_with_bytes(cls, binary: bytes, mime_type: str, filename: str = None):
        if filename is None or len(filename) == 0:
            return cls.new(string='', binary=binary, mime_type=mime_type)
        # create with 'filename'
        return cls.new(string='', binary=binary, mime_type=mime_type, parameters={
            'filename': filename,
        })

    #
    #  File Data URI:
    #
    #     "data:image/jpg;base64,{BASE64_ENCODE}"
    #     "data:audio/mp4;base64,{BASE64_ENCODE}"
    #

    @classmethod
    def image(cls, jpeg: bytes, filename: str = None):
        return cls.create_with_bytes(binary=jpeg, mime_type='image/jpeg', filename=filename)

    @classmethod
    def audio(cls, mp4: bytes, filename: str = None):
        return cls.create_with_bytes(binary=mp4, mime_type='audio/mp4', filename=filename)
