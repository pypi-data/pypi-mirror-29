.. _module_ext_security_msf:

MSF
===

This sections contains module documentation of msf module.

msf
^^^

Module msf provides class Client for MSF (MetaSploit Framework) using external modules
`msgpack-python <http://msgpack.org/>`_ in version >= 0.4.8,  
`requests <http://docs.python-requests.org/en/master/>`_ in version >= 2.11.1.

Unit tests available at hydratk/ext/security/msf/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _path - path to daemon script
* _host - host
* _port - RPC port
* _user - username
* _passw - password
* _token - authentication token

**Properties (Getters)** :

* path - returns _path
* host - returns _host
* port - returns _port
* user - returns _user
* passw - returns _passw
* token - returns _token

**Methods**: 

* __init__

Method sets _path, _host, _port _user, _passw according to configuration. Parameters host, port, user, passw can be specified in constuctor.

* start

Method starts RPC daemon. First it fires event msf_before_start. It executes MSF daemon script. RPC path, host, port, user, passw
are read from configuration by default, path can be specified in method parameter. After that it fires event msf_after_start and returns bool.

  .. code-block:: python
  
     from hydratk.extensions.security.msf import Client
  
     c = Client()
     res = c.start('/usr/bin/msfrpcd')
     
* stop

Method stops RPC daemon. First it fires event msf_before_stop and terminates deamon process. After that it fires event msf_after_stop and
returns bool.

  .. code-block:: python
  
     res = c.stop()
     
* call

Method calls any RPC method. First it fires event msf_before_call where parameters method, params can be rewritten. 
Parameters are required in list form of values (for standard params) or dictionaries (for dict params), the ordering is important.
Method is called via requests method post, data are encoded to message-pack format using msgpack method packb.
Method by default (if not already authenticated) authenticates the user using RPC method auth.login. Then it calls requested RPC method. 
After that it fires event msf_after_call and returns tuple (result (bool), method output (dict)).

  .. code-block:: python
  
     params = ['msf', 'msf'] # username, password
     res, out = c.call('auth-login', params)
     
     {'token': 'TEMPCcNsp6CVSl548A9jAfmPzqFe4bpI', 'result': 'success'}
     
* api_help

Method returns help text for requested RPC API according to configuration in module msf_api.     
     
* _get_process

Auxiliary method to get RPC process, used to check whether process was started in method start or terminted in method stop.     