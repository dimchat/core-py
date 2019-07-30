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

"""
    Profile Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~~~~

    1. contains 'ID' only, means query profile for ID
    2. contains 'profile' and 'signature' (must match), means reply
"""

from mkm import Meta, Profile

from ..protocol import ContentType, CommandContent
from .meta import MetaCommand


class ProfileCommand(MetaCommand):
    """
        Profile Command
        ~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command   : "profile", // command name
            ID        : "{ID}",    // entity ID
            meta      : {...},     // only for handshaking with new friend
            profile   : {...}      // when profile is empty, means query for ID
        }

    """

    def __init__(self, content: dict):
        super().__init__(content)
        # profile
        profile = content.get('profile')
        if isinstance(profile, str):
            # compatible with v1.0
            profile = {
                'ID': content['ID'],
                'data': profile,
                'signature': content.get("signature")
            }
        self.__profile = Profile(profile)

    #
    #   profile
    #
    @property
    def profile(self) -> Profile:
        return self.__profile

    @profile.setter
    def profile(self, value: Profile):
        self.__profile = value
        if value is None:
            self.pop('profile', None)
            self.pop('signature', None)
        else:
            self['profile'] = value.get('data')
            self['signature'] = value.get('signature')

    #
    #   Factories
    #
    @classmethod
    def query(cls, identifier: str) -> CommandContent:
        content = {
            'type': ContentType.Command,
            'command': 'profile',
            'ID': identifier,
        }
        return ProfileCommand(content)

    @classmethod
    def response(cls, identifier: str, profile: Profile, meta: Meta=None) -> CommandContent:
        content = {
            'type': ContentType.Command,
            'command': 'profile',
            'ID': identifier,
            'profile': profile.get('data'),
            'signature': profile.get('signature'),
        }
        if meta is not None:
            content['meta'] = meta
        return ProfileCommand(content)
