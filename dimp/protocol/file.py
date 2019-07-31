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

import hashlib
import os
from binascii import b2a_hex, a2b_hex

from dkd import Content
from dkd.content import message_content_classes
from mkm.crypto.utils import base64_encode, base64_decode

from .types import ContentType


def hex_encode(data: bytes) -> str:
    """ HEX Encode """
    return b2a_hex(data).decode('utf-8')


def hex_decode(string: str) -> bytes:
    """ HEX Decode """
    return a2b_hex(string)


def md5(data: bytes) -> bytes:
    hash_obj = hashlib.md5()
    hash_obj.update(data)
    return hash_obj.digest()


class FileContent(Content):
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

    def __init__(self, content: dict):
        super().__init__(content)
        self.__attachment: bytes = None

    # URL
    @property
    def url(self) -> str:
        return self.get('URL')

    @url.setter
    def url(self, string: str):
        if string is None:
            self.pop('URL', None)
        else:
            self['URL'] = string

    # file data (it's too big to set in the dictionary)
    @property
    def data(self) -> bytes:
        return self.__attachment

    @data.setter
    def data(self, attachment: bytes):
        self.__attachment = attachment

    # filename
    @property
    def filename(self) -> str:
        return self.get('filename')

    @filename.setter
    def filename(self, string: str):
        if string is None:
            self.pop('filename', None)
        else:
            self['filename'] = string

    @property
    def file_ext(self) -> str:
        filename = self.filename
        if filename is not None:
            root, ext = os.path.splitext(filename)
            if ext is not None:
                return ext[1:]

    # password for decrypting the downloaded data from CDN
    @property
    def password(self) -> dict:
        return self.get('password')

    @password.setter
    def password(self, key: dict):
        if key is None:
            self.pop('password', None)
        else:
            self['password'] = key

    #
    #   Factory
    #
    @classmethod
    def new(cls, data: bytes, filename: str=None) -> Content:
        content = {
            'type': ContentType.File,
        }
        content = FileContent(content)
        content.data = data
        if filename is not None:
            content.filename = filename
        return content


class ImageContent(FileContent):
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

    def __init__(self, content: dict):
        super().__init__(content)
        self.__thumbnail: bytes = None

    # thumbnail of image data
    @property
    def thumbnail(self) -> bytes:
        if self.__thumbnail is None:
            base64 = self.get('thumbnail')
            if base64 is not None:
                self.__thumbnail = base64_decode(base64)
        return self.__thumbnail

    @thumbnail.setter
    def thumbnail(self, small_image: bytes):
        if small_image is None:
            self.pop('thumbnail', None)
        else:
            self['thumbnail'] = base64_encode(small_image)
        self.__thumbnail = small_image

    #
    #   Factory
    #
    @classmethod
    def new(cls, data: bytes, filename: str=None) -> FileContent:
        content = {
            'type': ContentType.Image,
        }
        content = ImageContent(content)
        content.data = data
        if filename is not None:
            content.filename = filename
        return content


class AudioContent(FileContent):
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

    def __init__(self, content: dict):
        super().__init__(content)

    # ASR text
    @property
    def text(self) -> bytes:
        return self.get('text')

    @text.setter
    def text(self, string: str):
        if string is None:
            self.pop('text', None)
        else:
            self['text'] = string

    #
    #   Factory
    #
    @classmethod
    def new(cls, data: bytes, filename: str=None) -> FileContent:
        content = {
            'type': ContentType.Audio,
        }
        content = ImageContent(content)
        content.data = data
        if filename is not None:
            content.filename = filename
        return content


class VideoContent(FileContent):
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

    def __init__(self, content: dict):
        super().__init__(content)
        self.__snapshot: bytes = None

    # snapshot of video
    @property
    def snapshot(self) -> bytes:
        if self.__snapshot is None:
            base64 = self.get('snapshot')
            if base64 is not None:
                self.__snapshot = base64_decode(base64)
        return self.__snapshot

    @snapshot.setter
    def snapshot(self, small_image: bytes):
        if small_image is None:
            self.pop('snapshot', None)
        else:
            self['snapshot'] = base64_encode(small_image)
        self.__snapshot = small_image

    #
    #   Factory
    #
    @classmethod
    def new(cls, data: bytes, filename: str=None) -> FileContent:
        content = {
            'type': ContentType.Video,
        }
        content = VideoContent(content)
        content.data = data
        if filename is not None:
            content.filename = filename
        return content


message_content_classes[ContentType.File] = FileContent
message_content_classes[ContentType.Image] = ImageContent
message_content_classes[ContentType.Audio] = AudioContent
message_content_classes[ContentType.Video] = VideoContent
