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
- Has a built-in password meter
- Responsive design that works on mobiles, tablets, and desktops.
- Works with Windows/Linux servers.

<img align="center" src="src/screen.png"></img>

## Installation

*You can easily install using Python3 and Flask. Check the next section to know how.*

*To enable ldap services in the server(Windows) you need to install the Certificate services on the server. [Follow this steps to do it](https://www.watchguard.com/help/docs/ssl/3/en-us/content/en-us/manage_system/active_directory_auth_w-ldap-ssl.html)*



## Docker

You can use the Alpine Docker Builder image and then copy the assets over to an Alpine container.

You can pass environment attributes directly into docker without modifying the appsettings.json

```


```

## Customization and Configuration

All server-side settings and client-side settings are stored in the `/appsettings.json` file.
The most relevant configuration entries are shown below. Make sure you make your changes to the `config.json` file using a regular text editor like [Visual Studio Code](https://code.visualstudio.com) or [sublime Text](https://www.sublimetext.com/).

This is the Format of the config file:

``` json
{
  "SECRET_KEY_FLASK": "werewtrwetewrwer53535353",
  "SLACK_BOT_TOKEN" : "xoxb-",
  "domain": "",
  "BASEDN": "OU=Users,dc=domain,dc=com",
  "user_admin" : "admin-user",
  "passwd_admin" : "",
  "slack_db" : "",
  "Slack_Activation" : "False",
  "debug": "True",
  "company": "DIGITALEBRAIN",
  "RECAPTCHA_PUBLIC_KEY": "",
  "RECAPTCHA_PRIVATE_KEY": ""
}
```


- To enable The Secret Key in the App:
  1. Find the `PrivateKey` entry and enter your private key within double quotes (`"`)
  2. Find the `SiteKey` entry and enter your Site Key within double quotes (`"`)

  "SECRET_KEY_FLASK": "werewtrwetewrwer53535353",
  "SLACK_BOT_TOKEN" : "xoxb-",
  "domain": "",
  "BASEDN": "OU=Users,dc=domain,dc=com",
  "user_admin" : "admin-user",
  "passwd_admin" : "",
  "slack_db" : "",
  "Slack_Activation" : "False",
  "debug": "True",
  "company": "DIGITALEBRAIN",
  "RECAPTCHA_PUBLIC_KEY": "",
  "RECAPTCHA_PRIVATE_KEY": ""

- To change the language of the reCAPTCHA widget
  - Find the `LanguageCode` entry and enter [one of the options listed here](https://developers.google.com/recaptcha/docs/language). By default this is set to `en`
- To enable/disable the password meter
  - Find the `ShowPasswordMeter` entry and set it to `true` or `false` (without quotes)
- To enable restricted group checking
  1. Find the `CheckRestrictedAdGroups` entry and set it to `true` (without quotes)
  2. Find the `RestrictedADGroups` entry and add any groups that are sensitive.  Accounts in these groups (directly or inherited) will not be able to change their password.
- Find the `DefaultDomain` entry and set it to your default Active Directory domain. This should eliminate confusion about using e-mail domains / internal domain names. **NOTE:** if you are using a subdomain, and you have errors, please try using your top-level domain. Thank you.
- To provide an optional paramerter to the URL to set the username text box automatically
  1. `http://mypasscore.com/?userName=someusername`
  2. This helps the user incase they forgot thier username and, also comes in handy when sending a link to the application or having it embeded into another application were the user is all ready signed in.
- To specify which (DC) attribute is used to search for the specific user.
  - With the `IdTypeForUser` it is possible to select one of six Attributes that will be used to search for the specifiv user.
  - The possible values are:
    - `DistinguishedName` or `DN`
    - `GloballyUniqueIdentifier` or `GUID`
    - `Name`
    - `SamAccountName` or `SAM`
    - `SecurityIdentifier` or `SID`
    - `UserPrincipalName` or `UPN`
- The rest of the configuration entries are all pretty much all UI strings. Change them to localize, or to brand this utility, to meet your needs.


## Troubleshooting

- None Reported

### LDAP Support

- None reported


## Build your own version

If you need to modify the source code (either backend or frontend). You require Python3 and Flask. Run the following command according to your target platform.

### Windows

```

```

### Linux (portable)

```

```

### MacOS (OS X)

```

```

*Note* -


```
## License

PyPass is open source software and [MIT licensed]. Please star this project if you like it.(LICENSE)

```