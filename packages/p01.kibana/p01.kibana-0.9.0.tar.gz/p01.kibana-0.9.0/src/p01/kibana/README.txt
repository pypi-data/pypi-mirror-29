======
README
======

This package offers a client and server for logging from a python application to
an elsticsearch server. The KibanaServer is used as man in the middle and
buffers write access given from KibanaClient to one or more elasticsearch
server. The KibanaClient outputs it's logging data in the json event format
used by elasticsearch. This means the server only needs to ship them to the
elasticsearch server in batches without manipulate them. The KibanaServer is
used for take some load from the elasticsearch server.

Note: the KibanaClient and KibanaServer communicate via UDP which is very fast
but can also drop packages on overload or network troubles. But it doesn't
slow down your application processing because of it's state less concept.

  >>> import p01.kibana.server


KibanaServer
------------

Setup a KibanaServer:

  >>> interface = '0.0.0.0:2200'
  >>> esoptions = {'hosts': ['0.0.0.0:9200']}
  >>> server = p01.kibana.server.KibanaServer(interface, esoptions)
  >>> server
  <KibanaServer 0.0.0.0:2200 -> 0.0.0.0:9200>

As you can see, the server provides the following internals:

  >>> server._host
  '0.0.0.0'

  >>> server._port
  2200

  >>> server._interval
  5.0

  >>> server._loglevel
  0


ElasticSearchBackend
--------------------

The server provides a ElasticSearchBackend instance. This backend will write
the collected messages to elasticsearch:

  >>> backend = server._backend
  >>> backend
  <ElasticSearchBackend 0.0.0.0:9200>

  >>> backend._hosts
  ['0.0.0.0:9200']

  >>> backend.server
  <KibanaServer 0.0.0.0:2200 -> 0.0.0.0:9200>

  >>> backend.es
  <Elasticsearch([{u'host': u'0.0.0.0', u'port': 9200}])>
