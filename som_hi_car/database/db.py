from flask_sqlalchemy import SQLAlchemy

# Inicialitzar SQLAlchemy
db = SQLAlchemy()
print(f"db initialized: {db}, session available: {hasattr(db, 'session')}")