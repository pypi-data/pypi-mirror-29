Firebase ORM Python
=======================================
Django like models for NoSQL database Firestore.

________

Installation
============

.. code-block:: shell

    $ pip install firebase_orm

Initialize
==========

Create settings.py in the root directory of the project:

    settings.py

    .. code-block:: python

        CERTIFICATE = 'path/to/serviceAccountKey.json'
        BUCKET_NAME = '<BUCKET_NAME>.appspot.com'

CERTIFICATE
    Once you have created a `Firebase console <https://console.firebase.google.com/?authuser=0>`_ project and downloaded a JSON file with your service account credentials.

BUCKET_NAME
    The bucket name must not contain gs:// or any other protocol prefixes. For example, if the bucket URL displayed in the `Firebase console <https://console.firebase.google.com/?authuser=0>`_ is gs://bucket-name.appspot.com, pass the string bucket-name.appspot.com

Usage
======

Create model:
"""""""""""""

.. code-block:: python

    from firebase_orm import models


    class Article(models.Model):
        headline = models.CharField()
        type_article = models.CharField(db_column='type')

        class Meta:
            db_table = 'medications'

        def __str__(self):
            return self.headline

Use API:
""""""""

.. code-block:: pycon

    # Import the models we created
    >>> from models import Article

    # Create a new Article.
    >>> a = Article(headline='Django is cool')

    # Save the object into the database. You have to call save() explicitly.
    >>> a.save()

    # Now it has an ID.
    >>> a.id
    1

    # Fields are represented as attributes on the Python object.
    >>> a.headline
    'Django is cool'

    # Firebase ORM provides a rich database lookup API.
    >>> Article.objects.get(id=1)
    <Article: Django is cool>
    >>> Article.objects.get(id=2)
    Traceback (most recent call last):
        ...
    DoesNotExist: Article matching query does not exist.

