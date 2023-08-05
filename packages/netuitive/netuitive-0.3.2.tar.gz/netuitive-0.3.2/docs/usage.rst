========
Usage
========

To use Netuitive Python Client in a project::

    import netuitive
    import time

    # Setup the Client
    ApiClient = netuitive.Client(api_key='<my_api_key>')

    # setup the Element
    MyElement = netuitive.Element()

    # Add an Attribute
    MyElement.add_attribute('Language', 'Python')

    # Add a Tag
    MyElement.add_tag(('Production', 'True')

    # Add a child Element relation
    MyElement.add_relation('my_child_hostname')

    # Add a Metric Sample
    timestamp = int(time.mktime(time.gmtime()))
    MyElement.add_sample('cpu.idle', timestamp, 1, host='my_hostname')

    # Add a Metric Sample with a Sparse Data Strategy
    timestamp = int(time.mktime(time.gmtime()))
    MyElement.add_sample('app.zero', timestamp, 1, host='my_hostname', sparseDataStrategy='ReplaceWithZero')

    # Add a Metric Sample with unit type
    timestamp = int(time.mktime(time.gmtime()))
    MyElement.add_sample('app.requests', timestamp, 1, host='my_hostname', unit='requests/s')

    # Add a Metric Sample with utilization tag
    timestamp = int(time.mktime(time.gmtime()))
    MyElement.add_sample('app.requests', timestamp, 1, host='my_hostname', tags=[{'utilization': 'true'}])

    # Add a Metric Sample with min/max values
    timestamp = int(time.mktime(time.gmtime()))
    MyElement.add_sample('app.percent_used', timestamp, 50, host='my_hostname', unit='percent', min=0, max=100)

    # Send the Samples
    ApiClient.post(MyElement)

    # Remove the samples already sent
    MyElement.clear_samples()

    # Create an Event
    MyEvent = netuitive.Event('my_hostname', 'INFO', 'test event','this is a test message', 'INFO')

    # Send the Event
    ApiClient.post_event(MyEvent)
