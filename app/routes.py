from flask import Blueprint, render_template, request, redirect
import psycopg2

main_routes = Blueprint("main_routes", __name__)

# Conexão com o banco de dados
conn = psycopg2.connect(
    host="localhost",
    database="eltec",
    user="postgres",
    password="181508"
)

@main_routes.route("/")
def index():
    return render_template("index.html")

@main_routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        conn.commit()
        cursor.close()

        return redirect("/")
    return render_template("register.html")

@main_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return "Login bem-sucedido!"
        else:
            return "Credenciais inválidas!"
    return render_template("login.html")
