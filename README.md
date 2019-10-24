# Decentralized Instant Messaging Protocol (Python)

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/dimchat/core-py/blob/master/LICENSE)
[![Version](https://img.shields.io/badge/alpha-0.5.2-red.svg)](https://github.com/dimchat/core-py/wiki)
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
    #   ISocialNetworkDataSource
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

messanger.py

```python
class Messanger(Transceiver, ITransceiverDelegate):
    """ Transform and send message """
    
    def __init__(self):
        super().__init__()
        self.delegate = self

    #
    #  ITransceiverDelegate
    #
    def send_package(self, data: bytes, handler: ICompletionHandler) -> bool:
        # TODO: send out data
        pass

    def upload_data(self, data: bytes, msg: InstantMessage) -> str:
        # TODO: upload onto FTP server
        pass

    def download_data(self, url: str, msg: InstantMessage) -> bytes:
        # TODO: download from FTP server
        pass


#
#  global
#
messanger = Messanger()
messanger.barrack = facebook
messanger.key_cache = keystore
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
    msg = InstantMessage.new(content=content, sender=sender, receiver=receiver)
    return messanger.encrypt_sign(msg)


if __name__ == '__main__':
    moki = ID("moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk");
    hulk = ID("hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj");
    content = TextContent.new(text='Hello world!')
    msg = pack(content=content, sender=moki, receiver=hulk)
    
    # TODO: send out the request data
    request = json.dumps(msg) + '\n'
    data = request.encode('utf-8')
```

receive.py

```python
def receive(pack: bytes) -> InstantMessage:
    msg = json.loads(pack.decode('utf-8'))
    r_msg = ReliableMessage(msg)
    i_msg = messanger.verify_decrypt(r_msg)
    # TODO: process message content
    pass
```

Copyright &copy; 2019 Albert Moky
