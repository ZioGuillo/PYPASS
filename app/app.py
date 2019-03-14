import json

from flask import Flask, render_template, flash, url_for, redirect

from forms import passwdchangeform
from model import reset_passwd

# In the console to get secret key app
# import secrets
# secrets.token_hex(16)

# ===============

file = open("config.json")
variables = json.loads(file.read())

# ===============

app = Flask(__name__)
app.config['SECRET_KEY'] = variables['SECRET_KEY_FLASK']     #
domain = variables['domain']                                 # "contoso.com"
BASEDN = variables['BASEDN']                                 # "OU=Users,dc=contoso,dc=com"
user_admin = variables['user_admin']                         # "administrador"
passwd_admin = variables['passwd_admin']                     # "fsdfsfs#@$SDA"
enable = variables['Slack_Activation']                       #  True  # Slack Activation True to activate


@app.route("/")
@app.route("/reset", methods=['GET', 'POST'])
def reset():
    # context = {}
    form = passwdchangeform()
    if form.validate_on_submit():
        # noinspection PyBroadException
        try:
            if reset_passwd(domain, user_admin, passwd_admin, BASEDN, str(form.username.data), str(form.password.data), str(form.new_password.data), enable=True):
                flash(u'Password reseated for ' + str(form.username.data), 'success')
                return redirect(url_for('reset'))
            else:
                flash(u'Not possible reset your password: ' + str(form.username.data), 'success')
                return redirect("/reset")
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
    # app.run()
    # app.run(ssl_context='adhoc')
    # app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
    app.run(host='0.0.0.0', debug=variables['debug'], ssl_context=('cert.pem', 'key.pem'), port=443)
