import json
from flask import Flask, render_template, flash, url_for, redirect
from forms import passwdchangeform
from model import reset_passwd
import ssl

# In the console to get secret key app
# import secrets
# stk = secrets.token_hex(16)

# ===============

file = open("src/config.json")
variables = json.loads(file.read())

ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ctx.load_cert_chain('src/' + variables['CRT_CERTIFICATE'], 'src/' + variables['KEY_CERTIFICATE'])

# ===============

app = Flask(__name__)
app.config['SECRET_KEY'] = variables['SECRET_KEY_FLASK']     #
app.config['RECAPTCHA_PUBLIC_KEY'] = variables['RECAPTCHA_PUBLIC_KEY']
app.config['RECAPTCHA_PRIVATE_KEY'] = variables['RECAPTCHA_PRIVATE_KEY']
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
            if reset_passwd(domain, user_admin, passwd_admin, BASEDN, str(form.username.data), str(form.password.data),
                            str(form.new_password.data), enable=enable):
                flash(u'Your password was changed for: ' + str(form.username.data), 'success')
                return redirect(url_for('reset'))
            else:
                flash(u'Not possible reset the password for: ' + str(form.username.data), 'success')
                return redirect("reset")
        except ValueError:
            pass

    return render_template('reset.html', title='AD Password Reset | ' + variables['company'],
                           form=form, company=variables['company'])


# 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    # Only for debugging while developing

    # app.run(host='0.0.0.0', debug=variables['debug'])
    app.run(debug=variables['debug'], host='0.0.0.0', port=5000, ssl_context=ctx)
    # app.run()
    # app.run(ssl_context='adhoc')
    # app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
    # app.run(host='0.0.0.0', debug=variables['debug'], ssl_context=('cert.pem', 'key.pem'), port=443)
