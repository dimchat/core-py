#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    DIMP Test
    ~~~~~~~~~

    Unit test for DIMP
"""

import json
import unittest

from mkm.utils import *

from tests.immortals import *
from tests.database import *


def print_data(data: CAData):
    clazz = data.__class__.__name__
    print('<%s>' % clazz)
    print('    <issuer>%s</issuer>' % data.issuer)
    print('    <validity>%s</validity>' % data.validity)
    print('    <subject>%s</subject>' % data.subject)
    print('    <key>%s</key>' % data.key)
    print('</%s>' % clazz)


def print_ca(ca: CertificateAuthority):
    clazz = ca.__class__.__name__
    print('<%s>' % clazz)
    print('    <version>%d</version>' % ca.version)
    print('    <sn>%s</sn>' % ca.sn)
    print('    <info>%s</info>' % ca.info)
    print('    <signature>%s</signature>' % base64_encode(ca.signature))
    print('</%s>' % clazz)


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


barrack.cache_meta(meta=Meta(moki_meta), identifier=ID(moki_id))
barrack.cache_meta(meta=Meta(hulk_meta), identifier=ID(hulk_id))

database.cache_private_key(private_key=PrivateKey(moki_sk), identifier=ID(moki_id))
database.cache_private_key(private_key=PrivateKey(hulk_sk), identifier=ID(hulk_id))

moki.delegate = barrack

common = {}


class CATestCase(unittest.TestCase):

    def test1_subject(self):
        print('\n---------------- %s' % self)

        issuer = {
            'O': 'GSP',
            'OU': 'Service Operation Department',
            'CN': 'dim.chat',
        }

        common['issuer'] = CASubject(issuer)
        print('issuer: ', common['issuer'])
        self.assertEqual(common['issuer'].organization, issuer['O'])

        subject = {
            'C': 'CN',
            'ST': 'Guangdong',
            'L': 'Guangzhou',

            'O': 'GSP',
            'OU': 'Service Operation Department',
            'CN': '127.0.0.1',
        }

        common['subject'] = CASubject(subject)
        print('subject: ', common['subject'])
        self.assertEqual(common['subject'].organization, subject['O'])

    def test2_validity(self):
        print('\n---------------- %s' % self)

        validity = {
            'NotBefore': 123,
            'NotAfter': 456,
        }
        common['validity'] = CAValidity(validity)
        print('validity: ', common['validity'])

    def test3_key(self):
        print('\n---------------- %s' % self)

        key = moki_pk
        common['key'] = PublicKey(key)
        print('pubic key: ', common['key'])

    def test4_ca(self):
        print('\n---------------- %s' % self)

        info = {
            'Issuer': common['issuer'],
            'Validity': common['validity'],
            'Subject': common['subject'],
            'Key': common['key'],
        }
        common['info'] = CAData(info)
        print_data(common['info'])

        string = json.dumps(common['info']).encode('utf-8')
        signature = moki.sign(string)
        ca = {
            'version': 1,
            'sn': 1234567,
            'info': string,
            'signature': base64_encode(signature)
        }
        common['ca'] = CertificateAuthority(ca)
        print_ca(common['ca'])


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

        content = TextContent.new('Hello')
        print('text content: ', content)
        self.assertEqual(content.type, MessageType.Text)
        TransceiverTestCase.content = content

        command = CommandContent.new('handshake')
        print('command content: ', command)
        self.assertEqual(command.type, MessageType.Command)
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

        cmd = MetaCommand.response(identifier=moki_id, meta=moki_meta)
        print(cmd)
        print('cmd.meta: %s' % cmd.meta)
        self.assertEqual(cmd.meta, moki_meta)

    def test_profile(self):
        print('\n---------------- %s' % self)
        id1 = ID(moki_id)
        sk1 = PrivateKey(moki_sk)
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
        base64 = cmd['signature']
        self.assertTrue(pk1.verify(string.encode('utf-8'), base64_decode(base64)))


if __name__ == '__main__':
    unittest.main()
