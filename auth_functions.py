from flask import render_template, request, redirect, session
from db_functions import verify_user, user_exists, create_user
from session_functions import update_activity

def handle_login():
    if request.method == 'POST':
        user = verify_user(request.form['username'], request.form['password'])
        if user:
            session['loggedin'] = True
            session['name'] = user['name']
            update_activity()
            return redirect('/home')
    return render_template('login.html')

def handle_register():
    if request.method == 'POST':
        if request.form['password'] == request.form['confirm_password']:
            if not user_exists(request.form['username'], request.form['email']):
                create_user(request.form['name'], request.form['email'], 
                           request.form['username'], request.form['phone'], 
                           request.form['password'])
                return redirect('/login')
    return render_template('register.html')
