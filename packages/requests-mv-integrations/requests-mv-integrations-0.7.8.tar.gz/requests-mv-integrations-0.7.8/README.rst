.. -*- mode: rst -*-

requests-mv-integrations
------------------------

Extension of Python HTTP `requests <https://pypi.python.org/pypi/requests>`_ with verbose
logging using `logging-mv-integrations <https://pypi.python.org/pypi/logging-mv-integrations>`_.


Badges
------

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs| |license|
    * - info
      - |hits| |contributors|
    * - tests
      - |travis| |coveralls|
    * - package
      - |version| |supported-versions|
    * - other
      - |requires|


.. |docs| image:: https://readthedocs.org/projects/requests-mv-integrations/badge/?style=flat
    :alt: Documentation Status
    :target: http://requests-mv-integrations.readthedocs.io

.. |hits| image:: http://hits.dwyl.io/TuneLab/requests-mv-integrations.svg
    :alt: Hit Count
    :target: http://hits.dwyl.io/TuneLab/requests-mv-integrations

.. |contributors| image:: https://img.shields.io/github/contributors/TuneLab/requests-mv-integrations.svg
    :alt: Contributors
    :target: https://github.com/TuneLab/requests-mv-integrations/graphs/contributors

.. |license| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :alt: License Status
    :target: https://opensource.org/licenses/MIT

.. |travis| image:: https://travis-ci.org/TuneLab/requests-mv-integrations.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/TuneLab/requests-mv-integrations

.. |coveralls| image:: https://coveralls.io/repos/TuneLab/requests-mv-integrations/badge.svg?branch=master&service=github
    :alt: Code Coverage Status
    :target: https://coveralls.io/r/TuneLab/requests-mv-integrations

.. |requires| image:: https://requires.io/github/TuneLab/requests-mv-integrations/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/TuneLab/requests-mv-integrations/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/requests_mv_integrations.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/requests_mv_integrations

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/requests-mv-integrations.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/requests-mv-integrations

.. end-badges


Install
-------

.. code-block:: bash

    pip install requests_mv_integrations


Architecture
------------

``requests-mv-integrations`` is an extension of the `Python package requests <https://pypi.python.org/pypi/requests>`_
and it is used for TUNE Multiverse Integrations for handling all HTTP requests including APIs in REST and SOAP,
screen scrapping, and handling response downloads in JSON, XML, and CSV.

.. image:: ./images/requests_mv_integrations.png
   :scale: 50 %
   :alt: UML requests-mv-integrations


Usage
-----

.. code-block:: python

    URL_TUNE_MAT_API_COUNTRIES = \
        'https://api.mobileapptracking.com/v2/countries/find.json'

    from requests_mv_integrations import (
        RequestMvIntegrationDownload,
    )
    request_download = RequestMvIntegrationDownload(logger_level=logging.DEBUG)

    result = \
        request_download.request(
            request_method='GET',
            request_url=URL_TUNE_MAT_API_COUNTRIES,
            request_params=None,
            request_retry=None,
            request_headers=HEADER_CONTENT_TYPE_APP_JSON,
            request_label="TMC Countries"
        )

    json_tune_mat_countries = result.json()

    pprint(json_tune_mat_countries)


Example
^^^^^^^

.. code-block:: bash

    $ python3 examples/example_request.py

    {
        "asctime": "2017-10-13 12:02:53 -0700",
        "levelname": "INFO",
        "name": "__main__",
        "version": "00.05.04",
        "message": "Start"
    }
    {
        "asctime": "2017-10-13 12:02:53 -0700",
        "levelname": "DEBUG",
        "name": "requests_mv_integrations",
        "version": "00.05.04",
        "message": "TMC Countries: Start"
    }
    ...
    {
        "asctime": "2017-10-13 12:02:53 -0700",
        "levelname": "DEBUG",
        "name": "requests_mv_integrations",
        "version": "00.05.04",
        "message": "TMC Countries: Details",
        "request_data": "",
        "request_headers": {
            "Content-Type": "application/json",
            "User-Agent": "(requests-mv-integrations/00.05.04, Python/3.6.2)"},
            "request_label": "TMC Countries",
            "request_method": "GET",
            "request_params": {},
            "request_url": "https://api.mobileapptracking.com/v2/countries/find.json",
            "timeout": 60
    }
    {
        "asctime": "2017-10-13 12:02:53 -0700",
        "levelname": "DEBUG",
        "name": "requests_mv_integrations",
        "version": "00.05.04",
        "message": "TMC Countries: Curl",
        "request_curl": "curl --verbose
            -X GET
            -H 'Content-Type: application/json'
            -H 'User-Agent: (requests-mv-integrations/00.05.04, Python/3.6.2)'
            --connect-timeout 60
            -L 'https://api.mobileapptracking.com/v2/countries/find.json'",
        "request_label": "TMC Countries",
        "request_method": "GET"
    }
    ...
    {
        'data': [
            {'id': 0, 'name': 'International (Generic)'},
            {'id': 4, 'name': 'Afghanistan'},
            {'id': 8, 'name': 'Albania'},
            {'id': 10, 'name': 'Antarctica'},
            {'id': 12, 'name': 'Algeria'},
            {'id': 16, 'name': 'American Samoa'},
            {'id': 20, 'name': 'Andorra'},
            {'id': 24, 'name': 'Angola'},
            {'id': 28, 'name': 'Antigua And Barbuda'},
            {'id': 31, 'name': 'Azerbaijan'},
        ],
        'response_size': '845',
        'status_code': 200,
    }


Classes
-------

- ``class RequestMvIntegration`` -- Base class using `requests <https://pypi.python.org/pypi/requests>`_ with retry functionality and verbose logging.
- ``class RequestMvIntegrationDownload`` -- Download file handling.
- ``class RequestMvIntegrationUpload`` -- Upload file handling.

Requirements
------------

``requests-mv-integrations`` module is built upon Python 3 and has dependencies upon
several Python modules available within `Python Package Index PyPI <https://pypi.python.org/pypi>`_.

.. code-block:: bash

    make install

or

.. code-block:: bash

    python3 -m pip uninstall --yes --no-input -r requirements.txt
    python3 -m pip install --upgrade -r requirements.txt


Packages
^^^^^^^^

- **beautifulsoup4**: https://pypi.python.org/pypi/beautifulsoup4
- **deepdiff**: https://pypi.python.org/pypi/deepdiff
- **logging-mv-integrations**: https://pypi.python.org/pypi/logging-mv-integrations
- **pyhttpstatus-utils**: https://pypi.python.org/pypi/pyhttpstatus-utils
- **requests**: https://pypi.python.org/pypi/requests
- **safe-cast**: https://pypi.python.org/pypi/safe-cast
