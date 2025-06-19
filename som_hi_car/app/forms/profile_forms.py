from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, DateField, SelectField,BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional
from app.daos.ubicacio_dao import UbicacioDAO
from database.db import db

class ProfileForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    cognom = StringField('Cognom', validators=[DataRequired()])
    email = StringField('Correu electrònic', validators=[DataRequired(), Email()])
    telefon_mobil = StringField('Telèfon mòbil', validators=[DataRequired()])
    telefon_fix = StringField('Telèfon fix', validators=[Optional()])
    adreca = StringField('Adreça', validators=[Optional()])
    data_naixement = DateField('Data de naixement', validators=[Optional()])
    nova_contrasenya = PasswordField('Nova contrasenya', validators=[
        Optional(),
        Length(min=8, message="La contrasenya ha de tenir almenys 8 caràcters")
    ])
    avatar = FileField('Imatge de perfil', validators=[
        Optional(),
        FileAllowed(['jpg', 'png'], 'Només es permeten imatges JPG o PNG')
    ])
    ubicacio_id = SelectField('Ubicació', coerce=int, validators=[Optional()])

    confirmation_needed = BooleanField('¿Confirmación necesaria?')


    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        ubicacio_dao = UbicacioDAO(db)
        ubicacions = ubicacio_dao.get_all()
        self.ubicacio_id.choices = [(0, 'Selecciona una ubicació')] + [(u.id, u.nom) for u in ubicacions]