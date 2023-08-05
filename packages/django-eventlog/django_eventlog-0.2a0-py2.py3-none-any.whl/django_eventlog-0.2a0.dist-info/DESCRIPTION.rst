.. image:: https://travis-ci.org/bartTC/django-eventlog.svg?branch=master
    :target: https://travis-ci.org/bartTC/django-eventlog

.. image:: https://codecov.io/github/bartTC/django-eventlog/coverage.svg?branch=master
    :target: https://codecov.io/github/bartTC/django-eventlog?branch=master

===============
django-eventlog
===============

django-eventlog is a very simple Event logger you can use to track certain
events in your code. Events are stored in a Django model and can be viewed
in the Django Admin.

Events can be grouped in a "Event Group" and when hovering over one item
in the admin, all events of the same group are highlighted.

.. image:: https://github.com/bartTC/django-eventlog/raw/master/docs/_static/screenshot.png
   :scale: 100 %

While looking similar, it's not intended to be a replacement for your regular
Python ``logging`` facility, rather an addition to it.

My intention was that users with no access to regular log files can see the
progress and success of certain events. I use it primarily in Task Queues
like Celery_ to inform staff user about the state of background tasks.

django-eventlog stores it's data in a regular database model, so each log entry
will trigger a SQL Insert. Therefore you should be careful using it in high
performance and/or high volume environments.

See the docs for further information.




