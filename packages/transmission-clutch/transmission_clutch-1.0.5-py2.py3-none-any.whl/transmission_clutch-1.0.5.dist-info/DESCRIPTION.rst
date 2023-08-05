Clutch
======

``clutch`` is a `Python <http://python.org/>`__ library for controlling
`Transmission <http://www.transmissionbt.com/>`__.

``clutch`` is compatible with both Python2 and Python3.

To install:

::

    pip install transmission-clutch

To use:

::

    >>> from clutch.core import Client

``clutch`` was designed to be a more lightweight and consistent
`Transmission <http://www.transmissionbt.com/>`__ RPC library than what
was currently available for `Python <http://python.org/>`__. Instead of
simply using the keys/fields in the `Transmission RPC
spec <https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt>`__
which have a mix of dashed separated words and mixed case words,
``clutch`` tries to convert all keys to be more Pythonic: underscore
separated words. This conversion is done so that it is still possible to
specify the fields/argument specified in the `Transmission RPC
spec <https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt>`__,
but if you do so your mileage may vary *(probably want to avoid it)*.

``clutch`` is designed to work with all versions of
`Transmission <http://www.transmissionbt.com/>`__, but for renamed
fields before and after Transmission version 1.60 (`RPC
v5 <https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt#L593>`__)
you must specify the correct argument names (no automatic renames).

To use ``clutch`` to control a default ``transmission-daemon`` on
``localhost``:

::

    >>> client = Client()
    >>> client.list()

which produces a list of dictionaries with the torrent information (keys
are the fields: client.list\_fields), and is synonymous to calling

::

    >>> client.torrent.get(client.list_fields)

To use different connection information:

-  complete path

   ::

         >>> client = Client(address="https://host:port/path")

-  default URL, but port change to 8080

   ::

         >>> client = Client(port=8080)

-  default URL, but different host

   ::

         >>> client = Client(host="github.com")

-  default URL, but use a username and password

   ::

         >>> client = Client(username='username', password='password')

``clutch``'s RPC methods are namespaced into four sections:

`Client <https://github.com/mhadam/clutch/blob/master/clutch.py#L683>`__:

-  port\_test -- return if transmission port is open.
-  blocklist\_update -- update block list and return block list size.
-  *list* (``torrent.get`` helper) -- list basic torrent info for all
   torrents.

`Client.queue <https://github.com/mhadam/clutch/blob/master/clutch.py#L342>`__:

-  move\_bottom -- move torrent to bottom of the queue.
-  move\_down -- move torrent down in the queue.
-  move\_top -- move torrent to the top of the queue.
-  move\_up -- move torrent up in the queue.

`Client.session <https://github.com/mhadam/clutch/blob/master/clutch.py#L349>`__:

-  close -- shutdown the Transmission daemon.
-  get -- get session properties.
-  set -- set session properties.
-  stats -- get session statistics.

`Client.torrent <https://github.com/mhadam/clutch/blob/master/clutch.py#L417>`__:

-  add -- add a new torrent.
-  get -- get torrent properties.
-  *files* (``torrent.get`` helper) -- get file information for one or
   more torrents.
-  *percent\_done* (``torrent.get`` helper) -- get torrent percent done
   for one or more torrents.
-  remove -- remove a torrent from transmission and optionally delete
   the data.
-  set -- set torrent properties.
-  set\_location -- set/move torrent location.



