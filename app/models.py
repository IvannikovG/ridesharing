from app import db, login
from flask import current_app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime
from time import time
import jwt


@login.user_loader
def load_user(id):
    return Account.query.get(int(id))


coriders = db.Table('coriders',
                    db.Column('ride_id', db.Integer, db.ForeignKey('ride.id')),
                    db.Column('account_id', db.Integer,
                              db.ForeignKey('account.id'))
                    )


class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(150), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cars = db.relationship('Car', backref='owner', lazy='dynamic')
    about_me = db.Column(db.String(200))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    member_since_utc = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id,
                           'exp': time() + expires_in}, app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    def rides(self):
        return Ride.query.join(coriders, (coriders.c.account_id == Account.id)).filter(
            coriders.c.account_id == self.id).order_by(Ride.timestamp.desc())

    @ staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')[
                'reset_password']
        except:
            return

        return Account.query.get(id)

    def __repr__(self):
        return f'<User> {self.username}'


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(64), index=True)
    model = db.Column(db.String(64), index=True)
    color = db.Column(db.String(64), index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __repr__(self):
        return f'<Car> {self.brand} {self.color}'


class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver = db.Column(db.Integer, db.ForeignKey('account.id'))
    car = db.Column(db.Integer, db.ForeignKey('car.id'))
    created_utc = db.Column(db.DateTime, default=datetime.utcnow)
    from_location = db.Column(db.String)
    to_location = db.Column(db.String)
    ride_time = db.Column(db.DateTime, default=datetime.utcnow)
    ride_with = db.relationship('Account', secondary=coriders,
                                backref=db.backref('riders', lazy='dynamic'), lazy='dynamic')
    free_seats = db.Column(db.Integer)
    about_ride = db.Column(db.String(200))
    language = db.Column(db.String(5))
    chat_messages = db.relationship(
        'ChatMessage', backref='ride', lazy='dynamic')

    def subscribe_to_ride(self, user):
        if not self.is_subscribed(user):
            self.ride_with.append(user)

    def unsubscribe_from_ride(self, user):
        if self.is_subscribed(user):
            self.ride_with.remove(user)

    def is_subscribed(self, user):
        return self.ride_with.filter(coriders.c.account_id == user.id).count() > 0

    def has_seats(self):
        return self.free_seats > 0


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'))
    content = db.Column(db.String)
    user_posted = db.Column(db.Integer, db.ForeignKey('account.id'))
    user_posted_username = db.Column(
        db.String, db.ForeignKey('account.username'))
