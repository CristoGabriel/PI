from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy

#Criação da aplicação baseada no Flask
app = Flask(__name__)

app.config.from_pyfile('configuracao.py')

db = SQLAlchemy(app)

#===================CLASSES===================

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(20), nullable=False)
    adm = db.Column(db.String(3), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name
    
class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.String(10), nullable=False)
    periodo = db.Column(db.String(10), nullable=False)
    professor = db.Column(db.String(40), nullable=False)
    materia = db.Column(db.String(40), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name

#===================FIMCLASSES===================

#===================ROTAS===================
@app.route('/')
def index():
    imagem_url = '/static/imagens/logo_mt.png'
    ver = Agendamento.query.order_by(Agendamento.id)
    return render_template('index.html', agendamentos=ver, imagem_url=imagem_url)

@app.route('/login')
def login():
    imagem_url = '/static/imagens/logo_mt.png'
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima,imagem_url=imagem_url)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = Usuario.query.filter_by(nome=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuarioLogado'] = usuario.nome
            session['uu'] = usuario.adm
            flash(usuario.nome + ' logado com sucesso!')
            session['user_id'] = usuario.id
            proximaPagina = request.form['proxima']
            return redirect(proximaPagina)
        else:
            flash('Usuário não logado.')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuarioLogado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/agendar')
def agendar():
    imagem_url = '/static/imagens/logo_mt.png'
    if 'usuarioLogado' not in session or session['usuarioLogado'] == None:
        return redirect(url_for('login', proxima=url_for('agendar')))
    return render_template('agendar.html',imagem_url=imagem_url)

@app.route('/deletar/<int:id>/<string:professor>')
def deletar(id, professor):
    if 'usuarioLogado' not in session or session['usuarioLogado'] == None:
        return redirect(url_for('login'))
    
    if session['usuarioLogado'] != professor:
        flash('Você não tem permissão para excluir este agendamento.')
        return redirect(url_for('index'))

    Agendamento.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Agendamento Cancelado!')
    return redirect(url_for('index'))

@app.route('/criar', methods=['POST',])
def criar():
    data = request.form['data']
    periodo = request.form['periodo']
    professor = session['usuarioLogado']
    materia = request.form['materia']
    if not data or not periodo or not professor or not materia:
        flash('Por favor preencha todos os campos.')
        return redirect(url_for('agendar'))
    
    
    agendamento_existente = Agendamento.query.filter_by(data=data, periodo=periodo).first()
    if agendamento_existente:
        flash('Data e período já estão em uso. Por favor, escolha outro horário.')
        return redirect(url_for('agendar'))
    
    novoagd = Agendamento(data=data, periodo=periodo, professor=professor, materia=materia)
    db.session.add(novoagd)
    db.session.commit()
    flash(' Agendamento feito!')
    return redirect(url_for('index'))

@app.route('/cadastro', methods=['POST',])
def cadastro():
    nome = request.form['nome']
    senha = request.form['senha']
    if not nome or not senha:
        flash('Por favor preencha todos os campos.')
        return redirect(url_for('cadastro'))
    user = Usuario.query.filter_by(nome=nome).first()
    if user:
        flash('Este nome de usuário já está em uso!')
        return redirect(url_for('cadastro'))
    
    novouser = Usuario(nome=nome, senha=senha)
    db.session.add(novouser)
    db.session.commit()
    flash('Usuário cadastrado!')
    return redirect(url_for('login'))

@app.route('/pagcadastro')
def pagcadastro():
    imagem_url = '/static/imagens/logo_mt.png'
    if session.get('usuarioLogado') != 'adm':
        flash('Você não tem permissão para criar novos usuários.')
        return redirect(url_for('index'))
    return render_template('cadastro.html',imagem_url=imagem_url)

@app.route('/admpagina')
def admpagina():
    user = Usuario.query.order_by(Usuario.id)

    if session.get('uu') != 'sim':
        flash('Você não tem permissão para acessar essa página.')
        return redirect(url_for('index'))
    return render_template('admpage.html', usuarios=user)

@app.route('/setadm/<string:adm>/<int:id>')
def setadm(adm, id):
    usuario = Usuario.query.get(id)
    if usuario:
        usuario.adm = "não" if usuario.adm == "sim" else "sim"
        db.session.commit()
    return redirect(url_for('admpagina'))



#===================FIMROTAS===================

#Execução da aplicação
if __name__ == '__main__':
    app.run(debug=True)