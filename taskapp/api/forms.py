from flask_wtf import Form, FlaskForm
from flask_wtf.file import FileField
import wtforms as wtf
from wtforms.validators import InputRequired, NumberRange
from wtforms.fields import FieldList, FormField

class PromptForm(Form):
    question = wtf.StringField('', [InputRequired()])

    def __init__(self, *args, **kwargs):
        super().method(*args, **kwargs)
        if 'question' in kwargs and kwargs['question'] is not None:
            self.question.label.text = kwargs['question']


class QuestionForm(Form):
    prompts = FieldList(FormField(PromptForm), label='Questions', min_entries=1)

