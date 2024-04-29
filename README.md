# SDWUI Auto TLS-HTTPS Extension
 This extension allows you to easily, or even completely automatically start using HTTPS with SDWUI. [It will help prevent your shrek image generations from being stolen! (see below)]
 
 Extension implementation of https://github.com/AUTOMATIC1111/stable-diffusion-webui/pull/4417
 
 *This extension is **not** intended for use with Google **Collab** instances.*
 
### Usecase 1 - Automatic(Default):
If this extension is enabled it will, by default:
- generate a key/cert pair
- read the Python trust store from Python certifi
- create an intermediary bundle made from fusing our cert with the certifi trust store
- pass bundle to requests using the `REQUESTS_CA_BUNDLE` environment variable
 
### Usecase 2 - Bring your own certificate:
If passed an existing key/cert pair by using `--tls-keyfile` and `--tls-certfile`, the extension will try to do the same as **Usecase 1** but with your specific certificate.
*note: if you choose this option make sure that your SDWUI server name (--server-name) matches the common name set in the certificate you pass. Otherwise you will likely encounter an exception causing your program to crash.*

 
With both of these methods, by passing the certificate to Python requests as being trusted, the webui will be able to run using HTTPS. This is because the certificate will then be seen as valid by the SDWUI processes after the extension passes it to the webui.

## Installation
You can install this extension automatically using SDWUI's "Extensions" tab if your installation is up to date.
\
See https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Extensions

For security reasons you may encounter an error in the console upon restart after installing **if** you are running with `--listen` and do not include `--enable-insecure-extension-access`.

**If you are using a relatively new version of sdwui, you will want to add `--disable-tls-verify` to your launch options if you are going with usecase 1.**

### But... I'm still getting certificate errors / I'm getting warnings
![warning](https://i0.wp.com/DeployHappiness.com/wp-content/uploads/2019/02/01.png?resize=442%2C230&ssl=1)

If you are in fact connecting to the link output by the webui console, this is **expected**, do not be alarmed. You have two options, the second is slightly more difficult to setup. 

**A.** You can simply [tell your browser to add an exception](https://support.mozilla.org/en-US/kb/error-codes-secure-websites#w_bypassing-the-warning). (most browsers have similar steps)\
**B.** You can **properly** configure things so that the browser knows that you trust the sdwui page:

This extension is, **right now**, dealing only with Python's certificate trust store. It is **not** interacting with your system level trust store. Operating system specific trust store support may be added later, but if having to give a certificate exception at the browser level is not adequate for you then you could add the `webui.cert` to your OS's trust store which should eliminate those warnings.

Here's how to do that on some common platforms:

[Windows](https://www.thewindowsclub.com/manage-trusted-root-certificates-windows)
\
[OSX](https://support.apple.com/guide/keychain-access/add-certificates-to-a-keychain-kyca2431/mac)
\
[Linux(Ubuntu)](https://ubuntu.com/server/docs/security-trust-store)

Additionally, firefox users should read https://support.mozilla.org/en-US/kb/setting-certificate-authorities-firefox


## Why?

 Without this extension, SDWUI will simply use unencrypted HTTP. Read [this article by cloudflare](https://www.cloudflare.com/learning/ssl/why-is-http-not-secure/) if you would like to better understand why this is bad. But long story short, If an attacker were to join your local network, they would be able to passively listen to your SDWUI traffic and grab entire images without even having direct access to your SDWUI server.
 
 Here's an example of this using [wireshark](https://www.wireshark.org/):
 
By filtering in Wireshark to connections made to my SDWUI and HTTP protocol, we can easily see the HTTP GET and response containing the entire unencrypted image which was generated in SDWUI.
 
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

 [![](https://dcbadge.vercel.app/api/server/Jpc8wnftd4)](https://discord.gg/Jpc8wnftd4)
