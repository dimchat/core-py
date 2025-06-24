# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

from typing import Optional, Any, Dict

from mkm import ID

from ..protocol import ContentType
from ..protocol import MoneyContent, TransferContent

from .base import BaseContent


class BaseMoneyContent(BaseContent, MoneyContent):
    """
        Money Message Content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x40),
            sn   : 123,

            currency : "RMB", // USD, USDT, ...
            amount   : 100.00
        }
    """

    def __init__(self, content: Dict[str, Any] = None,
                 msg_type: str = None,
                 currency: str = None, amount: float = None):
        if content is None:
            # 1. new content with type, currency & amount
            assert currency is not None and amount is not None, \
                'money content error: %s, %s, %s' % (msg_type, currency, amount)
            if msg_type is None:
                msg_type = ContentType.MONEY
            super().__init__(None, msg_type)
            # set values to inner dictionary
            self['currency'] = currency
            self['amount'] = amount
        else:
            # 2. content info from network
            assert msg_type is None and currency is None and amount is None,\
                'params error: %s, %s, %s, %s' % (content, msg_type, currency, amount)
            super().__init__(content=content)

    @property  # Override
    def currency(self) -> str:
        return self.get_str(key='currency', default='')

    @property  # Override
    def amount(self) -> float:
        return self.get_float(key='amount', default=0.0)

    @amount.setter  # Override
    def amount(self, value: float):
        self['amount'] = value


class TransferMoneyContent(BaseMoneyContent, TransferContent):
    """
        Transfer Money Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x41),
            sn   : 123,

            currency : "RMB",    // USD, USDT, ...
            amount   : 100.00,
            remitter : "{FROM}", // sender ID
            remittee : "{TO}"    // receiver ID
        }
    """

    def __init__(self, content: Dict[str, Any] = None,
                 currency: str = None, amount: float = None):
        msg_type = ContentType.TRANSFER if content is None else None
        super().__init__(content, msg_type, currency=currency, amount=amount)

    @property  # Override
    def remitter(self) -> Optional[ID]:
        sender = self.get('remitter')
        return ID.parse(identifier=sender)

    @remitter.setter  # Override
    def remitter(self, sender: Optional[ID]):
        self.set_string(key='remitter', value=sender)

    @property  # Override
    def remittee(self) -> Optional[ID]:
        receiver = self.get('remittee')
        return ID.parse(identifier=receiver)

    @remittee.setter  # Override
    def remittee(self, receiver: Optional[ID]):
        self.set_string(key='remittee', value=receiver)
