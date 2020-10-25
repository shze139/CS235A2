from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='dev'


    from . import movie
    app.register_blueprint(movie.bp)

    from . import auth
    app.register_blueprint(auth.bp)


    return app