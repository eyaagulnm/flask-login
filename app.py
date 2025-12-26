from flask import Flask, render_template, request, redirect, session
from session_functions import check_session, update_activity
from auth_functions import handle_login, handle_register

app = Flask(__name__)
app.secret_key = 'mysecretkey12345'

@app.before_request
def before_request():
    return check_session()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return handle_login()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return handle_register()

@app.route('/home')
def home():
    update_activity()
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')  

if __name__ == '__main__':
    app.run(debug=True)
