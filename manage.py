from flask import Flask

from taskapp.app import create_app
from taskapp.extensions import Base, engine, db_session
from taskapp.settings import DevConfig, ProdConfig
import os
import sys
import click
from taskapp.app import app_runner
from flask_socketio import SocketIO

if os.environ.get("TASKAPP_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)




def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import taskapp.models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    from taskapp.models import Game, Prompt, Question

    new_game = Game()
    new_game.active = True   
    db_session.add(new_game)
    db_session.commit()

    

    num_questions = 5
    num_prompts = 2

    for idx_question in range(num_questions):
        new_question = Question()
        for idx in range(num_prompts):
            new_prompt = Prompt()
            new_prompt.prompt = f'Prompt # {idx_question*num_prompts+idx}'
            new_prompt.answer = f'Correct Answer {idx}'
            new_prompt.point_value = 3
            new_question.prompts.append(new_prompt)
            db_session.add(new_prompt)

        new_question.question_number = idx_question + 1
        new_question.game = new_game
        db_session.add(new_question)
        if idx_question == 0:
            new_game.current_question = new_question

    db_session.commit()

    #question_1 = Question.query.filter(Question.question_number == 1).one()
    #current_game = Game.query.filter(Game.active == True).one()
    #current_game.current_question = question_1
    #db_session.commit()

@click.command()
@click.option('--host', default='127.0.0.1', help='IP address to bind webserver.  Localhost or local IP')
@click.option('--port', default=5000, help='Port number for web-server')
def main_function(host, port):
    app_runner.run(app=app, host=host, port=port)
    #app.run(host=host, port=port)

if __name__ == '__main__':

    if len(sys.argv)>1 and sys.argv[1] == 'init_db':
        init_db()
        sys.exit()

    main_function()