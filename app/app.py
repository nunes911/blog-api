from flask import Flask, Blueprint
import os
from models import db
from api import api
from views.user import user
from views.post import post


def create_app():
    app = Flask('app')

    blueprint = Blueprint('api', __name__)

    api.init_app(blueprint)
    app.register_blueprint(blueprint)
    api.add_namespace(user)
    api.add_namespace(post)

    # SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['DEBUG'] = True
    app.config['USE_RELOADER'] = True

    db.init_app(app)

    return app
