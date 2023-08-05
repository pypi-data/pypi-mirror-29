Compound JSONAPI
================

The Compound JSONAPI package is an extension to `Marshmallow`_ and has been
heavily influenced by `Marshmallow JSONAPI`_. The difference to
`Marshmallow JSONAPI`_ is that the Compound JSONAPI is focused on loading
and dumping objects to compound JSONAPI documents that contain all the
serialised data, rather than using JSONAPI's link functionality. It has one
main advantage over `Marshmallow JSONAPI`_ in that it can load and dump full
circular graph structures.

Sourcecode can be found here:
  https://bitbucket.org/mhall/compound-jsonapi/
Documentation can be found here:
  http://compound-jsonapi.readthedocs.io/

  .. _`Marshmallow`: http://marshmallow.readthedocs.io
  .. _`Marshmallow JSONAPI`: http://marshmallow-jsonapi.readthedocs.io


1.0.1
-----

- *BUGFIX*: Fix issues introduced by the load/dump API change in Marshmallow

1.0.0
-----

Initial version


