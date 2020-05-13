import itsdangerous
from flask import Blueprint, render_template, request, redirect, url_for, flash
try:
    from flask_login import current_user, login_user, logout_user
except:
    from flask.ext.login import current_user, login_user, logout_user
from . import forms
from taskapp.models import User
from taskapp.extensions import login_manager, db_session
from taskapp.utils import redirect_logged_in

blueprint = Blueprint('public', __name__, static_folder='../static')

login_manager.login_view = 'public.login'

@blueprint.route('/')
def index():
    return render_template('public/index.html')

@blueprint.route('/login', methods=['GET', 'POST'])
@redirect_logged_in('user.questions')
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.login.data, form.password.data)
        if user:
            login_user(user, remember=bool(form.remember_me.data))
            return redirect(request.args.get('next') or url_for('user.questions'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('public/login.html', form=form)

@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignupForm()

    if form.validate_on_submit():
        if User.query.filter(User.name == form.username.data).count():
            flash('An account with this username already exists.', 'danger')
        elif User.query.filter(User.email == form.email.data).count():
            flash('An account with this email already exists.', 'danger')
        else:
            user = User(form.username.data, form.email.data, form.password.data)
            db_session.add(user)
            db_session.commit()
            login_user(user)
            return redirect(url_for('user.questions'))
    return render_template('public/signup.html', form=form)

@blueprint.route('/login/forgot', methods=['GET', 'POST'])
@redirect_logged_in('user.questions')
def forgot_password():
    form = forms.ForgotPasswordForm()

    # Don't tell the user whether or not the entered email belongs to an
    # account, or this view could be used to scrape emails.
    submitted = False
    if form.validate_on_submit():
        submitted=True

        user = User.from_name_or_email(form.email.data)
        #if user:
        #    mail.send_message('OSPC password reset notification',
        #        recipients=[user.email],
        #        body=render_template('emails/forgot_password.html', user=user))
    return render_template('public/forgot_password.html', form=form, submitted=submitted)

@blueprint.route('/login/change', methods=['GET', 'POST'])
@redirect_logged_in('user.questions')
def password_change():
    token = request.args.get('token')
    if not token:
        return redirect(url_for('public.forgot_password'))

    max_age = 24 * 60 * 60 # 24 hours in seconds
    user = User.from_token(token, 'reset', max_age=max_age)
    if not user:
        flash('The password reset link is invalid or expired.', 'danger')
        return redirect(url_for('public.forgot_password'))

    form = forms.ChangePasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db_session.commit()

        flash('Password updated.', 'success')
        login_user(user)
        return redirect(url_for('user.questions'))
    return render_template('public/password_change.html', form=form)

@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('public.index'))