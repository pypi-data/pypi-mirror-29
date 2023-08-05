Annotype: Python 3 annotations and marshmallow
==============================================

**Annotype** combines Python 3 annotations and Marshmallow for powerful
validation of function arguments.

.. code:: python

    from annotype import annotyped
    from marshmallow import (
        Schema,
        fields
    )


    class PersonSchema(Schema):
        firstname = fields.Str(required=True)
        lastname = fields.Str(required=True)

    @annotyped()
    def salute(person: SampleSchema):
        print 'Hello {} {}'.format(person['firstname'], person['lastnamename'])

    person = dict(firstname='John')

    # This will raise a ValidationError because lastname is not defined
    salute(person)

    @annotyped()
    def welcome(firstname: fields.Str(), lastname: fields.Str()):
        print 'Welcome {} {}'.format(firstname, lastname)

    # This will also raise a ValidationError because lastname is not a string
    welcome('Jane', 1)

In short, annotype allows you to validate data using the powerful
marshmallow library and the Python 3 annotations.

Get It Now
----------

::

    $ pip install -U annotype

Documentation
-------------

See marshmallow documentation available here
http://marshmallow.readthedocs.io/ .

Requirements
------------

-  Python >= 3.4
-  marshmallow >= 3.0.0

License
-------

MIT licensed. See the bundled
`LICENSE <https://github.com/cbourget/annotype/blob/pypi/LICENSE>`__
file for more details.


