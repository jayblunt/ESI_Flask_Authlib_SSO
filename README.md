# ESI Single Sign On sample with Flask and Authlib

The [Eve Online](https://www.eveonline.com/) [Swagger Interface](https://esi.evetech.net/ui/) uses OAUTH2 for authorization. 

There is a CCP blog entry ([ESI STEP BY STEP - SSO TO AUTHENTICATED CALLS](https://developers.eveonline.com/blog/article/sso-to-authenticated-calls)) that walks through the process.

There is also a repository example by @Kyria [here](https://github.com/Kyria/flask-esipy-example).

[Authlib](https://authlib.org/) makes the process much simpler. 

This snippet uses Authlib and Flask to implement basic SSO for Eve. It assumes that you have a registered [application](https://developers.eveonline.com/applications) that you are using.

As of writing, the Eve SSO is not OpenID compatible - the OpenID scopes are not available and there is no standard id_token. This example works around this by decoding the access token and using that as the userinfo.
