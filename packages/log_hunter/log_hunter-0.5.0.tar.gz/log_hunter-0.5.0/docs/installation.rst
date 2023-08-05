.. highlight:: shell

============
Installation
============


Stable release
--------------

To install Hunter Log File Access, run this command in your terminal:

.. code-block:: console

    $ pip install log_hunter

Note: on OSX you have to install openssl with homebrew and specify the library location
for the cryptography library to compile.

.. code-block:: console

    $ brew install openssl
    $ pip install log_hunter --global-option=build_ext --global-option="-L/usr/local/opt/openssl/lib" --global-option="-I/usr/local/opt/openssl/include"


This is the preferred method to install Hunter Log File Access, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

From sources
------------

The sources for Hunter Log File Access can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/ptillemans/log_hunter

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://gitlab.melexis.com/cbs/log_hunter


Configuration
-------------

The username password needs to be set in the *.netrc* file in your home folder. Add the following snippet
to the file:

.. code-block:: console

    machine hunter.melexis.com
      login sammy
      password YyTouN6dKbb2Mf


This will allow access to hunter.

