.. _module_ext_trackapps_trac:

Trac
====

This sections contains module documentation of trac module.

trac
^^^^

Module provides class Client. It uses hydratk.lib.network.rpc.client.RPCClient (XMLRPC) for communication with server.
Unit tests available at hydratk/extensions/trackapps/mantis/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - RPCClient object instance
* _url - server url
* _user - username
* _passw - password
* _project - project name
* _return_fields - list of returned fields
* _default_values - dictionary of default values
* _is_connected - bool, connection status

**Properties (Getters)** :

* client - returns _client
* url - returns _url
* user - returns _user
* passw - returns _passw
* project - returns _project
* return_fields - returns _return_fields
* default_values - returns _default_values
* is_connected - returns _is_connected

**Methods**: 

* __init__

Method initializes RPCClient. Sets _url, _user, _passw, _project, _return_fields, _default_values if configured.

* connect

Method connects to server. First it fires event track_before_connect where parameters (url, user, passw, project) can be rewritten.
It initializes proxy to URL {user}:{passw}@url/project/login/xmlrpc and checks connection using remote method system.getAPIVersion.
After that it fires event track_after_connect and returns bool.

  .. code-block:: python
  
     from hydratk.extensions.trackapps.trac import Client
  
     c = Client()
     url, user, passw, project = 'https://trac.devzing.com/demo', 'demo', 'password', 'project1'
     res = c.connect(url, user, passw, project)     
     
* read

Method reads records on server. First it fires event track_before_read where parameters (id, fields, query) can be rewritten.
It calls method ticket.get to read concrete record or method ticket.query to read all records matching with query (uses ticket.get for all found records).
It parses the response and transforms result to dictionary. After that it fires event track_after_read and returns tuple of bool, list of dictionary.      

  .. code-block:: python
  
     # concrete record
     id = 2
     res, recs = c.read(id)    
          
     # return fields
     fields = ['description', 'id', 'priority', 'summary', 'type']
     res, recs = c.read(id, fields)       
     
     # query
     res, recs = c.read(query='type=enhancement')    
     
* create

Method create record on server. First it fires event track_before_create where parameter params can be rewritten.
It calls method ticket.create. Server replies with int. After that it fires event track_after_create and returs id of created record.

  .. code-block:: python
  
     params = {'type': 'defect', 'priority': 'major', 'summary': 'test hydra', 'description': 'test hydra'}
     id = c.create(params)      
     
* update

Method updates record on server. First it fires event track_before_update where parameters (id, params) can be rewritten.
It calls method ticket.update. After that it fires event track_after_update and returns bool.

  .. code-block:: python
  
     res = c.update(id, {'summary': 'test hydra 2'})   
             
* delete

Method deletes record on server. First it fires event track_before_delete where parameter id can be rewritten. It calls method
ticket.delete. After that it fires event tack_after_delete and returns bool.

  .. code-block:: python
  
     res = c.delete(id)
     
* _parse_record

Auxiliary method used to parse server SOAP response in read. Many xml elements are complex. The method goes through all configured 
parameters (mapping rec_fields) and parses the content according to type. It returns the parameters in dictionary form.

* _toxml

Auxiliary method used to prepare xml content from dictionary of parameters in create, update. It uses mapping rec_fields to prepare
xml according to type.                 