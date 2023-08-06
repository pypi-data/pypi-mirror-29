===========
Stuweparser
===========

.. image:: https://travis-ci.org/Trybnetic/stuweparser.svg?branch=master
    :target: https://travis-ci.org/Trybnetic/stuweparser?branch=master

.. image:: https://landscape.io/github/Trybnetic/stuweparser/master/landscape.svg?style=flat
   :target: https://landscape.io/github/Trybnetic/stuweparser/master

.. image:: https://coveralls.io/repos/github/Trybnetic/stuweparser/badge.svg?branch=master
    :target: https://coveralls.io/github/Trybnetic/stuweparser?branch=master

.. image:: https://img.shields.io/github/license/trybnetic/stuweparser.svg
    :target: https://github.com/trybnetic/stuweparser/blob/master/LICENSE.txt


This package contains a collection of functions to crawl and parse the website
of the `Studierendenwerk Tübingen-Hohenheim <https://www.my-stuwe.de/>`_.


Getting Started
===============
These instructions will get you a copy of the ``stuweparser`` package on your
local machine. If you only want to use ``stuweparser`` as a python package
use ``pip3`` in order to install it into your python3 environment. If you want
to inspect and change the code download and install it via ``git clone`` and
``python3 setup.py``. For details see below.


Prerequisites
-------------
You need python 3.4 or newer and git installed on your machine. We recommend to
install Minicoda (https://conda.io/miniconda.html) before installing
``stuweparser`` or to create a virtualenv within your personal folder.

Development
^^^^^^^^^^^
If you want to develop ``stuweparser`` you should additionally install:

.. code:: bash

   pip3 install --user tox pylint pytest pycodestyle sphinx


Installing
----------
If you want to use the package you can install the package by running

.. code:: bash

    git clone https://github.com/trybnetic/stuweparser.git
    cd stuweparser
    python3 setup.py install


Documentation and Examples
--------------------------
Documentation and examples can be found in the ``doc/`` folder after cloning
the repository.

If you have installed ``sphinx`` you should be able to build the documentation with:

.. code:: bash

   cd doc/
   make html

The entry point for the html documentation is ``doc/build/html/index.html``.


Running the tests
=================
If you have cloned ``stuweparser`` from github, you can start the tests by
executing the following within the outer ``stuweparser`` folder:

.. code:: bash

    py.test

For full tests you can run:

.. code:: bash

    tox -e test

For manually checking coding guidelines run:

.. code:: bash

    pycodestyle stuweparser tests
    pylint --ignore-patterns='.*\.so' --rcfile=setup.cfg -j 2 stuweparser tests

For more details on which tests run in the continuous testing environment
look at the file ``tox.ini``.


Authors
=======
See also the list of `contributors
<https://github.com/trybnetic/stuweparser/contributors>`_ who participated in
this project.


License
=======
This project is licensed under the MIT License - see the `LICENSE.txt
<https://github.com/trybnetic/stuweparser/blob/master/LICENSE.txt>`_ file for
details

Acknowledgments
===============
This package originates from python scripts written by `Steffen Lindner
<https://github.com/NE4Y>`_ in his repository `Mensa Tübingen App
<https://github.com/NE4Y/Mensa-App-Tuebingen>`_.
