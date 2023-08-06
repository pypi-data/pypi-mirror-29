jeeves-deepspeech
=================

WIP

.. image:: https://badge.fury.io/py/jeeves-deepspeech.png
    :target: https://badge.fury.io/py/jeeves-deepspeech

.. image:: https://travis-ci.org/narfman0/jeeves-deepspeech.png?branch=master
    :target: https://travis-ci.org/narfman0/jeeves-deepspeech

DeepSpeech STT plugin for jeeves

Installation
------------

Install via pip::

    pip install jeeves-deepspeech

Development
-----------

Install all the testing requirements::

    pip install -r requirements_test.txt

Run tox to ensure everything works::

    make test

You may also invoke `tox` directly if you wish.

Release
-------

To publish your plugin to pypi, sdist and wheels are (registered,) created and uploaded with::

    make release

License
-------

Copyright (c) 2018 Jon Robison

See LICENSE for details
