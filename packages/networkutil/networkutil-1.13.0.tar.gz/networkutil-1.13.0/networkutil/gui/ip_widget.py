# encoding: utf-8

from uiutil.widget.entry import TextEntry
from ..validation import valid_ip, valid_ip_network


class IPEntry(TextEntry):
    DEFAULT_VALUE = u'0.0.0.0'
    VALID_CHARACTERS = u'0123456789ABCDEFabcdef:'

    def __init__(self,
                 *args,
                 **kwargs):

        super(IPEntry, self).__init__(*args,
                                      **kwargs)

    @staticmethod
    def valid(value):
        return valid_ip(value)

    @staticmethod
    def permit_invalid_value(value):
        return len([c for c in value if c not in IPEntry.VALID_CHARACTERS]) == 0


class IPNetworkEntry(TextEntry):
    DEFAULT_VALUE = u'0.0.0.0'
    VALID_CHARACTERS = u'0123456789ABCDEFabcdef:/'

    def __init__(self,
                 strict=True,
                 *args,
                 **kwargs):

        self.strict = strict

        super(IPNetworkEntry, self).__init__(*args,
                                             **kwargs)

    def valid(self,
              value):
        return valid_ip_network(value,
                                strict=self.strict)

    @staticmethod
    def permit_invalid_value(value):
        return len([c for c in value if c not in IPNetworkEntry.VALID_CHARACTERS]) == 0
