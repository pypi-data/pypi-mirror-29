|Build Status| |Coverage Status| |Documentation Status|

Contacthub Python SDK
=====================

This is the official Python SDK for `Contacthub REST
API <http://developer.contactlab.com/documentation/>`__.
This SDK easily allows to access your data on Contacthub, making the
authentication immediate and simplifying read/write operations.

For all information about Contacthub, check
`here <https://explore.contactlab.com/contacthub/?lang=en>`__.

You can find the official documentation of this SDK on
`ReadTheDocs <http://contacthub-sdk-python.readthedocs.io/en/latest/index.html>`__.

Table of contents
-----------------

-  `Introduction <http://contacthub-sdk-python.readthedocs.io/en/latest/>`__
-  `Getting
   started <http://contacthub-sdk-python.readthedocs.io/en/latest/getting_started.html>`__

   -  `Installing and importing the
      SDK <http://contacthub-sdk-python.readthedocs.io/en/latest/getting_started.html#installing-the-sdk>`__
   -  `Performing simple operations on
      customers <http://contacthub-sdk-python.readthedocs.io/en/latest/getting_started.html#performing-simple-operations-on-customers>`__

-  `Authentication <http://contacthub-sdk-python.readthedocs.io/en/latest/authentication.html>`__

   -  `Authentication via configuration
      file <http://contacthub-sdk-python.readthedocs.io/en/latest/authentication.html#authenticating-via-configuration-file>`__
   -  `Proxies <http://contacthub-sdk-python.readthedocs.io/en/latest/authentication.html#proxies>`__

-  `Operations on
   Customers <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html>`__

   -  `Add a new
      customer <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#create-and-add-a-new-customer>`__
   -  `Get all
      customers <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#get-all-customers>`__
   -  `Get a single
      customer <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#get-a-single-customer>`__
   -  `Query on
      customers <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#query>`__
   -  `Update a
      customer <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#update-a-customer>`__

      -  `Full update -
         Put <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#full-update-put>`__
      -  `Partial update -
         Patch <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#partial-update-patch>`__

   -  `Delete a
      customer <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#delete-a-customer>`__
   -  `Tag <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#tags>`__
   -  `Additional
      entities <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#additional-entities>`__

      -  `Education <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#education>`__
      -  `Job <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#job>`__
      -  `Like <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#like>`__
      -  `Subscription <http://contacthub-sdk-python.readthedocs.io/en/latest/customer_operation.html#subscription>`__

-  `Operations on
   Events <http://contacthub-sdk-python.readthedocs.io/en/latest/event_operations.html>`__

   -  `Add a new
      event <http://contacthub-sdk-python.readthedocs.io/en/latest/event_operations.html#add-a-new-event>`__

      -  `Sessions <http://contacthub-sdk-python.readthedocs.io/en/latest/event_operations.html#sessions>`__
      -  `External
         ID <http://contacthub-sdk-python.readthedocs.io/en/latest/event_operations.html#externalid>`__

   -  `Get all
      events <http://contacthub-sdk-python.readthedocs.io/en/latest/event_operations.html#get-all-events>`__
   -  `Get a single
      event <http://contacthub-sdk-python.readthedocs.io/en/latest/event_operations.html#get-a-single-event>`__

-  `Exception
   Handling <http://contacthub-sdk-python.readthedocs.io/en/latest/exception_handling.html>`__
-  `API
   Reference <http://contacthub-sdk-python.readthedocs.io/en/latest/api_reference.html>`__

.. |Build Status| image:: https://travis-ci.org/contactlab/contacthub-sdk-python.svg?branch=master
   :target: https://travis-ci.org/contactlab/contacthub-sdk-python
.. |Coverage Status| image:: https://coveralls.io/repos/github/contactlab/contacthub-sdk-python/badge.svg
   :target: https://coveralls.io/github/contactlab/contacthub-sdk-python
.. |Documentation Status| image:: https://readthedocs.org/projects/contacthub-sdk-python/badge/?version=latest
   :target: http://contacthub-sdk-python.readthedocs.io/en/latest/?badge=latest
