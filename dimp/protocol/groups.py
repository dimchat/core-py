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
    Group Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~~

    1. invite member
    2. expel member
    3. member quit
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict

from mkm.types import DateTime
from mkm import ID

from .types import ContentType
from .commands import Command
from .base import BaseCommand


# noinspection PyAbstractClass
class HistoryCommand(Command, ABC):
    """
        History Command
        ~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x89),
            sn   : 123,

            command : "...", // command name
            time    : 0,     // command timestamp
            extra   : info   // command parameters
        }
    """

    # -------- command names begin --------
    # account
    REGISTER = "register"
    SUICIDE = "suicide"
    # -------- command names end --------


class GroupCommand(HistoryCommand, ABC):
    """
        Group Command
        ~~~~~~~~~~~~~

        data format: {
            type : i2s(0x89),
            sn   : 123,

            command : "reset",   // "invite", "quit", "query", ...
            time    : 0,         // timestamp

            group   : "{GROUP_ID}",
            member  : "{MEMBER_ID}",
            members : ["{MEMBER_ID}",]
        }
    """

    # -------- command names begin --------
    # founder/owner
    FOUND = "found"
    ABDICATE = "abdicate"
    # member
    INVITE = "invite"
    EXPEL = "expel"  # Deprecated (use 'reset' instead)
    JOIN = "join"
    QUIT = "quit"
    RESET = "reset"
    QUERY = "query"  # (not history command)
    # administrator/assistant
    HIRE = "hire"
    FIRE = "fire"
    RESIGN = "resign"
    # -------- command names end --------

    #
    #   group (group ID already fetched in Content)
    #

    #
    #   member/members
    #
    @property
    @abstractmethod
    def member(self) -> Optional[ID]:
        raise NotImplemented

    @member.setter
    @abstractmethod
    def member(self, user: Optional[ID]):
        raise NotImplemented

    @property
    @abstractmethod
    def members(self) -> Optional[List[ID]]:
        raise NotImplemented

    @members.setter
    @abstractmethod
    def members(self, users: Optional[List[ID]]):
        raise NotImplemented

    #
    #   Factory methods
    #

    @classmethod
    def create(cls, cmd: str, group: ID, member: ID = None, members: List[ID] = None):
        return BaseGroupCommand(cmd=cmd, group=group, member=member, members=members)

    @classmethod
    def invite(cls, group: ID, member: ID = None, members: List[ID] = None):
        return InviteGroupCommand(group=group, member=member, members=members)

    @classmethod
    def expel(cls, group: ID, member: ID = None, members: List[ID] = None):
        """ Deprecated (use 'reset' instead) """
        return ExpelGroupCommand(group=group, member=member, members=members)

    @classmethod
    def join(cls, group: ID):
        return JoinGroupCommand(group=group)

    @classmethod
    def quit(cls, group: ID):
        return QuitGroupCommand(group=group)

    @classmethod
    def query(cls, group: ID, last_time: DateTime = None):
        return QueryGroupCommand(group=group, last_time=last_time)

    @classmethod
    def reset(cls, group: ID, members: List[ID]):
        return ResetGroupCommand(group=group, members=members)

    # Administrators, Assistants

    @classmethod
    def hire(cls, group: ID, administrators: List[ID] = None, assistants: List[ID] = None):
        return HireGroupCommand(group=group, administrators=administrators, assistants=assistants)

    @classmethod
    def fire(cls, group: ID, administrators: List[ID] = None, assistants: List[ID] = None):
        return FireGroupCommand(group=group, administrators=administrators, assistants=assistants)

    @classmethod
    def resign(cls, group: ID):
        return ResignGroupCommand(group=group)


# noinspection PyAbstractClass
class InviteCommand(GroupCommand, ABC):
    pass


# noinspection PyAbstractClass
class ExpelCommand(GroupCommand, ABC):
    """ Deprecated (use 'reset' instead) """
    pass


# noinspection PyAbstractClass
class JoinCommand(GroupCommand, ABC):
    pass


# noinspection PyAbstractClass
class QuitCommand(GroupCommand, ABC):
    pass


class QueryCommand(GroupCommand, ABC):
    """
    NOTICE:
        This command is just for querying group info,
        should not be saved in group history
    """

    @property
    @abstractmethod
    def last_time(self) -> Optional[DateTime]:
        """ Last group history time for querying """
        raise NotImplemented


# noinspection PyAbstractClass
class ResetCommand(GroupCommand, ABC):
    pass


"""
    Administrator
    ~~~~~~~~~~~~~
"""


