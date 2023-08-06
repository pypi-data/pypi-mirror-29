# encoding: utf-8

from uiutil.widget.entry import TextEntry
from ..validation import valid_ipv6, valid_ipv6_network


class IPv6Entry(TextEntry):
    DEFAULT_VALUE = u'::'
    VALID_CHARACTERS = u'0123456789ABCDEFabcdef:'

    def __init__(self,
                 *args,
                 **kwargs):

        super(IPv6Entry, self).__init__(*args,
                                        **kwargs)

    @staticmethod
    def valid(value):
        return valid_ipv6(value)

    @staticmethod
    def permit_invalid_value(value):
        return len([c for c in value if c not in IPv6Entry.VALID_CHARACTERS]) == 0


class IPv6NetworkEntry(TextEntry):
    DEFAULT_VALUE = u'::'
    VALID_CHARACTERS = u'0123456789ABCDEFabcdef:/'

    def __init__(self,
                 strict=True,
                 *args,
                 **kwargs):

        self.strict = strict

        super(IPv6NetworkEntry, self).__init__(*args,
                                               **kwargs)

    def valid(self,
              value):
        return valid_ipv6_network(value,
                                  strict=self.strict)

    @staticmethod
    def permit_invalid_value(value):
        return len([c for c in value if c not in IPv6NetworkEntry.VALID_CHARACTERS]) == 0
