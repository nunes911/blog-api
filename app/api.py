from flask_restx import Api


authorizartions = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(version='1.0', title='Blog',
          description='Api de administração do Blog', authorizations=authorizartions)
