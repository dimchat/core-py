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

from typing import Optional

from mkm import ID, Meta, Profile

from .command import Command
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
            profile   : {...},     // when profile is empty, means query for ID
            signature : "..."      // old profile's signature for querying
        }

    """

    def __new__(cls, cmd: dict):
        """
        Create profile command

        :param cmd: command info
        :return: ProfileCommand object
        """
        if cmd is None:
            return None
        elif cls is ProfileCommand:
            if isinstance(cmd, ProfileCommand):
                # return ProfileCommand object directly
                return cmd
        # new ProfileCommand(dict)
        return super().__new__(cls, cmd)

    def __init__(self, content: dict):
        if self is content:
            # no need to init again
            return
        super().__init__(content)
        # lazy
        self.__profile: Profile = None

    #
    #   profile
    #
    @property
    def profile(self) -> Optional[Profile]:
        if self.__profile is None:
            profile = self.get('profile')
            if isinstance(profile, str):
                # compatible with v1.0
                dictionary = {
                    'ID': self.identifier,
                    'data': profile,
                    'signature': self.get("signature")
                }
                profile = dictionary
            self.__profile = Profile(profile)
        return self.__profile

    @profile.setter
    def profile(self, value: Profile):
        if value is None:
            self.pop('profile', None)
            self.pop('signature', None)
        else:
            self['profile'] = value.get('data')
            self['signature'] = value.get('signature')
        self.__profile = value

    #
    #   signature
    #
    @property
    def signature(self) -> Optional[str]:
        return self.get('signature')

    @signature.setter
    def signature(self, value: str):
        if value is None:
            self.pop('signature', None)
        else:
            assert 'data' not in self and 'profile' not in self and 'meta' not in self, 'profile cmd error'
            self['signature'] = value

    #
    #   Factories
    #
    @classmethod
    def new(cls, content: dict=None, identifier: ID=None, meta: Meta=None, profile: Profile=None, signature: str=None):
        """
        Create profile command for entity

        :param content:    command info
        :param identifier: entity ID
        :param meta:       entity meta
        :param profile:    entity profile
        :param signature:  old profile's signature for querying
        :return: ProfileCommand object
        """
        if content is None:
            # create empty content
            content = {}
        # set command name: 'profile'
        if 'command' not in content:
            content['command'] = Command.PROFILE
        # set profile info
        if profile is not None:
            assert profile.identifier == identifier, 'profile ID error: %s, %s' % (profile, identifier)
            content['profile'] = profile.get('data')
            content['signature'] = profile.get('signature')
        elif signature is not None:
            content['signature'] = signature
        return super().new(content=content, identifier=identifier, meta=meta)

    @classmethod
    def query(cls, identifier: ID, signature: str=None):
        return cls.new(identifier=identifier, signature=signature)

    @classmethod
    def response(cls, identifier: ID, profile: Profile, meta: Meta=None):
        return cls.new(identifier=identifier, meta=meta, profile=profile)


# register command class
Command.register(command=Command.PROFILE, command_class=ProfileCommand)
