from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email, Length
from app.models import Account
from flask_login import current_user


class CreateCarForm(FlaskForm):
    brand = StringField(_l('Car brand'), validators=[DataRequired()])
    model = StringField(_l('Car model'), validators=[DataRequired()])
    color = StringField(_l('Car color'), validators=[DataRequired()])
    submit = SubmitField(_l('Create car'))


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'))
    email = StringField(_l('Email'))
    about_me = TextAreaField(_l('About me'), validators=[
                             Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = Account.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(
                    _l('Please use a different username. This one is taken.'))

    def validate_email(self, email):
        if email.data != self.original_email:
            user = Account.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError(
                    _l('Please use a different email. This one is taken.'))


class DeleteProfileForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
