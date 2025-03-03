from flask import Flask, request, jsonify, render_template
import sqlite3
import os
import hashlib

app = Flask(__name__)

# Unsichere Konfiguration - Hartcodierte Credentials
DB_USER = "admin"
DB_PASSWORD = "SuperSecretPassword123!"  # SICHERHEITSLÜCKE: Hartcodiertes Passwort
API_KEY = "sk_test_51NzQHpLkjhgfdsaqwertyuiop"  # SICHERHEITSLÜCKE: Hartcodierter API-Schlüssel

# Unsichere Datenbankverbindung
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialisierung der Datenbank
def init_db():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
    
    # Füge einen Testbenutzer hinzu
    conn.execute('''
    INSERT OR IGNORE INTO users (username, password, email)
    VALUES ('testuser', 'unsecurepassword', 'test@example.com')
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, email FROM users').fetchall()
    conn.close()
    
    return jsonify([dict(user) for user in users])

@app.route('/api/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    
    # SICHERHEITSLÜCKE: SQL Injection
    conn = get_db_connection()
    query = f"SELECT id, username, email FROM users WHERE username = '{username}'"
    user = conn.execute(query).fetchone()
    conn.close()
    
    if user:
        return jsonify(dict(user))
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    
    if not data or not all(k in data for k in ('username', 'password', 'email')):
        return jsonify({"error": "Missing required fields"}), 400
    
    # SICHERHEITSLÜCKE: Unsichere Passwort-Speicherung (kein Salting)
    password_hash = hashlib.md5(data['password'].encode()).hexdigest()
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
        (data['username'], password_hash, data['email'])
    )
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not all(k in data for k in ('username', 'password')):
        return jsonify({"error": "Missing username or password"}), 400
    
    # SICHERHEITSLÜCKE: Unsichere Passwort-Speicherung (kein Salting)
    password_hash = hashlib.md5(data['password'].encode()).hexdigest()
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT id, username, email FROM users WHERE username = ? AND password = ?',
        (data['username'], password_hash)
    ).fetchone()
    conn.close()
    
    if user:
        # SICHERHEITSLÜCKE: Keine ordnungsgemäße Sitzungsverwaltung
        return jsonify({"message": "Login successful", "user": dict(user)})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/logs', methods=['GET'])
def get_logs():
    # SICHERHEITSLÜCKE: Unsichere Dateioperationen
    log_file = request.args.get('file', 'app.log')
    
    try:
        with open(log_file, 'r') as f:
            content = f.read()
        return content
    except:
        return jsonify({"error": "Could not read log file"}), 500

if __name__ == '__main__':
    init_db()
    # SICHERHEITSLÜCKE: Debug-Modus in Produktion aktiviert
    app.run(debug=True, host='0.0.0.0', port=5000) 