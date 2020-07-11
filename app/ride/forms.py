from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, TextAreaField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email, Length
from app.models import Account
from flask_login import current_user


class CreateRideForm(FlaskForm):
    from_location = StringField(_l('Ride from'), validators=[DataRequired()])
    to_location = StringField(_l('Ride to'), validators=[DataRequired()])
    ride_time = DateTimeField(
        _l('Ride date and time'), format='%d-%m-%y %H:%M')
    cars = SelectField(_l('Car'), choices=[], validate_choice=False)
    free_seats = SelectField(
        _l('Seats'), choices=[1, 2, 3, 4, 5, 6], validate_choice=False)
    about_ride = TextAreaField(_l('About ride'))
    submit = SubmitField(_l('Submit'))


class ChatForm(FlaskForm):
    message = StringField(_l('Your message'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
