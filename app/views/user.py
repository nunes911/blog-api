from flask import request, current_app
from functools import wraps
import bcrypt
import datetime
from flask_restx import Resource, fields
import jwt
from api import api
from models import db, User

user = api.namespace('user', description='')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        if not token:
            return {"erro": "Um token valido precisa ser informado no header"}, 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(token=token).first()
        except:
            return {'erro': 'Token invalido'}, 403

        return f(current_user, *args, **kwargs)

    return decorated


@user.route('/user/create')
class NewUser(Resource):
    new_user = user.model(
        "model_new_user",
        {
            "username": fields.String(description="Username", required=True),
            "password": fields.String(description="Senha", required=True)
        }
    )

    @user.expect(new_user)
    def post(self):
        '''
        Criar um novo usuário para o sistema
        '''

        resp = request.json
        username = resp['username']
        password = resp['password']

        if not username:
            return "Missing username", 400
        if not password:
            return "Missing password", 400

        check_user = User.query.filter_by(username=username).first()

        if check_user:
            return f"Username {username} already exists.", 400

        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(username=username, password=hash_password)
        db.session.add(new_user)
        db.session.commit()

        return f"User {username} has been created successfully", 200


@user.route('/user/login')
class LoginUser(Resource):
    login = user.model(
        "model_login",
        {
            "username": fields.String(description="Username", required=True),
            "password": fields.String(description="Senha", required=True)
        }
    )

    @user.expect(login)
    def post(self):
        '''
        Endpoint de Login que recebe usuário e senha anteriormente cadastrados e retorna um token.
        '''

        resp = request.json
        username = resp['username']
        password = resp['password']

        if not username:
            return "Missing username", 400
        if not password:
            return "Missing password", 400

        user = User.query.filter_by(username=username).first()

        if not user:
            return f"Username not found.", 404

        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            token = jwt.encode({'user': username,
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)},
                               current_app.config['SECRET_KEY'])

            return {'token': token}, 200
        else:
            return "Wrong Password", 404
