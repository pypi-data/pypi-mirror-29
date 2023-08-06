.. _module_ext_trackapps_jira:

Jira
====

This sections contains module documentation of jira module.

jira
^^^^

Module provides class Client. It uses hydratk.lib.network.rest.client.RESTClient for communication with server.
Unit tests available at hydratk/extensions/trackapps/jira/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - RESTClient object instance
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

Method initializes RESTClient. Sets _url, _user, _passw, _project, _return_fields, _default_values if configured.

* connect

Method connects to server. First it fires event track_before_connect where parameters (url, user, passw, project) can be rewritten.
Sends POST request to URL /rest/auth/1/session with JSON body containing uthentication parameters. Server replies with JSON.
After that it fires event track_after_connect and returns bool.

  .. code-block:: python
  
     from hydratk.extensions.trackapps.jira import Client
  
     c = Client()
     url, user, passw, project = 'https://freeswitch.org/jira', 'lynus', 'bowman', 'TEST'
     res = c.connect(url, user, passw, project)    
     
* read

Method reads records on server. First it fires event track_before_read where parameters (id, fields, query, limit, offset) can be rewritten.
query is string see Jira documentation. Input parameters are transformed to JQL format (id provided key=project-id otherwise project=project)
It sends POST request to URL /rest/api/2/search with JSON body.       
Server replies with JSON, records are stored in element issues. After that it fires event track_after_read and returns tuple of bool, list of dictionary.      

  .. code-block:: python
  
     # concrete record
     id = 4
     res, recs = c.read(id)  
     
     # return fields
     fields = ['creator', 'description', 'id', 'status']
     res, recs = c.read(id, fields)
     
     # query 
     res, recs = c.read(query='priority=Minor')
     
     # limit 
     res, recs = c.read(limit=5)
     
     # offset
     res, recs = c.read(limit=1, offset=5)
     
* create

Method create record on server. First it fires event track_before_create where parameter params can be rewritten.
It sends POST request to URL /rest/api/2/issue with JSON body prepared from params. Server replies with JSON containing id (HTTP status 200, 201).
After that it fires event track_after_create and returs id of created record.

  .. code-block:: python
  
     params = {'summary': 'hydra test', 'description': 'hydra desc', 'customfield_10024': '1234567890123456789012345678901234567890'}
     params['components'] = [{'self': 'https://freeswitch.org/jira/rest/api/2/component/11220', 'id': '11220', 'name': 'test', 'description': 'A test component'}]
     id = c.create(params)      
     
* update

Method updates record on server. First it fires event track_before_update where parameters (id, params) can be rewritten.
It sends PUT request to URL /rest/api/2/issue/project-id. Server replies with JSON (HTTP status 200, 204). After that it fires event track_after_update and returns bool.

  .. code-block:: python
  
     res = c.update(id, {'summary': 'test hydra 2'})   
             