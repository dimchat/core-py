# -*- coding: utf-8 -*-

from dimp import *

text_content = {
    'sn': 412968873,
    'text': 'Hey guy!',
    'type': 1
}
text_content = TextContent(text_content)

reliable_message = {
    'sender': "moki@4WDfe3zZ4T7opFSi3iDAKiuTnUHjxmXekk",
    'receiver': "hulk@4YeVEN3aUnvC1DNUufCq1bs9zoBSJTzVEj",
    'time': 1545405083,

    'data': "9cjCKG99ULCCxbL2mkc/MgF1saeRqJaCc+S12+HCqmsuF7TWK61EwTQW"
            "ZSKskUeF",
    'key': "WH/wAcu+HfpaLq+vRblNnYufkyjTm4FgYyzW3wBDeRtXs1TeDmRxKVu7"
           "nQI/sdIALGLXrY+O5mlRfhU8f8TuIBilZUlX/eIUpL4uSDYKVLaRG9pO"
           "crCHKevjUpId9x/8KBEiMIL5LB0Vo7sKrvrqosCnIgNfHbXMKvMzwcqZ"
           "EU8=",
    'signature': "Yo+hchWsQlWHtc8iMGS7jpn/i9pOLNq0E3dTNsx80QdBboTLeKoJYAg/"
                 "lI+kZL+g7oWJYpD4qKemOwzI+9pxdMuZmPycG+0/VM3HVSMcguEOqOH9"
                 "SElp/fYVnm4aSjAJk2vBpARzMT0aRNp/jTFLawmMDuIlgWhBfXvH7bT7"
                 "rDI="
}
reliable_message = ReliableMessage(reliable_message)
