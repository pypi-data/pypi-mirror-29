.. _module_ext_trackapps_main:

Main
====

This sections contains module documentation of main trackapps modules.

bootstrapper
^^^^^^^^^^^^

Module provides bootstrapper (method run_app) for TrackApps extension. 
You can run it in standalone mode using method command trackapps (i.e. installed to /usr/local/bin/trackapps).
Unit tests available at hydratk/extensions/trackapps/bootstrapper/01_methods_ut.jedi

trackapps
^^^^^^^^^

Modules provides class Extension inherited from class hydratk.core.extension.Extension.
Unit tests available at hydratk/extensions/trackapps/trackapps/01_methods_ut.jedi

**Methods** :

* _init_extension

Method sets extension metadata (id, name, version, author, year). 

* _check_dependencies

Method checks if all required modules are installed.

* _uninstall

Method returns additional uninstall data.

* _register_actions

Methods registers actions hooks according to profile htk (default mode) or trackapps (standalone mode)

* _register_htk_actions

Method registers action hooks for default mode.

commands - track
long options - tr-app, tr-action, tr-type, tr-input, tr-output, tr-url, tr-user, tr-passw, tr-dev-key, tr-domain, tr-project,
tr-id, tr-fields, tr-query, tr-order-by, tr-limit, tr-offset, tr-page, tr-per-page, tr-params, tr-path, tr-steps

* _register_standalone_actions

Method registers action hooks for standalone mode.

commands - run, help
long options - app, action, type, input, output, url, user, passw, dev-key, domain, project, id, fields, query, order-by, limit,
offset, page, per-page, params, path, steps
global options - config, debug, debug-channel, language, run-mode, force, interactive, home

* init_client

Method initializes client for given application (BUGZILLA, MANTIS, TRAC, JIRA, TESTLINK, QC), case is ignored. It raises NotImplementedError for not
supported application. Method returns client instance. Parameters are passed as args, kwargs.

* handle_track

Method handles command track. It uses common options tr-app (application name, mandatory), tr-action (action name, read|create|update|delete, mandatory).
Remaining options are optional and can be configured: tr-url, tr-user (not for testlink), tr-passw (not for testlink), tr-dev-key (testlink only),
tr-domain (qc only), tr-project (not for bugzilla), type (type of entity, testlink and qc only).

Method connects to server using client method connect (specific parameters). Then it calls method according to action (read, create, update, delete)
and disconnect from server.

* read

Method handles action read. It uses optional options: tr-id, tr-fields, tr-query, tr-order-by, tr-limit, tr-offset, tr-page, tr-per-page.
For bugzilla, mantis, trac, jira it calls client method read. For testlink it calls read_test_suite, read_test_plan or read_test according to tr-type.
Options tr-id, tr-path are mandatory in this case and method prompts user to set them (if not set already).

For qc it calls read_test_folder, read_test_set or read according to tr-type. Options tr-id, tr-path are mandatory in this case and method prompts user to set them (if not set already).
The result is written to file (if option tr-output set) or printed.

  .. code-block:: python
  
     # bugzilla
     htk --tr-app bugzilla --tr-action read --tr-id 40 --tr-url https://app.devzing.com/demo/bugzilla --tr-user demo@devzing.com --tr-passw password track
     trackapps --app bugzilla --action read --id 40 --url https://app.devzing.com/demo/bugzilla --user demo@devzing.com --passw password run
     
     # mantis
     htk --tr-app mantis --tr-action read --tr-id 1 --tr-url https://app.devzing.com/demo/mantisbt --tr-user demo --tr-passw password --tr-project "Sample Project" track
     trackapps --app mantis --action read --id 1 --url https://app.devzing.com/demo/mantisbt --user demo@devzing.com --passw password --project "Sample Project" run
     
     # trac
     htk --tr-app trac --tr-action read --tr-id 2 --tr-url https://trac.devzing.com/demo --tr-user demo --tr-passw password --tr-project project1 track
     trackapps --app trac --action read --id 2 --url https://trac.devzing.com/demo --user demo --passw password --project project1 run
     
     # jira
     htk --tr-app jira --tr-action read --tr-id 4 --tr-url https://freeswitch.org/jira --tr-user lynus --tr-passw bowman --tr-project TEST track
     trackapps --app jira --action read --id 4 --url https://freeswitch.org/jira --user lynus --passw bowman --project TEST run
     
     # testlink
     htk --tr-app testlink --tr-action read --tr-url http://127.0.0.1:81 --tr-dev-key 3db69a303c75cdaa08c98b12d5f9f2aa --tr-project bowman --tr-path "suite 1/suite 4" --tr-type test-suite track        
     trackapps --app testlink --action read --url http://127.0.0.1:81 --dev-key 3db69a303c75cdaa08c98b12d5f9f2aa --project bowman --path "suite 1/suite 4" --type test-suite run
     
     # qc
     htk --tr-app qc --tr-action read --tr-url url --tr-user user --tr-passw passw --tr-domain dom --tr-project proj --tr-id 8594 track
     trackapps --app qc --action read --url url --user user --passw passw --domain dom --project proj --id 8594 run
     
