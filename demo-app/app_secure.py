from flask import Flask, request, jsonify, render_template, session
import sqlite3
import os
import hashlib
import secrets
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))

# Sichere Konfiguration - Umgebungsvariablen statt hartcodierter Credentials
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
API_KEY = os.getenv('API_KEY')

# Konfiguriere Logging
if not os.path.exists('logs'):
    os.mkdir('logs')
    
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('DevSecOps Demo App gestartet')

# Sichere Datenbankverbindung
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
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        salt TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
    
    # Füge einen Testbenutzer mit sicherem Passwort-Hashing hinzu
    salt = secrets.token_hex(16)
    password = 'testpassword'
    password_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    ).hex()
    
    try:
        conn.execute('''
        INSERT INTO users (username, password, salt, email)
        VALUES (?, ?, ?, ?)
        ''', ('testuser', password_hash, salt, 'test@example.com'))
        conn.commit()
    except sqlite3.IntegrityError:
        # Benutzer existiert bereits
        pass
    
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
    
    # Sichere parametrisierte Abfrage
    conn = get_db_connection()
    user = conn.execute(
        'SELECT id, username, email FROM users WHERE username = ?', 
        (username,)
    ).fetchone()
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
    
    # Sichere Passwort-Speicherung mit Salting und starkem Hashing
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        data['password'].encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    ).hex()
    
    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO users (username, password, salt, email) VALUES (?, ?, ?, ?)',
            (data['username'], password_hash, salt, data['email'])
        )
        conn.commit()
        conn.close()
        
        app.logger.info(f"Neuer Benutzer registriert: {data['username']}")
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not all(k in data for k in ('username', 'password')):
        return jsonify({"error": "Missing username or password"}), 400
    
    conn = get_db_connection()
    user_data = conn.execute(
        'SELECT id, username, password, salt, email FROM users WHERE username = ?',
        (data['username'],)
    ).fetchone()
    conn.close()
    
    if not user_data:
        # Verzögere die Antwort, um Timing-Angriffe zu erschweren
        import time
        time.sleep(0.5)
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Überprüfe das Passwort mit dem gespeicherten Salt
    password_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        data['password'].encode('utf-8'), 
        user_data['salt'].encode('utf-8'), 
        100000
    ).hex()
    
    if password_hash == user_data['password']:
        # Sichere Sitzungsverwaltung
        session.clear()
        session['user_id'] = user_data['id']
        session['username'] = user_data['username']
        
        app.logger.info(f"Benutzer angemeldet: {user_data['username']}")
        return jsonify({
            "message": "Login successful", 
            "user": {
                "id": user_data['id'],
                "username": user_data['username'],
                "email": user_data['email']
            }
        })
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    # Sichere Implementierung - nur autorisierte Benutzer können Logs sehen
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Sichere Dateioperationen - feste Pfade, keine Benutzerinputs
    try:
        with open('logs/app.log', 'r') as f:
            content = f.read()
        return content
    except:
        return jsonify({"error": "Could not read log file"}), 500

if __name__ == '__main__':
    init_db()
    # Debug-Modus nur in Entwicklungsumgebung aktivieren
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000) 