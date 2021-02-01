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

from typing import Optional, Union

from mkm.crypto import base64_encode, base64_decode, hex_encode, md5
from mkm.crypto import SymmetricKey

from dkd import ContentType, BaseContent


def data_filename(data: bytes, ext: str = None) -> str:
    filename = hex_encode(md5(data))
    if ext is None or len(ext) == 0:
        return filename
    return filename + '.' + ext


class FileContent(BaseContent):
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

    def __init__(self, content: Optional[dict] = None, content_type: Union[ContentType, int] = 0,
                 filename: Optional[str] = None, data: Optional[bytes] = None):
        if content is None:
            if content_type == 0:
                content_type = ContentType.FILE
            super().__init__(content_type=content_type)
        else:
            super().__init__(content=content)
        self.__attachment = data  # attachment (file data)
        self.__password = None    # symmetric key for decryption
        # set values to inner dictionary
        if filename is not None:
            self['filename'] = filename
        if data is not None:
            self['data'] = base64_encode(data=data)

    # URL
    @property
    def url(self) -> Optional[str]:
        return self.get('URL')

    @url.setter
    def url(self, string: str):
        if string is None:
            self.pop('URL', None)
        else:
            self['URL'] = string

    # file data (it's too big to set in the dictionary)
    @property
    def data(self) -> Optional[bytes]:
        if self.__attachment is None:
            base64 = self.get('data')
            if base64 is not None:
                self.__attachment = base64_decode(base64)
        return self.__attachment

    @data.setter
    def data(self, attachment: bytes):
        self.__attachment = attachment
        if attachment is None:
            self.pop('data', None)
        else:
            self['data'] = base64_encode(attachment)

    # filename
    @property
    def filename(self) -> Optional[str]:
        return self.get('filename')

    @filename.setter
    def filename(self, string: str):
        if string is None:
            self.pop('filename', None)
        else:
            self['filename'] = string

    # password for decrypting the downloaded data from CDN
    @property
    def password(self) -> Optional[SymmetricKey]:
        if self.__password is None:
            self.__password = SymmetricKey.parse(key=self.get('password'))
        return self.__password

    @password.setter
    def password(self, key: SymmetricKey):
        self.__password = key
        if key is None:
            self.pop('password', None)
        else:
            self['password'] = key.dictionary


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

    def __init__(self, content: Optional[dict] = None, filename: Optional[str] = None, data: Optional[bytes] = None,
                 thumbnail: Optional[bytes] = None):
        super().__init__(content, ContentType.IMAGE, filename=filename, data=data)
        self.__thumbnail = thumbnail
        if thumbnail is not None:
            self['thumbnail'] = base64_encode(data=thumbnail)

    # thumbnail of image
    @property
    def thumbnail(self) -> Optional[bytes]:
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

    def __init__(self, content: Optional[dict] = None, filename: Optional[str] = None, data: Optional[bytes] = None,
                 text: Optional[str] = None):
        super().__init__(content, ContentType.AUDIO, filename=filename, data=data)
        if text is not None:
            self['text'] = text

    # ASR text
    @property
    def text(self) -> Optional[bytes]:
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

    def __init__(self, content: Optional[dict] = None, filename: Optional[str] = None, data: Optional[bytes] = None,
                 snapshot: Optional[bytes] = None):
        super().__init__(content, ContentType.VIDEO, filename=filename, data=data)
        self.__snapshot = snapshot
        if snapshot is not None:
            self['snapshot'] = base64_encode(data=snapshot)

    # snapshot of video
    @property
    def snapshot(self) -> Optional[bytes]:
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
