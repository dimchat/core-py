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

from typing import Dict, Any, Optional

from mkm.types import DateTime
from mkm.types import Dictionary, Converter
from mkm.crypto import VerifyKey, SignKey
from mkm.format import TransportableData
from mkm.format import json_encode, json_decode, utf8_encode
from mkm import ID, Document

from ..crypto import EncodeAlgorithms


"""
    Base Documents
    ~~~~~~~~~~~~~~

    Implementations of Document/Visa/Bulletin
"""


class BaseDocument(Dictionary, Document):

    def __init__(self, document: Dict[str, Any] = None,
                 doc_type: str = None, identifier: ID = None,
                 data: Optional[str] = None, signature: Optional[TransportableData] = None):
        # check parameters
        if document is not None:
            # 0. document info from network
            assert doc_type is None and identifier is None and data is None and signature is None, \
                'params error: %s, %s, %s, %s, %s' % (document, doc_type, identifier, data, signature)
            properties = None  # lazy
            # waiting to verify
            # all documents must be verified before saving into local storage
            status = 0
        elif data is None or signature is None:
            # 1. new empty document
            assert doc_type is not None and doc_type != '*' and identifier is not None, \
                'document info error: %s, %s, %s, %s' % (doc_type, identifier, data, signature)
            assert data is None and signature is None, \
                'document info error: %s, %s, %s, %s' % (doc_type, identifier, data, signature)
            document = {
                'did': str(identifier),
                'type': doc_type,
            }
            # new properties with created time
            properties = {
                'type': doc_type,  # deprecated
                'created_time': DateTime.current_timestamp(),
            }
            # waiting to sign
            status = 0
        else:
            # 2. document with data and signature loaded from local storage
            assert doc_type is not None and doc_type != '*' and identifier is not None, \
                'document info error: %s, %s, %s, %s' % (doc_type, identifier, data, signature)
            document = {
                'did': str(identifier),
                'type': doc_type,
                'data': data,
                'signature': signature.object,
            }
            properties = None  # lazy
            # document loaded from local storage,
            # no need to verify again.
            status = 1
        # initialize with document info
        super().__init__(dictionary=document)
        # lazy load
        self.__identifier = identifier
        self.__json = data      # JsON.encode(properties)
        self.__sig = signature  # LocalUser(identifier).sign(data)
        self.__properties = properties
        self.__status = status  # 1 for valid, -1 for invalid

    # @property  # Override
    # def type(self) -> Optional[str]:
    #     doc_type = self.get_property(name='type')  # deprecated
    #     if doc_type is None:
    #         ext = SharedAccountExtensions()
    #         doc_type = ext.helper.get_document_type(document=self.dictionary, default=None)
    #         # doc_type = self.get_str(key='type', default=None)
    #     return doc_type

    @property  # Override
    def identifier(self) -> ID:
        if self.__identifier is None:
            self.__identifier = ID.parse(identifier=self.get('did'))
        return self.__identifier

    @property  # private
    def data(self) -> Optional[str]:
        """
        Get serialized properties

        :return: JsON string
        """
        if self.__json is None:
            self.__json = self.get_str(key='data', default=None)
        return self.__json

    @property  # private
    def signature(self) -> Optional[bytes]:
        """
        Get signature for serialized properties

        :return: signature data
        """
        ted = self.__sig
        if ted is None:
            base64 = self.get('signature')
            self.__sig = ted = TransportableData.parse(base64)
        if ted is not None:
            return ted.data

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
            assert self.__json is not None, 'document data error: %s' % self
            signature = self.signature
            assert signature is not None, 'document signature error: %s' % self
            return signature
        # 1. update sign time
        self.set_property(name='time', value=DateTime.current_timestamp())
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
        ted = TransportableData.create(data=signature, algorithm=EncodeAlgorithms.DEFAULT)
        # 3. update 'data' & 'signature' fields
        self['data'] = data             # JsON string
        self['signature'] = ted.object  # BASE-64
        self.__json = data
        self.__sig = ted
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
    def get_property(self, name: str) -> Optional[Any]:
        info = self.properties
        if info is not None:
            return info.get(name)

    # Override
    def set_property(self, name: str, value: Optional[Any]):
        """ Update property with key and value """
        # 1. reset status
        assert self.__status >= 0, 'status error: %s' % self
        self.__status = 0
        # 2. update property value with name
        info = self.properties
        if info is None:
            assert False, 'failed to get properties: %s' % self
        elif value is None:
            info.pop(name, None)
        else:
            info[name] = value
        # 3. clear data signature after properties changed
        self.pop('data', None)
        self.pop('signature', None)
        self.__json = None
        self.__sig = None

    #
    #  properties getter/setter
    #

    @property  # Override
    def time(self) -> Optional[DateTime]:
        seconds = self.get_property(name='time')
        return Converter.get_datetime(value=seconds, default=None)

    @property  # Override
    def name(self) -> Optional[str]:
        text = self.get_property(name='name')
        return Converter.get_str(value=text, default=None)

    @name.setter  # Override
    def name(self, text: str):
        self.set_property(name='name', value=text)
