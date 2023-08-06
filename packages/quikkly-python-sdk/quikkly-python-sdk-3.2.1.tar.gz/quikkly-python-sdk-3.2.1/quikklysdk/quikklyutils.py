"""High-level interface to the Quikkly Python SDK.
"""
from __future__ import absolute_import, division

import argparse
import six


ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def int_to_alphanumeric(x, alphabet=ALPHABET):
    assert len(set(alphabet)) == len(alphabet), 'Duplicate characters in alphabet'
    assert isinstance(x, six.integer_types), 'Number must be integer'
    assert x >= 0, 'Number must be positive'
    base = len(alphabet)

    if x == 0:
        return alphabet[0]
    else:
        text = ''
        while x > 0:
            digit = x % base
            text += alphabet[digit]
            x //= base
        return text[::-1]  # Reverse


def alphanumeric_to_int(text, alphabet=ALPHABET):
    assert len(set(alphabet)) == len(alphabet), 'Duplicate characters in alphabet'
    assert text, 'Text must be provided'
    base = len(alphabet)
    x = 0
    for char in text:
        if char not in alphabet:
            raise ValueError('Unexpected character "%s" for alphabet %s' % (char, alphabet))
        x *= base
        x += alphabet.index(char)
    return x


def parse_hex(value):
    if not value:
        raise argparse.ArgumentTypeError('Hex number not provided')
    if value.startswith('0x'):
        value = value[2:]
    try:
        return int(value, base=16)
    except ValueError:
        raise argparse.ArgumentTypeError('Not a valid hex number.')


def parse_alnum(value):
    if not value:
        raise argparse.ArgumentTypeError('Alphanumeric string not provided')
    try:
        return alphanumeric_to_int(value)
    except ValueError:
        raise argparse.ArgumentTypeError('Not a valid a-zA-Z0-9 alphanumeric string.')
