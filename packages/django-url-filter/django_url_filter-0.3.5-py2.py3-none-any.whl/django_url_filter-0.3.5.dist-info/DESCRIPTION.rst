=================
Django URL Filter
=================

.. image:: https://badge.fury.io/py/django-url-filter.svg
    :target: http://badge.fury.io/py/django-url-filter
.. image:: https://readthedocs.org/projects/django-url-filter/badge/?version=latest
    :target: http://django-url-filter.readthedocs.io/en/latest/?badge=latest
.. image:: https://travis-ci.org/miki725/django-url-filter.svg?branch=master
    :target: https://travis-ci.org/miki725/django-url-filter
.. image:: https://coveralls.io/repos/miki725/django-url-filter/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/miki725/django-url-filter?branch=master

Django URL Filter provides a safe way to filter data via human-friendly URLs.

* Free software: MIT license
* GitHub: https://github.com/miki725/django-url-filter
* Documentation: http://django-url-filter.readthedocs.io/

Overview
--------

The main goal of Django URL Filter is to provide an easy URL interface
for filtering data. It allows the user to safely filter by model
attributes and also allows to specify the lookup type for each filter
(very much like Django's filtering system in ORM).

For example the following will retrieve all items where the id is
``5`` and title contains ``"foo"``::

    example.com/listview/?id=5&title__contains=foo

In addition to basic lookup types, Django URL Filter allows to
use more sophisticated lookups such as ``in`` or ``year``.
For example::

    example.com/listview/?id__in=1,2,3&created__year=2013

Requirements
------------

* Python 2.7, 3.x, pypy or pypy3
* Django 1.8+ (there are plans to support older Django versions)
* Django REST Framework 2 or 3 (only if you want to use DRF integration)

Installing
----------

Easiest way to install this library is by using ``pip``::

    $ pip install django-url-filter

Usage Example
-------------

To make example short, it demonstrates Django URL Filter integration
with Django REST Framework but it can be used without DRF (see below).

::

  from url_filter.integrations.drf import DjangoFilterBackend


  class UserViewSet(ModelViewSet):
      queryset = User.objects.all()
      serializer_class = UserSerializer
      filter_backends = [DjangoFilterBackend]
      filter_fields = ['username', 'email']

Alternatively filterset can be manually created and used directly
to filter querysets::

  from django.http import QueryDict
  from url_filter.filtersets import ModelFilterSet


  class UserFilterSet(ModelFilterSet):
      class Meta(object):
          model = User

  query = QueryDict('email__contains=gmail&joined__gt=2015-01-01')
  fs = UserFilterSet(data=query, queryset=User.objects.all())
  filtered_users = fs.filter()

Above will automatically allow the use of all of the Django URL Filter features.
Some possibilities::

    # get user with id 5
    example.com/users/?id=5

    # get user with id either 5, 10 or 15
    example.com/users/?id__in=5,10,15

    # get user with id between 5 and 10
    example.com/users/?id__range=5,10

    # get user with username "foo"
    example.com/users/?username=foo

    # get user with username containing case insensitive "foo"
    example.com/users/?username__icontains=foo

    # get user where username does NOT contain "foo"
    example.com/users/?username__icontains!=foo

    # get user who joined in 2015 as per user profile
    example.com/users/?profile__joined__year=2015

    # get user who joined in between 2010 and 2015 as per user profile
    example.com/users/?profile__joined__range=2010-01-01,2015-12-31

    # get user who joined in after 2010 as per user profile
    example.com/users/?profile__joined__gt=2010-01-01

Features
--------

* **Human-friendly URLs**

  Filter querystring format looks
  very similar to syntax for filtering in Django ORM.
  Even negated filters are supported! Some examples::

    example.com/users/?email__contains=gmail&joined__gt=2015-01-01
    example.com/users/?email__contains!=gmail  # note !

* **Related models**

  Support related fields so that filtering can be applied to related
  models. For example::

    example.com/users/?profile__nickname=foo

* **Decoupled filtering**

  How URLs are parsed and how data is filtered is decoupled.
  This allows the actual filtering logic to be decoupled from Django
  hence filtering is possible not only with Django ORM QuerySet but
  any set of data can be filtered (e.g. SQLAlchemy query objects)
  assuming corresponding filtering backend is implemented.

* **Usage-agnostic**

  This library decouples filtering from any particular usage-pattern.
  It implements all the basic building blocks for creating
  filtersets but it does not assume how they will be used.
  To make the library easy to use, it ships with some integrations
  with common usage patterns like integration with Django REST Framework.
  This means that its easy to use in custom applications with custom
  requirements (which is probably most of the time!)




History
-------

0.3.5 (2018-02-27)
~~~~~~~~~~~~~~~~~~

* Django 2 support.
* Using `tox-travis <https://github.com/tox-dev/tox-travis>`_ for travis builds.
* Fixed negated queries in Django backend.
  Previously negation did ``NOT (condition1 and condition2)`` vs expected
  ``NOT condition1 and NOT condition2``.
  See `#53 <https://github.com/miki725/django-url-filter/issues/53>`_.

0.3.4 (2017-08-17)
~~~~~~~~~~~~~~~~~~

* Py36 compatibility by switching to ``enum-compat`` from ``enum34``
* Improvement to ``README`` by including imports in code examples
* Defaulting ``SQLAlchemyModelFilterSet`` to use ``SQLAlchemyFilterBackend``
* Defaulting ``PlainModelFilterSet`` to use ``PlainFilterBackend``
* Using universal wheels for distribution

0.3.3 (2017-06-15)
~~~~~~~~~~~~~~~~~~

* Fixed bug which did not allow to use SQLAlchemy backend fully
  without having ``django.contrib.contenttypes`` in installed apps.
  See `#36 <https://github.com/miki725/django-url-filter/issues/36>`_.
* Improved SQLAlchemy versions compatibility.
* Added ``URLFilterBackend`` alias in DRF integration for backend to reduce
  confusion with ``DjangoFilterBackend`` as in url filter core backend.

0.3.2 (2017-05-19)
~~~~~~~~~~~~~~~~~~

* Fixed plain backend to return list in Python 3 vs ``filter()`` generator
  which is not compatible with Django pagination since it requires ``len()``
  to be implemented.

0.3.1 (2017-05-18)
~~~~~~~~~~~~~~~~~~

* Fixed bug where default filters were used in root filtersets.
  As a result additional querystring parameters were validation which
  broke other functionality such as pagination.

0.3.0 (2017-01-26)
~~~~~~~~~~~~~~~~~~

* Added plain objects filtering support.
  More in `docs <https://django-url-filter.readthedocs.io/en/latest/usage.html#plain-filtering>`_
  and GitHub issue `#8 <https://github.com/miki725/django-url-filter/issues/8>`_.
* Added `CallableFilter <https://django-url-filter.readthedocs.io/en/latest/api/url_filter.filters.html#url_filter.filters.CallableFilter>`_ which allows to implement custom filters.
* Normalizing to DRF's ``ValidationError`` when using ``StrictMode.Fail``
  since filterset raises Django's ``ValidationError`` which caused 500 status code.
* Fixes ``ModelFilterSet`` automatic introspection to ignore ``GenericForeignKey``
  since they dont have form fields associated with them.
  See `#20 <https://github.com/miki725/django-url-filter/issues/20>`_.
* Releasing with `wheels <http://pythonwheels.com/>`_.

0.2.0 (2015-09-12)
~~~~~~~~~~~~~~~~~~

* Added `SQLAlchemy <http://www.sqlalchemy.org/>`_ support.
* ``FilterSet`` instances have much more useful ``__repr__`` which
  shows all filters at a glance. For example::

    >>> PlaceFilterSet()
    PlaceFilterSet()
      address = Filter(form_field=CharField, lookups=ALL, default_lookup="exact", is_default=False)
      id = Filter(form_field=IntegerField, lookups=ALL, default_lookup="exact", is_default=True)
      name = Filter(form_field=CharField, lookups=ALL, default_lookup="exact", is_default=False)
      restaurant = RestaurantFilterSet()
        serves_hot_dogs = Filter(form_field=BooleanField, lookups=ALL, default_lookup="exact", is_default=False)
        serves_pizza = Filter(form_field=BooleanField, lookups=ALL, default_lookup="exact", is_default=False)
        waiter = WaiterFilterSet()
          id = Filter(form_field=IntegerField, lookups=ALL, default_lookup="exact", is_default=True)
          name = Filter(form_field=CharField, lookups=ALL, default_lookup="exact", is_default=False)

0.1.1 (2015-09-06)
~~~~~~~~~~~~~~~~~~

* Fixed installation issue where not all subpackages were installed.

0.1.0 (2015-08-30)
~~~~~~~~~~~~~~~~~~

* First release on PyPI.


Credits
-------

Development Lead
----------------

* Miroslav Shubernetskiy - https://github.com/miki725

Contributors
------------

* João Neto - https://github.com/netjinho
* Jorik Kraaikamp - https://github.com/JostCrow
* Håken Lid - https://github.com/haakenlid
* Ryan O’Hara - https://github.com/ryan-copperleaf
* webrunners - https://github.com/webrunners



License
-------

::

    The MIT License (MIT)

    Copyright (c) 2015, Miroslav Shubernetskiy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.


