from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class VehicleForm(FlaskForm):
    matricula = StringField('Matrícula', validators=[DataRequired(), Length(min=7, max=8)])
    marca = StringField('Marca', validators=[DataRequired(), Length(min=1, max=50)])
    model = StringField('Model', validators=[DataRequired(), Length(min=1, max=50)])
    color = StringField('Color', validators=[Length(max=30)])
    num_places = IntegerField('Nombre de places', validators=[DataRequired(), NumberRange(min=1, max=9)])
    tipus_vehicle_id = SelectField('Tipus de vehicle', coerce=int, validators=[DataRequired()])