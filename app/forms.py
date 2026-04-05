from flask import current_app
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class passwdchangeform(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8),
                                                                     EqualTo('new_password')])
    submit = SubmitField('Change Password')
    recaptcha = RecaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not current_app.config.get("RECAPTCHA_ENABLED", True):
            self.recaptcha.validators = []
            self.recaptcha.render_kw = {"disabled": True}


class loginform(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Check')
