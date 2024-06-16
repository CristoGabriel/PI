from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy

#Criação da aplicação baseada no Flask
app = Flask(__name__)

app.config.from_pyfile('configuracao.py')

db = SQLAlchemy(app)

#===================CLASSES===================

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name
    
class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    horario = db.Column(db.String(5), nullable=False)
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
    usuario = Usuario.query.filter_by(login=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuarioLogado'] = usuario.login
            flash(usuario.login + ' logado com sucesso!')
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

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuarioLogado' not in session or session['usuarioLogado'] == None:
        return redirect(url_for('login'))

    Agendamento.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Agendamento Cancelado!')
    return redirect(url_for('index'))

@app.route('/criar', methods=['POST',])
def criar():
    horario = request.form['horario']
    professor = request.form['professor']
    materia = request.form['materia']
    if not horario or not professor or not materia:
        flash('Por favor preencha todos os campos.')
        return redirect(url_for('agendar'))
    u = Agendamento.query.filter_by(horario=horario).first()
    if u:
        flash('Este horário não está disponível!')
        return redirect(url_for('agendar'))
    
    novoagd = Agendamento(horario=horario, professor=professor, materia=materia)
    db.session.add(novoagd)
    db.session.commit()
    flash(' Agendamento feito!')
    return redirect(url_for('index'))

#===================FIMROTAS===================

#Execução da aplicação
if __name__ == '__main__':
    app.run(debug=True)