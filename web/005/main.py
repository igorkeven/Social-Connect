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
    












if __name__ in '__main__':
        app.run(debug=True)