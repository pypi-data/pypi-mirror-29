WebPy-GraphQL
=============

Adds GraphQL support to your WebPy application.

Usage
-----

Just use the ``GraphQLView`` view from ``webpy_graphql``

.. code:: python

    from webpy_graphql import GraphQLView

    urls = ("/graphql", "GQLGateway")

    app = web.application(urls, globals())

    class GQLGateway(BaseResponse):
        view = GraphQLView('graphql', schema=GQLSchema, graphiql=True)

        def GET(self):
            return self.view.dispatch_request()

        def POST(self):
            return self.view.dispatch_request()

This will add ``/graphql``  endpoints to your app.

Supported options
~~~~~~~~~~~~~~~~~

-  ``schema``: The ``GraphQLSchema`` object that you want the view to
   execute when it gets a valid request.
-  ``context``: A value to pass as the ``context`` to the ``graphql()``
   function.
-  ``root_value``: The ``root_value`` you want to provide to
   ``executor.execute``.
-  ``pretty``: Whether or not you want the response to be pretty printed
   JSON.
-  ``executor``: The ``Executor`` that you want to use to execute
   queries.
-  ``graphiql``: If ``True``, may present
   `GraphiQL <https://github.com/graphql/graphiql>`__ when loaded
   directly from a browser (a useful tool for debugging and
   exploration).
-  ``batch``: Set the GraphQL view as batch (for using in
   `Apollo-Client <http://dev.apollodata.com/core/network.html#query-batching>`__
   or
   `ReactRelayNetworkLayer <https://github.com/nodkz/react-relay-network-layer>`__)


