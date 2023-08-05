django-tigger
#############

Bounce users out of your view by raising an exception

Introduction
============

You're probably used to this sort of workflow:

.. code:: python

    from django.http import Http404
    from django.views.generic import TemplateView

    class MyView(TemplateView):
        def get_context(self, **kwargs):
            # do some stuff
            raise Http404

...but wouldn't it be nice if rather than just bombing out with a 404, you
could bounce the user out to a redirect and attach a friendly message?  That's
what django-tigger does!

.. code:: python

    from django.core.urlresolvers import reverse
    from django.views.generic import TemplateView
    from tigger.exceptions import Bounce

    class MyView(TemplateView):
        def get_context(self, **kwargs):
            # do some stuff
            raise Bounce(
                reverse("some-url"),
                message="The wonderful thing about tiggers...",
                level="WARN"
            )

The above code will bounce the user to whatever ``some-url`` resolves to and
dump a message on the screen using the Django messaging framework.


Installation
============

1. Use pip: ``pip install django-tigger``.
2. Add ``django_tigger.middleware.BouncingMiddleware`` to your ``MIDDLEWARE``
   list in your Django settings.  Note that you don't need to add this to
   ``INSTALLED_APPS`` as this package doesn't have any models, migrations, or
   anything that would require that.


Use
====

Basically anywhere you want to just bail out of your current process and
instead redirect the user, call ``Bounce()`` and pass in a few arguments:

* ``url``: The only required argument, this is where you're bouncing your user
  to.
* ``message``: If supplied, this will attach a message to the user's session
  using the Django messaging framework
* ``level``: The level of the message.  Must be one of ``DEBUG``, ``INFO``,
  ``SUCCESS``, ``WARNING``, ``ERROR``.  The default is ``INFO``.


Support
=======

I've used this in Python 3 and Django 1.11, but I see no reason why it wouldn't
work in Python 2.7 and Django 1.10.  Older than that though, and you'll have
trouble.  Newer than that, and you should be fine.

This isn't particularly complex code ;-)


