# Decentralized Instant Messaging Protocol (Python)

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/dimchat/core-py/blob/master/LICENSE)
[![Version](https://img.shields.io/badge/alpha-0.8.0-red.svg)](https://github.com/dimchat/core-py/wiki)
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
    #   Barrack
    #
    def create_user(self, identifier: ID) -> User:
        assert identifier.type.is_user(), 'user ID error: %s' % identifier
        if identifier.is_broadcast:
            # create user 'anyone@anywhere'
            return User(identifier=identifier)
        assert self.meta(identifier) is not None, 'failed to get meta for user: %s' % identifier
        # TODO: check user type
        u_type = identifier.type
        if u_type.is_person():
            return User(identifier=identifier)
        if u_type.is_robot():
            return Robot(identifier=identifier)
        if u_type.is_station():
            return Station(identifier=identifier)
        raise TypeError('unsupported user type: %s' % u_type)

    def create_group(self, identifier: ID) -> Group:
        assert identifier.type.is_group(), 'group ID error: %s' % identifier
        if identifier.is_broadcast:
            # create group 'everyone@everywhere'
            return Group(identifier=identifier)
        assert self.meta(identifier) is not None, 'failed to get meta for group: %s' % identifier
        # TODO: check group type
        g_type = identifier.type
        if g_type == NetworkID.Polylogue:
            return Polylogue(identifier=identifier)
        if g_type == NetworkID.Chatroom:
            raise NotImplementedError('Chatroom not implemented')
        if g_type.is_provider():
            return ServiceProvider(identifier=identifier)
        raise TypeError('unsupported group type: %s' % g_type)


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
class Messenger(Transceiver, ConnectionDelegate):
    """ Transform and send/receive message """
    
    def __init__(self):
        super().__init__()
        # self.barrack = facebook
        # self.key_cache = keystore
        self.delegate: MessengerDelegate = None

    def encrypt_content(self, content: Content, key: dict, msg: InstantMessage) -> bytes:
        password = SymmetricKey(key=key)
        assert password == key, 'irregular symmetric key: %s' % key
        # check attachment for File/Image/Audio/Video message content before
        if isinstance(content, FileContent):
            data = password.encrypt(data=content.data)
            # upload (encrypted) file data onto CDN and save the URL in message content
            url = self.delegate.upload_data(data=data, msg=msg)
            if url is not None:
                content.url = url
                content.data = None
        return super().encrypt_content(content=content, key=password, msg=msg)

    def decrypt_content(self, data: bytes, key: dict, msg: SecureMessage) -> Optional[Content]:
        password = SymmetricKey(key=key)
        content = super().decrypt_content(data=data, key=password, msg=msg)
        if content is None:
            return None
        # check attachment for File/Image/Audio/Video message content after
        if isinstance(content, FileContent):
            i_msg = InstantMessage.new(content=content, envelope=msg.envelope)
            # download from CDN
            file_data = self.delegate.download_data(content.url, i_msg)
            if file_data is None:
                # save symmetric key for decrypted file data after download from CDN
                content.password = password
            else:
                # decrypt file data
                content.data = password.decrypt(data=file_data)
                assert content.data is not None, 'failed to decrypt file data with key: %s' % key
                content.url = None
        return content

    #
    #   Send message
    #
    def send_message(self, msg: InstantMessage, callback: Callback=None, split: bool=True) -> bool:
        """
        Send instant message (encrypt and sign) onto DIM network

        :param msg:      instant message
        :param callback: callback function
        :param split:    if it's a group message, split it before sending out
        :return:         False on data/delegate error
        """
        # Send message (secured + certified) to target station
        s_msg = self.encrypt_message(msg=msg)
        r_msg = self.sign_message(msg=s_msg)
        receiver = self.facebook.identifier(msg.envelope.receiver)
        ok = True
        if split and receiver.type.is_group():
            # split for each members
            members = self.facebook.members(identifier=receiver)
            if members is None or len(members) == 0:
                # FIXME: query group members from sender
                messages = None
            else:
                messages = r_msg.split(members=members)
            if messages is None:
                # failed to split msg, send it to group
                ok = self.__send_message(msg=r_msg, callback=callback)
            else:
                # sending group message one by one
                for r_msg in messages:
                    if not self.__send_message(msg=r_msg, callback=callback):
                        ok = False
        else:
            ok = self.__send_message(msg=r_msg, callback=callback)
        # TODO: if OK, set iMsg.state = sending; else set iMsg.state = waiting
        return ok

    def __send_message(self, msg: ReliableMessage, callback: Callback) -> bool:
        data = self.serialize_message(msg=msg)
        handler = MessageCallback(msg=msg, cb=callback)
        return self.delegate.send_package(data=data, handler=handler)

    #
    #   ConnectionDelegate
    #
    def received_package(self, data: bytes) -> Optional[bytes]:
        """
        Processing received message package

        :param data: message data
        :return: response message data
        """
        # 1. deserialize message
        r_msg = self.deserialize_message(data=data)
        # 2. process message
        response = self.process_message(msg=r_msg)
        if response is None:
            # nothing to response
            return None
        # 3. pack response
        user = self.facebook.current_user
        assert user is not None, 'failed to get current user'
        sender = self.facebook.identifier(r_msg.envelope.sender)
        i_msg = InstantMessage.new(content=response, sender=user.identifier, receiver=sender)
        s_msg = self.encrypt_message(msg=i_msg)
        msg_r = self.sign_message(msg=s_msg)
        assert msg_r is not None, 'failed to response: %s' % i_msg
        # serialize message
        return self.serialize_message(msg=msg_r)

    def process_message(self, msg: ReliableMessage) -> Optional[Content]:
        # TODO: try to verify/decrypt message and process it
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
def pack(content: Content, sender: ID, receiver: ID) -> ReliableMessage:
    # 1. create InstantMessage
    i_msg = InstantMessage.new(content=content, sender=sender, receiver=receiver)
    # 2. encrypt 'content' to 'data' for receiver
    s_msg = messenger.encrypt_message(msg=i_msg)
    # 3. sign 'data' by sender
    r_msg = messenger.sign_message(msg= s_msg)
    # OK
    return r_msg


def send(content: Content, sender: ID, receiver: ID) -> bool:
    # 1. pack message
    r_msg = pack(content=content, sender=sender, receiver=receiver)
    # 2. callback handler
    callback = None
    # 3. encode and send out
    return messenger.send_message(msg=r_msg, callback=callback)


if __name__ == '__main__':
    moki = facebook.identifier('moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk')
    hulk = facebook.identifier('hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj')
    # Say Hi
    text='Hello world!'
    content = TextContent.new(text=text)
    send(content=content, sender=moki, receiver=hulk)
```

receive.py

```python
def unpack(msg: ReliableMessage) -> Content:
    # 1. verify 'data' with 'signature'
    s_msg = messenger.verify_message(msg=msg)
    # 2. check group message
    receiver = facebook.identifier(msg.envelope.receiver)
    if receiver.type.is_group():
        # TODO: split it
        pass
    # 3. decrypt 'data' to 'content'
    i_msg = messenger.decrypt_message(msg=s_msg)
    # OK
    return i_msg.content


#
#   StationDelegate
#
def receive_package(data: bytes, station: Station):
    # 1. decode messsage package
    r_msg = messenger.deserialize_message(data=data)
    # 2. verify and decrypt message
    content = unpack(msg=r_msg)
    # TODO: process message content
```

Copyright &copy; 2019 Albert Moky
