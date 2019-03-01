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

from mkm.utils import base64_decode, base64_encode
from dkd.transform import json_dict, json_str
from dkd.contents import serial_number

from mkm import ID, PrivateKey
from dkd import MessageType, CommandContent


class ProfileCommand(CommandContent):

    def __init__(self, content: dict):
        super().__init__(content)
        # ID
        self.identifier = ID(content['ID'])
        # profile
        if 'profile' in content:
            self.profile = json_dict(content['profile'])
        else:
            self.profile = None
        # signature
        if 'signature' in content:
            self.signature = base64_decode(content['signature'])
        else:
            self.signature = None

    @classmethod
    def query(cls, identifier: ID) -> CommandContent:
        content = {
            'type': MessageType.Command,
            'sn': serial_number(),
            'command': 'profile',
            'ID': identifier,
        }
        return ProfileCommand(content)

    @classmethod
    def response(cls, identifier: ID, profile: str, signature: str) -> CommandContent:
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
    def pack(cls, identifier: ID, private_key: PrivateKey, profile: dict) -> CommandContent:
        if 'ID' in profile:
            if identifier != profile['ID']:
                raise AssertionError('ID not match:', profile)
        else:
            profile['ID'] = identifier
        string = json_str(profile)
        sig = private_key.sign(string.encode('utf-8'))
        sig = base64_encode(sig)
        return cls.response(identifier=identifier, profile=string, signature=sig)
