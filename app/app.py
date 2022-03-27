from flask import Flask, Blueprint
from models import db
from api import api
from views.user import user



def create_app():
    app = Flask('app')

    blueprint = Blueprint('api', __name__)

    api.init_app(blueprint)
    app.register_blueprint(blueprint)
    api.add_namespace(user)

    # SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = '9a29b63856e26fe7182b4efa182b5e40'

    db.init_app(app)

    return app
