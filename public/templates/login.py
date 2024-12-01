from flask import Flask, redirect, request, render_template, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RUANSAURE'

# Página inicial com o formulário de login
@app.route('/')
def index():
    return render_template("login.html")

# Rota para processar o login
@app.route('/form-login', methods=['POST'])
def login():
    nome = request.form.get('usuario')
    senha = request.form.get('senha')
    if nome == 'Ruan' and senha == 'sdz7':
        return render_template("medio_porte.html")
    else:
        flash("Usuário ou senha inválidos.")
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

    
   