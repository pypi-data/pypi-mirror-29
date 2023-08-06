======
djaTeX
======

|

Description
-----------

This project provides a python module named djatex which allows a
django app to generate a PDF document from a LaTeX template file.

|

Example
--------

A small django project is included, with an example django app that generates a one-page PDF document in the LaTeX article style.

To set up the example server, run the following commands::

   $ python3 -m venv pythonenv
   $ source pythonenv/bin/activate
   $ pip install django
   $ python setup.py install
   $ cd example
   $ python manage.py migrate
   $ python manage.py runserver

You should now have an http server running on localhost port 8000.  Connect to localhost:8000 with your web browser to generate a PDF.


