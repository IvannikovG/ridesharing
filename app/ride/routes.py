from app import db
from app.ride import bp
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required
from wtforms import SelectField
from app.ride.forms import CreateRideForm, ChatForm
from app.models import Account, Car, coriders, Ride, ChatMessage
from app.translate import translate
from werkzeug.urls import url_parse
from datetime import datetime
from flask_babel import _, lazy_gettext as _l, get_locale
import os
from app.email import send_email
from app.auth.email import send_password_reset_email
from guess_language import guess_language


@bp.route('/create_ride', methods=['GET', 'POST'])
@login_required
def create_ride():
    form = CreateRideForm()
    cars = Car.query.filter_by(owner_id=current_user.id).all()
    form.cars.choices = [(car.id, car.brand) for car in cars]
    if form.validate_on_submit():
        language = guess_language(form.about_ride.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        ride = Ride(driver=current_user.id,
                    car=form.cars.data,
                    from_location=form.from_location.data,
                    to_location=form.to_location.data,
                    ride_time=form.ride_time.data,
                    free_seats=form.free_seats.data,
                    about_ride=form.about_ride.data,
                    language=language)
        db.session.add(ride)
        db.session.commit()
        flash(_('Ride was created'))
        return redirect(url_for('ride.available_rides'))
    return render_template('ride/create_ride.html', form=form)


@bp.route('/available_rides', methods=['GET'])
@login_required
def available_rides():
    page = request.args.get('page', 1, type=int)
    req = request.args
    rides = Ride.query.filter(Ride.free_seats > 0).paginate(
        page, current_app.config['RIDES_PER_PAGE'], False)
    next_url = url_for('ride.available_rides', page=rides.next_num) \
        if rides.has_next else None
    prev_url = url_for('ride.available_rides', page=rides.prev_num) \
        if rides.has_prev else None
    return render_template('ride/available_rides.html',
                           rides=rides.items, next_url=next_url, prev_url=prev_url, req=req)


@bp.route('/subscribe_to_ride/<ride_id>', methods=['GET', 'POST'])
@login_required
def subscribe_to_ride(ride_id):
    ride = Ride.query.filter_by(id=ride_id).first()
    ride.free_seats -= 1
    ride.subscribe_to_ride(current_user)
    db.session.add(ride)
    db.session.commit()
    flash(_('Subscribed to ride'))
    return redirect(url_for('ride.chat', ride_id=ride.id))


@bp.route('/unsubscribe_from_ride/<ride_id>', methods=['GET', 'POST'])
@login_required
def unsubscribe_from_ride(ride_id):
    ride = Ride.query.filter_by(id=ride_id).first()
    ride.unsubscribe_from_ride(current_user)
    ride.free_seats += 1
    db.session.add(ride)
    db.session.commit()
    flash(_('Unsubscribed from ride'))
    return redirect(url_for('main.index'))


@bp.route('/chat/<ride_id>', methods=['GET', 'POST'])
@login_required
def chat(ride_id):
    form = ChatForm()
    ride = Ride.query.filter_by(id=ride_id).first()
    messages = ChatMessage.query.filter_by(ride_id=ride_id)
    if form.validate_on_submit():
        message = ChatMessage(
            ride_id=ride.id, content=form.message.data,
            user_posted=current_user.id,
            user_posted_username=current_user.username)
        db.session.add(message)
        db.session.commit()
    return render_template('ride/chat.html', ride=ride, form=form, messages=messages)
