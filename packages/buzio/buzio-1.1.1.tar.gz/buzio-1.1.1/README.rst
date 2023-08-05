Welcome to Buzio's documentation!
=================================

.. image:: https://img.shields.io/pypi/v/buzio.svg
   :target: https://pypi.python.org/pypi/buzio
.. image:: https://travis-ci.org/chrismaille/buzio.svg?branch=master
    :target: https://travis-ci.org/chrismaille/buzio
.. image:: https://img.shields.io/pypi/pyversions/buzio.svg
   :target: https://pypi.python.org/pypi/buzio
.. image:: https://coveralls.io/repos/github/chrismaille/buzio/badge.svg?branch=master
	:target: https://coveralls.io/github/chrismaille/buzio?branch=master
.. image:: https://readthedocs.org/projects/buzio/badge/?version=latest
	:target: http://buzio.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status
.. image:: https://api.codacy.com/project/badge/Grade/5a70e225a4744cbc828013eeb003f2d7
    :target: https://www.codacy.com/app/chrismaille/buzio?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=chrismaille/buzio&amp;utm_campaign=Badge_Grade
.. image:: https://api.codeclimate.com/v1/badges/c90dd31c86a382ce3d99/maintainability
   :target: https://codeclimate.com/github/chrismaille/buzio/maintainability
   :alt: Maintainability
.. image:: https://requires.io/github/chrismaille/buzio/requirements.svg?branch=master
     :target: https://requires.io/github/chrismaille/buzio/requirements/?branch=master
     :alt: Requirements Status

* Read the Docs: http://buzio.readthedocs.io/
* Source Code: https://github.com/chrismaille/buzio

Buzio_ is a python library tool for printing formatted text in terminal, similar to termcolor_ or colored_.

Installing Buzio
-----------------

Install Buzio using the command::

    $ pip install buzio

Importing the Library
---------------------

.. code-block:: python

    from buzio import console, formatStr

The ``console`` is a instance of the ``Console`` class initialized with default color themes. You can also import the class and instantiate with your own settings (See the :doc:reference for more info)

The ``formatStr`` is also a instance of the ``Console`` class too, but instead of printing in terminal the message, this instance just return the formatted text.

The default color themes
++++++++++++++++++++++++

=================== =======================
Method              Text Color
=================== =======================
console.box         Fore.CYAN
console.error       Fore.RED
console.info        Fore.CYAN
console.section     Fore.LIGHTYELLOW_EX
console.success     Fore.GREEN
console.warning     Fore.YELLOW
=================== =======================

These colors are based in colorama_ constants.

Generate fancy formats
......................

**"Section" example 1**:

.. code-block:: python

	from buzio import console

	console.section("First Section")

Terminal output::

	$ >> First Section
	$ ----------------

Humanize Python objects
.......................

Buzio_ can automatically humanize any python object for printing in terminal:

.. code-block:: python

	from datetime import datetime, timedelta
	from buzio import console
	
	today = datetime.now()
	yesterday = today - timedelta(days=1)
	my_dict = {
		"start day": yesterday,
		"end day": today
	}

	console.box(my_dict, date_format="%a, %b-%d-%Y")

The output on terminal will be (in blue color)::

	$ *********************************
	$ *                               *
	$ *  start day: Thu, Feb-01-2018  *
	$ *   end day: Fri, Feb-02-2018   *
	$ *                               *
	$ *********************************

Ask for Input data
..................

You can use Buzio_ to automatically generate "choose" and "select" questions, based on Python objects:

**"Choose" example:**

.. code-block:: python

	from buzio import console

	my_choices = [
		"Orange",
		"Apple",
		"Potato"
	]

	console.choose(my_choices)

Terminal output::

	$ 1. Orange
	$ 2. Apple
	$ 3. Potato
	$ 
	$ Select (1-3): ?

Run terminal commands
.....................

You can use Buzio_ to run terminal commands (using Python ``subprocess``) and get the *stdout* result::

	>>> from buzio import console
	>>> ret = console.run("echo HelloWorld!", get_stdout=True, verbose=True)
	Cmd: echo HelloWorld!
	>>> print(ret)
	HelloWorld!

Further reading
---------------

Please check full documentation in http://buzio.readthedocs.io/

.. _Buzio: https://github.com/chrismaille/buzio
.. _colored: https://pypi.python.org/pypi/colored
.. _termcolor: https://pypi.python.org/pypi/termcolor
.. _colorama: https://pypi.python.org/pypi/colorama