# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2022 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
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

import time
from typing import Dict, Any, Optional, Union

from mkm.types import Dictionary, Converter
from mkm.crypto import VerifyKey, SignKey
from mkm.crypto import json_encode, json_decode, utf8_encode, base64_encode, base64_decode
from mkm import ID, Document
from mkm.factory import AccountFactoryManager


"""
    Base Documents
    ~~~~~~~~~~~~~~

    Implementations of Document/Visa/Bulletin
"""


class BaseDocument(Dictionary, Document):

    def __init__(self, document: Dict[str, Any] = None,
                 doc_type: str = None, identifier: ID = None,
                 data: Optional[str] = None, signature: Union[bytes, str, None] = None):
        # check signature
        if signature is None:
            base64 = None
        elif isinstance(signature, bytes):
            base64 = base64_encode(data=signature)
        else:
            # assert isinstance(signature, str), 'document signature error: %s' % signature
            base64 = signature
            signature = base64_decode(string=base64)
        properties = None
        status = 0
        if document is None:
            assert identifier is not None, 'doc ID should not be empty'
            if data is None or base64 is None:
                """ Create a new empty document with ID and doc type """
                document = {
                    'ID': str(identifier),
                }
                if doc_type is None or len(doc_type) == 0 or doc_type == '*':
                    properties = {
                        'created_time': time.time(),
                    }
                else:
                    properties = {
                        'type': doc_type,
                        'created_time': time.time(),
                    }
            else:
                """ Create document with ID, data and signature loaded from local storage """
                document = {
                    'ID': str(identifier),
                    'data': data,
                    'signature': base64
                }
                # all documents must be verified before saving into local storage
                status = 1
        # initialize with document info
        super().__init__(dictionary=document)
        # lazy load
        self.__identifier = identifier
        self.__data = data  # JsON.encode(properties)
        self.__signature = signature  # LocalUser(identifier).sign(data)
        self.__properties = properties
        self.__status = status  # 1 for valid, -1 for invalid

    @property  # Override
    def type(self) -> Optional[str]:
        doc_type = self.get_property(key='type')
        if doc_type is None:
            gf = AccountFactoryManager.general_factory
            doc_type = gf.get_document_type(document=self.dictionary)
        return doc_type

    @property  # Override
    def identifier(self) -> ID:
        if self.__identifier is None:
            self.__identifier = ID.parse(identifier=self.get(key='ID'))
        return self.__identifier

    @property  # private
    def data(self) -> Optional[str]:
        """
        Get serialized properties

        :return: JsON string
        """
        if self.__data is None:
            self.__data = self.get_str(key='data')
        return self.__data

    @property  # private
    def signature(self) -> Optional[bytes]:
        """
        Get signature for serialized properties

        :return: signature data
        """
        if self.__signature is None:
            base64 = self.get_str(key='signature')
            if base64 is not None:
                self.__signature = base64_decode(string=base64)
                assert self.__signature is not None, 'document signature error: %s' % base64
        return self.__signature

    @property  # Override
    def valid(self) -> bool:
        return self.__status > 0

    #
    #  signature
    #

    # Override
    def verify(self, public_key: VerifyKey) -> bool:
        """
        Verify 'data' and 'signature' with public key

        :param public_key: public key in meta.key
        :return: True on signature matched
        """
        if self.__status > 0:
            # already verify OK
            return True
        data = self.data
        signature = self.signature
        if data is None:
            # NOTICE: if data is empty, signature should be empty at the same time
            #         this happen while document not found
            if signature is None:
                self.__status = 0
            else:
                # data signature error
                self.__status = -1
        elif signature is None:
            # signature error
            self.__status = -1
        elif public_key.verify(data=utf8_encode(string=data), signature=signature):
            # signature matched
            self.__status = 1
        # NOTICE: if status is 0, it doesn't mean the document is invalid,
        #         try another key
        return self.__status == 1

    # Override
    def sign(self, private_key: SignKey) -> Optional[bytes]:
        """
        Encode properties to 'data' and sign it to 'signature'

        :param private_key: private key match meta.key
        :return: signature, None on error
        """
        if self.__status > 0:
            # already signed/verified
            assert self.__data is not None, 'document data error: %s' % self
            signature = self.signature
            assert signature is not None, 'document signature error: %s' % self
            return signature
        # 1. update sign time
        self.set_property(key='time', value=time.time())
        # 2. encode & sign
        info = self.properties
        if info is None:
            # assert False, 'should not happen'
            return None
        data = json_encode(info)
        if len(data) == 0:
            # properties error
            return None
        signature = private_key.sign(data=utf8_encode(string=data))
        if len(signature) == 0:
            # assert False, 'should not happen'
            return None
        # 3. update 'data' & 'signature' fields
        self['data'] = data  # JsON string
        self['signature'] = base64_encode(data=signature)
        self.__data = data
        self.__signature = signature
        # 4. update status
        self.__status = 1
        return signature

    #
    #  properties
    #

    @property  # Override
    def properties(self) -> Optional[Dict[str, Any]]:
        """ Load properties from data """
        if self.__status < 0:
            # invalid
            return None
        if self.__properties is None:
            data = self.data
            if data is None:
                # create new properties
                self.__properties = {}
            else:
                # get properties from data
                self.__properties = json_decode(string=data)
                assert isinstance(self.__properties, Dict), 'document data error: %s' % data
        return self.__properties

    # Override
    def get_property(self, key: str) -> Optional[Any]:
        info = self.properties
        if info is not None:
            return info.get(key)

    # Override
    def set_property(self, key: str, value: Optional[Any]):
        """ Update property with key and value """
        # 1. reset status
        assert self.__status >= 0, 'status error: %s' % self
        self.__status = 0
        # 2. update property value with name
        info = self.properties
        # assert isinstance(info, Dict), 'failed to get properties: %s' % self
        if value is None:
            info.pop(key, None)
        else:
            info[key] = value
        # 3. clear data signature after properties changed
        self.pop('data', None)
        self.pop('signature', None)
        self.__data = None
        self.__signature = None

    #
    #  properties getter/setter
    #

    @property  # Override
    def time(self) -> float:
        seconds = self.get_property(key='time')
        value = Converter.get_time(value=seconds)
        return 0.0 if value is None else value

    @property  # Override
    def name(self) -> Optional[str]:
        return self.get_property(key='name')

    @name.setter  # Override
    def name(self, value: str):
        self.set_property(key='name', value=value)
