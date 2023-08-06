======
Models
======

--------
Abstract
--------

Все модели являются подклассами от Document или EmbeddedDocument.

Поля документов являются инстансами классов от Field.

Document должен иметь аттрибут ``__collection__`` с именем коллекции.


--------------
Create a model
--------------

Basic example
=============

.. code:: python

    from yadm import Document, fields

    class User(Document):
        __collection__ = 'users'
        created_at = DatetimeField(auto_now=True)
        name = fields.StringField()
        email = fields.EmailField()


We declare model ``User`` with three fields. It's easy.


Embedded documents
==================

.. code:: python

    from yadm import Document, EmbeddedDocument fields

    class Point(EmbeddedDocument):
        position = StringField()
        address = StringField()
        www = StringField()
        phone = StringField()


    class Action(Document)
        __collection__ = 'posts'
        created_at = DatetimeField(auto_now=True)
        title = fields.StringField()
        email = fields.EmailField()
        contact = fields.EmbeddedDocumentField(ContactDetails)
