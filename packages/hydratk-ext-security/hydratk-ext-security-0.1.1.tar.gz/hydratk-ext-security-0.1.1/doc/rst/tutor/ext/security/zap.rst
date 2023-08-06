.. _tutor_security_tut2_zap:

Tutorial 2: ZAP
===============

Client to ZAP (Zed Attack Proxy).
See project `homepage <https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project>`_ for installation, tutorials, reference manual.
The application is not installed together with hydratk. It is included in `Kali <https://www.kali.org/>`_ 

Command line
^^^^^^^^^^^^

It is controlled via command sec-zap with following options.

Mandatory:

* --sec-action <string> - action, export|scan|spider|start|stop

Optional: 

* --sec-format <string>] - output format, har|html|json|md|xml, default json, supported for action export
* --sec-host <string>] - host, default 127.0.0.1
* --sec-method <string>] - HTTP method, default GET, supported for action scan
* --sec-output <filename>] - output filename, supported for action export
* --sec-params <dict>] - request parameters key1:val1|key2:val2, supported for actions scan|spider
* --sec-path <path>] - path to proxy control script, default zap.sh, supported for action start
* --sec-port <number>] - proxy port, default 8080
* --sec-type <string>] - output type, alert|msg|url, default alert, supported for action export
* --sec-url <string>] - URL, supported for actions export|scan|spider

Configuration
^^^^^^^^^^^^^

Use section zap in configuration file.

* path - path to proxy control script, default zap.sh, used as --sec-path
* host - host, default 127.0.0.1, used as --sec-host
* port - port, default 8080, used as --sec-port

Start, stop
^^^^^^^^^^^

ZAP is started via control script (i.e. /usr/share/zaproxy/zap.sh in Kali). Configure the path according to 
your installation. Startup takes 10s.

  .. code-block:: bash
  
     # start with configured parameters
     $ htk --sec-action start sec-zap
     
     $ ps -ef | grep zap
     java -Xmx989m -jar /usr/share/zaproxy/zap-2.6.0.jar -daemon -config api.disablekey=true -host 127.0.0.1 -port 8080
     
     # start with overriden parameters
     $ htk --sec-action start --sec-path /usr/share/zaproxy/zap.sh --sec-host 0.0.0.0 --sec-port 8000 sec-zap
     
     $ ps -ef | grep zap
     java -Xmx989m -jar /usr/share/zaproxy/zap-2.6.0.jar -daemon -config api.disablekey=true -host 0.0.0.0 -port 8000
     
     # stop
     htk --sec-action stop sec-zap
     
     # stop when started with non-default host, port
     htk --sec-host 0.0.0.0 --sec-port 8000 sec-zap
     
Spider
^^^^^^

Spider process is used to go through requested web site and find URLs which can be tested.
The process is time consuming, progress and count of found URLs is printed.
URL not found by spider can't be tested by scan process.

