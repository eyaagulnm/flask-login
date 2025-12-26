import pymysql

def get_db():
    return pymysql.connect(
        host='localhost', user='root', password='Suriya@16',
        database='login_app', cursorclass=pymysql.cursors.DictCursor
    )

def verify_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def user_exists(username, email):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username, email))
    exists = cursor.fetchone()
    conn.close()
    return exists

def create_user(name, email, username, phone, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(name,email,username,phone,password) VALUES(%s,%s,%s,%s,%s)",
                   (name, email, username, phone, password))
    conn.commit()
    conn.close()