* create

Method handles action create. It uses optional options tr-params (key1:val1,key2:val2), tr-input (filename, stored as description), tr-steps (key1:val1,key2:val2|key1:val1,key2:val2).
Default parameter values can be configured, method automatically sets them if not provided in tr-params. Required parameters can be configured.
Method prompts user to set them (if not set already in tr-params). You can also configure lov for required parameters, method shows the list when prompting.

For bugzilla, mantis, trac, jira it calls client method create. For testlink it calls create_test_suite, create_test_plan, create_build or create_test
according to tr-type. Option tr-path and some parameters (name, plan) are mandatory in this case and user is prompted.
For qc it calls create_test_folder, create_test_set, create_test or create according to tr-type. Option tr-path is mandatory in this case and user is prompted.
Ater that prints id of created record.

  .. code-block:: python
  
     # bugzilla
     htk --tr-app bugzilla --tr-action create --tr-url https://app.devzing.com/demo/bugzilla --tr-user demo@devzing.com --tr-passw password
         --tr-params "summary:test hydra,version:1,product:FooBar,component:Bar" track
     trackapps --app bugzilla --action create --url https://app.devzing.com/demo/bugzilla --user demo@devzing.com --passw password
               --params "summary:test hydra,version:1,product:FooBar,component:Bar" run         
     
     # mantis
     htk --tr-app mantis --tr-action create --tr-url https://app.devzing.com/demo/mantisbt --tr-user demo --tr-passw password --tr-project "Sample Project"
         --tr-params "category:defect,summary:test hydra,description:test hydra" track
     trackapps --app mantis --action create --url https://app.devzing.com/demo/mantisbt --user demo --passw password --project "Sample Project"
               --params "category:defect,summary:test hydra,description:test hydra" run         
     
     # trac
     htk --tr-app trac --tr-action create --tr-url https://trac.devzing.com/demo --tr-user demo --tr-passw password --tr-project project1
         --tr-params "type:defect,priority:major,summary:test hydra,description:test hydra" track
     trackapps --app trac --action create --url https://trac.devzing.com/demo --user demo --passw password --project project1
               --params "type:defect,priority:major,summary:test hydra,description:test hydra" run         
     
     # jira
     htk --tr-app jira --tr-action create --tr-url https://freeswitch.org/jira --tr-user lynus --tr-passw bowman --tr-project TEST
         --tr-params "summary:hydra test,description:hydra desc,customfield_10024:1234567890123456789012345678901234567890" track
     trackapps --app jira --action create --url https://freeswitch.org/jira --user lynus --passw bowman --project TEST
               --params "summary:hydra test,description:hydra desc,customfield_10024:1234567890123456789012345678901234567890" run         
     
     # testlink      
     htk --tr-app testlink --tr-action create --tr-url http://127.0.0.1:81 --tr-dev-key 3db69a303c75cdaa08c98b12d5f9f2aa --tr-project bowman
         --tr-type test --tr-path "suite 1/test" --tr-params "testcasename:test,authorlogin:lynus,summary:test" track
     trackapps --app testlink --action create --url http://127.0.0.1:81 --dev-key 3db69a303c75cdaa08c98b12d5f9f2aa --project bowman
               --type test --path "suite 1/test" --params "testcasename:test,authorlogin:lynus,summary:test" run   
               
     # qc 
     htk --tr-app qc --tr-action create --tr-params "name:hydra,description:hydra desc" track
     trackapps --app qc --action create --params "name:hydra,description:hydra desc" run               
               
