from app import db, mail
from app.main import bp
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required
from wtforms import SelectField
from app.main.forms import CreateCarForm, EditProfileForm, DeleteProfileForm
from app.models import Account, Car, Ride, coriders, ChatMessage
from app.translate import translate
from werkzeug.urls import url_parse
from datetime import datetime
from flask_babel import _, lazy_gettext as _l, get_locale
import os
from guess_language import guess_language


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    current_rides = Ride.query.join(coriders, coriders.c.ride_id == Ride.id).filter(
        coriders.c.account_id == current_user.id)
    req = request.args
    return render_template('main/index.html', title='Home', current_rides=current_rides, req=req)


@bp.route('/create_car', methods=['GET', 'POST'])
@login_required
def create_car():
    form = CreateCarForm()
    if form.validate_on_submit():
        car = Car(brand=form.brand.data,
                  model=form.model.data, color=form.color.data, owner=current_user)
        db.session.add(car)
        db.session.commit()
        flash(_('Your car has been created. Find it in your profile'))
        return redirect(url_for('main.index'))
    return render_template('main/create_car.html', title='Create Car', form=form)


@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = Account.query.filter_by(username=username).first_or_404()
    cars = Car.query.filter_by(owner_id=current_user.id)
    page = request.args.get('page', 1, type=int)
    req = request.args
    rides_as_driver = Ride.query.filter_by(driver=current_user.id).paginate(
        page, current_app.config['RIDES_PER_PAGE'], False)
    next_url = url_for('main.user', username=current_user.username, page=rides.next_num) \
        if rides_as_driver.has_next else None
    prev_url = url_for('main.user', username=current_user.username, page=rides.prev_num) \
        if rides_as_driver.has_prev else None
    return render_template('main/user.html', user=user,
                           cars=cars, rides_as_driver=rides_as_driver.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash(_('Edited profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.dat = current_user.about_me

    return render_template('main/edit_profile.html', form=form)


@bp.route('/delete_profile', methods=['GET', 'POST'])
@login_required
def delete_profile():
    form = DeleteProfileForm()
    if form.validate_on_submit():
        flash(_('Form valid'))
        if not current_user.email == form.email.data:
            flash('Enter YOUR email')
            return redirect(url_for('main.delete_profile'))
        else:
            user = Account.query.filter_by(email=form.email.data).first()

            if user.check_password(form.password.data):
                db.session.delete(current_user)
                db.session.commit()
                flash('Deleted account')
                return redirect(url_for('auth.register'))
            else:
                flash('Account can not be deleted using this credentials')
                return redirect(url_for('main.delete_profile'))
    return render_template('main/delete_profile.html', form=form)


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['original_language'],
                                      request.form['target_language'])})
