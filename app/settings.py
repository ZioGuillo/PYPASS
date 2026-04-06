import json
import os
import ssl
import tempfile
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "src" / "config.json"
load_dotenv(BASE_DIR.parent / ".env")

CONFIG_KEYS = {
    "SECRET_KEY_FLASK",
    "SLACK_BOT_TOKEN",
    "domain",
    "BASEDN",
    "user_admin",
    "passwd_admin",
    "slack_db",
    "Slack_Activation",
    "debug",
    "company",
    "RECAPTCHA_PUBLIC_KEY",
    "RECAPTCHA_PRIVATE_KEY",
    "RECAPTCHA_ENABLED",
    "CRT_CERTIFICATE",
    "KEY_CERTIFICATE",
}


def _load_config_file():
    if not CONFIG_PATH.exists():
        return {}

    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def load_settings():
    settings = _load_config_file()

    for key in CONFIG_KEYS:
        value = os.getenv(key)
        if value is not None and value != "":
            settings[key] = value

    return settings


def _resolve_relative_path(path_value):
    if not path_value:
        return ""

    path = Path(str(path_value))
    if not path.is_absolute():
        path = BASE_DIR / "src" / path

    return str(path)


def _write_pem_file(filename, pem_value, mode):
    runtime_dir = Path(tempfile.gettempdir()) / "pypass"
    runtime_dir.mkdir(parents=True, exist_ok=True)

    pem_path = runtime_dir / filename
    normalized_pem = pem_value if pem_value.endswith("\n") else f"{pem_value}\n"
    pem_path.write_text(normalized_pem, encoding="utf-8")
    pem_path.chmod(mode)

    return str(pem_path)


def _resolve_tls_file(settings, file_key, pem_key, filename, mode):
    pem_value = os.getenv(pem_key, "").strip()
    if pem_value:
        return _write_pem_file(filename, pem_value, mode)

    return _resolve_relative_path(settings.get(file_key, ""))


def build_ssl_context(settings):
    cert_path = _resolve_tls_file(settings, "CRT_CERTIFICATE", "CRT_CERTIFICATE_PEM", "tls.crt", 0o644)
    key_path = _resolve_tls_file(settings, "KEY_CERTIFICATE", "KEY_CERTIFICATE_PEM", "tls.key", 0o600)

    if not cert_path or not key_path:
        return None

    cert_file = Path(cert_path)
    key_file = Path(key_path)
    if not cert_file.exists() or not key_file.exists():
        return None

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(str(cert_file), str(key_file))
    return ssl_context