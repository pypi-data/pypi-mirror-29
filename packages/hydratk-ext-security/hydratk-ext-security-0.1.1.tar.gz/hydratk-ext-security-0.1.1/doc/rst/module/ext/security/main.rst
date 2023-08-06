.. _module_ext_security_main:

Main
====

This sections contains module documentation of main security modules.

bootstrapper
^^^^^^^^^^^^

Module provides bootstrapper (method run_app) for Security extension. 
You can run it in standalone mode using method command security (i.e. installed to /usr/local/bin/security).
Unit tests available at hydratk/extensions/security/bootstrapper/01_methods_ut.jedi

security
^^^^^^^^

Modules provides class Extension inherited from class hydratk.core.extension.Extension.
Unit tests available at hydratk/extensions/security/security/01_methods_ut.jedi

**Methods** :

* _init_extension

Method sets extension metadata (id, name, version, author, year). 

* _check_dependencies

Method checks if all required modules are installed.

* _uninstall

Method returns additional uninstall data.

* _register_actions

Methods registers actions hooks according to profile htk (default mode) or security (standalone mode)

* _register_htk_actions

Method registers action hooks for default mode.

commands - sec-msf, sec-zap
long options - sec-action, sec-format, sec-host, sec-method, sec-output, sec-params, sec-passw, sec-path, sec-port, sec-type, sec-url, sec-user

* _register_standalone_actions

Method registers action hooks for standalone mode.

commands - help, msf, zap
long options - action, format, host, method, output, params, passw, path, port, type, url, user
global options - config, debug, debug-channel, language, run-mode, force, interactive, home

* sec_msf

Method handles command msf. It uses option sec-action (action name, call|start|stop). Remaining options are optional:
sec-path (path to daemon control script, configurable, default msfrpcd), sec-host (host, configurable, default 127.0.0.1),
sec-port (RPC port, configurable, default 55553), sec-user (username, configurable, default msf), sec-passw (password, configurable, default msf),
sec-method (RPC method), sec-params (method parameters in list form val1|val2|key3:val3).

  .. code-block:: python
  
     # start msf
     htk --sec-action start --sec-path /usr/bin/msfrpcd --sec-host 127.0.0.1 --sec-port 55553 --sec-user msf --sec-passw msf sec-msf
     
     # stop msf
     htk --sec-action stop sec-msf
     
     # call RPC method
     htk --sec-action call --sec-method auth.login --sec-params "msf|msf" sec-msf

* sec_zap

Method handles command zap. It uses option sec-action (action name, export|scan|spider|start|stop). Remaining options are optional:
sec-path (path to proxy control script, configurable, default zap.sh), sec-host (proxy host, configurable, default 127.0.0.1),
sec-port (proxy port, configurable, default 8080), sec-url (url), sec-method (HTTP method, default GET), sec-params (request parameters
in dict form key1:val1|key2:val2), sec-type (output type, alert|msg|url, default alert), sec-format (output format, har|html|json|md|xml,
default json), sec-output (output filename).

  .. code-block:: python
  
     # start zap
     htk --sec-action start --sec-path /usr/share/zaproxy/zap.sh --sec-host 127.0.0.1 --sec-port 8080 sec-zap
     
     # stop zap
     htk --sec-action stop sec-zap
     
     # spider
     htk --sec-action spider --sec-url http://localhost/mutillidae/index.php sec-zap

     # scan
     htk --sec-action scan --sec-url http://localhost/mutillidae/index.php?page=user-info.php 
     --sec-params "username:ZAP|password:ZAP|user-info-php-submit-button:View Account Details" sec-zap
     
     htk --sec-action scan --sec-url http://localhost/mutillidae/index.php?page=login.php --sec-method POST
     --sec-params "username:ZAP|password:ZAP|login-php-submit-button:Login" sec-zap
     
     # export
     htk --sec-action export --sec-type alert --sec-format html --sec-output alert.html sec-zap
     htk --sec-action export --sec-type msg --sec-format har --sec-output msg.har sec-zap
     htk --sec-action export --sec-type url --sec-format json --sec-output url.json sec-zap

configuration
^^^^^^^^^^^^^

Configuration is stored in /etc/hydratk/conf.d/hydratk-ext-security.conf   
It has separate configuration for each tool.

**msf**

* path - path to MSF RPC daemon script, default msfrpcd
* host - host, default 127.0.0.1
* port - RPC port, default 55553
* user - username, default msf
* passw - password, default msf

**zap**

* path - path to ZAP proxy control script, default zap.sh
* host - host, default 127.0.0.1             
* port - proxy port, default 8080