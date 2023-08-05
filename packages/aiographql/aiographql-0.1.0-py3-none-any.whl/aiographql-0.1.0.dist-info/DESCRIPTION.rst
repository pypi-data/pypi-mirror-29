
* `asyncio <https://docs.python.org/3/library/asyncio.html>`_ - explicit concurrency `to reduce race conditions <https://glyph.twistedmatrix.com/2014/02/unyielding.html>`_
* `graphql <http://graphql.org/>`_ - all you need and nothing more in one request +auto docs of your api
* `uvloop, protocol <https://github.com/MagicStack/uvloop#performance>`_ - `top performance <https://magic.io/blog/uvloop-blazing-fast-python-networking/>`_
* minimal http - unlike REST frameworks that are waste of time for ``/graphql`` endpoint
* pluggable context - for auth, logging, etc
* exception handling - at all levels, with default or custom handler

Usage::

    pip install aiographql

    cat <<'END' >serve.py
    import asyncio, aiographql, graphene

    class User(graphene.ObjectType):
        id = graphene.ID(required=True)
        name = graphene.String()

    class Query(graphene.ObjectType):
        me = graphene.Field(User)

        async def resolve_me(self, info):
            await asyncio.sleep(1)  # DB
            return User(id=42, name='John')

    schema = graphene.Schema(query=Query, mutation=None)
    aiographql.serve(schema)
    END

    UNIX_SOCK=/tmp/worker0 python3 serve.py

    curl --unix-socket /tmp/worker0 http:/ --data-binary '{"query": "{
        me {
            id
            name
        }
    }", "variables": null}'

    # Result:
    # 1 second async await for DB and then:
    {"data":{"me":{"id":"42","name":"John"}}}

See `more examples and tests <https://github.com/academicmerit/aiographql/tree/master/tests>`_ about JWT auth, concurrent slow DB queries, etc.

Config::

    import aiographql; help(aiographql.serve)

    serve(schema, get_context=None, unix_sock=None, exception_handler=None, enable_uvloop=True, run=True)
        Configure the stack and start serving requests

* ``schema``: ``graphene.Schema`` - GraphQL schema to serve
* ``get_context``: ``None`` or ``callable(headers: bytes, request: dict): mixed`` - callback to produce GraphQL context, for example auth
* ``unix_sock``: ``str`` - path to unix socket to listen for requests, defaults to env var ``UNIX_SOCK`` or ``'/tmp/worker0'``
* ``exception_handler``: ``None`` or ``callable(loop, context: dict)`` - default or custom exception handler as defined `here <https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.set_exception_handler>`_
* ``enable_uvloop``: ``bool`` - enable uvloop for top performance, unless you have a better loop
* ``run``: ``bool`` - if ``True``, run the loop and the coroutine serving requests, else return this coroutine
* return: ``coroutine`` or ``None`` - the coroutine serving requests, unless ``run=True``


