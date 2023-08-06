.. _tutor_security_tut1_msf:

Tutorial 2: MSF
===============

Client to MSF (MetaSploit Framework).
See project `homepage <https://www.metasploit.com/>`_ for installation, tutorials, reference manual.
The application is not installed together with hydratk. It is included in `Kali <https://www.kali.org/>`_ 

Command line
^^^^^^^^^^^^

It is controlled via command sec-msf with following options.

Mandatory:

* --sec-action <string> - action, call|start|stop

Optional: 

* --sec-area <string> - RPC area, supported for action help
* --sec-host <string> - host, default 127.0.0.1
* --sec-method <string> - RPC method name, format area.method, supported for actions call|help
* --sec-params <list> - method parameters val1|val2|key3:val3, supported for action call
* --sec-passw <string> - password, default msf
* --sec-path <path> - path to daemon script, default msfrpcd, supported for action start
* --sec-port <number> - RPC port, default 55553
* --sec-user <string> - username, default msf

Configuration
^^^^^^^^^^^^^

Use section msf in configuration file.

* path - path to daemon script, default msfrpcd, used as --sec-path
* host - host, default 127.0.0.1, used as --sec-host
* port - port, default 55553, used as --sec-port
* user - username, default msf, used as --sec-user
* passw - password, default msf, used as --sec-passw

Start, stop
^^^^^^^^^^^

MSF is started via daemon script (i.e. /usr/bin/msfrpcd in Kali). Configure the path according to 
your installation. Startup takes 10s.

  .. code-block:: bash
  
     # start with configured parameters
     $ htk --sec-action start sec-msf
     
     $ ps -ef | grep msf
     msfrpcd
     
     # start with overriden parameters
     $ htk --sec-action start --sec-path /usr/bin/msfrpcd --sec-host 0.0.0.0  --sec-port 8000 --sec-user htk --sec-passw htk sec-msf
     
     $ ps -ef | grep msf
     msfrpcd
     
     # stop
     htk --sec-action stop sec-msf
 
RPC help
^^^^^^^^

The client communicates with MSF via RPC API, see `documentation <http://www.rubydoc.info/github/rapid7/metasploit-framework/Msf/RPC>`_
and is also provided by client action help.

The API methods are grouped in several areas and each method has title area.method.

  .. code-block:: bash
  
     # list areas
     $ htk --sec-action help sec-msf
     
     Areas:
       auth
       console
       core
       db
       job
       module
       plugin
       session
       
     # list area methods
     $ htk --sec-action help --sec-area auth sec-msf
    
     auth area methods:
       login_noauth
       logout
       token_add
       token_generate
       token_list
       token_remove
       
     # get method description
     $ htk --sec-action help --sec-method auth.token_add sec-msf    

     Method auth.token_add
       description: Adds a new token to the database.
       params:
         token - direction: in, type: string, description: A unique token.
         result - direction: out, type: string, description: A successful message: success.  
     
Call method
^^^^^^^^^^^

If you want to call any RPC method, use action call. Specify the name in option --sec-method and parameters in option --sec-params.
Some methods use complicated parameters (combination of values and dictionaries). It is better to use client API instead of console interface.

  .. code-block:: bash
  
     $ htk -d 1 --sec-action call --sec-method module.info --sec-params "payload|android/meterpreter/reverse_tcp" sec-msf
     
     {'name': 'Android Meterpreter, Android Reverse TCP Stager', 'license': ['Metasploit Framework License (BSD)'], 
      'filepath': '/usr/share/metasploit-framework/modules/payloads/stagers/android/reverse_tcp.rb', 'rank': 300, 'references': [], 
      'authors': ['mihi', 'egypt <egypt@metasploit.com>', 'OJ Reeves'], 'description': 'Run a meterpreter server in Android. Connect back stager'}     
         
API
^^^

This section shows several examples how to use MSF client as API in your extensions/libraries.
API uses HydraTK core functionalities so it must be running.

Methods    

* start: start RPC daemon, params: rpc_path
* stop: stop RPC daemon 
* call: call RPC method, params: method, params
* api_help: get API help, params: area, method

Examples

  .. code-block:: python
  
     # import client
     from hydratk.extensions.security.msf import Client
     c = Client()
     
     # start
     res = c.start('/usr/bin/msfrpcd')
     
     # call
     params = ['msf', 'msf'] # username, password
     res, out = c.call('auth-login', params)
     
     {'token': 'TEMPCcNsp6CVSl548A9jAfmPzqFe4bpI', 'result': 'success'}      
     
     # stop
     res = c.stop()                      