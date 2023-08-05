=========
recontact
=========

|

Description
-----------

This is a pluggable django application which provides a contact form
that generates an email message to specified addresses.  The form is
protected by an invisible recaptcha.

|

Example
--------

A small django project is included, with an example django app
containing a contact form.

To set up the example server, run the following commands::

   $ python3 -m venv pythonenv
   $ source pythonenv/bin/activate
   $ python -m pip install django
   $ python setup.py install
   $ cd example
   $ python manage.py migrate
   $ python manage.py runserver

You should now have an http server running on localhost port 8000.
Connect to localhost:8000 with your web browser to test the form.
