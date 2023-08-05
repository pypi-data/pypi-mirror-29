=====================
django-simple-viewset
=====================

Simple viewset for models CRUD operations.

.. code:: python

    # myapp/models.py
    from django.db import models

    class MyModel(models.Model):
        ...
        class Meta:
            ...
            default_permissions = ('add', 'change', 'delete', 'read')


.. code:: python

    # myapp/views.py
    from viewset import ModelViewSet
    from .models import MyModel

    class MyModelViewSet(ModelViewSet):
        model = MyModel


.. code:: python

    # myapp/urls.py
    from django.conf.urls import include
    from myapp.views import MyModelViewSet

    urlpatterns = [
        url(r'', include(MyModelViewSet().urls())),
    ]


.. code:: python

    # settings.py
    INSTALLED_APPS = [
        'simple_viewset',
    ]
