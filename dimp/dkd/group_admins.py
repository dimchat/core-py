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


from typing import Optional, Any, Dict, List

from mkm import ID

from ..protocol import GroupCommand
from ..protocol import HireCommand, FireCommand, ResignCommand

from .groups import BaseGroupCommand


"""
    Administrator
    ~~~~~~~~~~~~~
"""


class HireGroupCommand(BaseGroupCommand, HireCommand):

    def __init__(self, content: Dict[str, Any] = None, group: ID = None,
                 administrators: List[ID] = None,
                 assistants: List[ID] = None):
        cmd = GroupCommand.HIRE if content is None else None
        super().__init__(content, cmd=cmd, group=group)
        # group admins
        if administrators is not None:
            self['administrators'] = ID.revert(identifiers=administrators)
        # group bots
        if assistants is not None:
            self['assistants'] = ID.revert(identifiers=assistants)

    @property  # Override
    def administrators(self) -> Optional[List[ID]]:
        users = self.get('administrators')
        if isinstance(users, List):
            # convert all items to ID objects
            return ID.convert(array=users)
        assert users is None, 'ID list error: %s' % users

    @administrators.setter  # Override
    def administrators(self, users: List[ID]):
        if users is None:
            self.pop('administrators', None)
        else:
            self['administrators'] = ID.revert(identifiers=users)

    @property  # Override
    def assistants(self) -> Optional[List[ID]]:
        bots = self.get('assistants')
        if isinstance(bots, List):
            # convert all items to ID objects
            return ID.convert(array=bots)
        assert bots is None, 'ID list error: %s' % bots

    @assistants.setter  # Override
    def assistants(self, bots: List[ID]):
        if bots is None:
            self.pop('assistants', None)
        else:
            self['assistants'] = ID.revert(identifiers=bots)


class FireGroupCommand(BaseGroupCommand, FireCommand):

    def __init__(self, content: Dict[str, Any] = None, group: ID = None,
                 administrators: List[ID] = None,
                 assistants: List[ID] = None):
        cmd = GroupCommand.FIRE if content is None else None
        super().__init__(content=content, cmd=cmd, group=group)
        # group admins
        if administrators is not None:
            self['administrators'] = ID.revert(identifiers=administrators)
        # group bots
        if assistants is not None:
            self['assistants'] = ID.revert(identifiers=assistants)

    @property  # Override
    def administrators(self) -> Optional[List[ID]]:
        users = self.get('administrators')
        if isinstance(users, List):
            # convert all items to ID objects
            return ID.convert(array=users)
        assert users is None, 'ID list error: %s' % users

    @administrators.setter  # Override
    def administrators(self, users: List[ID]):
        if users is None:
            self.pop('administrators', None)
        else:
            self['administrators'] = ID.revert(identifiers=users)

    @property  # Override
    def assistants(self) -> Optional[List[ID]]:
        bots = self.get('assistants')
        if isinstance(bots, List):
            # convert all items to ID objects
            return ID.convert(array=bots)
        assert bots is None, 'ID list error: %s' % bots

    @assistants.setter  # Override
    def assistants(self, bots: List[ID]):
        if bots is None:
            self.pop('assistants', None)
        else:
            self['assistants'] = ID.revert(identifiers=bots)


class ResignGroupCommand(BaseGroupCommand, ResignCommand):

    def __init__(self, content: Dict[str, Any] = None, group: ID = None):
        cmd = GroupCommand.RESIGN if content is None else None
        super().__init__(content=content, cmd=cmd, group=group)
