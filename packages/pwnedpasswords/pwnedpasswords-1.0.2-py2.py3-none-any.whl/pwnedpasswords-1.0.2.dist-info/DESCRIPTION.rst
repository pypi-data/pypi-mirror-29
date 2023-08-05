.. raw:: html

   <!--
   Copyright 2012-2018 Lionheart Software LLC

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   -->

|image0|

Python Library and CLI for the Pwned Password v2 API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|Version| |Python Versions|

Installation
------------

pwnedpasswords is available for download through the Python Package
Index (PyPi). You can install it right away using pip.

.. code:: bash

    pip install pwnedpasswords

--------------

Usage
-----

.. code:: python

    import pwnedpasswords
    password = pwnedpasswords.Password("testing 123")

    # Return the number of times `testing 123` appears in the Pwned Passwords database.
    password.check()

And that’s it! You’re done.

Notes
^^^^^

pwnedpasswords will automatically check to see if your provided input
looks like a SHA-1 hash. If it looks like plain text, it’ll
automatically hash it before sending it to the Pwned Passwords API.

If you’d like to check an already hashed password *before* providing it
as input, set the ``plain_text`` parameter when initializing the
``Password`` object. There’s not much value to doing this, since
pwnedpasswords will do this for you automatically, but it gives you just
a little extra control in case you’re feeling paranoid.

.. code:: python

    password = pwnedpasswords.Password("b8dfb080bc33fb564249e34252bf143d88fc018f")

Likewise, if a password *looks* like a SHA-1 hash, but is actually a
user-provided password, set ``plain_text`` to ``True``.

.. code:: python

    password = pwnedpasswords.Password("1231231231231231231231231231231231231231", plain_text=True)

``check``
~~~~~~~~~

This is the preferred method to call the Pwned Passwords API. By
default, the ``check`` method uses the
``https://api.pwnedpasswords.com/range/`` endpoint, which is
`k-anonymous <https://en.wikipedia.org/wiki/K-anonymity>`_.

.. code:: python

    password = pwnedpasswords.Password("username")
    password.check()
    # 8340

If you’d like to force pwnedpasswords to use the search endpoint instead
(https://api.pwnedpasswords.com/pwnedpassword/), set the ``anonymous``
parameter to ``False``.

.. code:: python

    password = pwnedpasswords.Password("password")
    password.check(anonymous=False)
    # 3303003

You might want to do this if you’d prefer faster response times, and
aren’t that worried about leaking passwords you’re searching for over
the network.

Lower-level Usage
-----------------

If you’d like direct access to the search and range endpoints, you can
call them directly.

``search``
~~~~~~~~~~

.. code:: python

    password = pwnedpasswords.Password("testing 123")
    password.search()
    # outputs 1

``range``
~~~~~~~~~

.. code:: python

    password = pwnedpasswords.Password("098765")
    password.range()
    # outputs a dictionary mapping SHA-1 hash suffixes to frequency counts

Command Line Utility
--------------------

pwnedpasswords comes bundled with a handy command line utility for
checking passwords against the Pwned Passwords database.

.. code:: bash

    $ pwnedpasswords 123456password
    240

The output is simply the number of entries returned from the Pwned
Passwords database.

If you’d like to use the CLI in a script, pwnedpasswords returns an exit
code equal to the base-10 log of the result count, plus 1. If there are
no matches in the API, the exit status will be ``0``.

If you’d like to take a look under the hood to make sure things are
working as they should, set the ``--verbose`` flag.

.. code:: bash

    $ pwnedpasswords 123456password --verbose
    INFO:pwnedpasswords.pwnedpasswords:https://api.pwnedpasswords.com/range/5052C
    INFO:pwnedpasswords.pwnedpasswords:Entry found
    240

Support/Questions
-----------------

Please file an issue in GitHub if you run into any issues, or would like
to contribute. Thanks!

License
-------

Apache License, Version 2.0. See `LICENSE <https://github.com/lionheart/pwnedpasswords/blob/master/LICENSE>`_ for details.

.. |image0| image:: meta/repo-banner.png
.. |Version| image:: https://img.shields.io/pypi/v/pwnedpasswords.svg?style=flat
   :target: https://github.com/lionheart/pwnedpasswords/blob/master/https://pypi.python.org/pypi/pwnedpasswords
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/pwnedpasswords.svg?style=flat
   :target: https://github.com/lionheart/pwnedpasswords/blob/master/https://pypi.python.org/pypi/pwnedpasswords


