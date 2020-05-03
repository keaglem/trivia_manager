from flask import Blueprint, render_template, url_for, flash, \
    current_app, jsonify, request, abort, redirect
try:
    from flask_login import current_user, login_required
except:
    from flask.ext.login import current_user, login_required
from . import forms
from taskapp.models import User
from taskapp.extensions import db_session
import numpy
import datetime
from flask_socketio import emit
from .. import app
from ..utils import get_current_question

blueprint = Blueprint('api', __name__, url_prefix='/api', static_folder='../static')

    


def send_active_jobs():
    app.app_runner.emit('active jobs', {'num_jobs': get_total_active_jobs()}, namespace='/live_connect')

@blueprint.route('/question', methods=['GET', 'POST'])
@blueprint.route('/question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def question(question_id=None):
    """Create an embeddable form that will redirect to '/upload'"""
    question = get_current_question()

    if not question:
        return render_template('user/submissions.html')

    prompts = question.prompts
    
    form = forms.QuestionForm()
    for prompt in prompts:
        form.prompts.append_entry(forms.PromptForm(question=prompt.question))

    if form.validate_on_submit():
        print('Thanks for the answer')
        return render_template('user/submissions.html')
    return render_template('user/submissions.html', form=form)


