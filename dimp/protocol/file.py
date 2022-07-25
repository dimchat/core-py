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

from abc import ABC
from typing import Optional, Union

from mkm.crypto import SymmetricKey

from dkd import Content


class FileContent(Content, ABC):
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

    @property
    def url(self) -> Optional[str]:
        raise NotImplemented

    @url.setter
    def url(self, string: str):
        raise NotImplemented

    @property
    def data(self) -> Optional[bytes]:
        # file data (it's too big to set in the dictionary)
        raise NotImplemented

    @data.setter
    def data(self, attachment: bytes):
        raise NotImplemented

    @property
    def filename(self) -> Optional[str]:
        raise NotImplemented

    @filename.setter
    def filename(self, string: str):
        raise NotImplemented

    @property
    def password(self) -> Optional[SymmetricKey]:
        # password for decrypting the downloaded data from CDN
        raise NotImplemented

    @password.setter
    def password(self, key: SymmetricKey):
        raise NotImplemented

    #
    #  Factories
    #
    @classmethod
    def file(cls, filename: str, data: Union[bytes, str, None]):
        from ..dkd import BaseFileContent
        return BaseFileContent(filename=filename, data=data)

    @classmethod
    def image(cls, filename: str, data: Union[bytes, str, None]):
        from ..dkd import ImageFileContent
        return ImageFileContent(filename=filename, data=data)

    @classmethod
    def audio(cls, filename: str, data: Union[bytes, str, None]):
        from ..dkd import AudioFileContent
        return AudioFileContent(filename=filename, data=data)

    @classmethod
    def video(cls, filename: str, data: Union[bytes, str, None]):
        from ..dkd import VideoFileContent
        return VideoFileContent(filename=filename, data=data)


class ImageContent(FileContent, ABC):
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

    @property
    def thumbnail(self) -> Optional[bytes]:
        # thumbnail of image
        raise NotImplemented

    @thumbnail.setter
    def thumbnail(self, small_image: bytes):
        raise NotImplemented


class AudioContent(FileContent, ABC):
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

    @property
    def text(self) -> Optional[bytes]:
        # Automatic Speech Recognition
        raise NotImplemented

    @text.setter
    def text(self, string: str):
        raise NotImplemented


class VideoContent(FileContent, ABC):
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

    @property
    def snapshot(self) -> Optional[bytes]:
        # snapshot of video
        raise NotImplemented

    @snapshot.setter
    def snapshot(self, small_image: bytes):
        raise NotImplemented
