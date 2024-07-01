#Instalação do Mysql Connector Python
import mysql.connector
from mysql.connector import errorcode

#Estabelecer a conexão
#Atenção no usuário e senha de conexão
print("Conexão a ser estabelecida...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Usuário ou senha inválida')
      else:
            print(err)

#Criação da estrutura do banco de dados
cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS `CONSULTORIA`;")
cursor.execute("CREATE DATABASE `CONSULTORIA`;")
cursor.execute("USE `CONSULTORIA`;")

#Criar as tabelas
TABLES = {}

TABLES['Usuario'] = ('''
      CREATE TABLE `usuario` (
      `id` int(11) NOT NULL AUTO_INCREMENT,                     
      `nome` varchar(255) NOT NULL,
      `senha` varchar(255),
      `telefone` varchar(11) NOT NULL,
      `email` varchar(255) NOT NULL,
      `mensagem` varchar(500) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Consultor'] = ('''
      CREATE TABLE `consultor` (
      `id` int(11) NOT NULL AUTO_INCREMENT,                     
      `nome` varchar(255) NOT NULL,
      `senha` varchar(255),
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')



#Criação das tabelas dentro da estrutura do banco de dados
for tabelaNome in TABLES:
      tabelaSQL = TABLES[tabelaNome]
      try:
            print('Criação da tabela {}:'.format(tabelaNome), end=' ')
            cursor.execute(tabelaSQL)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# Inserção de Usuário
usuarioSQL = 'INSERT INTO usuario (nome, senha, telefone, email, mensagem) VALUES (%s, %s, %s, %s, %s)'
usuarios = [
    ("adm", "adm", "00000000000", "adm@gmail.com", "conta do administrador")
]
cursor.executemany(usuarioSQL, usuarios)
cursor.execute('select * from consultoria.usuario')
print(' -------------  Usuários:  -------------')
for usuario in cursor.fetchall():
    print(usuario[1])

# Inserção de Consultor
consultorSQL = 'INSERT INTO consultor (nome, senha) VALUES (%s, %s)'
consultors = [
    ("lu", "lu")
]
cursor.executemany(consultorSQL, consultors)
cursor.execute('select * from consultoria.consultor')
print(' -------------  Consultores:  -------------')
for consultor in cursor.fetchall():
    print(consultor[1])

conn.commit()
#Fechamento da conexão
cursor.close()
conn.close()