* update

Method handles action update. It uses options tr-id (mandatory), tr-params, tr-input. For bugzilla, mantis, trac, jira, qc is calls client method update.
For testlink it calls add_test_to_plan, update_test_execution or update according to tr-type. Parameters test, plan are mandatory in this case.
After that it confirms record update.

  .. code-block:: python
  
     # bugzilla
     htk --tr-app bugzilla --tr-action update --tr-url https://app.devzing.com/demo/bugzilla --tr-user demo@devzing.com --tr-passw password --tr-id -1 track
     trackapps --app bugzilla --action update --url https://app.devzing.com/demo/bugzilla --user demo@devzing.com --passw password --id -1 run         
     
     # mantis
     htk --tr-app mantis --tr-action update --tr-url https://app.devzing.com/demo/mantisbt --tr-user demo --tr-passw password --tr-project "Sample Project" --tr-id -1 track
     trackapps --app mantis --action update --url https://app.devzing.com/demo/mantisbt --user demo --passw password --project "Sample Project" --id -1 run         
     
     # trac
     htk --tr-app trac --tr-action update --tr-url https://trac.devzing.com/demo --tr-user demo --tr-passw password --tr-project project1 --tr-id -1 track
     trackapps --app trac --action update --url https://trac.devzing.com/demo --user demo --passw password --project project1 --id -1 run         
     
     # jira
     htk --tr-app jira --tr-action update --tr-url https://freeswitch.org/jira --tr-user lynus --tr-passw bowman --tr-project TEST --tr-id -1 track
     trackapps --app jira --action update --url https://freeswitch.org/jira --user lynus --passw bowman --project TEST --id -1 run         
     
     # testlink      
     htk --tr-app testlink --tr-action update --tr-url http://127.0.0.1:81 --tr-dev-key 3db69a303c75cdaa08c98b12d5f9f2aa --tr-project bowman --tr-id -1 track
     trackapps --app testlink --action update --url http://127.0.0.1:81 --dev-key 3db69a303c75cdaa08c98b12d5f9f2aa --project bowman --id -1 run 
     
     # qc
     htk --tr-app qc --tr-action update --tr-id 8595 --tr-params "status:Closed" track
     trackapps --app qc --action update --id 8595 --params "status:Closed" track
     
* delete

Method handles action delete (supported for mantis, trac, qc). It uses mandatory option tr-id and calls client method delete. Afte that it confirms record deletion.

  .. code-block:: python
     
     # mantis
     htk --tr-app mantis --tr-action delete --tr-url https://app.devzing.com/demo/mantisbt --tr-user demo --tr-passw password --tr-project "Sample Project" --tr-id -1 track
     trackapps --app mantis --action delete --url https://app.devzing.com/demo/mantisbt --user demo --passw password --project "Sample Project" --id -1 run         
     
     # trac
     htk --tr-app trac --tr-action delete --tr-url https://trac.devzing.com/demo --tr-user demo --tr-passw password --tr-project project1 --tr-id -1 track
     trackapps --app trac --action delete --url https://trac.devzing.com/demo --user demo --passw password --project project1 --id -1 run 
     
     # qc
     htk --tr-app qc --tr-action delete --tr-id 8595 track
     trackapps --app qc --action delete --id 8595 track
     
configuration
^^^^^^^^^^^^^

Configuration is stored in /etc/hydratk/conf.d/hydratk-ext-trackapps.conf   
Each application has its own section.

* url - server url
* user - username
* passw - password
* dev_key - developer key (testlink only)
* domain - application domain (qc only)
* project - project name (not for bugzilla)
* return_fields - record fields returned by read, key1,key2 (list)
* required_fields - fields requested by create when not set, key1,key2 (list)
* default_values - default parameters values used by create, key1:val1 key2:val (dictionary)
* lov - list of parameter values offered when prompting by create, key1:val1,val2 key2:val1,val2 (dictionary with list values)     

For qc the parameters: return_fields, required_fields, default_value, lov are configured per entity.   
                              