from flask import Flask, render_template, request, flash, redirect , session, jsonify, g
import sqlite3




app = Flask(__name__)
app.config['SECRET_KEY'] = 'igorkeven'
app.config['DATABASE'] = 'usuarios.db'



# função para conectar ao banco de dados
def get_db():
     if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory=sqlite3.Row
     return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def create_table():
    db = get_db()
    db.execute('''
         CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            tema TEXT DEFAULT '#3b5998',
            img_perfil TEXT DEFAULT '/static/imagens/user.png',
            img_capa TEXT DEFAULT '/static/imagens/fundo.jpg',
            email TEXT NOT NULL
        );

''')
    
    db.commit()

with app.app_context():
    create_table()



@app.route("/")
def login():
    return render_template('login.html')


@app.route("/acesso", methods=['POST'] )
def acesso():
    nome = request.form.get('email')
    senha = request.form.get('senha')

    if nome == 'igor' and senha == '123':
        return render_template('home.html')
    else:
        flash('nome e/ou senha invalidos , tente novamente!!')

        return redirect('/')
    
@app.route("/cadastro")
def cadastro():
     return render_template('cadastro.html')

@app.route("/cadastrando" , methods=['POST'])
def cadastrando():
    nome = request.form.get('nome') 
    senha = request.form.get('senha') 
    email = request.form.get('email') 
    tema = '#3b5998'
    img_capa = '/static/imagens/fundo.jpg'
    img_perfil = '/static/imagens/user.png'

    return redirect('/cadastro')









if __name__ in '__main__':
        app.run(debug=True)