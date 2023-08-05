================
healthyhouse-api
================


.. image:: https://img.shields.io/pypi/v/healthyhouse_api.svg
        :target: https://pypi.python.org/pypi/healthyhouse_api

.. image:: https://img.shields.io/travis/bsdis/healthyhouse_api.svg
        :target: https://travis-ci.org/bsdis/healthyhouse_api

.. image:: https://readthedocs.org/projects/healthyhouse-api/badge/?version=latest
        :target: https://healthyhouse-api.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




A wrapper of the rest API available for a healthyhouse installation.

The full API includes the following routes

- /api/v1/auth/check-token/
- /api/v1/auth/login/
- /api/v1/auth/logout/
- /api/v1/data-import/apps/
- /api/v1/data-import/orders/
- /api/v1/dosimeters/<pk>/
- /api/v1/dosimeters/set-results/
- /api/v1/dosimeters/set-status/
- /api/v1/municipality-radon-risk/
- /api/v1/orders/
- /api/v1/orders/<pk>/
- /api/v1/orders/<pk>/approve/
- /api/v1/orders/<pk>/change_status/
- /api/v1/orders/<pk>/generate_pdf_report/
- /api/v1/orders/<pk>/send_report/
- /api/v1/orders/default-products/
- /api/v1/orders/default-products/<pk>/
- /api/v1/orders/dosimeters/
- /api/v1/orders/dosimeters/<pk>/
- /api/v1/orders/generate_invoices_pdf/?order_number={order_number}
- /api/v1/orders/generate_reports_pdf/?order_number={order_number}
- /api/v1/profile/dosimeters/<pk>/
- /api/v1/profile/orders/

Only a subset of these are available for usage in this implementation. In time hope fully all will be added.

This software can be easily installed from pypi using

   $ pip install healthyhouse_api


* Free software: MIT license
* Documentation: https://healthyhouse-api.readthedocs.io.


Features
--------

* TODO

Credits
-------

