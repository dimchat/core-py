# -*- coding: utf-8 -*-
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

"""
    Profile Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~~~~

    1. contains 'ID' only, means query profile for ID
    2. contains 'profile' and 'signature' (must match), means reply
"""

import json

from dkd.utils import base64_encode, base64_decode
from dkd.contents import serial_number

from dkd import MessageType, CommandContent

from mkm import PrivateKey
from mkm import ID


class ProfileCommand(CommandContent):
    """
        Profile Command
        ~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command   : "profile",  // command name
            ID        : "{ID}",     // entity ID
            meta      : {...},      // only for handshaking with new friend
            profile   : "{...}",    // json(profile); when profile is empty, means query for ID
            signature : "{BASE64}", // sign(json(profile))
        }

    """

    #
    #   ID
    #
    @property
    def identifier(self) -> ID:
        value = self.get('ID')
        if value:
            return ID(value)

    @identifier.setter
    def identifier(self, value: str):
        if value:
            self['ID'] = value
        else:
            self.pop('ID')

    #
    #   profile
    #
    @property
    def profile(self) -> dict:
        value = self.get('profile')
        if value:
            return json.loads(value)

    @profile.setter
    def profile(self, value: dict):
        if value:
            self['profile'] = json.dumps(value)
        else:
            self.pop('profile')

    #
    #   signature
    #
    @property
    def signature(self) -> bytes:
        value = self.get('signature')
        if value:
            return base64_decode(value)

    @signature.setter
    def signature(self, value: bytes):
        if value:
            self['signature'] = base64_encode(value)
        else:
            self.pop('signature')

    #
    #   Factories
    #
    @classmethod
    def query(cls, identifier: str) -> CommandContent:
        content = {
            'type': MessageType.Command,
            'sn': serial_number(),
            'command': 'profile',
            'ID': identifier,
        }
        return ProfileCommand(content)

    @classmethod
    def response(cls, identifier: str, profile: str, signature: str) -> CommandContent:
        content = {
            'type': MessageType.Command,
            'sn': serial_number(),
            'command': 'profile',
            'ID': identifier,
            'profile': profile,
            'signature': signature,
        }
        return ProfileCommand(content)

    @classmethod
    def pack(cls, identifier: str, private_key: PrivateKey, profile: dict) -> CommandContent:
        if 'ID' in profile:
            if identifier != profile['ID']:
                raise AssertionError('ID not match:', profile)
        else:
            profile['ID'] = identifier
        string = json.dumps(profile)
        sig = private_key.sign(string.encode('utf-8'))
        sig = base64_encode(sig)
        return cls.response(identifier=identifier, profile=string, signature=sig)
