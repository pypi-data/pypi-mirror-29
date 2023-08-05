aws-ssm
=======

This package provides a decorator that injects parameters from the AWS EC2 Systems Manager (SSM) parameter store as environment variables.

This is useful for securely injecting secrets into the environment.

Usage
-----

By default, the decorator detects the hierarchy of your parameter namespace, strips the top level and creates an environment variable from the remaining namespace.

For example, if your parameter is called /my-app/db/password, the decorater will strip the top level (my-app) and create an environment variable called DB_PASSWORD and set the value of the parameter.


.. code:: python
  
  from aws_ssm import ssm

  @ssm(params=['/my-app/db/password'])
  def my_func(event, context):
    my_secret = os.environ['DB_PASSWORD']
    ...

  # The default separator is '/' but can be overriden via the separator parameter
  @ssm(params=['/my-app.db.password'], separator='.')
  def my_func(event, context):
    my_secret = os.environ['DB_PASSWORD']
    ...

  # If you encode the environment variable key in the value you can define a parser lambda function
  # E.g. assuming the value of /my-app/db/password is 'MYSQL_DB_PASSWORD=abc123'
  @ssm(params=['/my-app/db/password'], parser=lambda x: x.split('='))
  def my_func(event, context):
    print = os.environ['MYSQL_DB_PASSWORD'] # outputs abc123


Installation
------------

    pip install aws-ssm

Requirements
------------

- boto3_

.. _boto3: https://github.com/boto/boto3

Authors
-------

- `Justin Menga`_

.. _Justin Menga: https://github.com/mixja
