# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2021 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2021 Albert Moky
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

from typing import Optional, Union, Any, Dict

from mkm import ID
from dkd import ContentType, BaseContent

from ..protocol import MoneyContent, TransferContent


class BaseMoneyContent(BaseContent, MoneyContent):
    """
        Money Message Content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x40,
            sn   : 123,

            currency : "RMB", // USD, USDT, ...
            amount   : 100.00
        }
    """

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 msg_type: Union[int, ContentType] = 0,
                 currency: Optional[str] = None, amount: Optional[float] = 0.0):
        if content is None and msg_type == 0:
            msg_type = ContentType.MONEY
        super().__init__(content=content, msg_type=msg_type)
        # set values to inner dictionary
        if currency is not None:
            self['currency'] = currency
        if amount > 0:
            self['amount'] = amount

    @property  # Override
    def currency(self) -> str:
        return self.get('currency')

    @property  # Override
    def amount(self) -> float:
        value = self.get('amount')
        return 0 if value is None else float(value)

    @amount.setter  # Override
    def amount(self, value: float):
        self['amount'] = value


class TransferMoneyContent(BaseMoneyContent, TransferContent):
    """
        Transfer Money Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x41,
            sn   : 123,

            currency : "RMB",    // USD, USDT, ...
            amount   : 100.00,
            remitter : "{FROM}", // sender ID
            remittee : "{TO}"    // receiver ID
        }
    """

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 currency: Optional[str] = None, amount: Optional[float] = 0.0):
        super().__init__(content=content, msg_type=ContentType.TRANSFER, currency=currency, amount=amount)

    @property  # Override
    def remitter(self) -> Optional[ID]:
        sender = self.get('remitter')
        return ID.parse(identifier=sender)

    @remitter.setter  # Override
    def remitter(self, sender: Optional[ID]):
        if sender is None:
            self.pop('remitter', None)
        else:
            self['remitter'] = str(sender)

    @property  # Override
    def remittee(self) -> Optional[ID]:
        receiver = self.get('remittee')
        return ID.parse(identifier=receiver)

    @remittee.setter  # Override
    def remittee(self, receiver: Optional[ID]):
        if receiver is None:
            self.pop('remittee', None)
        else:
            self['remittee'] = str(receiver)
