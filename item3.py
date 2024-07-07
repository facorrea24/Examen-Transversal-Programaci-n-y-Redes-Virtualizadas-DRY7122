import hashlib
import sqlite3
from flask import Flask, request, jsonify

# 1. Gestión de claves y base de datos SQL
app = Flask(__name__)

# Crear una base de datos SQLite y una tabla para almacenar usuarios
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (name TEXT, password_hash TEXT)''')
    conn.commit()
    conn.close()

# Crear el sitio web en el puerto 5800
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, password_hash) VALUES (?, ?)", (name, password_hash))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Usuario registrado correctamente'})

@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name=? AND password_hash=?", (name, password_hash))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'Inicio de sesión exitoso'})
    else:
        return jsonify({'message': 'Nombre de usuario o contraseña incorrecta'})

if __name__ == '__main__':
    init_db()
    app.run(port=5800)