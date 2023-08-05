#######
pygclip
#######

.. image:: https://travis-ci.org/brymck/pygclip.svg?branch=master
    :target: https://travis-ci.org/brymck/pygclip

:code:`pygmentize` to clipboard for macOS

This utility package is designed to send code through :code:`pygmentize` and save it as rich HTML in your macOS
clipboard. It can then be pasted easily anything accept styled HTML input like Evernote, OneNote, Gmail, etc.

.. image:: assets/screenshot.png

*****
Usage
*****

:code:`pygclip` offers a couple ways to receive code:

- From a file
- Via the standard input
- Pulling it from your clipboard

Examples below:

File
====

.. code-block:: python

    def foo():
        return 'bar'

.. code-block:: bash

    $ pygclip -s monokai -l python path/to/file.py

Standard input
==============

.. code-block:: bash

    $ pygclip -s monokai -l python
    def foo():
        bar()

Clipboard
=========

.. code-block:: bash

    $ pygclip -s monokai -l python -c
