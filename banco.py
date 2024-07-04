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
cursor.execute("DROP DATABASE IF EXISTS `CHROMEBOOKS`;")
cursor.execute("CREATE DATABASE `CHROMEBOOKS`;")
cursor.execute("USE `CHROMEBOOKS`;")

#Criar as tabelas
TABLES = {}

TABLES['Usuario'] = ('''
      CREATE TABLE `usuario` (
      `id` int(11) NOT NULL AUTO_INCREMENT,                     
      `nome` varchar(20) NOT NULL,
      `senha` varchar(20) NOT NULL,
      `adm` varchar(3),
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Agendamento'] = ('''
      CREATE TABLE `agendamento` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `data` varchar(10) NOT NULL,
      `periodo` varchar(10) NOT NULL,
      `professor` varchar(40) NOT NULL,
      `materia` varchar(40) NOT NULL,
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
usuarioSQL = 'INSERT INTO usuario (nome, senha, adm) VALUES (%s, %s, %s)'
usuarios = [
    ("adm", "adm", "sim"),
    ("cristhian", "cristhian", "nao"),
    ("yuri", "yuri", "nao"),
    ("caio", "caio", "nao"),
    ("renan", "renan", "nao"),
]
cursor.executemany(usuarioSQL, usuarios)
cursor.execute('select * from chromebooks.usuario')
print(' -------------  Usuários:  -------------')
for usuario in cursor.fetchall():
    print(usuario[1])


agendamentoSQL = 'INSERT INTO agendamento (data, periodo, professor, materia) VALUES (%s, %s, %s, %s)'
agendamentos = [
    ("2024-06-18", "MATUTINO", "cristhian", "INGLÊS"),
]
cursor.executemany(agendamentoSQL, agendamentos)
cursor.execute('select * from chromebooks.agendamento')
print(' -------------  Agendamentos:  -------------')
for agendamento in cursor.fetchall():
    print(agendamento[1])


conn.commit()
#Fechamento da conexão
cursor.close()
conn.close()
