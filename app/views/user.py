from flask import request
import bcrypt
from flask_restx import Resource, fields
from api import api
from models import db, User


user = api.namespace('user', description='')

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
            return "Login Completed", 200
        else:
            return "Wrong Password", 404
