=======
READ ME
=======

Provides persistence to zeromq.


Why:
====

The persizmq package provides different classes to use zeromq with persistence.

How:
====
Code Examples:
--------------

Check the unittests for examples on how to use the components. These will always be up to date.

Installation:
-------------

code::
    pip3 install persizmq

ThreadedSubscriber:
-------------------

The ThreadedSubscriber provides easy background listening on a zeromq.

Storages:
---------

Storages store messages in a persistent way. The can be combined with a ThreadedSubscriber to build persistent subscribers.
So far there are two storages:
1. PersistentStorage: It represents a FIFO queue on disk.
2. PersistentLatestStorage: It just stores the newest message on disk.


Publisher:
----------

The PersistentPublisher persists a message before publishing.
