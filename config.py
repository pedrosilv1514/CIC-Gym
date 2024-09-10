# config.py
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'your_secret_key'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Pe023194)'
    MYSQL_DB = 'academia'
    MYSQL_CURSORCLASS = 'DictCursor'