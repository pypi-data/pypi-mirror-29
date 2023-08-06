Molo Commenting
===============

.. image:: https://travis-ci.org/praekelt/molo.commenting.svg?branch=develop
    :target: https://travis-ci.org/praekelt/molo.commenting
    :alt: Continuous Integration

.. image:: https://coveralls.io/repos/praekelt/molo.commenting/badge.png?branch=develop
    :target: https://coveralls.io/r/praekelt/molo.commenting?branch=develop
    :alt: Code Coverage

Installation::

   pip install molo.commenting


Django setup::

   INSTALLED_APPS = INSTALLED_APPS + (
      'django_comments',
      'molo.commenting',
      'notifications'
   )
   COMMENTS_APP = 'molo.commenting'
   COMMENTS_FLAG_THRESHHOLD = 3
   COMMENTS_HIDE_REMOVED = False
   SITE_ID = 1

In your urls.py::

   urlpatterns += [
       url(r'^commenting/',include('molo.commenting.urls', namespace='molo.commenting', app_name='molo.commenting')),
       url(r'', include('django_comments.urls')),
   ]

In your article_page.html::

   {% block content %}
    {% include "comments/comment_block.html" %}
   {% endblock %}
