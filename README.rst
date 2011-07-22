BayCitizen / django-embedly
===========================

This package provides a template filter to parse embed URLs and call the
embedly API to generate embed HTML. It uses django's caching backend to cache
the response and it saves the same data in a database for embedly doomsday
scenario.

Installation
------------

Install requirements: pip install -r requirements.txt

Add 'embeds' to INSTALLED_APPS in settings.py.

Run syncdb.

Also, under django's settings.py add an entry for

EMBEDLY_KEY = <embedly key>

which can be obtained by signing up for the service.

Usage
-----

Given a template context variable that looks like::

    my_text = """
    The following line will be replaced with video embed HTML.

    Embed:http://www.youtube.com/watch?v=DCL1RpgYxRM
    """

Include these lines in your template to embed the youtube video with a maximum
width of 400px::

    {% load embed_filters %}

    {{ my_text|embedly:"400" }}