class HireCommand(GroupCommand, ABC):

    @property
    @abstractmethod
    def administrators(self) -> Optional[List[ID]]:
        raise NotImplemented

    @administrators.setter
    @abstractmethod
    def administrators(self, users: List[ID]):
        raise NotImplemented

    @property
    @abstractmethod
    def assistants(self) -> Optional[List[ID]]:
        raise NotImplemented

    @assistants.setter
    @abstractmethod
    def assistants(self, bots: List[ID]):
        raise NotImplemented


class FireCommand(GroupCommand, ABC):

    @property
    @abstractmethod
    def administrators(self) -> Optional[List[ID]]:
        raise NotImplemented

    @administrators.setter
    @abstractmethod
    def administrators(self, users: List[ID]):
        raise NotImplemented

    @property
    @abstractmethod
    def assistants(self) -> Optional[List[ID]]:
        raise NotImplemented

    @assistants.setter
    @abstractmethod
    def assistants(self, bots: List[ID]):
        raise NotImplemented


# noinspection PyAbstractClass
class ResignCommand(GroupCommand, ABC):
    pass


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class BaseHistoryCommand(BaseCommand, HistoryCommand):

    def __init__(self, content: Dict = None,
                 msg_type: str = None, cmd: str = None):
        if content is None:
            if msg_type is None:
                msg_type = ContentType.HISTORY
            assert cmd is not None, 'command name should not empty'
        super().__init__(content, msg_type, cmd=cmd)


class BaseGroupCommand(BaseHistoryCommand, GroupCommand):

    def __init__(self, content: Dict = None,
                 cmd: str = None, group: ID = None,
                 member: ID = None, members: List[ID] = None):
        super().__init__(content, None, cmd=cmd)
        if group is not None:
            self.group = group
        if member is not None:
            self.member = member
        elif members is not None:
            self.members = members

    #
    #   group (group ID already fetched in Content)
    #

    #
    #   member/members
    #
    @property  # Override
    def member(self) -> Optional[ID]:
        return ID.parse(identifier=self.get('member'))

    @member.setter  # Override
    def member(self, user: ID):
        self.set_string(key='member', value=user)
        self.pop('members', None)

    @property  # Override
    def members(self) -> Optional[List[ID]]:
        array = self.get('members')
        if array is not None:
            # convert all items to ID objects
            return ID.convert(array=array)
        # get from 'member'
        single = self.member
        return [] if single is None else [single]

    @members.setter  # Override
    def members(self, users: List[ID]):
        if users is None:
            self.pop('members', None)
        else:
            self['members'] = ID.revert(identifiers=users)
        self.pop('member', None)


class InviteGroupCommand(BaseGroupCommand, InviteCommand):

    def __init__(self, content: Dict = None,
                 group: ID = None, member: ID = None, members: List[ID] = None):
        cmd = GroupCommand.INVITE if content is None else None
        super().__init__(content, cmd=cmd, group=group, member=member, members=members)


class ExpelGroupCommand(BaseGroupCommand, ExpelCommand):
    """ Deprecated, use 'reset' instead """

    def __init__(self, content: Dict = None,
                 group: ID = None, member: ID = None, members: List[ID] = None):
        cmd = GroupCommand.EXPEL if content is None else None
        super().__init__(content, cmd=cmd, group=group, member=member, members=members)


class JoinGroupCommand(BaseGroupCommand, JoinCommand):

    def __init__(self, content: Dict = None, group: ID = None):
        cmd = GroupCommand.JOIN if content is None else None
        super().__init__(content, cmd=cmd, group=group)


class QuitGroupCommand(BaseGroupCommand, QuitCommand):

    def __init__(self, content: Dict = None, group: ID = None):
        cmd = GroupCommand.QUIT if content is None else None
        super().__init__(content, cmd=cmd, group=group)


class QueryGroupCommand(BaseGroupCommand, QueryCommand):

    def __init__(self, content: Dict = None, group: ID = None, last_time: DateTime = None):
        cmd = GroupCommand.QUERY if content is None else None
        super().__init__(content, cmd=cmd, group=group)
        if last_time is not None:
            self.set_datetime(key='last_time', value=last_time)

    @property  # Override
    def last_time(self) -> Optional[DateTime]:
        return self.get_datetime(key='last_time', default=None)


class ResetGroupCommand(BaseGroupCommand, ResetCommand):

    def __init__(self, content: Dict = None, group: ID = None, members: List[ID] = None):
        cmd = GroupCommand.RESET if content is None else None
        super().__init__(content, cmd=cmd, group=group, members=members)


"""
    Administrator
    ~~~~~~~~~~~~~
"""


class HireGroupCommand(BaseGroupCommand, HireCommand):

    def __init__(self, content: Dict = None, group: ID = None,
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

    def __init__(self, content: Dict = None, group: ID = None,
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

    def __init__(self, content: Dict = None, group: ID = None):
        cmd = GroupCommand.RESIGN if content is None else None
        super().__init__(content=content, cmd=cmd, group=group)
