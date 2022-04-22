# BLOG-API
Api para gerenciamento de um blog.

## Requerimentos

Requerimentos necessários:
- Python 3.8.10

## CONFIGURAR PROJETO

Instale e crie um ambiente virtual para o projeto:
```
pip install virtualenv
virtualenv {nome_da_env} --python=3.8.10
```

Inicie o ambiente virtual:
```
source {nome_da_env}/bin/activate
```

Na pasta app, instale as bibliotecas necessárias:
```
pip install -r requirements.txt
```

Parar levantar os serviço, rodar o run.py:
```
python run.py
```

## TESTES

Para realizar testes do projeto:

```
pytest -v --disable-warnings
```