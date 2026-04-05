import json
import socket
import ssl
from pathlib import Path

from flask import Flask, render_template, flash, url_for, redirect, jsonify

from forms import passwdchangeform
from model import reset_passwd

# In the console to get secret key app
# import secrets
# stk = secrets.token_hex(16)pip install 

# ===============

base_dir = Path(__file__).resolve().parent
config_path = base_dir / "src" / "config.json"
with config_path.open("r", encoding="utf-8") as config_file:
    variables = json.load(config_file)

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(
    str(base_dir / "src" / variables["CRT_CERTIFICATE"]),
    str(base_dir / "src" / variables["KEY_CERTIFICATE"]),
)

# ===============

app = Flask(__name__)
app.config['SECRET_KEY'] = variables['SECRET_KEY_FLASK']     #
recaptcha_public = variables.get('RECAPTCHA_PUBLIC_KEY', '').strip()
recaptcha_private = variables.get('RECAPTCHA_PRIVATE_KEY', '').strip()
recaptcha_flag = str(variables.get('RECAPTCHA_ENABLED', True)).lower() in {"true", "1", "yes"}
recaptcha_enabled = recaptcha_flag and bool(recaptcha_public and recaptcha_private)

app.config['RECAPTCHA_PUBLIC_KEY'] = recaptcha_public
app.config['RECAPTCHA_PRIVATE_KEY'] = recaptcha_private
app.config['RECAPTCHA_ENABLED'] = recaptcha_enabled
app.config['TESTING'] = variables['debug']
domain = variables['domain']                                 # "contoso.com"
BASEDN = variables['BASEDN']                                 # "OU=Users,dc=contoso,dc=com"
user_admin = variables['user_admin']                         # "administrador"
passwd_admin = variables['passwd_admin']                     # "fsdfsfs#@$SDA"
enable = variables['Slack_Activation']                       #  True  # Slack Activation True to activate


@app.route("/", methods=['GET', 'POST'])
@app.route("/reset", methods=['GET', 'POST'])
def reset():
    # context = {}
    form = passwdchangeform()
    if form.validate_on_submit():
        # noinspection PyBroadException
        try:
            if reset_passwd(
                domain,
                user_admin,
                passwd_admin,
                BASEDN,
                str(form.username.data),
                str(form.password.data),
                str(form.new_password.data),
                enable=enable,
            ):
                flash(u"Your password was changed for: " + str(form.username.data), "success")
                return redirect(url_for("reset"))
            else:
                flash(u"Not possible reset the password for: " + str(form.username.data), "success")
                return redirect("reset")
        except ValueError:
            pass
        except Exception:
            flash(
                "Could not connect to the directory server. Please try again later.",
                "danger",
            )

    return render_template(
        'reset.html',
        title='AD Password Reset | ' + variables['company'],
        form=form,
        company=variables['company'],
        recaptcha_enabled=recaptcha_enabled,
    )


def _ldap_reachable(host, port=636, timeout=2.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


@app.get("/health/ldap")
def ldap_health():
    return jsonify({"ok": _ldap_reachable(domain)})


@app.get("/.well-known/appspecific/com.chrome.devtools.json")
def chrome_devtools_probe():
    return "", 204


# 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    # Only for debugging while developing

    # app.run(host='0.0.0.0', debug=variables['debug'])
    app.run(debug=variables['debug'], host='0.0.0.0', port=443, ssl_context=ctx)
    # app.run()
    # app.run(ssl_context='adhoc')
    # app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
    # app.run(host='0.0.0.0', debug=variables['debug'], ssl_context=('cert.pem', 'key.pem'), port=443)
