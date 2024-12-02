from flask import Flask, render_template, request, flash, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_super_secreta'

# Configuração do banco de dados
DATABASE = 'users.db'

def init_db():
    """Inicializa o banco de dados"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefone TEXT NOT NULL,
                genero TEXT NOT NULL,
                data_nasc TEXT NOT NULL
            )
        """)
        conn.commit()

@app.route("/", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        # Obtendo dados do formulário
        nome = request.form.get("nome")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        genero = request.form.get("genero")
        data_nasc = request.form.get("data_nasc")

        # Validação simples
        if not nome or not email or not telefone or not genero or not data_nasc:
            flash("Todos os campos são obrigatórios!", "error")
            return redirect("/")
        
        try:
            # Salvando os dados no banco
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (nome, email, telefone, genero, data_nasc)
                    VALUES (?, ?, ?, ?, ?)
                """, (nome, email, telefone, genero, data_nasc))
                conn.commit()
                flash("Cadastro realizado com sucesso!", "success")
                return redirect("/")
        except sqlite3.IntegrityError:
            flash("O email já está cadastrado!", "error")
            return redirect("/")
    
    return render_template("cadastro.html")

@app.route("/usuarios")
def usuarios():
    """Listagem de usuários cadastrados"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        usuarios = cursor.fetchall()
    return render_template("usuarios.html", usuarios=usuarios)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
