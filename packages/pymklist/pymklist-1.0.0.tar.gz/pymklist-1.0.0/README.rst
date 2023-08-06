========
pymklist
========


.. image:: https://img.shields.io/pypi/v/pymklist.svg
        :target: https://pypi.python.org/pypi/pymklist

.. image:: https://img.shields.io/travis/rienafairefr/pymklist.svg
        :target: https://travis-ci.org/rienafairefr/pymklist

.. image:: https://coveralls.io/repos/github/rienafairefr/pymklist/badge.svg?branch=master
        :target: https://coveralls.io/github/rienafairefr/pymklist?branch=master


LDraw mklist in Python

Once installed with `pip install pymklist`, it should be an almost drop-in replacement for the make-list bash file found in
`https://github.com/nathaneltitane/ldraw` or the Windows executable mklist.exe found in LDraw.org complete.zip
you can start it by just doing `mklist` on the command-line.

You can instruct mklist to generate the parts.lst with a sort on the description (`--description`) or the code (`--number`),
use `mklist --help` for usage description

pymklist has been tested on Python 2.7, 3.4, 3.5 and 3.6

You can also get the parts list from Python code, just do

`from mklist.generate import get_parts_lst` and call the `get_parts_lst` function to get a list

or `from mklist.generate import generate_parts_lst` to generate a parts.lst


* Free software: GNU General Public License v3


Features
--------

* TODO
