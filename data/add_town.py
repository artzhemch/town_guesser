from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class AddTownForm(FlaskForm):
    town_name = StringField('Название города', validators=[DataRequired()])
    api_request_string = StringField('Запрос к API')
    submit = SubmitField('Submit')
