# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2023 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2023 Albert Moky
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
from mkm.types import Dictionary
from mkm.crypto import DecryptKey, SymmetricKey

from .algorithms import EncodeAlgorithms


class BaseFileWrapper(Dictionary):
    """
        File Content MixIn

            {
                data     : "...",        // base64_encode(fileContent)
                filename : "photo.png",

                URL      : "http://...", // download from CDN
                // before fileContent uploaded to a public CDN,
                // it should be encrypted by a symmetric key
                key      : {             // symmetric key to decrypt file content
                    algorithm : "AES",   // "DES", ...
                    data      : "{BASE64_ENCODE}",
                    ...
                }
            }
    """

    def __init__(self, dictionary: Dict[str, Any]):
        super().__init__(dictionary=dictionary)
        # file data (not encrypted)
        self.__attachment: Optional[TransportableData] = None
        # download from CDN
        self.__url: Optional[URI] = None
        # key to decrypt data downloaded from CDN
        self.__password: Optional[DecryptKey] = None

    #
    #   file data
    #

    @property
    def data(self) -> Optional[TransportableData]:
        ted = self.__attachment
        if ted is None:
            base64 = self.get('data')
            self.__attachment = ted = TransportableData.parse(base64)
        return ted

    @data.setter
    def data(self, ted: Optional[TransportableData]):
        if ted is None:
            self.pop('data', None)
        else:
            self['data'] = ted.object
        self.__attachment = ted

    def set_data(self, binary: Optional[bytes]):
        """ set binary data """
        if binary is None or len(binary) == 0:
            ted = None
            self.pop('data', None)
        else:
            ted = TransportableData.create(data=binary, algorithm=EncodeAlgorithms.DEFAULT)
            self['data'] = ted.object
        self.__attachment = ted

    #
    #   file name
    #

    @property
    def filename(self) -> Optional[str]:
        return self.get_str(key='filename', default=None)

    @filename.setter
    def filename(self, name: Optional[str]):
        if name is None:  # or len(name) == 0:
            self.pop('filename', None)
        else:
            self['filename'] = name

    #
    #   download URL
    #

    @property
    def url(self) -> Optional[URI]:
        if self.__url is None:
            remote = self.get_str(key='URL', default=None)
            # TODO: convert str to URI
            self.__url = remote
        return self.__url

    @url.setter
    def url(self, remote: Optional[URI]):
        if remote is None:
            self.pop('URL', None)
        else:
            # convert URI to str
            self['URL'] = remote
        self.__url = remote

    #
    #   decrypt key
    #

    @property
    def password(self) -> Optional[DecryptKey]:
        if self.__password is None:
            info = self.get('key')
            self.__password = SymmetricKey.parse(key=info)
        return self.__password

    @password.setter
    def password(self, key: Optional[DecryptKey]):
        self.set_map(key='key', value=key)
        self.__password = key
