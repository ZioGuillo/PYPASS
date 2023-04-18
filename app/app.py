import secrets
from flask import render_template, json, redirect, url_for, Flask
from flask_wtf import CSRFProtect
from forms import passwdchangeform

file = open("src/config.json")
variables = json.loads(file.read())

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['RECAPTCHA_PUBLIC_KEY'] = variables['RECAPTCHA_PUBLIC_KEY']
app.config['RECAPTCHA_PRIVATE_KEY'] = variables['RECAPTCHA_PRIVATE_KEY']
csrf = CSRFProtect(app)


@app.route('/')
def hello_world():
    data = 'Hello World01!'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/html'),
        ('Content-Length', str(len(data)))
    ]
    return render_template('index.html', data=data)


@app.route('/reset', methods=['GET', 'POST'])
def password_change():
    form = passwdchangeform()
    if form.validate_on_submit():
        # handle form submission here
        # e.g. retrieve form data and call reset_password function
        # then redirect to success page
        return redirect(url_for('reset'))
    return render_template('reset.html', form=form)


@app.route('/changed')
def password_changed():
    return 'Your password has been changed successfully!'


@app.route('/<path:dummy>')
def page_not_found(dummy):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
