# Decentralized Instant Messaging Protocol (Python)

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/dimchat/core-py/blob/master/LICENSE)
[![Version](https://img.shields.io/badge/alpha-0.7.8-red.svg)](https://github.com/dimchat/core-py/wiki)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/dimchat/core-py/pulls)
[![Platform](https://img.shields.io/badge/Platform-Python%203-brightgreen.svg)](https://github.com/dimchat/core-py/wiki)

## Talk is cheap, show you the codes!

### Dependencies

```javascript
pip3 install dimp
```

### Common Extensions

facebook.py

```python
class Facebook(Barrack):
    """ Access database to load/save user's private key, meta and profiles """
    
    def save_private_key(self, private_key: PrivateKey, identifier: ID) -> bool:
        # TODO: save private key into safety storage
        pass
    
    def save_meta(self, meta: Meta, identifier: ID) -> bool:
        if not meta.match_identifier(identifier):
            return False
        # TODO: save meta to local/persistent storage
        pass
    
    def save_profile(self, profile: Profile) -> bool:
        if not self.verify_profile(profile):
            return False
        # TODO: save to local storage
        pass
    
    def verify_profile(self, profile: Profile) -> bool:
        if profile is None:
            return False
        elif profile.valid:
            # already verified
            return True
        identifier = profile.identifier
        meta = None
        if identifier.type.is_user():
            # verify with user's meta.key
            meta = self.meta(identifier=identifier)
        elif identifier.type.is_group():
            # verify with group owner's meta.key
            group = self.group(identifier=identifier)
            if group is not None:
                meta = self.meta(identifier=group.owner)
        if meta is not None:
            return profile.verify(public_key=meta.key)
    
    #
    #   SocialNetworkDelegate
    #
    def user(self, identifier: ID) -> User:
        entity = super().user(identifier=identifier)
        if entity is not None:
            return entity
        meta = self.meta(identifier=identifier)
        if meta is not None:
            key = self.private_key_for_signature(identifier=identifier)
            if key is None:
                entity = User(identifier=identifier)
            else:
                entity = LocalUser(identifier=identifier)
            self.cache_user(user=entity)
            return entity

    def group(self, identifier: ID) -> Group:
        entity = super().group(identifier=identifier)
        if entity is not None:
            return entity
        meta = self.meta(identifier=identifier)
        if meta is not None:
            entity = Group(identifier=identifier)
            self.cache_group(group=entity)
            return entity


#
#  global
#
facebook = Facebook()
```

keystore.py

```python
class KeyStore(KeyCache):
    """ For reuse symmetric key """
    
    def save_keys(self, key_map: dict) -> bool:
        # TODO: save to local cache
        pass
    
    def load_keys(self) -> dict:
        # TODO: load from local cache
        pass


#
#  global
#
keystore = KeyStore()
```

messenger.py

```python
class MessengerDelegate(metaclass=ABCMeta):

    @abstractmethod
    def send_package(self, data: bytes) -> bool:
        """
        Send out a data package onto network

        :param data:    package data
        :return: True on success
        """
        pass


class Messenger(Transceiver, ConnectionDelegate):
    """ Transform and send/receive message """
    
    def __init__(self):
        super().__init__()
        self.delegate: MessengerDelegate = None
        
    @property
    def current_user(self) -> Optional[LocalUser]:
        # TODO: get current user from context
        pass

    #
    #  Conveniences
    #
    def encrypt_sign(self, msg: InstantMessage) -> ReliableMessage:
        # 1. encrypt 'content' to 'data' for receiver
        s_msg = self.encrypt_message(msg=msg)
        # 1.1. check group
        group = msg.content.group
        if group is not None:
            # NOTICE: this help the receiver knows the group ID
            #         when the group message separated to multi-messages,
            #         if don't want the others know you are the group members,
            #         remove it.
            s_msg.envelope.group = group
        # 1.2. copy content type to envelope
        #      NOTICE: this help the intermediate nodes to recognize message type
        s_msg.envelope.type = msg.content.type
        # 2. sign 'data' by sender
        r_msg = self.sign_message(msg=s_msg)
        # OK
        return r_msg

    def verify_decrypt(self, msg: ReliableMessage) -> Optional[InstantMessage]:
        # 1. verify 'data' with 'signature'
        s_msg = self.verify_message(msg=msg)
        if s_msg is None:
            # failed to verify message
            return None
        # 2. decrypt 'data' to 'content'
        i_msg = self.decrypt_message(msg=s_msg)
        # OK
        return i_msg

    #
    #   Sending
    #
    def send_content(self, content: Content, receiver: ID) -> bool:
        sender = self.current_user.identifier
        i_msg = InstantMessage.new(content=content, sender=sender, receiver=receiver)
        return self.send_message(msg=i_msg)
    
    def send_message(self, msg: InstantMessage) -> bool:
        r_msg = messenger.encrypt_sign(msg=msg)
        data = messenger.serialize_message(msg=r_msg)
        package = data + b'\n'
        self.delegate.send_package(data=package)

    #
    #   ConnectionDelegate
    #
    def received_package(self, data: bytes) -> Optional[bytes]:
        """ Processing received message package """
        r_msg = self.deserialize_message(data=data)
        response = self.process_message(msg=r_msg)
        if response is None:
            # nothing to response
            return None
        # response to the sender
        sender = self.current_user.identifier
        receiver = self.barrack.identifier(r_msg.envelope.sender)
        i_msg = InstantMessage.new(content=response, sender=sender, receiver=receiver)
        msg_r = self.encrypt_sign(msg=i_msg)
        return self.serialize_message(msg=msg_r)

    def process_message(self, msg: ReliableMessage) -> Optional[Content]:
        # TODO: verify, decrypt and process this message
        #       return a receipt as response
        pass


#
#  global
#
messenger = Messenger()
messenger.barrack = facebook
messenger.key_cache = keystore
```

### User Account

register.py

```python
def register(username: str) -> User:
    # 1. generate private key
    sk = PrivateKey({'algorithm': 'RSA'})
    
    # 2. generate meta with username(as seed) and private key
    meta = Meta.generate(private_key=sk, seed=username)
    
    # 3. generate ID with network type by meta
    identifier = meta.generate_identifier(network=network)
    
    # 4. save private key and meta info
    facebook.save_private_key(private_key=sk, identifier=identifier)
    facebook.save_meta(meta=meta, identifier=identifier)
    
    # 5. create user with ID
    return facebook.user(identifier)
```

### Messaging

send.py

```python
def pack(content: Content, sender: ID, receiver: ID) -> bytes:
    i_msg = InstantMessage.new(content=content, sender=sender, receiver=receiver)
    r_msg = messenger.encrypt_sign(msg=i_msg)
    return messenger.serialize_message(msg=r_msg)


def send(text: str, receiver: str, sender: str) -> bool:
    sender = facebook.identifier(sender)
    receiver = facebook.identifier(receiver)
    content = TextContent.new(text=text)
    data = pack(content=content, sender=sender, receiver=receiver)
    request = data + b'\n'
    # TODO: send out the request data


if __name__ == '__main__':
    moki = 'moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk'
    hulk = 'hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj'
    # Say Hi
    send(text='Hello world!', sender=moki, receiver=hulk)
```

receive.py

```python
def unpack(data: bytes) -> InstantMessage:
    r_msg = messenger.deserialize_message(data=data)
    return messenger.verify_decrypt(r_msg)


def process(content: Content, sender: ID) -> Content:
    # TODO: process message content from sender
    pass


def receive(pack: bytes) -> Content:
    i_msg = unpack(data)
    sender = facebook.identifier(i_msg.envelope.sender)
    return process(content=i_msg.content, sender=sender)
```

Copyright &copy; 2019 Albert Moky
