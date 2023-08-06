folk |folk_icon|
################
|PyPI-Status| |PyPI-Versions| |Build-Status| |Codecov| |LICENCE|

Folksy experiment management for Machine Learning.

.. |folk_icon| image:: https://github.com/shaypal5/folk/blob/01a04e5941499df730cbe475b7a47434a5e2ebe7/folk.png 
   :height: 32
   :width: 32 px
   :scale: 100 %

.. code-block:: python

    # TBD

.. contents::

.. section-numbering::


Installation
============

.. code-block:: bash

  pip install folk


Basic Use
=========

``folk`` is divided into several sub-modules by functionality:



Contributing
============

Package author and current maintainer is Shay Palachy (shay.palachy@gmail.com); You are more than welcome to approach him for help. Contributions are very welcomed.

Installing for development
----------------------------

Clone:

.. code-block:: bash

  git clone git@github.com:shaypal5/folk.git


Install in development mode:

.. code-block:: bash

  cd folk
  pip install -e .


Running the tests
-----------------

To run the tests use:

.. code-block:: bash

  pip install pytest pytest-cov coverage
  cd folk
  pytest


Adding documentation
--------------------

The project is documented using the `numpy docstring conventions`_, which were chosen as they are perhaps the most widely-spread conventions that are both supported by common tools such as Sphinx and result in human-readable docstrings. When documenting code you add to this project, follow `these conventions`_.

.. _`numpy docstring conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
.. _`these conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

Additionally, if you update this ``README.rst`` file,  use ``python setup.py checkdocs`` (or ``pipenv run`` the same command) to validate it compiles.


Credits
=======

Created by Shay Palachy (shay.palachy@gmail.com).


.. |PyPI-Status| image:: https://img.shields.io/pypi/v/folk.svg
  :target: https://pypi.python.org/pypi/folk

.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/folk.svg
   :target: https://pypi.python.org/pypi/folk

.. |Build-Status| image:: https://travis-ci.org/shaypal5/folk.svg?branch=master
  :target: https://travis-ci.org/shaypal5/folk

.. |LICENCE| image:: https://img.shields.io/github/license/shaypal5/folk.svg
  :target: https://github.com/shaypal5/folk/blob/master/LICENSE

.. |Codecov| image:: https://codecov.io/github/shaypal5/folk/coverage.svg?branch=master
   :target: https://codecov.io/github/shaypal5/folk?branch=master
