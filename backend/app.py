from flask import Flask, request, jsonify, session, g
from flask_cors import CORS
from config import Config
from database import get_db, close_db
from auth import verify_user, user_exists, create_user
from session import session_timeout
from datetime import timedelta
import time

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True, origins="http://localhost:3000")

@app.teardown_appcontext
def close_database(exception):
    close_db()

@app.before_request
def update_activity():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=10)
    if request.endpoint and not request.endpoint.startswith('static'):
        session.modified = True
        session['last_activity'] = time.time()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = verify_user(data['username'], data['password'])
    if user:
        session['user_id'] = user['username']  # FIXED: username instead of user_id
        session['username'] = user['username']
        session['last_activity'] = time.time()
        return jsonify({'message': 'Login successful', 'user': user}), 200
    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if user_exists(data['username']):
        return jsonify({'message': 'User already exists'}), 400
    if data['password'] != data['confirm_password']:
        return jsonify({'message': 'Passwords do not match'}), 400
    
    user_data = {
        'name': data['name'], 'email': data['email'],
        'username': data['username'], 'phone': data['phone'],
        'password': data['password']
    }
    
    if create_user(user_data):
        return jsonify({'message': 'Registration successful'}), 201
    return jsonify({'message': 'Registration failed'}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/home')
def home():
    timeout = session_timeout()
    if timeout:
        return timeout
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (session['user_id'],))
    user = cursor.fetchone()
    return jsonify({'message': 'Welcome Admin!', 'user': user})

@app.route('/api/check-session')
def check_session():
    if session.get('user_id'):
        return jsonify({'authenticated': True})
    return jsonify({'authenticated': False})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
