import os
import secrets

class Config:
    SQLALCHEMY_DATABASE_URI = 'oracle+oracledb://SOMHI:SOMHI@localhost:1521/xe'
    #SQLALCHEMY_DATABASE_URI = 'oracle+cx_oracle://SOMHI:somhi@localhost:1521/xe'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = os.path.join('static', 'images', 'avatars')

    # Mostra consultes SQL per depurar
    SQLALCHEMY_ECHO = True

    # En producció a false
    DEBUG = True

    SECRET_KEY = secrets.token_hex(16)  # Genera una clau secreta aleatòria de 32 caràcters hexadecimals