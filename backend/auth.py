from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db
import pymysql

def verify_user(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user and check_password_hash(user['password'], password):
        return user
    return None

def user_exists(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, username))
    return cursor.fetchone() is not None

def create_user(user_data):
    db = get_db()
    cursor = db.cursor()
    hashed_password = generate_password_hash(user_data['password'])
    try:
        # YOUR SCHEMA: user_id is PRIMARY KEY, phone is INT
        cursor.execute("""
    INSERT INTO users (id, name, email, username, phone, password) 
    VALUES (%s, %s, %s, %s, %s, %s)
""", (
    0,
    user_data['name'],
    user_data['email'],
    user_data['username'],
    int(user_data['phone']),
    hashed_password
))

        return True
    except Exception as e:
        print(f"DB Error: {e}")  # Debug
        return False
