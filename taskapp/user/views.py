from sqlalchemy.sql import func
from sqlalchemy.orm.exc import NoResultFound
from flask import Blueprint, request, redirect, url_for, current_app, render_template, flash
try:
    from flask_login import current_user, login_required
except:
    from flask.ext.login import current_user, login_required
from ..models import User
from ..extensions import login_manager, db_session
from . import forms

blueprint = Blueprint('user', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(id):
    """Used by Flask-Login to load a User model for a session that's logged in"""
    return User.query.get(int(id))
    

@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile_form = forms.UpdateProfileForm(prefix='profile_form')
    password_form = forms.UpdatePasswordForm(prefix='password_form')

    if profile_form.validate_on_submit() and profile_form.submit_button.data:
        current_user.email = profile_form.email.data
        db_session.commit()
        flash('Profile updated.', 'success')
    elif password_form.validate_on_submit() and password_form.submit_button.data:
        # Manually clear validation from profile_form, since it wasn't submitted
        profile_form.errors.clear()
        for field in profile_form:
            del field.errors[:]

        current_user.set_password(password_form.new_password.data)
        db_session.commit()
        flash('Password updated.', 'success')

    profile_form.email.data = current_user.email

    return render_template('user/profile.html', profile_form=profile_form, password_form=password_form)



