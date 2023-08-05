
Primed Toolkit
==============


.. image:: https://travis-ci.org/eyb1/primed.svg?branch=master
   :target: https://travis-ci.org/eyb1/primed
   :alt: Build Status

.. image:: https://coveralls.io/repos/github/eyb1/primed/badge.svg?branch=master
   :target: https://coveralls.io/github/eyb1/primed?branch=master
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/primed/badge/?version=latest
   :target: http://primed.readthedocs.io/?badge=latest
   :alt: Documentation Status

.. image:: https://requires.io/github/eyb1/primed/requirements.svg?branch=master
   :target: https://requires.io/github/eyb1/primed/requirements/?branch=master
   :alt: Requirements Status

.. image:: https://badge.fury.io/py/primed.svg
   :target: https://badge.fury.io/py/primed
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/l/primed.svg
   :target: https://pypi.python.org/pypi/primed/
   :alt: PyPI license


General utility and NLP functions. Currently under development, so use at your own risk. Tests and thorough documentation will be added at some point (meaning probably never, but I will bear it in mind).

Installation
------------

Simply use ``pip``\ :

.. code-block:: bash

   pip install primed --upgrade

Then, import the module:

.. code-block:: python

   import primed as ptk

NLP Examples
------------

Text should ideally be cleaned first (i.e. free of punctuation). You can use ``ptk.clean()``.

Clean text
^^^^^^^^^^

Removes extra spaces, punctuation, and optionally lowers the text. Careful using this if parsing for names, countries, smileys etc.

.. code-block:: python

   ptk.clean('Ha, this   is fun! YUP!!!', lower=True)

Case-insensitive replace
^^^^^^^^^^^^^^^^^^^^^^^^

Possibly the fastest method for a case-insensitive replace, tested against both using an arrayed string and using ``re``.

.. code-block:: python

   ptk.ireplace('I want a hIPpo for my birthday', 'hippo', 'giraffe')

Get all (x to y) grams
^^^^^^^^^^^^^^^^^^^^^^

Returns a dictionary of the ngrams with counts. Possibly the fastest method when compared with ``itertools``\ , ``textblob``\ , ``sklearn``\ , and ``nltk``.

.. code-block:: python

   ptk.ngrams('I love cats meow like really really love cats', min_grams=1, max_grams=10)

Create a comma-separated string using the Oxford comma
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Because this is the grammatically correct way...

.. code-block:: python

   ptk.oxfordize(['cats', 'kittens', 'quantum', 'simulation'])

Capitalize i's
^^^^^^^^^^^^^^

Pretty elementary implementation, included just in case.

.. code-block:: python

   ptk.capi('i am british, and i also codify things.')

Correct a / an select
^^^^^^^^^^^^^^^^^^^^^

Uses the Carnegie Mellon University Pronouncing Dictionary (CMUdict), based on the DoD ARPAbet. Currently uses a naive fall-back; a better alternative would be to guess / learn using existing words in CMUdict.

.. code-block:: python

   ptk.a('university')

Convert to snake text
^^^^^^^^^^^^^^^^^^^^^

Existing underscores are preserved.

.. code-block:: python

   ptk.snake('Hello  There! ')

Convert to Wikipedia URI
^^^^^^^^^^^^^^^^^^^^^^^^

Naive implementation for now, hoping redirects will help with the majority of capitalization issues for words subsequent to the first.

.. code-block:: python

   ptk.wiki_uri('DELTA-V Budget')

Utility Examples
----------------

Colourful printing
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   ptk.cprint('Text or object to be stringified', style='OK', bold=True, underline=True, newline=True)

Styles available:

.. code-block:: python

   'OK':    '\033[92m'
   'INFO':  '\033[94m'
   'WARN':  '\033[93m'
   'ERROR': '\033[91m'
   'FATAL': '\033[31m'

Notes
-----

``keeper``
^^^^^^^^^^^^^^

Using ``string.translate`` is quicker than using regular expressions (see https://stackoverflow.com/a/26517161/2178980).
