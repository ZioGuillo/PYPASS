# PyPass - Active Directory Password Reset Service

![Python](https://img.shields.io/badge/python-3.12-blue)
![Flask](https://img.shields.io/badge/flask-3.x-black)
![LDAP](https://img.shields.io/badge/ldap-ldaps-2f855a)
![Docker](https://img.shields.io/badge/docker-ready-2496ed)

PyPass is a simple self-service password change web app for Active Directory. It is built with Python, Flask, LDAP3, and a lightweight UI.

![PyPass Logo](src/pypass.png)

## Features

- Self-service password reset for AD users
- reCAPTCHA support
- Responsive UI for mobile and desktop
- Optional Slack notifications
- LDAP connectivity status badge (top-right)
- UI renders even if LDAP is offline (badge turns red)

## Requirements

- Python 3.12
- LDAP server reachable on port 636 (LDAPS)

## Quick start (local)

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r app/requirements.txt
cp .env.example .env
PYTHONPATH=app .venv/bin/flask --app app run --host 0.0.0.0 --port 5001
```

Open http://127.0.0.1:5001

## Configuration


## Configuration: Required Environment Variables

Set these variables in your `.env` file (for local/dev) or as GitHub/CI/CD secrets (for production):

```dotenv
# Flask secret key (required)
SECRET_KEY_FLASK=replace-with-flask-secret

# LDAP/Active Directory connection
DOMAIN=your-ldap-server.example.com
BASEDN=OU=Users,DC=example,DC=com
USER_ADMIN=your-ldap-service-account
PASSWD_ADMIN=your-ldap-service-password

# Slack integration (optional)
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_ACTIVATION=True

# Google reCAPTCHA (optional but recommended)
RECAPTCHA_PUBLIC_KEY=your-recaptcha-site-key
RECAPTCHA_PRIVATE_KEY=your-recaptcha-secret-key
RECAPTCHA_ENABLED=True

# TLS/SSL certificates (required for HTTPS)
CRT_CERTIFICATE=app/src/name.crt
KEY_CERTIFICATE=app/src/name.key

# App/company info (optional)
COMPANY=YourCompanyName
DEBUG=True
```


### For GitHub Actions or other CI/CD

Add the same variables as repository or environment secrets. All sensitive values (passwords, tokens, keys) must be set as secrets, not in code or config files.

**TLS assets:**
- You can provide certificate/key as file paths (`CRT_CERTIFICATE`, `KEY_CERTIFICATE`) or as inline PEM values (`CRT_CERTIFICATE_PEM`, `KEY_CERTIFICATE_PEM`).


### Generate a Flask secret key

```bash
python3.12 - <<'PY'
import secrets
print(secrets.token_hex(16))
PY
```


### LDAP status badge

The UI shows a green/red indicator based on `/health/ldap`, which attempts a TCP connect to the configured LDAP host on port 636. The page still loads if LDAP is offline, so you can verify the UI and config without a live LDAP connection. When LDAP is available, the badge turns green.


## reCAPTCHA Setup

PyPass uses Google reCAPTCHA via Flask-WTF.

1. Create keys at https://www.google.com/recaptcha/admin/create

2. Set `RECAPTCHA_PUBLIC_KEY` and `RECAPTCHA_PRIVATE_KEY` in `.env` or your deployment environment:

```dotenv
RECAPTCHA_PUBLIC_KEY=YOUR_SITE_KEY
RECAPTCHA_PRIVATE_KEY=YOUR_SECRET_KEY
RECAPTCHA_ENABLED=True
```

If you want to disable reCAPTCHA, set `RECAPTCHA_ENABLED` to `False`.


## LDAP Setup Guide

To enable LDAP/LDAPS connectivity from any LDAP server, confirm the items below:

1. **LDAPS endpoint**
  - Ensure the LDAP server supports LDAPS on port 636.
  - Open firewall rules to allow inbound 636 from the app host.
  - If you must use LDAP (389), update the code to use port 389 and disable SSL (not recommended).

2. **Certificates (LDAPS)**
  - The LDAP server must present a valid certificate.
  - If you use an internal CA, add the CA certificate to the OS trust store on the app host.

3. **Service account**
  - Create an LDAP user/service account with permission to read user attributes and change passwords.
  - In Active Directory, the account must be allowed to reset passwords for the target OU.

4. **Environment variables**
  - `DOMAIN`: LDAP hostname or IP (e.g., `ldap.example.com`)
  - `BASEDN`: Base DN for users (e.g., `OU=Users,DC=example,DC=com`)
  - `USER_ADMIN` / `PASSWD_ADMIN`: service account credentials

5. **Connectivity tests (optional)**
  - Test TLS handshake:
    ```bash
    openssl s_client -connect ldap.example.com:636
    ```
  - Test LDAP bind (if you have ldapsearch):
    ```bash
    ldapsearch -H ldaps://ldap.example.com:636 -D "user@example.com" -W -b "OU=Users,DC=example,DC=com"
    ```

If LDAP is unreachable, the app will still render and show a warning message, and the status badge turns red.


## Slack Setup


To enable Slack notifications:

1. Set `SLACK_BOT_TOKEN` and `SLACK_ACTIVATION=True` in your `.env` or deployment environment.
2. Export your Slack user list and save it in `app/src/`:

```python
import json
from slack_sdk import WebClient

SLACK_BOT_TOKEN = "xoxb-YOUR-TOKEN"
sc = WebClient(token=SLACK_BOT_TOKEN)
response = sc.users_list()
data = json.dumps(response.data, indent=4, sort_keys=True)
print(data)
```



Set `SLACK_BOT_TOKEN` in `.env` or your deployment environment before running this script.

```bash
python3.12 slack_file.py >> app/src/slack_db.json
```


## Docker

```bash
docker build -t pypass:latest .
docker run --dns <dns-or-ad-ip> --env-file .env --name pypass -d -p 80:5000 --rm pypass:latest
```


## Kubernetes (Example)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pypass
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pypass
  template:
    metadata:
      labels:
        app: pypass
    spec:
      containers:
        - name: pypass
          image: pypass:latest
          ports:
            - containerPort: 5000
          env:
            - name: PYTHONPATH
              value: "/app"
          volumeMounts:
            - name: config
              mountPath: /app/src/config.json
              subPath: config.json
      volumes:
        - name: config
          configMap:
            name: pypass-config
---
apiVersion: v1
kind: Service
metadata:
  name: pypass
spec:
  selector:
    app: pypass
  ports:
    - port: 80
      targetPort: 5000
```


Create a ConfigMap named `pypass-config` with your `config.json` before applying the manifest.

For secrets, use Kubernetes Secrets or your platform's secret store and expose them as environment variables with the same names shown in `.env.example`.


## Troubleshooting

- If LDAP is unreachable, the app shows a warning message and the status badge turns red.
- For LDAPS on Windows, ensure certificate services are installed on the domain controller.


## License

MIT. See [LICENSE](LICENSE).