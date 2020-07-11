from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email, Length
from app.models import Account
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember me'))
    submit = SubmitField(_l('Sign in'))


class RegisterForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    repeat_password = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Sign in'))

    def validate_username(self, username):
        user = Account.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_l('Please use a different username'))

    def validate_email(self, email):
        user = Account.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(_l('Please use a different email'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    repeat_password = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Reset'))
