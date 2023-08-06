============
Pretty upper
============


.. image:: https://img.shields.io/pypi/v/pretty_upper.svg
        :target: https://pypi.python.org/pypi/pretty_upper

.. image:: https://img.shields.io/travis/manikos/pretty_upper.svg
        :target: https://travis-ci.org/manikos/pretty_upper

.. image:: https://readthedocs.org/projects/pretty-upper/badge/?version=latest
        :target: https://pretty-upper.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Removes accents from vowels when a Greek word/sentence is all capitals


* Free software: MIT license
* Documentation: https://pretty-upper.readthedocs.io.


Features
--------

In Greek language (and in others too) there are some vowels that when are accented they have a special treatment during pronouncing the word.

The Greek language has 7 vowels: `α`, `ε`, `η`, `ι`, `ο`, `υ` and `ω` and all of them may be accented. 

The problem comes when an accented vowel gets capitalized. The accent is not removed making the all-capital word look ugly with unnecessary accents.

In Greek grammar, when a word is all-capital, all accents from vowels should be removed. Thus, making it look prettier.

The all-capital word is a common scenario in web pages, such as the navigation menu, call to action (CTA) buttons, some headings etc.

For example compare the word `ΜΕΝΟΎ` with `ΜΕΝΟΥ` (both means `menu` but former has accent on Υ and latter has not). Which is prettier for the web?

This package tries to solve this issue and remove the accent from vowels when are capitalized.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


=======
History
=======

0.1.0 (2018-03-10)
------------------

* First release on PyPI.


