from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TelField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, Optional

class RegisterForm(FlaskForm):
    nom_usuari = StringField('Nom d\'usuari', validators=[
        DataRequired(),
        Length(min=3, max=150, message="El nom d'usuari ha de tenir entre 3 i 150 caràcters")
    ])
    email = StringField('Correu electrònic', validators=[
        DataRequired(),
        Email(),
        Length(max=255, message="El correu electrònic no pot superar els 255 caràcters")
    ])
    phone = TelField('Telèfon mòbil', validators=[
        DataRequired(),
        Length(max=15, message="El telèfon no pot superar els 15 caràcters"),
        Regexp(r'^\+?\d{9,15}$', message="Format de telèfon no vàlid (ex. +34123456789)")
    ])
    password = PasswordField('Contrasenya', validators=[
        DataRequired(),
        Length(min=8, message="La contrasenya ha de tenir almenys 8 caràcters"),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)', message="La contrasenya ha de contenir lletres i números")
    ])
    confirm_password = PasswordField('Confirma la contrasenya', validators=[
        DataRequired(),
        EqualTo('password', message="Les contrasenyes han de coincidir")
    ])
    data_naixement = DateField('Data de naixement', validators=[
        Optional(),
        # Pots afegir una validació per assegurar que l'usuari tingui una edat mínima
    ])
    terms = BooleanField('Accepto els Termes i Condicions', validators=[DataRequired()])
    submit = SubmitField('Registra\'t')

class LoginForm(FlaskForm):
    identifier = StringField('Correu electrònic o Nom d\'usuari', validators=[
        DataRequired(),
        Length(min=3, max=255, message="El correu o nom d'usuari ha de tenir entre 3 i 255 caràcters")
    ])
    password = PasswordField('Contrasenya', validators=[
        DataRequired(),
    ])
    submit = SubmitField('Inicia sessió')