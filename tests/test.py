#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    DIMP Test
    ~~~~~~~~~

    Unit test for DIMP
"""

import unittest

from mkm.immortals import *
from mkm.utils import *
from dkd.transform import json_str, json_dict

import dimp

from tests.data import *


def print_data(data: dimp.CAData):
    clazz = data.__class__.__name__
    print('<%s>' % clazz)
    print('    <issuer>%s</issuer>' % data.issuer)
    print('    <validity>%s</validity>' % data.validity)
    print('    <subject>%s</subject>' % data.subject)
    print('    <key>%s</key>' % data.key)
    print('</%s>' % clazz)


def print_ca(ca: dimp.CertificateAuthority):
    clazz = ca.__class__.__name__
    print('<%s>' % clazz)
    print('    <version>%d</version>' % ca.version)
    print('    <sn>%s</sn>' % ca.sn)
    print('    <info>%s</info>' % ca.info)
    print('    <signature>%s</signature>' % base64_encode(ca.signature))
    print('</%s>' % clazz)


def print_msg(msg: dimp.Message):
    clazz = msg.__class__.__name__
    sender = msg.envelope.sender
    receiver = msg.envelope.receiver
    time = msg.envelope.time
    print('<%s sender="%s" receiver="%s" time=%d>' % (clazz, sender, receiver, time))
    if isinstance(msg, dimp.InstantMessage):
        print('    <content>%s</content>' % msg['content'])
    if isinstance(msg, dimp.SecureMessage):
        print('    <data>%s</data>' % msg['data'])
        if 'key' in msg:
            print('    <key>%s</key>' % msg['key'])
        if 'keys' in msg:
            print('    <keys>%s</keys>' % msg['keys'])
    if isinstance(msg, dimp.ReliableMessage):
        print('    <signature>%s</signature>' % msg['signature'])
    print('</%s>' % clazz)


key_store = dimp.KeyStore()

barrack = dimp.Barrack()
barrack.save_meta(meta=dimp.Meta(moki_meta), identifier=dimp.ID(moki_id))
barrack.save_meta(meta=dimp.Meta(hulk_meta), identifier=dimp.ID(hulk_id))
barrack.save_private_key(private_key=dimp.PrivateKey(moki_sk), identifier=dimp.ID(moki_id))
barrack.save_private_key(private_key=dimp.PrivateKey(hulk_sk), identifier=dimp.ID(hulk_id))

transceiver = dimp.Transceiver(current_user=moki, barrack=barrack, key_store=key_store)
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

        common['issuer'] = dimp.CASubject(issuer)
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

        common['subject'] = dimp.CASubject(subject)
        print('subject: ', common['subject'])
        self.assertEqual(common['subject'].organization, subject['O'])

    def test2_validity(self):
        print('\n---------------- %s' % self)

        validity = {
            'NotBefore': 123,
            'NotAfter': 456,
        }
        common['validity'] = dimp.CAValidity(validity)
        print('validity: ', common['validity'])

    def test3_key(self):
        print('\n---------------- %s' % self)

        key = moki_pk
        common['key'] = dimp.PublicKey(key)
        print('pubic key: ', common['key'])

    def test4_ca(self):
        print('\n---------------- %s' % self)

        info = {
            'Issuer': common['issuer'],
            'Validity': common['validity'],
            'Subject': common['subject'],
            'Key': common['key'],
        }
        common['info'] = dimp.CAData(info)
        print_data(common['info'])

        string = json_str(common['info']).encode('utf-8')
        signature = moki.privateKey.sign(string)
        ca = {
            'version': 1,
            'sn': 1234567,
            'info': string,
            'signature': base64_encode(signature)
        }
        common['ca'] = dimp.CertificateAuthority(ca)
        print_ca(common['ca'])

        moki.delegate = barrack
        self.assertTrue(common['ca'].verify(moki.publicKey))


class TransceiverTestCase(unittest.TestCase):

    envelope = None
    content = None
    command = None

    i_msg: dimp.InstantMessage = None
    s_msg: dimp.SecureMessage = None
    r_msg: dimp.ReliableMessage = None

    @classmethod
    def setUpClass(cls):
        sender = moki_id
        receiver = hulk_id
        cls.envelope = dimp.Envelope(sender=sender, receiver=receiver)
        cls.content = None
        cls.command = None

    def test_1_content(self):
        print('\n---------------- %s' % self)

        content = dimp.TextContent.new('Hello')
        print('text content: ', content)
        self.assertEqual(content.type, dimp.MessageType.Text)
        TransceiverTestCase.content = content

        command = dimp.CommandContent.new('handshake')
        print('command content: ', command)
        self.assertEqual(command.type, dimp.MessageType.Command)
        TransceiverTestCase.command = command

    def test_2_instant(self):
        print('\n---------------- %s' % self)

        content = TransceiverTestCase.content
        envelope = TransceiverTestCase.envelope
        print('content: ', content)
        print('envelope: ', envelope)

        i_msg = dimp.InstantMessage.new(content=content, envelope=envelope)
        print_msg(i_msg)
        TransceiverTestCase.i_msg = i_msg

    def test_3_send(self):
        print('\n---------------- %s' % self)

        pwd = dimp.SymmetricKey.generate({'algorithm': 'AES'})
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
        cmd = dimp.GroupCommand.invite(group=gid, member=mid)
        print(cmd)
        cmd = dimp.GroupCommand.expel(group=gid, member=mid)
        print(cmd)
        cmd = dimp.GroupCommand.quit(group=gid)
        print(cmd)

    def test_handshake(self):
        print('\n---------------- %s' % self)
        cmd = dimp.HandshakeCommand.start()
        print(cmd)
        cmd = dimp.HandshakeCommand.again(session='1234567890')
        print(cmd)
        cmd = dimp.HandshakeCommand.restart(session='1234567890')
        print(cmd)
        cmd = dimp.HandshakeCommand.accepted()
        print(cmd)

    def test_meta(self):
        print('\n---------------- %s' % self)
        cmd = dimp.MetaCommand.query(identifier=moki_id)
        print(cmd)
        cmd = dimp.MetaCommand.response(identifier=moki_id, meta=moki_meta)
        print(cmd)

    def test_profile(self):
        print('\n---------------- %s' % self)
        id1 = dimp.ID(moki_id)
        sk1 = dimp.PrivateKey(moki_sk)
        pk1 = sk1.publicKey
        profile = {
            'names': ['moky', 'albert']
        }
        cmd = dimp.ProfileCommand.pack(identifier=id1, private_key=sk1, profile=profile)
        print(cmd)
        string = cmd['profile']
        signature = cmd['signature']
        print('profile: %s, signature: %s' %(string, signature))
        self.assertTrue(pk1.verify(string.encode('utf-8'), base64_decode(signature)))


if __name__ == '__main__':
    unittest.main()
