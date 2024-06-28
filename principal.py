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
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(255), nullable=False)
    servicos = db.Column(db.String(255), nullable=False)
    dia = db.Column(db.String(255), nullable=False)
    horario = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.String(255), nullable=False)
#===================FIMCLASSES===================

#===================ROTAS===================
@app.route('/')
def index():
    imagem_url = '/static/imagens/fundo.png'
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




@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuarioLogado' not in session or session['usuarioLogado'] == None:
        return redirect(url_for('login'))
    
    if session['usuarioLogado'] != 'adm':
        flash('Você não tem permissão para excluir este agendamento.')
        return redirect(url_for('index'))

    Agendamento.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Agendamento Cancelado!')
    return redirect(url_for('index'))

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    service_prices = {
        'corte': 10,
        'barba': 20,
        'bigode': 30
    }
    valor = 0
    
    if request.method == 'POST':
        cliente = request.form['cliente']
        servicos = ', '.join(request.form.getlist('checkboxes'))
        dia = request.form.get('dia')
        horario = request.form.get('selecthorarios')
        selected_services = request.form.getlist('checkboxes')
        valor = sum(service_prices[checkbox] for checkbox in selected_services)

    novo_agendamento = Agendamento(cliente=cliente, servicos=servicos, dia=dia, horario=horario, valor=valor)
    db.session.add(novo_agendamento)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/bar')
def bar():
    
    return render_template('barber.html')

@app.route('/cadastro', methods=['POST',])
def cadastro():
    login = request.form['login']
    senha = request.form['senha']
    if not login or not senha:
        flash('Por favor preencha todos os campos.')
        return redirect(url_for('cadastro'))
    user = Usuario.query.filter_by(login=login).first()
    if user:
        flash('Este nome de usuário já está em uso!')
        return redirect(url_for('cadastro'))
    
    novouser = Usuario(login=login, senha=senha)
    db.session.add(novouser)
    db.session.commit()
    flash('Usuário cadastrado!')
    return redirect(url_for('index'))

@app.route('/pagcadastro')
def pagcadastro():
    return render_template('cadastro.html')


#===================FIMROTAS===================

#Execução da aplicação
if __name__ == '__main__':
    app.run(debug=True)