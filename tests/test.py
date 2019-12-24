#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    DIMP Test
    ~~~~~~~~~

    Unit test for DIMP
"""

import json
import unittest

from mkm.crypto.utils import *

from dimp import*

from tests.facebook import Facebook
from tests.keystore import KeyStore

facebook = Facebook()

keystore = KeyStore()

transceiver = Transceiver()
transceiver.barrack = facebook
transceiver.key_cache = keystore

moki_id = facebook.identifier(string='moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk')
hulk_id = facebook.identifier(string='hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj')


def print_msg(msg: Message):
    clazz = msg.__class__.__name__
    sender = msg.envelope.sender
    receiver = msg.envelope.receiver
    time = msg.envelope.time
    print('<%s sender="%s" receiver="%s" time=%d>' % (clazz, sender, receiver, time))
    if isinstance(msg, InstantMessage):
        print('    <content>%s</content>' % msg['content'])
    if isinstance(msg, SecureMessage):
        print('    <data>%s</data>' % msg['data'])
        if 'key' in msg:
            print('    <key>%s</key>' % msg['key'])
        if 'keys' in msg:
            print('    <keys>%s</keys>' % msg['keys'])
    if isinstance(msg, ReliableMessage):
        print('    <signature>%s</signature>' % msg['signature'])
    print('</%s>' % clazz)


class TransceiverTestCase(unittest.TestCase):

    envelope = None
    content = None
    command = None

    i_msg: InstantMessage = None
    s_msg: SecureMessage = None
    r_msg: ReliableMessage = None

    @classmethod
    def setUpClass(cls):
        sender = moki_id
        receiver = hulk_id
        cls.envelope = Envelope.new(sender=sender, receiver=receiver)
        cls.content = None
        cls.command = None

    def test_1_content(self):
        print('\n---------------- %s' % self)

        content = TextContent.new(text='Hello')
        print('text content: ', content)
        string = json.dumps(content)
        print('JSON: ', string)
        self.assertEqual(content.type, ContentType.Text)
        TransceiverTestCase.content = content

        image = FileContent.image(data=b'')
        print('image content: ', image)
        self.assertEqual(image.type, ContentType.Image)

        command = HandshakeCommand.start()
        print('command content: ', command)
        self.assertEqual(command.type, ContentType.Command)
        TransceiverTestCase.command = command

    def test_2_instant(self):
        print('\n---------------- %s' % self)

        content = TransceiverTestCase.content
        envelope = TransceiverTestCase.envelope
        print('content: ', content)
        print('envelope: ', envelope)

        i_msg = InstantMessage.new(content=content, envelope=envelope)
        print_msg(i_msg)
        TransceiverTestCase.i_msg = i_msg

    def test_3_send(self):
        print('\n---------------- %s' % self)

        pwd = SymmetricKey({'algorithm': 'AES'})
        print('password: %s' % pwd)

        i_msg = TransceiverTestCase.i_msg
        print_msg(i_msg)
        i_msg.delegate = transceiver
        s_msg = i_msg.encrypt(password=pwd)
        print_msg(s_msg)
        TransceiverTestCase.s_msg = s_msg

        s_msg.delegate = transceiver
        r_msg = s_msg.sign()
        print_msg(r_msg)
        TransceiverTestCase.r_msg = r_msg

    def test_4_receive(self):
        print('\n---------------- %s' % self)

        r_msg = TransceiverTestCase.r_msg
        r_msg.delegate = transceiver
        s_msg = r_msg.verify()
        print_msg(s_msg)

        s_msg.delegate = transceiver
        i_msg = s_msg.decrypt()
        print_msg(i_msg)

        content = i_msg.content
        print('receive message content: %s' % content)
        self.assertEqual(content, TransceiverTestCase.content)


class CommandTestCase(unittest.TestCase):

    def test_group(self):
        print('\n---------------- %s' % self)
        gid = 'immortals@7WxUCsdaNnr5DyYsVS3Ct6w2TMupBNJVNu'
        mid = 'hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj'
        cmd = GroupCommand.invite(group=gid, member=mid)
        print(cmd)
        cmd = GroupCommand.expel(group=gid, member=mid)
        print(cmd)
        cmd = GroupCommand.quit(group=gid)
        print(cmd)

    def test_handshake(self):
        print('\n---------------- %s' % self)

        cmd: HandshakeCommand = HandshakeCommand.start()
        print(cmd)

        cmd = HandshakeCommand.again(session='1234567890')
        print(cmd)
        self.assertEqual(cmd.message, 'DIM?')

        cmd = HandshakeCommand.restart(session='1234567890')
        print(cmd)

        cmd = HandshakeCommand.accepted()
        print(cmd)
        self.assertEqual(cmd.message, 'DIM!')

    def test_meta(self):
        print('\n---------------- %s' % self)

        cmd: MetaCommand = MetaCommand.query(identifier=moki_id)
        print(cmd)
        self.assertEqual(cmd.identifier, moki_id)

        moki_meta = facebook.meta(identifier=moki_id)
        cmd = MetaCommand.response(identifier=moki_id, meta=moki_meta)
        print(cmd)
        print('cmd.meta: %s' % cmd.meta)
        self.assertEqual(cmd.meta, moki_meta)

    def test_profile(self):
        print('\n---------------- %s' % self)
        id1 = ID(moki_id)
        sk1 = facebook.private_key_for_signature(identifier=id1)
        pk1 = sk1.public_key
        profile = {
            'names': ['moky', 'albert']
        }
        profile = json.dumps(profile)
        signature = sk1.sign(data=profile.encode('utf-8'))
        signature = base64_encode(signature)
        profile = {
            'ID': id1,
            'data': profile,
            'signature': signature,
        }
        profile = Profile(profile)
        cmd: ProfileCommand = ProfileCommand.response(identifier=id1, profile=profile)
        print(cmd)
        print('cmd.profile: %s' % cmd.profile)
        self.assertEqual(cmd.profile, profile)

        string = cmd['profile']
        b64 = cmd['signature']
        self.assertTrue(pk1.verify(string.encode('utf-8'), base64_decode(b64)))


if __name__ == '__main__':
    unittest.main()
