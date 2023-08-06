.. _module_ext_trackapps_mantis:

Mantis
======

This sections contains module documentation of mantis module.

mantis
^^^^^^

Module provides class Client. It uses hydratk.lib.network.soap.client.SOAPClient for communication with server.
Unit tests available at hydratk/extensions/trackapps/mantis/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - SOAPClient object instance
* _url - server url
* _user - username
* _passw - password
* _project - project name
* _project_id - id of project returned by server
* _return_fields - list of returned fields
* _default_values - dictionary of default values
* _is_connected - bool, connection status

**Properties (Getters)** :

* client - returns _client
* url - returns _url
* user - returns _user
* passw - returns _passw
* project - returns _project
* project_id - returns _project_id
* return_fields - returns _return_fields
* default_values - returns _default_values
* is_connected - returns _is_connected

**Methods**: 

* __init__

Method initializes SOAPClient. Sets _url, _user, _passw, _project, _return_fields, _default_values if configured.

* connect

Method connects to server. First it fires event track_before_connect where parameters (url, user, passw, project) can be rewritten.
It loads WSDL from URL /api/soap/mantisconnect.php?wsdl. Calls operation mc_project_get_id_from_name to get project id, server replies with int.
After that it fires event track_after_connect and returns bool.

  .. code-block:: python
  
     from hydratk.extensions.trackapps.mantis import Client
  
     c = Client()
     url, user, passw, project = 'https://app.devzing.com/demo/mantisbt', 'demo', 'password', 'Sample Project'
     res = c.connect(url, user, passw, project)      
     
* read

Method reads records on server. First it fires event track_before_read where parameters (id, fields, page, per_page) can be rewritten.
It calls operation mc_issue_get to read concrete record or operation mc_project_get_issues to read all records which belong to project.
Use parameters page, per_page to shorten the result. Server replies with SOAP response, which is parsed using method _parse_record. 
After that it fires event track_after_read and returns tuple of bool, list of dictionary.      

  .. code-block:: python
  
     # concrete record
     id = 1
     res, recs = c.read(id)  
          
     # return fields
     fields = ['category', 'id', 'priority', 'project']
     res, recs = c.read(id, fields)         
     
     # pagination
     page, per_page = 2, 2
     res, recs = c.read(page=page, per_page=per_page)     
     
* create

Method create record on server. First it fires event track_before_create where parameter params can be rewritten.
It calls operation mc_issue_add with xml prepared using method _toxml. Server replies with int.
After that it fires event track_after_create and returs id of created record.

  .. code-block:: python
  
     params = {'category': 'defect', 'summary': 'test hydra', 'description': 'test hydra'}
     id = c.create(params)       
     
* update

Method updates record on server. First it fires event track_before_update where parameters (id, params) can be rewritten.
It reads the record to get current settings. Current values must be sent event if they are not changed. 
It calls operation mc_issue_update with xml prepared using method _toxml. After that it fires event track_after_update and returns bool.

  .. code-block:: python
  
     res = c.update(id, {'summary': 'test hydra 2'})   
             
* delete

Method deletes record on server. First it fires event track_before_delete where parameter id can be rewritten. It calls operation
mc_issue_delete. After that it fires event tack_after_delete and returns bool.

  .. code-block:: python
  
     res = c.delete(id)
     
* _parse_record

Auxiliary method used to parse server SOAP response in read. Many xml elements are complex. The method goes through all configured 
parameters (mapping rec_fields) and parses the content according to type. It returns the parameters in dictionary form.

* _toxml

Auxiliary method used to prepare xml content from dictionary of parameters in create, update. It uses mapping rec_fields to prepare
xml according to type.                 