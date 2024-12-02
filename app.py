from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__, static_folder='public', template_folder='public')


# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota para a página inicial
@app.route('/')
def index():
    with open(os.path.join('public', 'index.html')) as f:
        return render_template_string(f.read())

# Rota para a página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        genero = request.form['genero']
        data_nasc = request.form['data_nasc']

        # Conectar ao banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Inserir os dados do usuário no banco de dados
        cursor.execute('''
            INSERT INTO users (nome, email, telefone, genero, data_nasc)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, email, telefone, genero, data_nasc))
        
        # Confirmar e fechar a conexão
        conn.commit()
        conn.close()

        # Redirecionar para a página inicial ou mostrar uma mensagem de sucesso
        return redirect(url_for('index'))

    with open(os.path.join('public', 'cadastro.html')) as f:
        return render_template_string(f.read())

# Função para criar a tabela no banco de dados (caso ainda não exista)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            genero TEXT NOT NULL,
            data_nasc TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa o banco de dados quando o app iniciar
init_db()

if __name__ == '__main__':
    app.run(debug=True)
