# Active Directory Password Reset Service ![PyPass Logo](src/pypass.png)
# PyPass: A self-service password change utility for Active Directory

*:star: Please star this project if you find it useful!*

- [PyPass: A self-service password change utility for Active Directory](#pypass-a-self-service-password-change-utility-for-active-directory)
  - [Overview](#overview)
    - [Features](#features)
  - [Installation](#installation)
  - [Docker](#docker)
  - [Customization and Configuration](#customization-and-configuration)
    - [Slack](#slack)
  - [Troubleshooting](#troubleshooting)
    - [LDAP Support](#ldap-support)
  - [Build your own version](#build-your-own-version)
  - [Create your own provider](#create-your-own-provider)
  - [License](#license)

## Overview

PyPass is a very simple 1-page web application written in [Python](https://www.python.org/), using [Flask](http://flask.pocoo.org/) , [Angular Material](https://material.angular.io/), [Ldap3](https://ldap3.readthedocs.io/), and [Microsoft Directory Services](https://docs.microsoft.com/en-us/dotnet/api/system.directoryservices) (Default provider).

It allows users to change their Active Directory password on their own, provided the user is not disabled.

PyPass does not require any configuration, as it obtains the principal context from the current domain. There really is no free alternative out there (that I know of) so hopefully this saves someone else some time and money.

### Features

PyPass has the following features:

- Easily localizable
- Supports [reCAPTCHA](https://www.google.com/recaptcha/intro/index.html)
- Responsive design that works on mobiles, tablets, and desktops.
- Works with Windows/Linux servers.

<img align="center" src="src/screen.png"></img>

## Installation

*You can easily install using Python3 and Flask. Check the next section to know how.*

*To enable ldap services in the server(Windows) you need to install the Certificate services on the server.
[Follow this steps to do it](https://www.watchguard.com/help/docs/ssl/3/en-us/content/en-us/manage_system/active_directory_auth_w-ldap-ssl.html)*


## Docker

1.  Just clone the repo and Modify the *config.json* file with the correct entries.
2.  After run the follow docker command:

    ``` docker
    >>>docker build -t pypass:latest .
    ```
3.  Run the Docker command to run the image:

    ```docker
    >>>docker run --dns <ip of your DNS server or AD> --name pypaxs -d -p 80:5000 --rm pypass:latest
    ```
By default the container will be run in the port:5000 and localhost. With this command you can route the port to the 80 or any you prefer.


## Customization and Configuration

All server-side settings and client-side settings are stored in the `src/config.json` file inside the APP folder.
The most relevant configuration entries are shown below. Make sure you make your changes to the `config.json` file using a regular text editor like [Visual Studio Code](https://code.visualstudio.com) or [sublime Text](https://www.sublimetext.com/).

This is the Format of the config file:

``` json
{
  "SECRET_KEY_FLASK": "werewtrwetewrwer53535353",
  "SLACK_BOT_TOKEN" : "xoxb-",
  "domain": "domain.com",
  "BASEDN": "OU=Users,dc=domain,dc=com",
  "user_admin" : "admin-user",
  "passwd_admin" : "password_admin",
  "slack_db" : "slack_db.json",
  "Slack_Activation" : "False",
  "debug": "True",
  "company": "DIGITALEBRAIN",
  "RECAPTCHA_PUBLIC_KEY": "GOOGLE CODE",
  "RECAPTCHA_PRIVATE_KEY": "GOOGLE CODE"
}
```


1.  To enable The Secret Key in the App:
    Find the `SECRET_KEY_FLASK` entry and enter your private key:
    To create your personal SECRET_KEY_FLASK In a command promt do the following:
    ``` command
    >>>python3
    Python 3.7.2
    [Clang 10.0.0 (clang-1000.11.45.5)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import secrets
    >>> stk = secrets.token_hex(16)
    >>> print(stk)
    ```
    Copy the code in the entrie.

2.  Find the `SLACK_BOT_TOKEN` entry and enter your Slack Token
    To get your slack Token [follow this steps](https://get.slack.help/hc/en-us/articles/215770388-Create-and-regenerate-API-tokens) and your Token need to start with *xoxb-*

3. For the AD Credentials need to have admin priviligies or the user be able to change passwords.

    ``` json
    "domain": "domain.com",
    "BASEDN": "OU=Users,dc=domain,dc=com",
    "user_admin" : "admin-user",
    "passwd_admin" : "password_admin",
    ```
## Slack

4. To enable and use the slack notification, you need to download the slack DB in a file and put in the same folder *SRC FOLDER* of the config file.
    - To Download the Slack DB do the follow.
    - Create a Python file and put this code:

    ``` python
    import json
    from slackclient import SlackClient

    SLACK_BOT_TOKEN = "xoxb-YOUR-TOKEN"
    data = json.dumps(sc.api_call("users.list"), indent=4, sort_keys=True)
    print(data)
    ```

    Once in the command promt line export the results in a JSON file:

    ``` cmd
    >>>python3 slack_file.py >> slack_db.json

    ```
    The File have to be in the *src* folder and put the complete name of the file in the entrie ```"slack_db" : "slack_db.json",```
    Once you have that change the ```"Slack_Activation" : "False"``` to ```True```.

5.  Put the Recaptcha Codes in the entries:

    ``` json
    "RECAPTCHA_PUBLIC_KEY": "GOOGLE CODE",
    "RECAPTCHA_PRIVATE_KEY": "GOOGLE CODE"
    ```
    To get this codes [click in this link](https://developers.google.com/recaptcha/)

6.  The rest of the configuration entries are all pretty much all UI strings. Change them to localize, or to brand this utility, to meet your needs.

## Troubleshooting

- None Reported

### LDAP Support

- None reported


## Build your own version

If you need to modify the source code (either backend or frontend). You require Python3 and Flask.


*Note* -


## License

PyPass is open source software and [MIT licensed](https://github.com/ZioGuillo/PYPASS/blob/master/LICENSE). *Please star this project if you like it.*