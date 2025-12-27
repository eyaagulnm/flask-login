from flask import session, jsonify
import time

def session_timeout():
    if not session.get('user_id'):
        return jsonify({'message': 'Not authenticated'}), 401
    
    last_activity = session.get('last_activity', 0)
    if time.time() - last_activity > 10:
        session.clear()
        return jsonify({'message': 'Session expired - 10s inactivity'}), 401
    return None
