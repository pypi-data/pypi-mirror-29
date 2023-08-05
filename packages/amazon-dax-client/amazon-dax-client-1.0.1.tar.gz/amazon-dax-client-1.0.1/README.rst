============================
Amazon DAX Client for Python
============================

The Amazon DAX Client for Python is used to access `Amazon DAX`_ clusters from
Python. It is nearly source-compatible with Boto3, with only a small change
needed to the client initialization to use DAX instead of DynamoDB.

.. _`Amazon DAX`: https://aws.amazon.com/dynamodb/dax/

Installation
------------
Install Amazon DAX Client using pip:

.. code-block:: sh

    $ pip install amazon-dax-client

Quick Start
-----------
Boto3 has two different interfaces, the *resource interface* and the botocore
*client interface*. Both are supported by the Amazon DAX client, with slightly
different client initialization.

For the resource API, change from:

.. code-block:: python

    ddb = boto3.resource('dynamodb')

to

.. code-block:: python

    dax = AmazonDaxClient.resource(
        endpoint_url='dax.abcdef.us-east-1.amazon.com')

All other ``boto3.resource()`` arguments are accepted.

For the botocore client API, change from:

.. code-block:: python

    session = botocore.session.get_session()
    ddb = session.create_client('dynamodb', ...)

to

.. code-block:: python

    session = botocore.session.get_session()
    dax = AmazonDaxClient(session, ...)

For Boto3 client API, change from:

.. code-block:: python

    ddb = boto3.client('dynamodb')

to

.. code-block:: python

    dax = AmazonDaxClient(endpoint_url='dax.abcdef.us-east-1.amazon.com')

The Boto3 and botocore client APIs are exactly the same.

Unsupported Features
--------------------
The Amazon DAX client does not support table operations. Any table manipulation
operations must use the regular Boto3 or botocore DynamoDB client.

Paginators are not currently supported for DAX.

Documentation
-------------
Once created, the interface is the same as the Boto3/botocore DynamoDB clients.

* `Boto3 DynamoDB resource API <http://boto3.readthedocs.io/en/latest/reference/services/dynamodb.html>`__
* `botocore DynamoDB client API <http://botocore.readthedocs.io/en/latest/reference/services/dynamodb.html>`__


For acomplete example, follow the guide to `create a sample app`_.

.. _`create a sample app`: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.client.sample-app.html

Publish
-------
To publish:

.. code-block:: sh

    python3 setup.py sdist bdist_wheel
    ./s3-upload $VERSION
    twine upload dist/*

Getting Help
------------
Please use these community resources for getting help.

* Ask a question on `StackOverflow <https://stackoverflow.com/>`__ and tag it with `amazon-dynamodb-dax <https://stackoverflow.com/questions/tagged/amazon-dynamodb-dax>`__
* Ask a question on `the AWS DynamoDB forum <https://forums.aws.amazon.com/forum.jspa?forumID=131&start=0>`__
* Open a support ticket with `AWS Support <https://console.aws.amazon.com/support/home#/>`__

