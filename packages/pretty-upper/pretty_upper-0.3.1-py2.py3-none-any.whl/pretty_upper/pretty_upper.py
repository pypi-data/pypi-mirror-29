# -*- coding: utf-8 -*-

from re import sub


def validate_word(s):
    if isinstance(s, str):
        return s
    err = 'Argument should be either str or unicode. Argument\'s type is "%s".'
    raise TypeError(err % s.__class__.__name__)


def pu(word):
    """
    Removes accent from the given word or phrase.

    If word is not an instance of str or unicode, raise TypeError.

    This is applied ONLY for the Greek language where when any small
    accented vowel (ά, έ, ή, ί, ό, ύ, ώ) is capitalized, the accent
    remains making it look ugly.

    Example: ΚΑΛΗΜΈΡΑ instead of ΚΑΛΗΜΕΡΑ

                        REPLACEMENT TABLE
    ------------------------------------------------------------
    Small GR letter |  Unicode  |  Small GR letter  |  Unicode
     (with accent)  |           |     (wo accent)   |
    ------------------------------------------------------------
           ά        |  U+03AC   |         α         |   U+03B1
           έ        |  U+03AD   |         ε         |   U+03B5
           ή        |  U+03AE   |         η         |   U+03B7
           ί        |  U+03AF   |         ι         |   U+03B9
           ό        |  U+03CC   |         ο         |   U+03BF
           ύ        |  U+03CD   |         υ         |   U+03C5
           ώ        |  U+03CE   |         ω         |   U+03C9
    """
    if not isinstance(word, str):
        err = 'Argument should be either str or unicode. ' \
              'Argument\'s type is "%s".'
        raise TypeError(err % word.__class__.__name__)
    replacement_table = {  # Greek lower vowels
                           u'ά': u'α',
                           u'έ': u'ε',
                           u'ή': u'η',
                           u'ί': u'ι',
                           u'ό': u'ο',
                           u'ύ': u'υ',
                           u'ώ': u'ω',
                           # Greek upper vowels
                           u'Ά': u'Α',
                           u'Έ': u'Ε',
                           u'Ή': u'Η',
                           u'Ί': u'Ι',
                           u'Ό': u'Ο',
                           u'Ύ': u'Υ',
                           u'Ώ': u'Ω',
    }
    for letter in replacement_table:
        word = sub(letter, replacement_table.get(letter), word)
    return word.upper()
