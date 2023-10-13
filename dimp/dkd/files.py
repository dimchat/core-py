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
    """
        File Message Content
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x10,
            sn   : 123,

            URL      : "http://", // upload to CDN
            data     : "...",     // if (!URL) base64_encode(fileContent)
            filename : "..."
        }
    """

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
    """
        Image Message Content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x12,
            sn   : 123,

            URL       : "http://", // upload to CDN
            data      : "...",     // if (!URL) base64_encode(image)
            thumbnail : "...",     // base64_encode(smallImage)
            filename  : "..."
        }
    """

    def __init__(self, content: Dict[str, Any] = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        msg_type = ContentType.IMAGE.value if content is None else None
        super().__init__(content, msg_type, data=data, filename=filename, url=url, password=password)
        # lazy load
        self.__thumbnail: Optional[TransportableData] = None

    @property  # Override
    def thumbnail(self) -> Optional[bytes]:
        ted = self.__thumbnail
        if ted is None:
            base64 = self.get('thumbnail')
            self.__thumbnail = ted = TransportableData.parse(base64)
        if ted is not None:
            return ted.data

    @thumbnail.setter  # Override
    def thumbnail(self, image: bytes):
        if image is None:  # or len(image) == 0:
            self.pop('thumbnail', None)
            ted = None
        else:
            ted = TransportableData.create(data=image)
            self['thumbnail'] = ted.object
        self.__thumbnail = ted


class AudioFileContent(BaseFileContent, AudioContent):
    """
        Audio Message Content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x14,
            sn   : 123,

            URL      : "http://", // upload to CDN
            data     : "...",     // if (!URL) base64_encode(audio)
            text     : "...",     // Automatic Speech Recognition
            filename : "..."
        }
    """

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
    """
        Video Message Content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x16,
            sn   : 123,

            URL      : "http://", // upload to CDN
            data     : "...",     // if (!URL) base64_encode(video)
            snapshot : "...",     // base64_encode(smallImage)
            filename : "..."
        }
    """

    def __init__(self, content: Dict[str, Any] = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        msg_type = ContentType.VIDEO.value if content is None else None
        super().__init__(content, msg_type, data=data, filename=filename, url=url, password=password)
        # lazy load
        self.__snapshot: Optional[TransportableData] = None

    @property  # Override
    def snapshot(self) -> Optional[bytes]:
        ted = self.__snapshot
        if ted is None:
            base64 = self.get('snapshot')
            self.__snapshot = ted = TransportableData.parse(base64)
        if ted is not None:
            return ted.data

    @snapshot.setter  # Override
    def snapshot(self, image: bytes):
        if image is None:  # or len(image) == 0:
            self.pop('snapshot', None)
            ted = None
        else:
            ted = TransportableData.create(data=image)
            self['snapshot'] = ted.object
        self.__snapshot = ted
