=====================
Jinja2 Django Version
=====================

A Jinja extenstion that creates a global variable with Django version
information for your Jinja2 templates:

Usage
-----
.. code-block:: console

    $ pip install jinja2-django-version

.. code-block:: python

    from jinja2 import Environment

    env = Environment(extensions=['jinja2_django_version.DjangoVersionExtension'])

    # 2.0
    template = env.from_string("{{ django_version }}")

    # 2.0
    template = env.from_string("{{ django_version.minor }}")

    # 2
    template = env.from_string("{{ django_version.major }}")

    # 2.0.2
    template = env.from_string("{{ django_version.micro }}")

    # (2, 0, 2, 'final', 0)
    template = env.from_string("{{ django_version.tuple }}")

    template.render()
