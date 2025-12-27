import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'dev-secret-key-change-in-production'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Suriya@16'
    MYSQL_DB = 'login_app'
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=10)
