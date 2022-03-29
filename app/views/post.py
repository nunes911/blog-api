from flask import request, current_app
from functools import wraps
import jwt, json
import datetime
from flask_restx import Resource, fields
from api import api
from models import db, User, Post


post = api.namespace('post', description='')


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
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return {'erro': 'Token invalido'}, 403

        return f(current_user, *args, **kwargs)

    return decorated


@post.route('/create')
class CreatePost(Resource):
    new_post = post.model(
        "model_new_post",
        {
            "title": fields.String(description="Titulo", required=True),
            "body": fields.String(description="Conteudo da publicacao", required=True)
        }
    )

    @post.doc(security='apikey')
    @token_required
    @post.expect(new_post)
    def post(self, current_user):
        '''
        Cria uma nova publicação
        '''

        resp = request.json
        title = resp['title']
        body = resp['body']

        if title == '':
            return "Missing Title", 401
        if body == '':
            return "Missing Body", 401

        try:
            new_post = Post(user_id=self.id, title=title, body=body)
            db.session.add(new_post)
            db.session.commit()

            return "Post created successfully", 200

        except Exception as e:
            return f"Error: {e}", 401


