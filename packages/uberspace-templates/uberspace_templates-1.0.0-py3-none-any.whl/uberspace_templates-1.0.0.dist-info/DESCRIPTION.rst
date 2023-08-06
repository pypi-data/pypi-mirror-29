
Uberspace Templates
===================

Setup applications and websites in seconds using this cli with many
templates.

Installation
------------

::

    pip3 install uberspace-templates

Usage
-----

::

    uberspace-templates init template name

    # Example
    uberspace-templates init flask my-application

Templates
~~~~~~~~~

Flask
~~~~~

::

    uberspace-templates init flask my-application

-  Setup of Git deployment (create virtualenv, install requirements.txt,
   copy config.py to project folder)
-  Create daemon and run gunicorn on a free port
-  Setup domain and renew LetsEncrypt
-  Setup reverse proxy

Vue.js
~~~~~~

::

    uberspace-templates init vuejs my-application

-  Setup of Git deployment (install dependencies, build for production,
   copy content to webroot)
-  Setup domain and renew LetsEncrypt
-  Setup Apache configuration

Website
~~~~~~~

::

    uberspace-templates init website my-application

-  Setup of Git deployment (copy content to webroot)
-  Setup domain and renew LetsEncrypt
-  Setup Apache configuration

Made with
=========

-  `click`_ - command line utility

Meta
----

| Lucas Hild - `https://lucas-hild.de`_
| This project is licensed under the MIT License - see the LICENSE file
  for details

.. _click: http://click.pocoo.org
.. _`https://lucas-hild.de`: https://lucas.hild.de


