.. _module_ext_trackapps_testlink:

TestLink
========

This sections contains module documentation of testlink module.

testlink
^^^^^^^^

Module provides class Client. It uses hydratk.lib.network.rpc.client.RPCClient (XMLRPC) for communication with server.
Unit tests available at hydratk/extensions/trackapps/testlink/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - RPCClient object instance
* _url - server url
* _dev_key - developer key
* _project - project name
* _project_id - id of project returned by server
* _return_fields - list of returned fields
* _default_values - dictionary of default values
* _is_connected - bool, connection status

**Properties (Getters)** :

* client - returns _client
* url - returns _url
* dev_key - returns _dev_key
* project - returns _project
* project_id - returns _project_id
* return_fields - returns _return_fields
* default_values - returns _default_values
* is_connected - returns _is_connected

**Methods**: 

* __init__

Method initializes RPCClient. Sets _url, _dev_key, _project, _return_fields, _default_values if configured.

* connect

Method connects to server. First it fires event track_before_connect where parameters (url, dev_key, project) can be rewritten.
It initializes proxy to URL /testlink/lib/api/xmlrpc/v1/xmlrpc.php. It calls method tl.getTestProjectByName to get project id.
After that it fires event track_after_connect and returns bool.

  .. code-block:: python
  
     from hydratk.extensions.trackapps.testlink import Client
  
     c = Client()
     url, dev_key, project = 'https://127.0.0.1', '3db69a303c75cdaa08c98b12d5f9f2aa', 'bowman'
     res = c.connect(url, dev_key, project)       
     
* read_test_suite

Method reads tests under test suite. First it fires event track_before_read_suite where parameters (path, steps, fields) can be rewritten.
It gets suite id from path using method _get_suite. It reads test cases using method tl.getTestCasesForTestSuite. Test case doesn't contain
name of test suite (only id of parent suite) which it belongs to. Method gets the name using method tl.getTestSuiteByID. 

Method returns tuple of bool, dictionary (key - test suite, value - list of test cases in dictionary form).

  .. code-block:: python
  
     # test cases without steps
     res, recs = c.read_test_suite('suite1')
     
     # include steps
     res, recs = c.read_test_suite('suite1', steps=True)
     
     # return fields
     fields = ['external_id', 'id', 'name']
     res, recs = c.read_test_suite('suite1/suite2', fields=fields)  
     
* create_test_suite

Methods creates new test suite on server. First it fires event track_before_create where parameters (path, name, details) can be rewritten. 
It gets id of parent suite from path using method _get_suite. It creates suite using method tl.createTestSuite.
After that it fires event track_after_create and returns id of created suite.

  .. code-block:: python
  
     path, suite = 'suite 1', 'test' 
     id = c.create_test_suite(path, suite)
     
* read_test_plan

Method reads test under test plan. First it fires event track_before_read_plan where parameters (plan, plan_id, build_id, fields) can be rewritten.
If plan name is provided the method gets its id using method tl.getTestPlanByName. If build_id is not provided method gets default build using method 
tl.getLatestBuildForTestPlan. 

It reads test cases using method tl.getTestCasesForTestPlan. After that it fires event track_after_read_plan and returns tuple of bool, list of dictionary.

  .. code-block:: python
   
     # plan name
     res, recs = c.read_test_plan('plan 1')   
     
     # plan id 
     res, recs = c.read_test_plan(plan_id=167)
     
     # build id
     res, recs = c.read_test_plan(plan_id=167, build_id=13)
     
     # return fields
     fields = ['external_id', 'tcase_name']
     res, recs = c.read_test_plan('plan 1', fields=fields) 
     
* create_test_plan

Method creates new test plan. First it fires event track_before_create where parameters (name, notes) can be rewritten.
It calls method tl.createTestPlan. After that it fires event track_after_create and returns id of created plan.

  .. code-block:: python
  
     id = c.create_test_plan('test')
     
* create_build

Method creates new build for test plan (specified by id). First it fires event track_before_create where parameters (plan, name, notes) can be rewritten.
It calls method tl.createBuild. After that it fires event track_after_create and returns id of created build.

  .. code-block:: python
  
     id = c.create_build(168, 'test') 
     
* read_test

Method reads test. First it fires event track_before_read where parameters (id, fields) can be rewritten.
It calls method tl.getTestCase. After that it fires event track_after_read and returns tuple of bool, dictionary.

  .. code-block:: python
  
     id = 3
     res, recs = c.read_test(id)   
     
     # return fields
     fields = ['tc_external_id', 'testcase_id']
     res, recs = c.read_test(id, fields=fields)
     
* create_test

Method creates new test. First it fires event track_before_create where parameters (path, params, steps) can be rewritten.
steps is list of dictionary. It gets suite id from path using method _get_suite. It calls method tl.createTestCase. 
After that it fires event track_after_create and returns id of created test.

  .. code-block:: python
  
     # test without steps
     path = 'suite 1/test'
     params = {'testcasename': 'test', 'authorlogin': 'lynus', 'summary': 'hydratk'}
     id = c.create_test(path, params)                               
     
     # include steps
     steps = [{'actions': 'DO', 'expected_results': 'OK'}]
     id = c.create_test(path, params, steps)
     
* add_test_to_plan

Method adds existing test to existing test plan. First it fires event track_before_update where parameters (test, plan, plan_id) can be rewritten.
If plan name is provided the method gets its id using method tl.getTestPlanByName. It calls method tl.addTestCaseToTestPlan.
After that it fires event track_after_update and returns bool.

  .. code-block:: python
  
     # plan name
     res = c.add_test_to_plan(id, plan)
     
     # plan id     
     res = c.add_test_to_plan(id, plan_id=plan_id)
     
* update_test_execution

Method updates execution status of given test. First it fires event track_before_update where parameters (test, status, notes, plan, plan_id, build_id) can be rewritten.
If plan name is provided the method gets its id using method tl.getTestPlanByName. If build_id is not provided method gets default build using method 
tl.getLatestBuildForTestPlan. It calls method tl.reportTCResult. After that it fires event track_after_update and returns bool.

  .. code-block:: python
  
     # plan name
     status = 'p'
     res = c.update_test_execution(id, status, plan=plan)
     
     # plan id
     res = c.update_test_execution(id, status, plan_id=plan_id)
     
     # build id      
     status = 'b'
     res = c.update_test_execution(id, status, plan_id=plan_id, build_id=build) 
     
* _get_suite

Auxiliary method to get suite id from the path. It goes through test suite hierarchy until it requested suite.
It calls method tl.getFirstLevelTestSuitesForTestProject for top level and method tl.getTestSuitesForTestSuite for lower levels.             