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

PyPass is a very simple 1-page web application written in [Python](https://www.python.org/), using [Flask](http://flask.pocoo.org/) , [Angular Material](https://material.angular.io/), [Typescript](http://www.typescriptlang.org/), and [Microsoft Directory Services](https://docs.microsoft.com/en-us/dotnet/api/system.directoryservices) (Default provider).

It allows users to change their Active Directory password on their own, provided the user is not disabled.

PyPass does not require any configuration, as it obtains the principal context from the current domain. There really is no free alternative out there (that I know of) so hopefully this saves someone else some time and money.

### Features

PyPass has the following features:

- Easily localizable
- Supports [reCAPTCHA](https://www.google.com/recaptcha/intro/index.html) (Next Update)
- Has a built-in password meter
- Responsive design that works on mobiles, tablets, and desktops.
- Works with Windows/Linux servers.

<img align="center" src="#"></img>

## Installation

*You can easily install using Powershell. Check the next section to know how.*



## Docker

You can use the Alpine Docker Builder image and then copy the assets over to an Alpine container.

You can pass environment attributes directly into docker without modifying the appsettings.json

```
docker build --rm -t pypass .
docker run \
-e AppSettings__LdapHostnames__0='ad001.example.com' \
-e AppSettings__LdapHostnames__1='ad002.example.com' \
-e AppSettings__LdapPort='636' \
-e AppSettings__LdapUsername='CN=First Last,OU=Users,DC=example,DC=com' \
-it \
-p 80:80 \
passcore:latest
```

## Customization and Configuration

All server-side settings and client-side settings are stored in the `/appsettings.json` file.
The most relevant configuration entries are shown below. Make sure you make your changes to the `appsettings.json` file using a regular text editor like [Visual Studio Code](https://code.visualstudio.com)

- To enable reCAPTCHA
  1. Find the `PrivateKey` entry and enter your private key within double quotes (`"`)
  2. Find the `SiteKey` entry and enter your Site Key within double quotes (`"`)
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

### Running as a sub application

To run as a sub application you need to modify the `base href="/"` value in the `wwwroot/index.html` file to be the base url for PassCore. For example you might have PassCore setup at /PassCore so you would put

```html

```

## Troubleshooting

- At first run if you find an error (e.g. **HTTP Error 502.5**) first ensure you have installed [.NET Core 2.1.1 Windows Server Hosting bundle](https://www.microsoft.com/net/download/thank-you/dotnet-runtime-2.1.1-windows-hosting-bundle-installer), or better.
- If you find an [HTTP Error 500](https://stackoverflow.com/questions/45415832/http-error-500-19-in-iis-10-and-visual-studio-2017) you can try
  1. Press Win Key+R to Open Run Window
  1. in the Run Window, enter "OptionalFeatures.exe"
  1. in the features window, Click: "Internet Information Services"
  1. Click: "World Wide Web Services"
  1. Click: "Application Development Features"
  1. Check the features.
- If you / your user's current password never seems to be accepted for reset; the affected person may need to use a domain-connected PC to login and reset their password on it first. Updated group policy settings could be blocking user changes, until a local login is completed.
- You can add permissions to your log folder using [icacls](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/icacls)
```

```
- If you find [Exception from HRESULT: 0x800708C5 .The password does not meet the password policy requirements](http://blog.cionsystems.com/?p=907) trying to change a password. Set 'Minimum password age' to 0 at 'Default Domain Policy'.

### LDAP Support

- If your users are having trouble changing passwords as in issues #8 or #9 : try configuring the section `PasswordChangeOptions` in the `/appsettings.json` file. Here are some guidelines:
  1. Ensure `UseAutomaticContext` is set to `false`
  1. Ensure `LdapUsername` is set to an AD user with enough permissions to reset user passwords
  1. Ensure `LdapPassword` is set to the correct password for the admin user mentioned above
  1. User @gadams65 suggests the following: Use the FQDN of your LDAP host. Enter the LDAP username without any other prefix or suffix such as `domain\\` or `@domain`. Only the username.
- You can also opt to use the Linux or MacOS version of PassCore. This version includes a LDAP Provider based on Novell. The same provider can be used with Windows, you must build it by yourself.


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


## Create your own provider

If you wish to create your owen provider, you need use our interface and common classes. You can use the following nuget to install them:


```
## License

PyPass is open source software and MIT licensed. Please star this project if you like it.