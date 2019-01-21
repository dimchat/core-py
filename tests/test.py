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

import dimp
from dkd.transform import json_str


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


class Common:

    issuer = None
    subject = None
    validity = None
    key = None

    info = None
    ca = None


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



if __name__ == '__main__':
    unittest.main()
