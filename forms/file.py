from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    type_f = TextAreaField("Тип файла")
    info = TextAreaField("Описание")
    type = TextAreaField("Категория")
    fil = TextAreaField("Файл")
    submit = SubmitField('Применить')