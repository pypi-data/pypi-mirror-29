.. _module_ext_security_zap:

ZAP
===

This sections contains module documentation of zap module.

zap
^^^

Module zap provides class Client for ZAP (Zed Attack Proxy) using external modules
`python-owasp-zap-v2.4 <https://github.com/zaproxy/zap-api-python/>`_ in version >= 0.0.10,  
`simplejson <https://github.com/simplejson/simplejson>`_ in version >= 3.8.2.

Unit tests available at hydratk/ext/security/zap/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - ZAPv2 object instance
* _path - path to control script
* _host - host
* _port - proxy port

**Properties (Getters)** :

* client - returns _client
* path - returns _path
* host - returns _host
* port - returns _port

**Methods**: 

* __init__

Method initializes ZAPv2. Sets _path, _host, _port according to configuration. Parameters host, port can be specified in constuctor.

* start

Method starts proxy. First it fires event zap_before_start. It executes ZAP control script in daemon mode. Proxy path, host, port
are read from configuration by default, path can be specified in method parameter. After that it fires event zap_after_start and returns bool.

  .. code-block:: python
  
     from hydratk.extensions.security.zap import Client
  
     c = Client()
     res = c.start('/usr/share/zaproxy/zap.sh')
     
* stop

Method stops proxy. First it fires event zap_before_stop and calls zapv2 method core.shutdown. After that it fires event zap_after_stop and
returns bool.

  .. code-block:: python
  
     res = c.stop()
     
* spider

Method executes spider process on given URL. First it fires event zap_before_spider where parameters url, params can be rewritten.
Given parameters are appended to URL as request parameters. It calls zapv2 method spider.scan and waits for completion (background process).
Progress status is printed. After that it fires event zap_after_spider and returns tuple (result (bool), count of found urls (int)).

  .. code-block:: python
  
     res, cnt = c.spider('http://localhost/mutillidae/index.php?page=login.php')
     
* scan

Method executes scan process on given URL. This URL must be already known by previous spider execution, otherwise it raises exception.
First it fires event zap_before_scan where parameters url, method, params can be rewritten. Given parameters are appended to URL as request parameters
in case of GET method or included to request body in case of POST method. It calls zapv2 method ascan.scan and wait for completion (background process).
Progress status is printed. After that it fires event zap_after_scan and returns tuple (result (bool), count of found alerts (int)).

  .. code-block:: python
  
     # GET
     params = {'username': 'ZAP', 'password': 'ZAP', 'user-info-php-submit-button': 'View Account Details'}
     res, cnt = c.scan('http://localhost/mutillidae/index.php?page=user-info.php', params=params)
     
     # POST          
     params = {'username': 'ZAP', 'password': 'ZAP', 'login-php-submit-button': 'Login'}
     res, cnt = c.scan('http://localhost/mutillidae/index.php?page=user-info.php', method='POST', params=params)
     
* export

Method prepares export file for given type and format. First it fires event zap_before_export where parameters out_type, out_format, output, url
can be rewritten. Default output filename is type.format if not specified. Parameter url is used for record filtering. Records are returned by zapv2 methods. 
Following types are supported:

alert - formats html|json|md|xml
msg - formats har|json
url - format json

After that it fires event zap_after_export and returns tuple (result (bool), output filename (strin)).

  .. code-block:: python
  
     # alert
     res, out = c.export('alert', 'html', 'alert.html')
     
     # msg
     res, out = c.export('msg', 'har', 'msg.har', 'http://localhost/mutillidae/index.php?page=login.php')
     
     # url
     res, out = c.export('url', 'json', 'url.json')