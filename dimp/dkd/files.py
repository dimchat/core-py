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

from typing import Optional, Any, Dict

from mkm.format import TransportableData
from mkm.types import URI
from mkm.crypto import DecryptKey

from dkd import ContentType

from ..crypto import BaseFileWrapper
from ..protocol import FileContent, ImageContent, AudioContent, VideoContent

from .contents import BaseContent


class BaseFileContent(BaseContent, FileContent):
    """ File Message Content """

    def __init__(self, content: Dict[str, Any] = None,
                 msg_type: int = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        if content is None:
            # 1. new content with type, data, filename, url & password
            if msg_type is None:
                msg_type = ContentType.FILE.value
            super().__init__(None, msg_type)
            # access via the wrapper
            wrapper = BaseFileWrapper(dictionary=self.dictionary)
            if data is not None:
                wrapper.data = data
            if filename is not None:
                wrapper.filename = filename
            if url is not None:
                wrapper.url = url
            if password is not None:
                wrapper.password = password
        else:
            # 2. content from network
            assert msg_type is None and data is None and filename is None and url is None and password is None, \
                'params error: %s, %s, %s, %s, %s, %s' % (content, msg_type, data, filename, url, password)
            super().__init__(content)
            wrapper = BaseFileWrapper(dictionary=self.dictionary)
        self.__wrapper = wrapper

    @property  # Override
    def data(self) -> Optional[bytes]:
        ted = self.__wrapper.data
        if ted is not None:
            return ted.data

    @data.setter  # Override
    def data(self, attachment: bytes):
        self.__wrapper.set_data(attachment)

    @property  # Override
    def filename(self) -> Optional[str]:
        return self.__wrapper.filename

    @filename.setter  # Override
    def filename(self, name: str):
        self.__wrapper.filename = name

    @property  # Override
    def url(self) -> Optional[URI]:
        return self.__wrapper.url

    @url.setter  # Override
    def url(self, remote: str):
        self.__wrapper.url = remote

    @property  # Override
    def password(self) -> Optional[DecryptKey]:
        return self.__wrapper.password

    @password.setter  # Override
    def password(self, key: DecryptKey):
        self.__wrapper.password = key


class ImageFileContent(BaseFileContent, ImageContent):
    """ Image Message Content """

    def __init__(self, content: Dict[str, Any] = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        msg_type = ContentType.IMAGE.value if content is None else None
        super().__init__(content, msg_type, data=data, filename=filename, url=url, password=password)

    @property  # Override
    def thumbnail(self) -> Optional[URI]:
        base64 = self.get_str(key='thumbnail', default=None)
        # TODO: convert 'data:' URI
        return base64

    @thumbnail.setter  # Override
    def thumbnail(self, base64: URI):
        self['thumbnail'] = base64


class AudioFileContent(BaseFileContent, AudioContent):
    """ Audio Message Content """

    def __init__(self, content: Dict[str, Any] = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        msg_type = ContentType.AUDIO.value if content is None else None
        super().__init__(content, msg_type, data=data, filename=filename, url=url, password=password)

    @property  # Override
    def text(self) -> Optional[str]:
        return self.get_str(key='text', default=None)

    @text.setter  # Override
    def text(self, asr: str):
        self['text'] = asr


class VideoFileContent(BaseFileContent, VideoContent):
    """ Video Message Content """

    def __init__(self, content: Dict[str, Any] = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        msg_type = ContentType.VIDEO.value if content is None else None
        super().__init__(content, msg_type, data=data, filename=filename, url=url, password=password)

    @property  # Override
    def snapshot(self) -> Optional[URI]:
        base64 = self.get_str(key='thumbnail', default=None)
        # TODO: convert 'data:' URI
        return base64

    @snapshot.setter  # Override
    def snapshot(self, base64: URI):
        self['snapshot'] = base64
