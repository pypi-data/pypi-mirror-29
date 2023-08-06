.. _module_ext_trackapps_bugzilla:

Bugzilla
========

This sections contains module documentation of bugzilla module.

bugzilla
^^^^^^^^

Module provides class Client. It uses hydratk.lib.network.rest.client.RESTClient for communication with server.
Unit tests available at hydratk/extensions/trackapps/bugzilla/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - RESTClient object instance
* _url - server url
* _user - username
* _passw - password
* _token - token provided by server after connection
* _return_fields - list of returned fields
* _default_values - dictionary of default values
* _is_connected - bool, connection status

**Properties (Getters)** :

* client - returns _client
* url - returns _url
* user - returns _user
* passw - returns _passw
* token - returns _token
* return_fields - returns _return_fields
* default_values - returns _default_values
* is_connected - returns _is_connected

**Methods**: 

* __init__

Method initializes RESTClient. Sets _url, _user, _passw, _return_fields, _default_values if configured.

* connect

Method connects to server. First it fires event track_before_connect where parameters (url, user, passw) can be rewritten.
Sends GET request to URL /rest.cgi/login with authentication parameters. Server replies with JSON (token included).
After that it fires event track_after_connect and returns bool.

  .. code-block:: python
  
     from hydratk.extensions.trackapps.bugzilla import Client
  
     c = Client()
     url, user, passw = 'https://app.devzing.com/demo/bugzilla', 'demo@devzing.com', 'password'
     res = c.connect(url, user, passw)    
     
* disconnect

Method disconnect from server. It sends GET request to URL /rest.cgi/logout with token parameter. After that it returns bool.

  .. code-block:: python
  
     res = c.disconnect()
     
* read

Method reads records on server. First it fires event track_before_read where parameters (id, fields, query, limit, offset) can be rewritten.
query is dictionary see Bugzilla documentation. It sends GET request to URL /rest.cgi/bug with parameters id, limit, offset, query.       
Server replies with JSON, records are stored in element bugs. After that it fires event track_after_read and returns tuple of bool, list of dictionary.      

  .. code-block:: python
  
     # concrete record
     id = 40
     res, recs = c.read(id)
     
     # return fields
     fields = ['creator', 'id', 'product', 'summary']
     res, recs = c.read(id, fields)
     
     # query 
     res, recs = c.read(query={'product': 'FooBar', 'summary': 'hydra'})
     
     # limit 
     res, recs = c.read(limit=5)
     
     # offset
     res, recs = c.read(limit=1, offset=offset-2)
     
* create

Method create record on server. First it fires event track_before_create where parameter params can be rewritten.
It sends POST request to URL /rest.cgi/bug with JSON body prepared from params. Server replies with JSON containing id.
After that it fires event track_after_create and returs id of created record.

  .. code-block:: python
  
     params = {'summary': 'test hydra', 'version': '1', 'product': 'FooBar', 'component': 'Bar'}
     id = c.create(params)       
     
* update

Method updates record on server. First it fires event track_before_update where parameters (id, params) can be rewritten.
It sends PUT request to URL /rest.cgi/bug/id. Server replies with JSON. After that it fires event track_after_update and returns bool.

  .. code-block:: python
  
     res = c.update(id, {'summary': 'test hydra 2'})   
             