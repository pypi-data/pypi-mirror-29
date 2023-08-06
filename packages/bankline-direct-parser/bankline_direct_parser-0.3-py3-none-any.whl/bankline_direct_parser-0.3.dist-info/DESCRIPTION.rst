Bankline Direct Parser
======================

Python module for parsing Natwest/RBS Bankline Direct Data Services files.


Requirements
------------

Only python 3.4+ supported.


Installation
------------

.. code-block:: bash

    pip install bankline-direct-parser


Usage
-----

.. code-block:: python

    from bankline_parser.data_services import parse

    # from file
    with open(filename) as f:
        parsed = parse(f)
        if parsed.is_valid():
            print(parsed.accounts[0].records[0].transaction_code)
        else:
            print(parsed.errors)

    # from list of rows
    parsed = parse(lines)


Model Layout
------------

.. code-block::

    DataServicesFile
        VolumeHeaderLabel
        [Account]
            FileHeaderLabel
            UserHeaderLabel
            [DataRecord|BalanceRecord]
            UserTrailerLabel


Development
-----------

.. image:: https://travis-ci.org/ministryofjustice/bankline-direct-parser.svg?branch=master
    :target: https://travis-ci.org/ministryofjustice/bankline-direct-parser

Please report bugs and open pull requests on `GitHub`_.

Use ``python setup.py test`` or ``tox`` to run all tests.

Distribute a new version by updating the ``version`` argument in ``setup.py:setup`` and run ``python setup.py sdist bdist_wheel upload``.


Copyright
---------

Copyright (C) 2018 HM Government (Ministry of Justice Digital Services).
See LICENSE.txt for further details.

.. _GitHub: https://github.com/ministryofjustice/bankline-direct-parser


