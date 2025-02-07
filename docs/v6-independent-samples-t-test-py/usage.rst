How to use
==========

Input arguments
---------------

.. describe the input arguments:
.. ['column_name', 'organizations_to_include']

Python client example
---------------------

To understand the information below, you should be familiar with the vantage6
framework. If you are not, please read the `documentation <https://docs.vantage6.ai>`_
first, especially the part about the
`Python client <https://docs.vantage6.ai/en/main/user/pyclient.html>`_.

.. TODO Update the code below and explain input

.. TODO Optionally/alternatively, explain how to run via the vantage6 UI

.. code-block:: python

  from vantage6.client import Client

  server = 'http://localhost'
  port = 7601
  api_path = '/api'
  private_key = None
  username = 'root'
  password = 'password'
  collaboration_id = 1
  organization_ids = [2]

  # Create connection with the vantage6 server
  client = Client(server, port, api_path)
  client.setup_encryption(private_key)
  client.authenticate(username, password)

  input_ = {
    'method': 'central',
    'args': [],
    'kwargs': {
        'column_name': 'my_value',
        'organizations_to_include': 'my_value',
    },
    'output_format': 'json'
  }

  my_task = client.task.create(
      collaboration=collaboration_id,
      organizations=organization_ids,
      name='v6-independent-samples-t-test-py',
      description='Independent Samples t-test: This test compares the means of two independent groups to see if there is a significant difference between them.',
      image='v6-independent-samples-t-test-py',
      input_=input_,
      databases=[{"label": "default"}],
  )

  task_id = my_task.get('id')
  results = client.wait_for_results(task_id)