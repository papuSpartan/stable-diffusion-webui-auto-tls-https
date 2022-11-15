# SDWUI Auto TLS-HTTPS Extension
Extension implementation of https://github.com/AUTOMATIC1111/stable-diffusion-webui/pull/4417

 This extension allows you to easily, or even completely automatically start using HTTPS with SDWUI. [It will help prevent your shrek image generations from being stolen! (see below)]
 
### Usecase 1 - Automatic(Default):
If this extension is enabled it will, by default:
- generate a key/cert pair
- read the Python trust store from Python certifi
- create an intermediary bundle made from fusing our cert with the certifi trust store
- pass bundle to requests using `REQUESTS_CA_BUNDLE`
 
### Usecase 2 - Bring your own certificate:
If passed an existing key/cert pair by using `--tls-certfile` and `--tls-certfile`, the extension will try to do the same as **Usecase 1** but with your specific certificate.
*note: if you choose this option make sure that your SDWUI server name (--server-name) matches the common name set in the certificate you pass. Otherwise you will likely encounter an exception causing your program to crash.*

 
With both of these methods, by passing the certificate to Python requests as being trusted, the webui will be able to run using HTTPS. This is because the certificate will then be seen as valid by the SDWUI processes after the extension passes it to the webui.

## Installation
You can install this extension automatically using SDWUI's "Extensions" tab if your installation is up to date.
\
See https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Extensions

For security reasoms you may encounter an error in the console upon restart after installing **if** you are running with `--listen` and do not include `--enable-insecure-extension-access`.

### But... I'm still getting certificate errors
This is normal. This extension is, **right now**, dealing only with Python's certificate trust store. It is **not** interacting with your system level trust store. Operating system specific trust store support may be added later, but if having to give a certificate exception at the browser level is not adequate for you then you could add the `webui.cert` to your OS's trust store which should eliminate those warnings.


## Why?

 Without this extension, SDWUI will simply use unencrypted HTTP. Read [this article by cloudflare](https://www.cloudflare.com/learning/ssl/why-is-http-not-secure/) if you would like to better understand why this is bad. But long story short, If an attacker were to join your local network, they would be able to passively listen to your SDWUI traffic and grab entire images without even having direct access to your SDWUI server.
 
 Here's an example of this using [wireshark](https://www.wireshark.org/):
 
By filtering in Wireshark to connections made to my SDWUI and HTTP protocol, we can easily see the HTTP GET and reponse containing the entire unencrypted image which was generated in SDWUI.
 
 GET Request:
![image](https://user-images.githubusercontent.com/30642826/201568983-170717f0-8bc9-40f3-890e-0cb6dce21f7d.png)

Unencrypted Response:
![image](https://user-images.githubusercontent.com/30642826/201569119-15610c55-8890-4627-bedd-b10be3838b67.png)

After receiving the response with the PNG data we can simply:
1. Select "Portable Network Graphics"
![image](https://user-images.githubusercontent.com/30642826/201569545-eaf9adac-9346-49e1-8c96-8e711203c8bd.png)
2. Right click and select export packet bytes
3. Read the file you saved the bytes to as a PNG
4. You have now stolen some poor user's shrek image 😢

![image](https://user-images.githubusercontent.com/30642826/201570306-87d62515-0c38-40c3-af84-936b5216c93a.png)
