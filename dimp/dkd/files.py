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

from mkm.types import URI
from mkm.format import TransportableData
from mkm.format import PortableNetworkFile
from mkm.crypto import DecryptKey

from ..crypto import BaseFileWrapper
from ..protocol import ContentType
from ..protocol import FileContent, ImageContent, AudioContent, VideoContent

from .contents import BaseContent


class BaseFileContent(BaseContent, FileContent):
    """ File Message Content """

    def __init__(self, content: Dict[str, Any] = None,
                 msg_type: str = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        if content is None:
            # 1. new content with type, data, filename, url & password
            if msg_type is None:
                msg_type = ContentType.FILE
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
        msg_type = ContentType.IMAGE if content is None else None
        super().__init__(content, msg_type, data=data, filename=filename, url=url, password=password)
        # small image
        self.__thumbnail: Optional[PortableNetworkFile] = None

    @property  # Override
    def thumbnail(self) -> Optional[PortableNetworkFile]:
        img = self.__thumbnail
        if img is None:
            base64 = self.get_str(key='thumbnail', default=None)
            img = self.__thumbnail = PortableNetworkFile.parse(base64)
        return img

    @thumbnail.setter  # Override
    def thumbnail(self, img: PortableNetworkFile):
        if img is None:
            self.pop('thumbnail', None)
        else:
            self['thumbnail'] = img.object
        self.__thumbnail = img


class AudioFileContent(BaseFileContent, AudioContent):
    """ Audio Message Content """

    def __init__(self, content: Dict[str, Any] = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        msg_type = ContentType.AUDIO if content is None else None
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
        msg_type = ContentType.VIDEO if content is None else None
        super().__init__(content, msg_type, data=data, filename=filename, url=url, password=password)
        # small image
        self.__snapshot: Optional[PortableNetworkFile] = None

    @property  # Override
    def snapshot(self) -> Optional[PortableNetworkFile]:
        img = self.__snapshot
        if img is None:
            base64 = self.get_str(key='snapshot', default=None)
            img = self.__snapshot = PortableNetworkFile.parse(base64)
        return img

    @snapshot.setter  # Override
    def snapshot(self, img: PortableNetworkFile):
        if img is None:
            self.pop('snapshot', None)
        else:
            self['snapshot'] = img.object
        self.__snapshot = img
