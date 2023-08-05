Gevent based kibana udp client and forward server. This implementation provides
a client and (proxy) server for send log messages from a python application to
an elasticsearch server. The log message format provides the elasticsearch
logstash message (v1) format which is used in kibana 4. This client/server
implemenation allows you to send log messages from your python application to elasticsearch without to use a logstash server. The server will receive log
message from the client and forward them to one or more elasticsearch servers. This is more or less the same as the new logstash-forwarder implementation
supports. The implementation offers an entry_point called proxy.
