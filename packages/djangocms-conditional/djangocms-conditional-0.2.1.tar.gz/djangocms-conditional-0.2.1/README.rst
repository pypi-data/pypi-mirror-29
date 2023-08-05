=====================
djangocms-conditional
=====================

.. image:: https://travis-ci.org/rhooper/djangocms-conditional.png?branch=master
        :target: https://travis-ci.org/rhooper/djangocms-conditional
        :alt: Latest Travis CI build status

.. image:: https://coveralls.io/repos/rhooper/djangocms-conditional/badge.png
        :target: https://coveralls.io/r/rhooper/djangocms-conditional
        :alt: Test coverage

Django CMS plugin that shows content if a user is logged in and a member of a specific Django group.

Documentation
-------------

The full documentation is at https://djangocms-conditional.readthedocs.org

Quickstart
----------

1.  Install djangocms-conditional::
    pip install djangocms-conditional

2. Add "djangocms_conditional" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'djangocms_conditional',
    ]

3. Run `python manage.py migrate` to create the djangocms_conditional models.

Features
--------

Shows and hides child plugins according to group membership, as configured in the plugin instance.

Caveats
-------

This plugin only prevents rendering of plugins, just like djangocms-timer,
and is subject to the same limitations:

In its current form, plugin won't save you from the queries to retrieve child
plugins due to the way plugin rendering works in django CMS. Still, the
``render`` method of child plugins is not executed (and grandchildren plugins
are not retrieved) with mitigating effect on performance hit.
