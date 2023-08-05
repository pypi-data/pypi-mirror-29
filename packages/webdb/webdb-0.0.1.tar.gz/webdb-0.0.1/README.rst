webdb
*****

webdb provides a simple JSON based database interface for
client side data access in web applications.

.. contents::


What is webdb?
==============

webdb is an adapter between you client side application
(most probably written in JS in a browser) and your
databases on the server. It can be used to access file, 
SQL, NoSQL and any other database you want using simple 
HTTP GET and POSTs.

How does it work?
=================

webdb is a cherrypy application that should be mounted under
a protected path. Typical would be ``/database``. All the
authentication stuff must be handled by cherrypy. 
The application accesses the database using and instance of
``webdb.adapters.AbstractDBMS``. This instance will dispatch
the right database (one might use several databases) and
handle the request.

Requests
========

Requests are HTTP GET requests for pulling and HTTP POST for
pushing data. The query is always encoded in JSON objects:

.. _webdbrequest:

::

	webdbrequest
		.database : string
		.request
			.table : string
			.operation : string
			.parameters: object

``webdbrequest.database``
	String name of the database. This name will be used
	to dispatch the right database adapter.
``webdbrequest.request.table``
	String name of the table to access.
``webdbrequest.request.operation``
	String name of the operation. It is one of
	``INSERT``, ``UPDATE``, ``DELETE``, ``SELECT``

``webdbrequest.request.parameters``
	Is a JSON object containing the parameters of the
	query. The structure depends on the operation:

	``INSERT``
		The parameter is just a map of key value pairs that
		will be attempted to put::

			.parameters: {string: value}

	``UPDATE``
		The parameter is an object containing
		a *set* and a *where* block::

			.parameters
				.where: {string: value}
				.set: {string: value}
		
		All key value pairs in *where* will be
		interpreted as ``AND`` joined conditions,
		all key value pairs in *set* will be
		interpreted as substitutions for the current
		values.
	
	``DELETE``
		The parameter is a map ``{string: value}``
		that will be interpreted as ``AND`` joined
		conditions::

			.parameters: {string: value}
	
	``SELECT``
		The parameter is an object containing
		a *where* and a *what* block::

			.parameters
				.where: {string: value}
				.what: list

		*where* will be interpreted as in ``UPDATE``,
		*what* is the list of columns to fetch.
		

``value`` is one of the following types: 
string, integer, float, boolean, date, time, datetime.

See `Handling Date and Time`_.


.. _webdbresult:
	
The server will return data depending on what the adapter
returns. If the adapter returns an exception, the server
will set the HTTP status to 404, the content-type to
``text/plain`` and return a (maybe) useful text.
If the server returns a structured result (for instance the
result of a SQL SELECT) it will set the HTTP status to 200
and the content-type to ``application/json`` and return the
json encoded data.
If the server returns nothing but the query did succeed it
will set the HTTP status to 204 and return nothing.

Isolating Users
===============

There might be several users accessing the same
database/table/whatever. To isolate access to this shared
data the ``inject`` operation can be used. The
``AbstractDBMS`` has an attribute ``inject`` that should be
a nested function returning the attribute value to inject
and an attribute ``inject_as`` that should be set to the
name of the table column that should be inserted.

A typical application might set the username in the session
and inject the username in the query::

	dbms = AbstractDBMS(
			inject = lambda: cherrypy.session["username"], 
			inject_as = "username")

**Note**: This will not actually work. One cannot
instantiate ``AbstractDBMS``, as it is abstract. This sample
is just meant to be a hint how one can implement injections.

Handling Date and Time
======================

Date and time are handled as JSON objects with a magic
attribute (the ``__type__``) ::

	time
		.__type__ = "time"
		.hour: int
		.minute: int
		.second: int
		.microsecond: int
		.utcoffset: int

	date
		.__type__ = "date"
		.year: int
		.month: int
		.day: int

	datetime
		.__type__ = "datetime"
		.year: int
		.month: int
		.day: int
		.hour: int
		.minute: int
		.second: int
		.microsecond: int
		.utcoffset: int


See also: 

- `utcoffset <https://docs.python.org/3/library/datetime.html#datetime.tzinfo.utcoffset>`_
- `python date and time representation <https://docs.python.org/3/library/datetime.html#module-datetime>`_

One can omit some attributes, they will be filled with zeros
automatically.