If web page contains form with HTTP GET parameters, include the parameters to URL.
Otherwise ZAP scan process can reject URL with GET parameters which was not found by spider.
Forms with HTTP POST parameters are not affected (ZAP spider uses HTTP GET method only, so POST parameters can't be passed).

  .. code-block:: bash
  
     # simple url
     $ htk --sec-action spider --sec-url "http://localhost/mutillidae/index.php?page=user-info.php" sec-zap  
  
     Progress spider: 100%
     240 urls found
  
     # additional url params
     $  htk --sec-action spider --sec-url "http://localhost/mutillidae/index.php?page=user-info.php" 
            --sec-params "username:ZAP|password:ZAP|user-info-php-submit-button:View Account Details" sec-zap
            
     Progress spider: 100%
     240 urls found
     
Found URLs can be exported in json form (list of URLs).

  .. code-block:: bash
  
     $ export
     $ htk --sec-action export --sec-type url sec-zap
     
     File url.json generated
  
     # specify output and format (only json is supported)
     $ htk --sec-action export --sec-type url --sec-format json --sec-output url.out sec-zap
     
     File url.out generated
     
     [
      "http://localhost",
      "http://localhost/robots.txt",
      "http://localhost/sitemap.xml",
      "http://localhost/mutillidae",
      "http://localhost/mutillidae/documentation",
      "http://localhost/mutillidae/documentation/change-log.html",
      "http://localhost/mutillidae/documentation/how-to-access-Mutillidae-over-Virtual-Box-network.php",
      "http://localhost/mutillidae/'index.php?iv=6bc24fc1ab650b25b4114e93a98f1eba'&page=view-user-privilege-level.php",
      "http://localhost/mutillidae/favicon.ico",
      "http://localhost/mutillidae/framer.html",
      "http://localhost/mutillidae/hints-page-wrapper.php?level1HintIncludeFile=50",
      "http://localhost/mutillidae/index.php",
      "http://localhost/mutillidae/index.php?choice=nmap&csrf-token&initials=ZAP&page=user-poll.php&user-poll-php-submit-button=Submit+Vote",
      "http://localhost/mutillidae/index.php?do=toggle-hints&page=user-info.php",
      "http://localhost/mutillidae/index.php?forwardurl=https://addons.mozilla.org/en-US/firefox/collections/jdruin/pro-web-developer-qa-pack/&page=redirectandlog.php",
      "http://localhost/mutillidae/index.php?iv=6bc24fc1ab650b25b4114e93a98f1eba&page=view-user-privilege-level.php",
      "http://localhost/mutillidae/index.php?page=php-errors.php",
      "http://localhost/mutillidae/index.php?page=styling-frame.php&page-to-frame=styling.php%3Fpage-title%3DStyling+with+Mutillidae",
      "http://localhost/mutillidae/index.php?page=user-info-xpath.php&password=ZAP&user-info-php-submit-button=View+Account+Details&username=ZAP",
     ]
     
Scan
^^^^

Scan process is used to test request url and find security alerts. Run spider before scan process which rejects unknown URLs.
The process is time consuming, progress and count of found alerts is printed.

To find more alerts you should provide form parameters including submit.

  .. code-block:: bash   

     # form with GET parameters
     $ htk --sec-action scan --sec-url "http://localhost/mutillidae/index.php?page=user-info.php" 
           --sec-params "username:ZAP|password:ZAP|user-info-php-submit-button=View Account Details" sec-zap             
           
     # form with POST parameters
     $ htk --sec-action scan --sec-url "http://localhost/mutillidae/index.php?page=login.php" --sec-method POST
           --sec-params "username:ZAP|password:ZAP|login-php-submit-button=Login" sec-zap
           
     Progress scan: 100%
     36 alerts found
     
Found alerts can be exported in html|json|md|xml format, default json.
Use option --sec-url to narrow the export, otherwise also alerts for other pages will be exported.

  .. code-block:: bash
  
     # json
     $ htk --sec-action export --sec-url "http://localhost/mutillidae/index.php?page=login.php" sec-zap
     
     File alert.json generated
     
     {
      "attack": "",
      "confidence": "Medium",
      "wascid": "15",
      "description": "The AUTOCOMPLETE attribute is not disabled on an HTML FORM/INPUT element containing password type input.  Passwords may be stored in browsers and retrieved.",
      "reference": "http://www.w3schools.com/tags/att_input_autocomplete.asp\nhttps://msdn.microsoft.com/en-us/library/ms533486%28v=vs.85%29.aspx",
      "sourceid": "3",
      "solution": "Turn off the AUTOCOMPLETE attribute in forms or individual input elements containing password inputs by using AUTOCOMPLETE='OFF'.",
      "param": "password",
      "method": "GET",
      "url": "http://localhost/mutillidae/index.php?page=login.php&popUpNotificationCode=BHE1",
      "pluginId": "10012",
      "other": "",
      "alert": "Password Autocomplete in Browser",
      "messageId": "1102",
      "id": "1350",
      "evidence": "<input SQLInjectionPoint=\"1\" type=\"password\" name=\"password\" size=\"20\"\r\n\t\t\t\t\t\t\t\t\t\t/>",
      "cweid": "525",
      "risk": "Low",
      "name": "Password Autocomplete in Browser"
     }
     
     # html
     $ htk --sec-action export --sec-type alert --sec-format html --sec-output alert.html --sec-url "http://localhost/mutillidae/index.php?page=login.php" sec-zap
     
     File alert.html generated
     
     # xml
     $ htk --sec-action export --sec-type alert --sec-format xml --sec-output alert.xml --sec-url "http://localhost/mutillidae/index.php?page=login.php" sec-zap
     
     File alert.xml generated     
     
     # md
     $ htk --sec-action export --sec-type alert --sec-format md --sec-output alert.md --sec-url "http://localhost/mutillidae/index.php?page=login.php" sec-zap
     
     File alert.md generated
     
     #ZAP Scanning Report
     ##Summary of Alerts

     | Risk Level | Number of Alerts |
     | --- | --- |
     | High | 4 |
     | Medium | 2 |
     | Low | 5 |
     | Informational | 0 |

     ##Alert Detail
     ### SQL Injection
     ##### High (Medium)
     #### Description
     <p>SQL injection may be possible.</p>

     * URL: [http://localhost/mutillidae/index.php?page=login.php](http://localhost/mutillidae/index.php?page=login.php)
     * Method: `POST`
     * Parameter: `password`
     * Attack: `ZAP' AND '1'='1' -- `
     
     * URL: [http://localhost/mutillidae/index.php?page=login.php](http://localhost/mutillidae/index.php?page=login.php)
     * Method: `POST`
     * Parameter: `username`     
     
     Instances: 2
     ### Solution
     <p>Do not trust client side input, even if there is client side validation in place.  </p><p>In general, type check all data on the server side.</p><p>If the application uses JDBC, use PreparedStatement or CallableStatement, with parameters passed by '?'</p><p>If the application uses ASP, use ADO Command Objects with strong type checking and parameterized queries.</p><p>If database Stored Procedures can be used, use them.</p><p>Do *not* concatenate strings into queries in the stored procedure, or use 'exec', 'exec immediate', or equivalent functionality!</p><p>Do not create dynamic SQL queries using simple string concatenation.</p><p>Escape all data received from the client.</p><p>Apply a 'whitelist' of allowed characters, or a 'blacklist' of disallowed characters in user input.</p><p>Apply the principle of least privilege by using the least privileged database user possible.</p><p>In particular, avoid using the 'sa' or 'db-owner' database users. This does not eliminate SQL injection, but minimizes its impact.</p><p>Grant the minimum database access that is necessary for the application.</p>

     ### Other information
     <p>The page results were successfully manipulated using the boolean conditions [ZAP' AND '1'='1' -- ] and [ZAP' AND '1'='2' -- ]</p><p>The parameter value being modified was NOT stripped from the HTML output for the purposes of the comparison</p><p>Data was returned for the original parameter.</p><p>The vulnerability was detected by successfully restricting the data originally returned, by manipulating the parameter</p>

     ### Reference
     * https://www.owasp.org/index.php/Top_10_2010-A1
     * https://www.owasp.org/index.php/SQL_Injection_Prevention_Cheat_Sheet

     #### CWE Id : 89
     #### WASC Id : 19
     #### Source ID : 1
     
Used messages can be also exported in format har|json, default json.

  .. code-block:: bash
  
     $ htk --sec-action export --sec-type msg --sec-format json --sec-output msg.json --sec-output msg.json --sec-url "http://localhost/mutillidae/index.php?page=login.php" export sec-zap
     
     File msg.json generated     

     $ htk --sec-action export --sec-type msg --sec-format har --sec-output msg.har --sec-output msg.json --sec-url "http://localhost/mutillidae/index.php?page=login.php" export sec-zap
     
     File msg.har generated     
        
     {
      "log" : {
      "version" : "1.2",
      "creator" : {
        "name" : "OWASP ZAP",
        "version" : "2.6.0"
      },
      "entries" : [ {
        "startedDateTime" : "2017-06-19T10:54:21.749+02:00",
        "time" : 38,
        "request" : {
          "method" : "GET",
          "url" : "http://localhost/mutillidae/index.php?page=login.php",
          "httpVersion" : "HTTP/1.1",
          "cookies" : [ ],
          "headers" : [ {
            "name" : "User-Agent",
            "value" : "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0"
          }, {
            "name" : "Pragma",
            "value" : "no-cache"
          }, {
            "name" : "Cache-Control",
            "value" : "no-cache"
          }, {
            "name" : "Content-Length",
            "value" : "0"
          }, {
            "name" : "Referer",
            "value" : "http://localhost/mutillidae/index.php?page=user-info.php&username=ZAP&password=ZAP&user-info-php-submit-button=View+Account+Details"
          }, {
            "name" : "Host",
            "value" : "localhost"
          } ],
          "queryString" : [ {
            "name" : "page",
            "value" : "login.php"
          } ],
          "postData" : {
            "mimeType" : "",
            "params" : [ ],
            "text" : ""
          },
          "headersSize" : 376,
          "bodySize" : 0
        },
        "response" : {
          "status" : 200,
          "statusText" : "OK",
          "httpVersion" : "HTTP/1.1",
          "cookies" : [ {
            "name" : "PHPSESSID",
            "value" : "a28mmgtotdm6udg1sagnmq0en4",
            "path" : "/",
            "domain" : "localhost",
            "expires" : "2017-06-19T11:22:37.761+02:00",
            "httpOnly" : false,
            "secure" : false
          }, {
            "name" : "showhints",
            "value" : "1",
            "domain" : "localhost",
            "expires" : "2017-06-19T11:22:37.761+02:00",
            "httpOnly" : false,
            "secure" : false
          } ],
          "headers" : [ {
            "name" : "Date",
            "value" : "Mon, 19 Jun 2017 08:54:21 GMT"
          }, {
            "name" : "Server",
            "value" : "Apache/2.4.25 (Debian)"
          }, {
            "name" : "Set-Cookie",
            "value" : "PHPSESSID=a28mmgtotdm6udg1sagnmq0en4; path=/"
          }, {
            "name" : "Set-Cookie",
            "value" : "showhints=1"
          }, {
            "name" : "Logged-In-User",
            "value" : ""
          }, {
            "name" : "Vary",
            "value" : "Accept-Encoding"
          }, {
            "name" : "Content-Type",
            "value" : "text/html;charset=UTF-8"
          } ],
          "content" : {
            "size" : 55988,
            "compression" : 0,
            "mimeType" : "text/html;charset=UTF-8",
            "text" : "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" 

API
^^^

This section shows several examples how to use ZAP client as API in your extensions/libraries.
API uses HydraTK core functionalities so it must be running.

Methods    

* start: start proxy, params: proxy_path
* stop: stop proxy 
* spider: spider url, params: url, params
* scan: scan url, params: url, method, params
* export: export to file, params: out_type, out_format, output, url

Examples

  .. code-block:: python
  
     # import client
     from hydratk.extensions.security.zap import Client
     c = Client()
     
     # start
     res = c.start('/usr/share/zaproxy/zap.sh')
     
     # spider
     res, cnt = c.spider('http://localhost/mutillidae/index.php?page=login.php')
     
     # scan
     # GET
     params = {'username': 'ZAP', 'password': 'ZAP', 'user-info-php-submit-button': 'View Account Details'}
     res, cnt = c.scan('http://localhost/mutillidae/index.php?page=user-info.php', params=params)
     
     # POST          
     params = {'username': 'ZAP', 'password': 'ZAP', 'login-php-submit-button': 'Login'}
     res, cnt = c.scan('http://localhost/mutillidae/index.php?page=user-info.php', method='POST', params=params)     
     
     # export
     # alert
     res, out = c.export('alert', 'html', 'alert.html')
     
     # msg
     res, out = c.export('msg', 'har', 'msg.har', 'http://localhost/mutillidae/index.php?page=login.php')
     
     # url
     res, out = c.export('url', 'json', 'url.json')     
     
     # stop
     res = c.stop()     