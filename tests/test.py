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


class Common(dimp.Barrack, dimp.KeyStore):

    issuer = None
    subject = None
    validity = None
    key = None

    info = None
    ca = None

    users = {}
    received_keys = {}
    sent_keys = {}

    transceiver: dimp.Transceiver = None

    def account(self, identifier: dimp.ID) -> dimp.Account:
        return Common.users[identifier]

    def group(self, identifier: dimp.ID) -> dimp.Group:
        pass

    def symmetric_key(self, sender: dimp.ID=None, receiver: dimp.ID=None) -> dimp.SymmetricKey:
        if sender:
            if sender in Common.received_keys:
                return Common.received_keys[sender]
        else:
            if receiver in Common.sent_keys:
                return Common.sent_keys[receiver]
            else:
                password = dimp.SymmetricKey.generate({'algorithm': 'AES'})
                Common.sent_keys[receiver] = password
                return password

    def save_symmetric_key(self, password: dimp.SymmetricKey, sender: dimp.ID=None, receiver: dimp.ID=None):
        if sender:
            Common.received_keys[sender] = password
        else:
            Common.sent_keys[receiver] = password


class CATestCase(unittest.TestCase):

    def test1_subject(self):
        print('\n---------------- %s' % self)

        issuer = {
            'O': 'GSP',
            'OU': 'Service Operation Department',
            'CN': 'dim.chat',
        }

        Common.issuer = dimp.CASubject(issuer)
        print('issuer: ', Common.issuer)
        self.assertEqual(Common.issuer.organization, issuer['O'])

        subject = {
            'C': 'CN',
            'ST': 'Guangdong',
            'L': 'Guangzhou',

            'O': 'GSP',
            'OU': 'Service Operation Department',
            'CN': '127.0.0.1',
        }

        Common.subject = dimp.CASubject(subject)
        print('subject: ', Common.subject)
        self.assertEqual(Common.subject.organization, subject['O'])

    def test2_validity(self):
        print('\n---------------- %s' % self)

        validity = {
            'NotBefore': 123,
            'NotAfter': 456,
        }
        Common.validity = dimp.CAValidity(validity)
        print('validity: ', Common.validity)

    def test3_key(self):
        print('\n---------------- %s' % self)

        key = moki_pk
        Common.key = dimp.PublicKey(key)
        print('pubic key: ', Common.key)

    def test4_ca(self):
        print('\n---------------- %s' % self)

        info = {
            'Issuer': Common.issuer,
            'Validity': Common.validity,
            'Subject': Common.subject,
            'Key': Common.key,
        }
        Common.info = dimp.CAData(info)
        print_data(Common.info)

        string = json_str(Common.info).encode('utf-8')
        signature = moki.privateKey.sign(string)
        ca = {
            'version': 1,
            'sn': 1234567,
            'info': string,
            'signature': base64_encode(signature)
        }
        Common.ca = dimp.CertificateAuthority(ca)
        print_ca(Common.ca)

        self.assertTrue(Common.ca.verify(moki.publicKey))


class TransceiverTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\n================ %s' % cls)

        id1 = dimp.ID(moki_id)
        sk1 = dimp.PrivateKey(moki_sk)
        user1 = dimp.User(identifier=id1, private_key=sk1)
        Common.users[id1] = user1

        id2 = dimp.ID(hulk_id)
        sk2 = dimp.PrivateKey(hulk_sk)
        user2 = dimp.User(identifier=id2, private_key=sk2)
        Common.users[id2] = user2

        Common.common = Common()

    def test_password(self):
        print('\n---------------- %s' % self)

        key = reliable_message['key']
        print('key: ', key)
        data = base64_decode(key)
        data = hulk.privateKey.decrypt(data)
        print('key: ', data)

        key = json_dict(data)
        password = dimp.SymmetricKey(key)
        # password.pop('iv')
        print('password: ', password)

        data = hulk.publicKey.encrypt(json_str(password).encode('utf-8'))
        print('key data: ', base64_encode(data))

        Common.common.save_symmetric_key(password=password, receiver=hulk.identifier)

    def test_trans(self):
        print('\n---------------- %s' % self)

        trans = dimp.Transceiver(account=moki, private_key=moki.privateKey,
                                 barrack=Common.common, store=Common.common)
        Common.transceiver = trans

        content = dimp.Content(text_content)
        print(content)

        msg_i1 = dimp.InstantMessage.new(content=content,
                                         sender=moki.identifier,
                                         receiver=hulk.identifier,
                                         time=1545405083)
        print_msg(msg_i1)

        msg_s1 = trans.encrypt(msg_i1)
        print_msg(msg_s1)

        msg_r1 = trans.sign(msg_s1)
        print_msg(msg_r1)

        trans = dimp.Transceiver(account=hulk, private_key=hulk.privateKey,
                                 barrack=Common.common, store=Common.common)
        Common.transceiver = trans

        msg_s2 = trans.verify(msg_r1)
        print_msg(msg_s2)

        msg_i2 = trans.decrypt(msg_s2)
        print_msg(msg_i2)

        self.assertEqual(msg_i2, msg_i1)

    def test_receive(self):
        print('\n---------------- %s' % self)

        trans = dimp.Transceiver(account=hulk, private_key=hulk.privateKey,
                                 barrack=Common.common, store=Common.common)
        Common.transceiver = trans

        r_msg = dimp.ReliableMessage(reliable_message)
        print_msg(r_msg)

        data = hulk.privateKey.decrypt(r_msg.key)
        key = dimp.SymmetricKey(json_dict(data))
        print(key)

        s_msg = trans.verify(r_msg)
        print_msg(s_msg)

        i_msg = trans.decrypt(s_msg)
        print_msg(i_msg)

        content = dimp.Content(text_content)
        print(content)

        self.assertEqual(i_msg.content, content)


class CommandTestCase(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
