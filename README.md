# Decentralized Instant Messaging Protocol (Python)

[![License](https://img.shields.io/github/license/dimchat/core-py)](https://github.com/dimchat/core-py/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/dimchat/core-py/pulls)
[![Platform](https://img.shields.io/badge/Platform-Python%203-brightgreen.svg)](https://github.com/dimchat/core-py/wiki)
[![Issues](https://img.shields.io/github/issues/dimchat/core-py)](https://github.com/dimchat/core-py/issues)
[![Repo Size](https://img.shields.io/github/repo-size/dimchat/core-py)](https://github.com/dimchat/core-py/archive/refs/heads/main.zip)
[![Tags](https://img.shields.io/github/tag/dimchat/core-py)](https://github.com/dimchat/core-py/tags)
[![Version](https://img.shields.io/pypi/v/dimp)](https://pypi.org/project/dimp)

[![Watchers](https://img.shields.io/github/watchers/dimchat/core-py)](https://github.com/dimchat/core-py/watchers)
[![Forks](https://img.shields.io/github/forks/dimchat/core-py)](https://github.com/dimchat/core-py/forks)
[![Stars](https://img.shields.io/github/stars/dimchat/core-py)](https://github.com/dimchat/core-py/stargazers)
[![Followers](https://img.shields.io/github/followers/dimchat)](https://github.com/orgs/dimchat/followers)

## Dependencies

| Name | Version | Description |
|------|---------|-------------|
| [Ming Ke Ming (名可名)](https://github.com/dimchat/mkm-py) | [![Version](https://img.shields.io/pypi/v/mkm)](https://pypi.org/project/mkm) | Decentralized User Identity Authentication |
| [Dao Ke Dao (道可道)](https://github.com/dimchat/dkd-py) | [![Version](https://img.shields.io/pypi/v/dkd)](https://pypi.org/project/dkd) | Universal Message Module |

## Examples

### extends Command

* _Handshake Command Protocol_
  0. (C-S) handshake start
  1. (S-C) handshake again with new session
  2. (C-S) handshake restart with new session
  3. (S-C) handshake success

```python
from enum import IntEnum
from typing import Optional, Any, Dict

from dimp import Command, BaseCommand


class HandshakeState(IntEnum):
    Start = 0    # C -> S, without session key(or session expired)
    Again = 1    # S -> C, with new session key
    Restart = 2  # C -> S, with new session key
    Success = 3  # S -> C, handshake accepted


class HandshakeCommand(BaseCommand):
    """
        Handshake Command
        ~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command : "handshake",    // command name
            title   : "Hello world!", // "DIM?", "DIM!"
            session : "{SESSION_ID}", // session key
        }
    """
    HANDSHAKE = 'handshake'

    def __init__(self, content: Dict[str, Any] = None, title: str = None, session: str = None):
        if content is None:
            # 1. new command with title & session key
            assert title is not None, 'handshake command error: %s' % session
            cmd = self.HANDSHAKE
            super().__init__(cmd=cmd)
            self['title'] = title
            self['message'] = title  # TODO: remove after all clients upgraded
            if session is not None:
                self['session'] = session
        else:
            # 2. command info from network
            assert title is None and session is None, 'params error: %s, %s, %s' % (content, title, session)
            super().__init__(content)

    @property
    def title(self) -> str:
        # TODO: modify after all clients upgraded
        text = self.get_str(key='title', default=None)
        if text is None:
            # compatible with v1.0
            text = self.get_str(key='message', default='')
        return text

    @property
    def session(self) -> Optional[str]:
        return self.get_str(key='session', default=None)

    @property
    def state(self) -> HandshakeState:
        return handshake_state(title=self.title, session=self.session)

    @classmethod
    def offer(cls, session: str = None) -> Command:
        """
        Create client-station handshake offer

        :param session: Old session key
        :return: HandshakeCommand object
        """
        return HandshakeCommand(title='Hello world!', session=session)

    @classmethod
    def ask(cls, session: str) -> Command:
        """
        Create station-client handshake again with new session

        :param session: New session key
        :return: HandshakeCommand object
        """
        return HandshakeCommand(title='DIM?', session=session)

    @classmethod
    def accepted(cls, session: str = None) -> Command:
        """
        Create station-client handshake success notice

        :return: HandshakeCommand object
        """
        return HandshakeCommand(title='DIM!', session=session)

    start = offer       # (1. C->S) first handshake, without session
    again = ask         # (2. S->C) ask client to handshake with new session key
    restart = offer     # (3. C->S) handshake with new session key
    success = accepted  # (4. S->C) notice the client that handshake accepted


def handshake_state(title: str, session: str = None) -> HandshakeState:
    # Server -> Client
    if title == 'DIM!':  # or title == 'OK!':
        return HandshakeState.Success
    if title == 'DIM?':
        return HandshakeState.Again
    # Client -> Server: "Hello world!"
    if session is None or len(session) == 0:
        return HandshakeState.Start
    else:
        return HandshakeState.Restart
```

### extends Content

```python
from abc import ABC, abstractmethod
from typing import Any, Dict

from dimp import ContentType
from dimp import Content
from dimp import BaseContent


class CustomizedContent(Content, ABC):
    """
        Application Customized message
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0xCC,
            sn   : 123,

            app   : "{APP_ID}",  // application (e.g.: "chat.dim.sechat")
            mod   : "{MODULE}",  // module name (e.g.: "drift_bottle")
            act   : "{ACTION}",  // action name (e.g.: "throw")
            extra : info         // action parameters
        }
    """

    @property
    @abstractmethod
    def application(self) -> str:
        """ App ID """
        raise NotImplemented

    @property
    @abstractmethod
    def module(self) -> str:
        """ Module Name """
        raise NotImplemented

    @property
    @abstractmethod
    def action(self) -> str:
        """ Action Name """
        raise NotImplemented

    @classmethod
    def create(cls, app: str, mod: str, act: str):
        return AppCustomizedContent(app=app, mod=mod, act=act)


class AppCustomizedContent(BaseContent, CustomizedContent):

    def __init__(self, content: Dict[str, Any] = None,
                 msg_type: int = None,
                 app: str = None, mod: str = None, act: str = None):
        if content is None:
            # 1. new content with type, application, module & action
            assert app is not None and mod is not None and act is not None, \
                'customized content error: %s, %s, %s, %s' % (msg_type, app, mod, act)
            if msg_type is None:
                msg_type = ContentType.CUSTOMIZED.value
            super().__init__(None, msg_type)
            self['app'] = app
            self['mod'] = mod
            self['act'] = act
        else:
            # 2. content info from network
            assert msg_type is None and app is None and mod is None and act is None, \
                'params error: %s, %s, %s, %s, %s' % (content, msg_type, app, mod, act)
            super().__init__(content)

    @property  # Override
    def application(self) -> str:
        return self.get_str(key='app', default='')

    @property  # Override
    def module(self) -> str:
        return self.get_str(key='mod', default='')

    @property  # Override
    def action(self) -> str:
        return self.get_str(key='act', default='')
```

### extends ID Address

* Examples in [dim plugins](https://pypi.org/project/dimplugins)

----

Copyright &copy; 2018 Albert Moky
[![Followers](https://img.shields.io/github/followers/moky)](https://github.com/moky?tab=followers)
