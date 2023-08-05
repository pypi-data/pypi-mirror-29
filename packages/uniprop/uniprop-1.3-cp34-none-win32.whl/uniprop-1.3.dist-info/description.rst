Summary
-------

This module reports the Unicode properties of codepoints, beyond what Python's ``unicodedata`` module provides.


Unicode
-------

This module supports Unicode 10.0.



Examples
--------

  .. sourcecode:: python

    >>> import uniprop
    >>> uniprop.script('A')
    'Latin'
    >>> uniprop.script('\N{GREEK SMALL LETTER ALPHA}')
    'Greek'
    >>> uniprop.block('A')
    'Basic_Latin'
    >>> uniprop.block('\N{GREEK SMALL LETTER ALPHA}')
    'Greek_And_Coptic'
    >>> uniprop.numeric_value('\N{VULGAR FRACTION ONE THIRD}')
    '1/3'
    >>> uniprop.numeric_value('A')
    'NaN'
    >>> uniprop.numeric_type('\N{VULGAR FRACTION ONE THIRD}')
    'Numeric'
    >>> uniprop.numeric_type('A')
    'None'

Please note that all of the results are strings. This differs from the ``unicodedata`` module where ``numeric_value`` returns a float.
