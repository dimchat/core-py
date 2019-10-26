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
from binascii import b2a_hex
from typing import Union

from mkm.crypto.utils import base64_encode, base64_decode

from dkd import Content, ContentType
from dkd.content import message_content_classes


def hex_encode(data: bytes) -> str:
    """ HEX Encode """
    return b2a_hex(data).decode('utf-8')


def md5(data: bytes) -> bytes:
    """ MD5 digest """
    hash_obj = hashlib.md5()
    hash_obj.update(data)
    return hash_obj.digest()


def data_filename(data: bytes, ext: str=None) -> str:
    filename = hex_encode(md5(data))
    if ext is None or len(ext) == 0:
        return filename
    return filename + '.' + ext


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

    def __new__(cls, content: dict):
        """
        Create file content

        :param content: content info
        :return: FileContent object
        """
        if content is None:
            return None
        elif cls is FileContent:
            if isinstance(content, FileContent):
                # return FileContent object directly
                return content
        # subclass or default FileContent(dict)
        return super().__new__(cls, content)

    def __init__(self, content: dict):
        super().__init__(content)
        # attachment (file data)
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
        if self.__attachment is None:
            base64 = self.get('data')
            if base64 is not None:
                self.__attachment = base64_decode(base64)
        return self.__attachment

    @data.setter
    def data(self, attachment: bytes):
        self.__attachment = attachment
        if attachment is None or len(attachment) == 0:
            self.pop('data', None)
        else:
            self['data'] = base64_encode(attachment)
            # reset filename
            self['filename'] = data_filename(attachment, self.file_ext)

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
    #   Factories
    #
    @classmethod
    def new(cls, data: Union[bytes, dict]):
        if isinstance(data, bytes):
            content = {
                'type': ContentType.File,
                'data': data,
            }
        elif isinstance(data, dict):
            content = data
            if 'type' not in content:
                content['type'] = ContentType.File
        else:
            raise TypeError('file content error: %s' % data)
        # create FileContent
        return cls(content)

    @classmethod
    def image(cls, data: bytes, thumbnail: bytes=None, filename: str=None):
        """
        Create image message content

        :param data:      Image data
        :param thumbnail: Image thumbnail
        :param filename:  Image filename
        :return: ImageContent object
        """
        content = {
            'type': ContentType.Image,
            'data': data,
        }
        if thumbnail is not None:
            content['thumbnail'] = base64_encode(thumbnail)
        if filename is not None:
            content['filename'] = filename
        return cls.new(content)

    @classmethod
    def video(cls, data: bytes, snapshot: bytes=None, filename: str=None):
        """
        Create video message content

        :param data:     Video data
        :param snapshot: Video snapshot
        :param filename: Video filename
        :return: VideoContent object
        """
        content = {
            'type': ContentType.Video,
            'data': data,
        }
        if snapshot is not None:
            content['snapshot'] = base64_encode(snapshot)
        if filename is not None:
            content['filename'] = filename
        return cls.new(content)

    @classmethod
    def audio(cls, data: bytes, text: str=None, filename: str=None):
        """
        Create audio message content

        :param data:     Audio data
        :param text:     Automatic Speech Recognition
        :param filename: Audio filename
        :return: AudioContent
        """
        content = {
            'type': ContentType.Audio,
            'data': data,
        }
        if text is not None:
            content['text'] = text
        if filename is not None:
            content['filename'] = filename
        return cls.new(content)


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

    def __new__(cls, content: dict):
        """
        Create image content

        :param content: content info
        :return: ImageContent object
        """
        if content is None:
            return None
        elif cls is ImageContent:
            if isinstance(content, ImageContent):
                # return ImageContent object directly
                return content
        # new ImageContent(dict)
        return super().__new__(cls, content)

    def __init__(self, content: dict):
        super().__init__(content)
        # thumbnail (lazy)
        self.__thumbnail: bytes = None

    # thumbnail of image
    @property
    def thumbnail(self) -> bytes:
        if self.__thumbnail is None:
            base64 = self.get('thumbnail')
            if base64 is not None:
                self.__thumbnail = base64_decode(base64)
        return self.__thumbnail

    @thumbnail.setter
    def thumbnail(self, small_image: bytes):
        self.__thumbnail = small_image
        if small_image is None:
            self.pop('thumbnail', None)
        else:
            self['thumbnail'] = base64_encode(small_image)


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

    def __new__(cls, content: dict):
        """
        Create audio content

        :param content: content info
        :return: AudioContent object
        """
        if content is None:
            return None
        elif cls is AudioContent:
            if isinstance(content, AudioContent):
                # return AudioContent object directly
                return content
        # new AudioContent(dict)
        return super().__new__(cls, content)

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

    def __new__(cls, content: dict):
        """
        Create video content

        :param content: content info
        :return: VideoContent object
        """
        if content is None:
            return None
        elif cls is VideoContent:
            if isinstance(content, VideoContent):
                # return VideoContent object directly
                return content
        # new VideoContent(dict)
        return super().__new__(cls, content)

    def __init__(self, content: dict):
        super().__init__(content)
        # snapshot (lazy)
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
        self.__snapshot = small_image
        if small_image is None:
            self.pop('snapshot', None)
        else:
            self['snapshot'] = base64_encode(small_image)


# register content classes
message_content_classes[ContentType.File] = FileContent
message_content_classes[ContentType.Image] = ImageContent
message_content_classes[ContentType.Audio] = AudioContent
message_content_classes[ContentType.Video] = VideoContent
