from email import header
import json
from models import User, db


class TestUser:
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    # def test_create_user_return_200(self, client):
    #     user = {"username": "testes", "password": "12345"}

    #     # Delete o usuario teste para esse teste ser válido
    #     u = User.query.filter_by(username='teste').first()
    #     db.session.delete(u)
    #     db.session.commit()

    #     resp = client.post("/user/create", data=json.dumps(user), headers=self.headers)
    #     print(resp.json)

    #     assert resp.status_code == 200
    #     assert resp.json == f"User {user['username']} has been created successfully"

    def test_missing_username_400(self, client):
        user = {"username": "", "password": "12345"}

        resp = client.post("/user/create", data=json.dumps(user), headers=self.headers)
        print(resp.json)

        assert resp.status_code == 400
        assert resp.json == "Missing username"

