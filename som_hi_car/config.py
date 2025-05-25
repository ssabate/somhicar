import os
import secrets

class Config:
    #SQLALCHEMY_DATABASE_URI = 'oracle+oracledb://SOMHI:SOMHI@localhost:1521/xe'
    #SQLALCHEMY_DATABASE_URI = 'oracle+cx_oracle://SOMHI:somhi@localhost:1521/xe'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://somhicar:somhicar@dpg-d0pluvumcj7s73ea9jpg-a:5432/somhicar'
    #postgresql: // somhicar: kSUjkeAgemEvXBVkPwMXKCi5OdBskbPT @ dpg - d0pluvumcj7s73ea9jpg - a.oregon - postgres.render.com / somhicar
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = os.path.join('static', 'images', 'avatars')

    # Mostra consultes SQL per depurar
    SQLALCHEMY_ECHO = True

    # En producció a false
    DEBUG = True

    SECRET_KEY = secrets.token_hex(16)  # Genera una clau secreta aleatòria de 32 caràcters hexadecimals