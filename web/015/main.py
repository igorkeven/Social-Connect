import os
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


@app.route('/sair')
def sair():
    session.clear()
    return redirect('/')


@app.route("/acesso", methods=['POST'] )
def acesso():
    nome = request.form.get('email')
    senha = request.form.get('senha')


    db = get_db()
    usuario = db.execute('SELECT * FROM usuario WHERE(nome = ? OR email = ?) AND senha = ?', (nome,nome,senha)).fetchone() 


    if usuario:
        session['id'] = usuario['id']
        return redirect('/home')
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

    db = get_db()
    cursor = db.execute(''' 
            INSERT INTO usuario (nome, senha, tema, img_perfil, img_capa, email) VALUES (?, ?, ?, ?, ?, ?)
''', (nome, senha, tema, img_perfil, img_capa, email))
    
    db.commit()

    flash(f'seja bem vindo, {nome}!!')
    session['id'] = cursor.lastrowid
    return redirect('/home')




@app.route('/home')
def home():
    if 'id' in session:
        id_usuario = session['id']
        db = get_db()
        usuario = db.execute('SELECT * FROM usuario WHERE id = ?', (id_usuario,)).fetchone()
        if usuario:
            nome = usuario['nome']
            tema = usuario['tema']
            img_capa = usuario['img_capa']
            img_perfil = usuario['img_perfil']


            return render_template('home.html', nome=nome, tema=tema,img_capa=img_capa, img_perfil=img_perfil)
        else:
            flash('usuario não encontrado!!')
            return redirect('/')
        
    else:
        flash('acesso restrito!!')
        return redirect('/')



@app.route('/mudarSenha', methods=['POST'])
def mudarSenha():
    senha = request.form.get('nova_Senha')
    if 'id' in session :
        id = session['id']

        db = get_db()
        db.execute('UPDATE usuario SET senha = ? WHERE id = ?', (senha, id))

        db.commit()

    flash(f'senha trocada com sucesso, nova senha: {senha}')
    return redirect('/home')

@app.route('/mudarTema', methods=['POST'])
def mudarTema():
    if 'id' in session:
        tema = request.form.get('color')
        id = session['id']
        db = get_db()
        db.execute('UPDATE usuario SET tema = ? WHERE id = ?', (tema, id))

        db.commit()

    flash(f'Tema alterado com sucesso')

@app.route('/nova_capa', methods=['POST'])
def nova_capa():
    if 'id' in session:
        img_capa = request.files.get('nova_capa')
        id = session['id']


        db = get_db()
        usuario = db.execute('SELECT * FROM usuario WHERE id = ?', (id,)).fetchone()
        nome = usuario['nome']

        nome_arquivo = f"foto_capa_{nome}_{id}"
        img_capa.save(os.path.join('static/imagens/fotosCapa/', nome_arquivo))
        caminho = f'/static/imagens/fotosCapa/{nome_arquivo}'



        
        db.execute('UPDATE usuario SET img_capa = ? WHERE id = ?', (caminho, id))

        db.commit()

    flash(f'Capa alterado com sucesso')
  



    return redirect('/home')



if __name__ in '__main__':
        app.run(debug=True)