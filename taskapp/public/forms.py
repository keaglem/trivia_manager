from flask_wtf import Form
import wtforms as wtf
from wtforms.validators import InputRequired, Email, Length, EqualTo, Regexp

class SignupForm(Form):
    username = wtf.StringField('Username', [InputRequired(), Regexp(r'^\w+$', 
        message='Username must contain only letters, numbers, and underscores.'), Length(min=5)],
        description='Each team has a single username.')
    email = wtf.StringField('Email', [InputRequired(), Email()],
        description='For teams, this is the email of the point of contact for the team.')
    email_repeat = wtf.StringField('Confirm Email',
                             [InputRequired(), EqualTo('email', message='Emails must match')])
    password = wtf.PasswordField('Password', [InputRequired(), Length(min=5)])
    password_repeat = wtf.PasswordField('Confirm Password',
                        [InputRequired(), EqualTo('password', message='Passwords must match')])
    submit_button = wtf.SubmitField('Sign up')


class LoginForm(Form):
    login = wtf.StringField('Username or Email', [InputRequired(), Length(min=5)])
    password = wtf.PasswordField('Password', [InputRequired(), Length(min=5)])
    remember_me = wtf.BooleanField('Remember me')
    submit_button = wtf.SubmitField('Log in')


class ForgotPasswordForm(Form):
    email = wtf.StringField('Email', [InputRequired(), Email()])
    submit_button = wtf.SubmitField('Send verification email')

class ChangePasswordForm(Form):
    password = wtf.PasswordField('Password', [InputRequired(), Length(min=5)])
    password_repeat = wtf.PasswordField('Confirm Password',
                        [InputRequired(), EqualTo('password', message='Passwords must match')])
    submit_button = wtf.SubmitField('Sign up')