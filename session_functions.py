import time
from flask import session, redirect, request

SESSION_TIMEOUT = 10

def check_session():
    if 'loggedin' in session:
        if time.time() - session.get('last_time', 0) > SESSION_TIMEOUT:
            session.clear()
            return redirect('/login')
    
    if request.endpoint not in ['login', 'register']:
        if not session.get('loggedin'):
            return redirect('/login')
    return None

def update_activity():
    session['last_time'] = time.time()
