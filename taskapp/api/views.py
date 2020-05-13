from flask import Blueprint, render_template, url_for, flash, \
    current_app, jsonify, request, abort, redirect
try:
    from flask_login import current_user, login_required
except:
    from flask.ext.login import current_user, login_required
from . import forms
from taskapp.models import User, Answer, Question
from taskapp.extensions import db_session
import numpy
import datetime
from flask_socketio import emit
from .. import app
from ..utils import get_current_question, get_current_game

blueprint = Blueprint('api', __name__, url_prefix='/api', static_folder='../static')

    
@blueprint.route('/set_current_question/<int:question_id>', methods=['POST'])
def set_current_question(question_id=None):
    question = Question.query.filter(Question.id == question_id).one_or_none()
    if question:
        get_current_game().current_question = question
        send_current_question(question_id)
        db_session.commit()

    return 'success'

def send_current_question(current_question_id=None):
    if not current_question_id:
        current_question_id = get_current_question().id
    app.app_runner.emit('current question', {'question_id': current_question_id}, namespace='/live_connect')

@blueprint.route('/question', methods=['GET', 'POST'])
@blueprint.route('/question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def question(question_id=None):
    """Create an embeddable form that will redirect to '/upload'"""
    question = get_current_question()

    if not question:
        return render_template('api/questions.html')

    prompts = question.prompts
    
    form = forms.QuestionForm()

    if form.validate_on_submit():
        received_values = form.data['prompts']
        print_answers = []
        for answers, prompts in zip(received_values, question.prompts):
            answer = answers['question']
            new_answer = Answer(received_answer=answer,
                                question=question,
                                user=current_user)
            db_session.add(new_answer)
            db_session.commit()

            if answer.lower() in prompts.answer.lower():
                response_string = 'Correct!'
            else:
                response_string = 'Not quite, pending judge review.'

            print_answers.append(f"Thanks for submitting: {' ... '.join([answer, response_string])}")
        return render_template('user/questions.html', answer='\n'.join(print_answers))

    form.prompts.pop_entry()
    for idx, prompt in enumerate(prompts):
        form.prompts.append_entry()
        form.prompts[idx].question.label.text = prompt.prompt

    return render_template('api/questions.html', form=form)


