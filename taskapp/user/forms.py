from flask_wtf import Form
import wtforms as wtf
from wtforms.validators import InputRequired, Email, Length, EqualTo, Regexp

class UpdateProfileForm(Form):
    email = wtf.StringField('Email', [InputRequired(), Email()])
    submit_button = wtf.SubmitField('Update profile')

class UpdatePasswordForm(Form):
    current_password = wtf.PasswordField('Current Password', [InputRequired(), Length(min=5)])
    new_password = wtf.PasswordField('New Password', [InputRequired(), Length(min=5)])
    new_password_repeat = wtf.PasswordField('Confirm new password',
                                    [InputRequired(), EqualTo('new_password', message='Passwords must match')])
    submit_button = wtf.SubmitField('Update password')
