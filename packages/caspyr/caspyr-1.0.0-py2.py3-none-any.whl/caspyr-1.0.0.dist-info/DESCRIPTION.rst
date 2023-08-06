caspyr
======

|PyPI-Status| |PyPI-Versions|

|LICENCE| |Donate|

Cinchingly awesome scripts of Pythonic rapture.

------------------------------------------

.. contents:: Table of contents
   :backlinks: top
   :local:


Installation
------------

Latest pypi stable release
~~~~~~~~~~~~~~~~~~~~~~~~~~

|PyPI-Status|

.. code:: sh

    pip install caspyr

Latest development release on github
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pull and install in the current directory:

.. code:: sh

    pip install -e git+https://github.com/casperdcl/caspyr.git@master#egg=caspyr

Tab completion
~~~~~~~~~~~~~~

Optionally, systems with ``bash-completion`` can install tab completion
support. The
`caspyr_completion.bash <https://raw.githubusercontent.com/casperdcl/caspyr/master/caspyr_completion.bash>`__
file needs to be copied to an appropriate folder.

On Ubuntu, the procedure would be:

.. code:: sh

    $ # Ensure completion works for `git` itself
    $ sudo apt-get install bash-completion

    $ # Install `caspyr` completions
    $ sudo wget \
        https://raw.githubusercontent.com/casperdcl/caspyr/master/caspyr_completion.bash \
        -O /etc/bash_completion.d/caspyr_completion.bash

followed by a terminal restart.


Changelog
---------

The list of all changes is available either on
`Github's Releases <https://github.com/casperdcl/caspyr/releases>`__
or on crawlers such as
`allmychanges.com <https://allmychanges.com/p/python/caspyr/>`__.

Licence
-------

Open Source (OSI approved): |LICENCE|

Copyright (c) 2016-8 Casper da Costa-Luis.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one
at `https://mozilla.org/MPL/2.0/ <https://mozilla.org/MPL/2.0/>`__.


Authors
-------

- Casper da Costa-Luis (`@casperdcl <https://github.com/casperdcl/>`__) |Donate|

|caspyr-hits|

.. |GitHub-Status| image:: https://img.shields.io/github/tag/casperdcl/caspyr.svg?maxAge=2592000
   :target: https://github.com/casperdcl/caspyr/releases
.. |PyPI-Status| image:: https://img.shields.io/pypi/v/caspyr.svg
   :target: https://pypi.python.org/pypi/caspyr
.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/caspyr.svg
   :target: https://pypi.python.org/pypi/caspyr
.. |caspyr-hits| image:: https://caspersci.uk.to/cgi-bin/hits.cgi?q=caspyr&a=hidden
.. |LICENCE| image:: https://img.shields.io/pypi/l/caspyr.svg
   :target: https://mozilla.org/MPL/2.0/
.. |Donate| image:: https://img.shields.io/badge/gift-donate-dc10ff.svg
   :target: https://caspersci.uk.to/donate.html


