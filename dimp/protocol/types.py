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


def i2s(value: int) -> str:
    return '%d' % value


class MetaType:
    """
        @enum MKMMetaVersion

        @abstract Defined for algorithm that generating address.

        @discussion Generate and check ID/Address

            MKMMetaVersion_MKM give a seed string first, and sign this seed to get
            fingerprint; after that, use the fingerprint to generate address.
            This will get a firmly relationship between (username, address and key).

            MKMMetaVersion_BTC use the key data to generate address directly.
            This can build a BTC address for the entity ID (no username).

            MKMMetaVersion_ExBTC use the key data to generate address directly, and
            sign the seed to get fingerprint (just for binding username and key).
            This can build a BTC address, and bind a username to the entity ID.

        Bits:
            0000 0001 - this meta contains seed as ID.name
            0000 0010 - this meta generate BTC address
            0000 0100 - this meta generate ETH address
            ...
    """

    DEFAULT = i2s(0x01)
    MKM = i2s(0x01)      # 0000 0001: username@address

    # Bitcoin
    BTC = i2s(0x02)      # 0000 0010: btc_address
    ExBTC = i2s(0x03)    # 0000 0011: username@btc_address (RESERVED)

    # Ethereum
    ETH = i2s(0x04)      # 0000 0100: eth_address
    ExETH = i2s(0x05)    # 0000 0101: username@eth_address (RESERVED)

    # ...


class DocumentType:

    VISA = 'visa'          # for user info (communicate key)

    PROFILE = 'profile'    # for user profile (reserved)

    BULLETIN = 'bulletin'  # for group info (owner, administrators and assistants)


class ContentType:
    """
        @enum DKDContentType

        @abstract A flag to indicate what kind of message content this is.

        @discussion A message is something send from one place to another one,
            it can be an instant message, a system command, or something else.

            DKDContentType_Text indicates this is a normal message with plaintext.

            DKDContentType_File indicates this is a file, it may include filename
            and file data, but usually the file data will encrypted and upload to
            somewhere and here is just a URL to retrieve it.

            DKDContentType_Image indicates this is an image, it may send the image
            data directly(encrypt the image data with Base64), but we suggest to
            include a URL for this image just like the 'File' message, of course
            you can get a snapshot of this image here.

            DKDContentType_Audio indicates this is a voice message, you can get
            a URL to retrieve the voice data just like the 'File' message.

            DKDContentType_Video indicates this is a video file.

            DKDContentType_Page indicates this is a web page.

            DKDContentType_Quote indicates this message has quoted another message
            and the message content should be a plaintext.

            DKDContentType_Command indicates this is a command message.

            DKDContentType_Forward indicates here contains a TOP-SECRET message
            which needs your help to redirect it to the true receiver.

        Bits:
            0000 0001 - this message contains plaintext you can read.
            0000 0010 - this is a message you can see.
            0000 0100 - this is a message you can hear.
            0000 1000 - this is a message for the bot, not for human.

            0001 0000 - this message's main part is in somewhere else.
            0010 0000 - this message contains the 3rd party content.
            0100 0000 - this message contains digital assets
            1000 0000 - this is a message send by the system, not human.

            (All above are just some advices to help choosing numbers :P)
    """

    ANY = i2s(0x00)        # 0000 0000 (Undefined)

    TEXT = i2s(0x01)       # 0000 0001

    FILE = i2s(0x10)       # 0001 0000
    IMAGE = i2s(0x12)      # 0001 0010
    AUDIO = i2s(0x14)      # 0001 0100
    VIDEO = i2s(0x16)      # 0001 0110

    # Web Page
    PAGE = i2s(0x20)       # 0010 0000

    # Name Card
    NAME_CARD = i2s(0x33)  # 0011 0011

    # Quote a message before and reply it with text
    QUOTE = i2s(0x37)      # 0011 0111

    MONEY = i2s(0x40)          # 0100 0000
    TRANSFER = i2s(0x41)       # 0100 0001
    LUCKY_MONEY = i2s(0x42)    # 0100 0010
    CLAIM_PAYMENT = i2s(0x48)  # 0100 1000 (Claim for Payment)
    SPLIT_BILL = i2s(0x49)     # 0100 1001 (Split the Bill)

    COMMAND = i2s(0x88)        # 1000 1000
    HISTORY = i2s(0x89)        # 1000 1001 (Entity History Command)

    # Application Customized
    APPLICATION = i2s(0xA0)       # 1010 0000 (Application 0nly, Reserved)
    # APPLICATION_1 = i2s(0xA1)   # 1010 0001 (Reserved)
    # ...                         # 1010 ???? (Reserved)
    # APPLICATION_15 = i2s(0xAF)  # 1010 1111 (Reserved)

    # CUSTOMIZED_0 = i2s(0xC0)    # 1100 0000 (Reserved)
    # CUSTOMIZED_1 = i2s(0xC1)    # 1100 0001 (Reserved)
    # ...                         # 1100 ???? (Reserved)
    ARRAY = i2s(0xCA)             # 1100 1010 (Content Array)
    # ...                         # 1100 ???? (Reserved)
    CUSTOMIZED = i2s(0xCC)        # 1100 1100 (Customized Content)
    # ...                         # 1100 ???? (Reserved)
    COMBINE_FORWARD = i2s(0xCF)   # 1100 1111 (Combine and Forward)

    # Top-Secret message forward by proxy (MTA)
    FORWARD = i2s(0xFF)           # 1111 1111
