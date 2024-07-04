import os

SECRET_KEY = 'teste123'
#Configuração da conexão com o banco de dados
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'root',
        servidor = 'localhost',
        database = 'chromebooks'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'