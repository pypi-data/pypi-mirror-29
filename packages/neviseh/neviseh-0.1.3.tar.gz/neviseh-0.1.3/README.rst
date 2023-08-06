Neviseh
=======

.. image:: https://travis-ci.org/meyt/neviseh.svg?branch=master
    :target: https://travis-ci.org/meyt/neviseh

.. image:: https://coveralls.io/repos/github/meyt/neviseh/badge.svg?branch=master
    :target: https://coveralls.io/github/meyt/neviseh?branch=master

Simple text processing tools in persian.


Features
--------

- Text normalization
- Keyboard layout mapping translation
- Calendar translation


Usage
-----

Currently we have two base modules for English and Persian texts,
each of these modules contains chaining-methods that apply on
initial value.

Example:

.. code:: python

    from neviseh import PersianText
    print(str(
        PersianText('123').translate_latin_numbers()
    ))
    # output: ۱۲۳

    print(str(
        PersianText('123.45').replace_decimal_dots().translate_latin_numbers()
    ))
    # output: ۱۲۳٫۴۵

for complete samples look tests.

TODO:
-----

- Affix spacing (`more <https://github.com/sobhe/hazm/blob/2971829c80bf9f253be2b37974dd0435f06e2a24/hazm/Normalizer.py#L65>`__)
- Calendar month names translation

.. - Normalize nowadays style using on social networks (like: خـٍـٍـٍـٍـٍْـٍْـٍْـٍْـٍْـٍـٍـٍـٍـٍورشیـב) (`more <https://github.com/sobhe/hazm/issues/117>`__)


Related projects
----------------

- `Hazm <https://github.com/sobhe/hazm>`__
- `persian.js <https://github.com/usablica/persian.js>`__
- `persianize.js <https://github.com/opencafe/persianize-node>`__
