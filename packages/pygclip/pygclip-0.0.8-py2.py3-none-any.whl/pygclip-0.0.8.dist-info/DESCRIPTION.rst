#######
pygclip
#######

.. image:: https://travis-ci.org/brymck/pygclip.svg?branch=master
    :target: https://travis-ci.org/brymck/pygclip

:code:`pygmentize` to clipboard for macOS

This utility package is designed to send code through :code:`pygmentize` and save it as rich HTML in your macOS
clipboard. It can then be pasted easily into anything that accepts styled HTML input, such as Evernote, OneNote, Gmail,
etc.

.. image:: https://github.com/brymck/pygclip/raw/master/assets/screenshot.png

*****
Usage
*****

:code:`pygclip` offers a couple ways to retrieve code for passing on to :code:`pygmentize`:

- From a file
- Via the standard input
- Pulling it from your clipboard

Examples below:

File
====

.. code-block:: bash

    $ cat path/to/file.py
    def foo():
        return 'bar'
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

    $ echo "def foo():\n    return 'bar'" | pbcopy
    $ pygclip -s monokai -l python -c


