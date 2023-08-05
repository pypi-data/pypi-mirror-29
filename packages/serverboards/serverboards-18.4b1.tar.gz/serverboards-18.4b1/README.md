# Python3 Serverboards bindings

https://serverboards.io

This python module allows to create plugins in the Python programming language
for Serverboards.

Serverboards is a Server Management, Automation and Monitoring platform.

It uses JSON RPC over stdin/stdout to allow plugins to extend the core
functionality; even the core functionality is programmed using this very
same bindings.

There are two versions:

* sync.py -- Classic Python. Blocks on every call although it does some
  tricks to allow some concurrent async code. It is very limited and its
  very difficult to do some kind of highly concurrent stuff. Only recommended
  as a basic start and for very simple plugins.

* async.py -- Curio based bindings that allow to reliably have several
  concurrent requests at the same time, each may be blocked doing some async
  work, as remote requests and so on.

Currently the sync version is more tested, but all future development will
be done on the async version.

Both provide the following basic building blocks:

## `@rpc_method`

Decorator over every function that is exported to the RPC.

## `rpc.call(method, *args, **kwargs)` / `rpc.event(method, *args, **kwargs)`

Perform remote calls or events. Events do not wait for a response.

## `rpc.subscribe(event, callback)`

Subscribe to a remote event. The callback will be called when that event
is emitted from the core.
