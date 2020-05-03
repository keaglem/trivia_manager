"""Helper functions and decorators."""
import functools

from flask import redirect, url_for, flash
try:
    from flask_login import current_user
except:
    from flask.ext.login import current_user

from .models import Game

def get_current_game():
    return Game.query.filter(Game.active==True).one_or_none()

def get_current_question():
    current_game = get_current_game()
    return current_game.current_question if current_game else None

def admin_required(f):
    """A decorator that will redirect if current user is not an admin."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if getattr(current_user, 'is_admin', False):
            return f(*args, **kwargs)
        flash('You are not authorized to view that page.', 'danger')
        return redirect(url_for('user.submissions'))
    return wrapper


def redirect_logged_in(view, **url_for_kwargs):
    """A decorator that will redirect to the given view if current user is logged on."""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated:
                return redirect(url_for(view, **url_for_kwargs))
            return f(*args, **kwargs)
        return wrapper
    return decorator

def push_notification(text):
    """Send a push notification over a socket.

    The PUSH_NOTIFICATION_PORT setting must be configured. 
    Exceptions will be silenced.
    """
