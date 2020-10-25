import os
from flask import Flask
from .adapters import repository as repo
from .adapters import memory_repository

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='dev'

    data_path = os.path.join(os.path.dirname(__file__), 'adapters', 'data')

    repo.repo_instance = memory_repository.MemoryRepository()
    memory_repository.populate(data_path, repo.repo_instance)


    from . import home
    app.register_blueprint(home.bp)

    from . import movie
    app.register_blueprint(movie.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    return app