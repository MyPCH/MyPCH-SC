# MyPCH proxy 
This demo will show how a third party micro service can hook in between the Tidepool client and backend.

For the MyPCH project this directory can be used to establish an end-2-end demo for real-world use cases.

It will demo how e.g. SCs can be integrated into the TP platform and deals
with the two gaps (authentification and encryption of data at rest) that 
were revealed during the initial analysis pertaining to the
specification of the requirements. A service that lack these properties will be able to integrate with the platform either directly by extending the proxy itself or indirectly by using the API of the proxy in their integration of the service.

## A prototype for a local demo
A prototype for a local demo (USB stick)

1. Build current proxy and upload to a docker repository available for the
kubernetes cluster used in 3.

2. Install the [tidepool uploader](https://github.com/tidepool-org/uploader) and adjust the API_URL to point to the local proxy.

3. Install the [tidepool backend](https://github.com/tidepool-org/development) and add a k8s manifest for the proxy to include it in the platform.

4. Adjust port-forwarding to the cluster to expose the proxy and to remove the exposure of the default API_URL. Configure the proxy to use the internal API_URL for forwarding POST requests.

## A prototype online

A public available front-end that will expose how the integration and the specific 
integration requirements (cf. the [Swagger](https://swagger.io/) interface that returns expected results depending on the active user). 

The demo is a template written in Python using Flask web application framework and deployed in [Heroku](https://www.heroku.com/). 

In the code we have marked a placeholder to handle the logic for GET/POST. In this case a SC-hook for integration to Semantic Container features.  

### Multiple users
As template for real-world use cases you can use the file account to describe different scenarios of multiple users in the same environment. The backend is refered to as a Health Data Store (HDS).

Examples of scenarios with users as patients, doctors from clinic and reseachers:

User scenario | Role |  Belongs to | Username | Post |Role Response 
------------ | -------------| -------------| -------------| -------------| -------------
private patient | patient | tpgroup | mypchtryinghard | You shall have access to watermarked data from ... |You are a RW user shall be able to upload valid data ...
patient1 at clinic1 | patient | clinic 1 | mypchpwd1 | You have full access to watermarked data from own account. You shall also have access to watermarked data from mypchpwd2 ... |You are a RW user and as allowed to send POST requests ...
patient2 at clinic1 | patient | clinic 1 | mypchpwd2 | You have full access to watermarked data from own account. You shall also have access to watermarked data from mypchpwd3 ... |You are a RW user and as allowed to send POST requests ...
patient2 at clinic1 | patient | clinic 2 | mypchpwd3 | You have full access to data from own account. You shall not be able to access data from others |You are a RW user and as allowed to send POST requests ...
doctor1 at clinic1 | advisor | clinic 1 | mypchcl1d1 | You have full access to watermarked data from all patients in the specific clinic |You are a RO user and is NOT allowed to send POST requests ...
doctor2 at clinic1 | advisor | clinic 1 | mypchcl1d2 | You have full access to watermarked data from all patients in the specific clinic. You also have access to aggregated data from a patient in another clinic |You are a RO user and is NOT allowed to send POST requests ...
reseacher at clinic | researcher | clinic 1 | mypchr1u1 | You have anonymouns and partial access to data from some patients |You are a RO user and is NOT allowed to send POST requests ...
reseacher1 at institute1 | researcher | 3rd party | mypchi1u1 |  You have partial (time and data types) access to watermarked data from some patients |You are a RO user and is NOT allowed to send POST requests ...
reseacher2 at institute1 | researcher | 3rd party | mypchi1u2 |  You have partial (time and data types) access to watermarked data from some patients |You are a RO user and is NOT allowed to send POST requests ...
reseacher1 at institute2 | researcher | 3rd party | mypchi2u1 |  You have partial (time and data types) access to watermarked data from some patients |You are a RO user and is NOT allowed to send POST requests ...

### Env variables for deployment
You'll need to set the following environment variables using heroku UI or heroku 
CLI:

- *GOOGLE_OAUTH_CLIENT_ID* set this to the client ID you got from Google.
- *GOOGLE_OAUTH_CLIENT_SECRET* set this to the client secret you got from Google.
- *FLASK_SECRET_KEY*: set this to a proper secret, cf. below
- *OAUTHLIB_RELAX_TOKEN_SCOPE* set to true

Use the following command to generate a decent value for the *FLASK_SECRET_KEY* 

```
$ python -c 'import os; print(os.urandom(16))'
```

Running with env variables in the dynos are only acceptable for initial flow tests 
where we pass bogus data around but will **not** be acceptable when we shall demo 
it with real devices. 

## OAuth credentials 
In this demo we use Google as our identity provider and hence need to construct app endpoint specific credentials. Go to the [Google Developers Console](https://console.developers.google.com) and create a new project and fill in the "Configure consent screen" under Web Application.

You need to fill in your heroku endpoint into "Authorized JavaScript origins" and
"Authorized redirect URIs". Once filled in, click "Create Client ID" and you 
will get a client ID and a client secret which is needed in the heroku env.

# Design notes: Security
## Authentification
The code will run in the cloud and we have to put some focus on security
aspects. We will require that access is limited to a set of individually 
authenticated users. As to the authentication itself, there is no need 
to re-invent the wheel, so we will use [OpenID Connect](https://openid.net/connect/) 
and we will pick an identity provider that have state-of-the art 
[U2F](https://en.wikipedia.org/wiki/Universal_2nd_Factor) support.

## Encryption
For initial tests, using environment variables for the demos are OK. To use in a real-world demo with upload data from real devices and using unencrypted environment variables will not meet state-of-the-art. Such demo shall use proper secret management supported by an [HSM](https://en.wikipedia.org/wiki/Hardware_security_module) so that
environment variables are not exposed in cleartext in the dynos.

We have used YubiKeys in our experiments.

## Standard and security validators
We believe in standards and best practices validators such as:

[W3 validator](https://validator.w3.org/)

[HTTPS security headers](https://securityheaders.com/) 

![Security Headers](https://img.shields.io/security-headers?url=https%3A%2F%2Fmypch.herokuapp.com)

An initial example of the prototype build online in Heroku can found at [online demo](https://mypch.herokuapp.com) with login or [online demo random](https://mypchrandom.herokuapp.com/) without login, which show  a random of the use cases when you push login.


