.. _module_ext_trackapps_qc:

Quality Center
==============

This sections contains module documentation of qc module.

qc
^^

Module provides class Client. It uses hydratk.lib.network.rest.client.RESTClient for communication with server.
Unit tests are not available now.

**Attributes** :

* _mh - MasterHead reference
* _client - RPCClient object instance
* _url - server url
* _user - username
* _passw - password
* _domain - application domain
* _project - project name
* _cookie - cookie set by server
* _return_fields - list of returned fields
* _default_values - dictionary of default values
* _is_connected - bool, connection status

**Properties (Getters)** :

* client - returns _client
* url - returns _url
* user - returns _user
* passw - returns _passw
* domain - returns _domain
* project - returns _project
* cookie - returns _cookie
* return_fields - returns _return_fields
* default_values - returns _default_values
* is_connected - returns _is_connected

**Methods**: 

* __init__

Method initializes RESTClient. Sets _url, _user, _passw, _domain, _project, _return_fields, _default_values if configured.

* connect

Method connects to server. First it fires event track_before_connect where parameters (url, user, passw, domain, project) can be rewritten.
It sends POST request to URL /authentication-point/authenticate with Basic authentication. Server replies with cookie in HTTP headers.
After that it fires event track_after_connect and returns bool.

  .. code-block:: python
  
     from hydratk.extensions.trackapps.qc import Client
     
     c = Client()
     res = c.connect(url, user, passw, domain, project)

* disconnect

Method disconnects from server. It sends POST request to URL /authentication-point/logout. After that returns bool.

  .. code-block:: python
  
     res = c.disconnect()
     
* read

Method reads record from server. First it fires event track_before_read where parameters (id, entity, fields, query, order_by, limit, offset) can be rewritten.
query must match QC format (see documentation for more detail). order_by is dictionary (key - fields, value - direction asc|desc).
Default entity is defect. It sends GET request to URL /rest/domains/domain/projects/project/entity+s (plural). Input parameters are sent within URL.     

Server replies with XML, list of element Entity with embedded list of element Field. 
After that it fires event track_after_read and returns tuple of bool, list of dictionary.

  .. code-block:: python
  
     # defect
     entity, query = 'defect', '{ID[=100]}'
     fields = ['name', 'owner', 'user-04', 'user-05']
     res, records = c.read(entity=entity, fields=fields, query=query)  
     
     # test
     id, entity = 49528, 'test'
     res, records = c.read(id=id, entity=entity)  
     
* create

Method creates record on server. First it fires event track_before_create where parameters (entity, params) can be rewritten.
It prepares xml request from parameters. Default entity is defect. It sends POST request to URL /rest/domains/domain/projects/project/entity+s.
Server replies with XML containing id (HTTP status 200, 201). After that it fires event track_after_create and returns id of created record.          

  .. code-block:: python
  
     # defect
     params = {'name': 'test', 'owner': 'x0549396', 'user-04': 'General', 'Status': 'New',
               'Detected on Date': '2016-03-07', 'Environment': 'Preproduction', 'Detected By': 'x0549396',
               'Defect Reason': '6 - Others', 'Severity': '5-Low', 'user-05': 'Other application',
               'Test Type': 'Sys-int Test', 'Description': 'Test'}
     id = c.create('defect', params) 
     
     
* update

Method updates record on server. First it fires event track_before_update where parameters (id, entity, params) can be rewritten.
It prepares xml request from parameters. Default entity is defect. It sends PUT request to URL /rest/domains/domain/projects/project/entity+s/id.
Server replies with XML (HTTP status 200). After that it fires event track_after_update and returns bool.    

  .. code-block:: python
  
     # defect
     params = {'name': 'test 2', 'Status': 'Closed'}
     res = c.update(id, 'defect', params)
                          
* delete

Method deletes record on server. First it fires event track_before_delete where parameters (id, entity) can be rewritten.
Default entity is defect. It sends DELETE request to URL /rest/domains/domain/projects/project/entity+s/id.
Server replies with XML (HTTP status 200). After that it fires event track_after_delete and returns bool. 

  .. code-block:: python
  
     # defect
     res = c.delete(id, 'defect')    
     
* read_test_folder

Method gets test cases under test folder. First it fires event track_before_read_folder where parameters (path, entity) can be rewritten.
Entity can be test-folder (default), test-set-folder. It gets the folder using method _get_folder.
It reads (using method read) all tests using query with hierarchical-path (reference to folder id) and prepares directory tree.

Then it reads details of each test (fields id, name) using method read.
After that it fires event track_after_read_folder and returns tuple of bool, list of dictionary.

  .. code-block:: python
  
     path = 'Subject/02 SYSINTTEST/31604_PoP_CRM/01_Drop_1/03 Customer mngt/CUSTM001 Authentication'
     res, tests = c.read_test_folder(path)  
     
* create_test_folder

Method creates new test folder. Parameters are path, name, entity. Entity can be test-folder (default), test-set-folder. 
It gets parent folder from path using method _get_folder. It calls method create and returns id of created folder.

  .. code-block:: python
    
     id = c.create_test_folder('Subject/.Trash/VAS', 'test')
     
* read_test_set

Method gets test cases under test set folder. First it fires event track_before_read_set where parameter id can be rewritten.
It reads (using method read, entity test-instance) all tests using query with cycle-id (test set id) and gets fields test-id, status, exec-date, actual-tester.
After that it fires event track_after_read_set and returns tuple of bool, list of dictionary.       

* create_test_set

Method creates new test set. Parameters are path, params. It calls method create (entity test-set) and returns id of created set.    

* create_test

Method creates new test. Parameters are path, params. It calls method create (entity test) and returns id of created test.

  .. code-block:: python
  
     params = {'name': 'test', 'subtype-id': 'MANUAL', 'owner': 'x0549396', 'user-04': '31604_PoP CRM',
               'user-01': '5-Low', 'user-05': 'xxx'}
     id = c.create_test('Subject/.Trash/VAS/test', params) 
     
* _get_folder

Auxiliary method to get folder id from path. Parameters are path, entity (test-folder default, test-set-folder).
It goes through directory tree (using method read) till it finds requested folder.                                              