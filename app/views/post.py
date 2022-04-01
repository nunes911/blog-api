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
            return {"erro": "A valid token must be informed in the header."}, 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return {'erro': 'Invalid token.'}, 403

        return f(current_user, *args, **kwargs)

    return decorated


@post.route('/list')
class PostList(Resource):
    @post.doc(security='apikey')
    @token_required
    def get(self, current_user):
        """
        Retorna a lista de publicações criadas.
        """
        all_post = Post.query.all()
        post_list = []

        try:
            for post in all_post:
                u = User.query.filter_by(id=post.user_id).first()
                post_list.append({'id': post.id,
                                  'user': u.username,
                                  'title': post.title,
                                  'body': post.body,
                                  'created_at': post.created_at.isoformat()})

            return post_list, 200

        except Exception as e:
            return f"Erro: {e}", 400


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
        """
        Cria uma nova publicação
        """

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


@post.route('/delete/<id>')
class DeletePost(Resource):
    @post.doc(security='apikey')
    @token_required
    def delete(self, current_user, id):
        """
        Deleta a postagem se o usuário for o criador da mesma.
        """
        post = Post.query.filter_by(id=id).first()

        if not post:
            return "This post doesn't exist.", 404
        elif post.user_id != self.id:
            return "User doesn't have permission to delete this post.", 400
        else:
            db.session.delete(post)
            db.session.commit()

            return f"Post {id} deleted successfully.", 200
