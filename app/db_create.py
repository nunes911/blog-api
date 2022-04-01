from models import db
from app import create_app


application = create_app()
db.drop_all(app=application)
db.create_all(app=application)
print('===== Criado Banco de Dados =====')
