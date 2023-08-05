===============================
Netuitive Python Client
===============================

|BuildStatus|_ |CoverageStatus|_

.. |BuildStatus| image:: https://travis-ci.org/Netuitive/netuitive-client-python.svg?branch=master
.. _BuildStatus: https://travis-ci.org/Netuitive/netuitive-client-python

.. |CoverageStatus| image:: https://coveralls.io/repos/github/Netuitive/netuitive-client-python/badge.svg?branch=master
.. _CoverageStatus: https://coveralls.io/github/Netuitive/netuitive-client-python?branch=master

| The Netuitive Python Client allows you to push data to `Netuitive <https://www.netuitive.com>`_ using Python. Netuitive provides an adaptive monitoring and analytics platform for cloud infrastructure and web applications.

| For more information, check out the `help docs <https://help.netuitive.com>`_ or contact `support <mailto:support@netuitive.com>`_.

The Netuitive Python Client can...

* ...create an `element <https://help.netuitive.com/Content/Performance/Elements/elements.htm>`_ in Netuitive with the following data:
    * Element Name
    * Attributes
    * Tags
    * Metric Samples
    * Element relations
    * Location
    * Metric Tags

* ...create an `event <https://help.netuitive.com/Content/Events/events.htm>`_ in Netuitive with the following data:
    * Element Name
    * Event Type
    * Title
    * Message
    * Level
    * Tags
    * Source

Using the Python Netuitive Client
----------------------------------

Setup the Client
~~~~~~~~~~~~~~~~~

``ApiClient = netuitive.Client(api_key='<my_api_key>')``


Setup the Element
~~~~~~~~~~~~~~~~~~

``MyElement = netuitive.Element()``

Add an Attribute
~~~~~~~~~~~~~~~~~

``MyElement.add_attribute('Language', 'Python')``

Add an Element relation
~~~~~~~~~~~~~~~~~~~~~~~~

``MyElement.add_relation('my_child_element')``

Add a Tag
~~~~~~~~~~

``MyElement.add_tag('Production', 'True')``

Add a Metric Sample
~~~~~~~~~~~~~~~~~~~~

``MyElement.add_sample('cpu.idle', 1432832135, 1, host='my_hostname')``

Add a Metric Sample with a Sparse Data Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``MyElement.add_sample('app.zero', 1432832135, 1, host='my_hostname', sparseDataStrategy='ReplaceWithZero')``

Add a Metric Sample with unit type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``MyElement.add_sample('app.requests', 1432832135, 1, host='my_hostname', unit='requests/s')``

Add a Metric Sample with utilization tag
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``MyElement.add_sample('app.requests', 1432832135, 1, host='my_hostname', tags=[{'utilization': 'true'}])``

Add a Metric Sample with min/max values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``MyElement.add_sample('app.percent_used', 1432832135, 50, host='my_hostname', unit='percent', min=0, max=100)``

Send the Samples
~~~~~~~~~~~~~~~~~

``ApiClient.post(MyElement)``

Remove the samples already sent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``MyElement.clear_samples()``

Create an Event
~~~~~~~~~~~~~~~~

``MyEvent = netuitive.Event(hst, 'INFO', 'test event','this is a test message', 'INFO')``

Send the Event
~~~~~~~~~~~~~~~

``ApiClient.post_event(MyEvent)``

Check that our local time is set correctly (returns True/False)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ApiClient.time_insync()``

Docker Example
----------
Included in this project is an example python script (`example/example.py`) which can be built and run within a Docker container. To send test data into your Netuitive environment run the following:

::

    docker build -t netuitive-client-python .
    docker run -e CUSTOM_API_KEY=<custom-api-key> netuitive-client-python

::

Make sure to use your **Custom** Netuitive datasource API key.

Copyright and License
---------------------

Copyright 2015-2016 Netuitive, Inc. under [the Apache 2.0 license](LICENSE).
