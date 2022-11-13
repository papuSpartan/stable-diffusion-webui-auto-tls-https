# SDWUI Auto TLS-HTTPS Extension
 This extension allows you to easily, or even completely automatically start using HTTPS while using SDWUI.
 
### Usecase 1 - Automatic(Default):
If this extension is enabled, by default, it will generate a key/cert pair and then add it to Python's(certifi) trust store. 
 
### Usecase 2 - Bring your own certificate:
If passed an existing key/cert pair by using `--tls-certfile` and `--tls-certfile`, the extension will try to add it to the Python(certifi) trust store.
*note: if you choose this option make sure that your SDWUI server name (--server-name) matches the common name set in the certificate you pass. Otherwise you will likely encounter an exception causing your program to crash.*

 
With both of these methods, by adding this signed certificate to Python's trust store, the webui will be able to run using HTTPS. This is because the certificate will then be seen as valid by your system when the extension passes it to the webui.
