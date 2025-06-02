import os
import secrets

class Config:
    #SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://somhicar:kSUjkeAgemEvXBVkPwMXKCi5OdBskbPT@dpg-d0pluvumcj7s73ea9jpg-a/somhicar'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://somhicar:somhicar@localhost:5434/somhicar'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = os.path.join('static', 'images', 'avatars')

    # Mostra consultes SQL per depurar
    SQLALCHEMY_ECHO = False

    # En producció a false
    DEBUG = True

    SECRET_KEY = secrets.token_hex(16)  # Genera una clau secreta aleatòria de 32 caràcters hexadecimals