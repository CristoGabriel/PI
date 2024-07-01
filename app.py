from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy

#Criação da aplicação baseada no Flask
app = Flask(__name__)

app.config.from_pyfile('configuracao.py')

db = SQLAlchemy(app)

#===================CLASSES

class Consultor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    senha = db.Column(db.String(255), nullable=True)
    telefone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    mensagem = db.Column(db.String(500), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name

#===================ROTAS

@app.route('/')
def index():
    imagem1 = '/static/imagens/rb.jpg'
    imagem2 = '/static/imagens/logointegrador.png'
    imagem3 = '/static/imagens/banco-do-brasil-5.png'
    return render_template('index.html', imagem1=imagem1, imagem2=imagem2, imagem3=imagem3)

@app.route('/fgts')
def fgts():
    return render_template('fgts.html')

@app.route('/inss')
def inss():
    return render_template('inss.html')

@app.route('/irrpf')
def irrpf():
    return render_template('irrpf.html')

@app.route('/servidores')
def servidores():
    return render_template('servidores.html')

@app.route('/auxilio')
def auxilio():
    return render_template('auxilio.html')

@app.route('/correntistabb')
def correntistabb():
    return render_template('correntistabb.html')

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    consultor = Consultor.query.filter_by(nome=request.form['usuario']).first()
    if consultor:
        if request.form['senha'] == consultor.senha:
            session['usuarioLogado'] = consultor.nome
            flash(consultor.nome + ' logado com sucesso!')
            session['user_id'] = consultor.id
            proximaPagina = request.form['proxima']
            return redirect(proximaPagina)
        else:
            flash('Usuário não logado.')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form['email']
    mensagem = request.form['mensagem']
    
    
    novo = Usuario(nome=nome, telefone=telefone, email=email, mensagem=mensagem)
    db.session.add(novo)
    db.session.commit()
    flash(' Mensagem enviada!')
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):

    Usuario.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Pedido Concluído')
    return redirect(url_for('consultor'))

@app.route('/consultor')
def consultor():
    if 'usuarioLogado' not in session or session['usuarioLogado'] == None:
        return redirect(url_for('login'))
    ver = Usuario.query.order_by(Usuario.id)
    return render_template('consultor.html', usuarios=ver)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['usuarioLogado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))




#Execução da aplicação
if __name__ == '__main__':
    app.run(debug=True)