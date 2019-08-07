# Decentralized Instant Messaging Protocol (Python)

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/dimchat/core-py/blob/master/LICENSE)
[![Version](https://img.shields.io/badge/alpha-0.1.0-red.svg)](https://github.com/dimchat/core-py/wiki)
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
        pass


#
#  singleton
#
facebook = Facebook()
```

keystore.py

```python
class KeyStore(KeyCache):
    """ For reuse symmetric key """
    
    def save_keys(self, key_map: dict) -> bool:
        pass
    
    def load_keys(self) -> dict:
        pass


#
#  singleton
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
        pass

    def upload_data(self, data: bytes, msg: InstantMessage) -> str:
        pass

    def download_data(self, url: str, msg: InstantMessage) -> bytes:
        pass


#
#  singleton
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
    user = User(identifier)
    facebook.cache_user(user)
    return user
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

Copyright &copy; 2019 Albert Moky
