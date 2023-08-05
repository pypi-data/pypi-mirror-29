.. -*- mode: rst -*-

pyhttpstatus-utils
------------------

Extension of Python Standard Library's `http.HTTPStatus <https://docs.python.org/3/library/http.html>`_ providing mapping of HTTP statuses.

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

.. |docs| image:: https://readthedocs.org/projects/pyhttpstatus-utils/badge/?style=flat
    :alt: Documentation Status
    :target: http://pyhttpstatus-utils.readthedocs.io

.. |hits| image:: http://hits.dwyl.io/TuneLab/pyhttpstatus-utils.svg
    :alt: Hit Count
    :target: http://hits.dwyl.io/TuneLab/pyhttpstatus-utils

.. |contributors| image:: https://img.shields.io/github/contributors/TuneLab/pyhttpstatus-utils.svg
    :alt: Contributors
    :target: https://github.com/TuneLab/pyhttpstatus-utils/graphs/contributors

.. |license| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :alt: License Status
    :target: https://opensource.org/licenses/MIT

.. |travis| image:: https://travis-ci.org/TuneLab/pyhttpstatus-utils.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/TuneLab/pyhttpstatus-utils

.. |coveralls| image:: https://coveralls.io/repos/TuneLab/pyhttpstatus-utils/badge.svg?branch=master&service=github
    :alt: Code Coverage Status
    :target: https://coveralls.io/r/TuneLab/pyhttpstatus-utils

.. |version| image:: https://img.shields.io/pypi/v/pyhttpstatus-utils.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pyhttpstatus-utils

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pyhttpstatus-utils.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pyhttpstatus-utils

.. |requires| image:: https://requires.io/github/TuneLab/pyhttpstatus-utils/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/TuneLab/pyhttpstatus-utils/requirements/?branch=master

.. end-badges


Install
-------

.. code-block:: bash

    pip install pyhttpstatus-utils

Functions
---------

- ``create_http_status_dict(override_dict=None)``: Create HTTP Status Dictionary with Overrides if provided.
- ``get_http_status_desc(http_status_code)``: Get HTTP status code description.
- ``get_http_status_name(http_status_code)``: Get HTTP status code name.
- ``get_http_status_phrase(http_status_code)``: Get HTTP status code phrase.
- ``get_http_status_type(http_status_code)``: Get HTTP status code type.
- ``is_http_status_successful(http_status_code)``: Check if HTTP Status Code is type Successful
- ``is_http_status_type(http_status_code)``: Match if provided HTTP Status Code is expected HTTP Status Code Type.
- ``validate_http_code(http_code, minimum=100, maximum=599, strict=True, default_http_code=0)``: Validate HTTP code. If strict, throw, else just return default_http_code.

Dictionaries
------------

- ``HTTP_STATUS_DICT``: Extracted from ``http.HTTPStatus``, a dictionary of each HTTP Status' name, code, phrase, and description.
- ``HTTP_STATUS_PHRASE_DICT``: Phrases of HTTP status codes.
- ``HTTP_STATUS_DESC_DICT``: Description of HTTP status codes.
- ``HTTP_STATUS_TYPE_DICT``: Types of HTTP status codes.

Enum Classes
------------

- ``HttpStatusCode``: Static enumeration of HTTP status mapping names to codes
- ``HttpStatusType``: Static enumeration of HTTP status mapping types to phrase
- ``HttpStatusCodeType``: Int enumeration of HTTP status mapping types to codes

HTTP Status Code Types
----------------------

- 100: HttpStatusType.INFORMATIONAL,
- 200: HttpStatusType.SUCCESSFUL,
- 300: HttpStatusType.REDIRECTION,
- 400: HttpStatusType.CLIENT_ERROR,
- 500: HttpStatusType.SERVER_ERROR


Requirements
------------

``pyhttpstatus-utils`` module is built upon Python 3 and has dependencies upon
several Python modules available within `Python Package Index PyPI <https://pypi.python.org/pypi>`_.

.. code-block:: bash

    make install-requirements

or

.. code-block:: bash

    python3 -m pip uninstall --yes --no-input -r requirements.txt
    python3 -m pip install --upgrade -r requirements.txt

