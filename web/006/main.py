from flask import Flask, render_template, request, flash, redirect , session, jsonify











app = Flask(__name__)
app.config['SECRET_KEY'] = 'igorkeven'


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