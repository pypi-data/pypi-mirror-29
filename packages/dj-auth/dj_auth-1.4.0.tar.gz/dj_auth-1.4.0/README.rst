=============================
dj_auth
=============================

.. image:: https://badge.fury.io/py/dj_auth.png
    :target: https://badge.fury.io/py/dj_auth

---

.. image:: https://gitlab.com/systent/dj_auth/badges/master/build.svg

.. image:: https://gitlab.com/systent/dj_auth/badges/master/coverage.svg

The goal of dj_auth is to limit data access for certain user over your django project.


Requirements
------------

::

    Django 1.9

Quickstart
----------

Install dj_auth::

    pip install dj_auth

Put dj_auth into your INSTALLED_APPS at settings module::

    INSTALLED_APPS = (
       ...
       'dj_auth',
    )

Create dj_auth database tables by running::

    python manage.py migrate


Extend the Queryset methods of your Models::

    from django.db import models

    from dj_auth.models import ObjectFilterQuerySetMixin

    class YourModelQuerySet(ObjectFilterQuerySetMixin, models.QuerySet):

        def sichtbar(self, sichtbar=True):
            return self.filter(sichtbar=sichtbar)


    class YourModel(models.Model):
        your_fielfs = models.SmallIntegerField()

        objects = YourModelQuerySet.as_manager()


Set DJ_AUTH constant in your settings.py::

    DJ_AUTH = {'content_type_exclude': ('contenttypes.contenttype', 'sessions.session', 'sites.site',
                                        'auth.user', 'auth.group', 'auth.permission', 'admin.logentry',
                                        'dj_auth.objectfilter',),
               'content_type_include': (),
               'global_fields_exclude':  ('user', ),
               'related_filter_fields_exclude': {'auth.user': ('groups', ), },
               }

In "content_type_exclude" you put the models on which you don't want create ObjectFilters

In "content_type_include" you put the models on which you want create ObjectFilters

In "global_fields_exclude" you put the fieldnames on which you don't want apply the ObjectFilter globally

In "related_filter_fields_exclude" you put the fieldnames on which you don't want apply the ObjectFilter for a specific Model

========
Features
========


ObjectFilterFormMixin
---------------------

First of all you have to create an ObjectFilter record for a specific user. Therefore you can should use ObjectFilterFormMixin::

    from django import forms

    from dj_auth.forms import ObjectFilterFormMixin

    class ObjectFilterForm(ObjectFilterFormMixin, forms.ModelForm):
        pass


ObjectFilterListMixin
---------------------

To limit data in ListView use ObjectFilterListMixin::

    from django.views.generic import ListView
    from django.contrib.auth import get_user_model

    from dj_auth.views import ObjectFilterListMixin

    class UserListView(ObjectFilterListMixin, ListView):
        model = get_user_model()


ObjectFilterDetailMixin
-----------------------

To limit data in DetailView use ObjectFilterDetailMixin::

    from django.views.generic import DetailView
    from django.contrib.auth import get_user_model

    from dj_auth.views import ObjectFilterDetailMixin

    class UserDetailView(ObjectFilterDetailMixin, DetailView):
        model = get_user_model()


ObjectFilterUpdateMixin
-----------------------

To limit data in UpdateView use ObjectFilterUpdateMixin::

    from django.views.generic import UpdateView
    from django.contrib.auth import get_user_model

    from dj_auth.views import ObjectFilterUpdateMixin

    class UserDetailView(ObjectFilterUpdateMixin, UpdateView):
        model = get_user_model()


ObjectFilterDeleteMixin
-----------------------

To limit data in UpdateView use ObjectFilterDeleteMixin::

    from django.views.generic import DeleteView
    from django.contrib.auth import get_user_model

    from dj_auth.views import ObjectFilterDeleteMixin

    class UserDetailView(ObjectFilterDeleteMixin, DeleteView):
        model = get_user_model()


====
Todo
====

* 

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ coverage run --source=dj_auth runtests.py && coverage html


Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
