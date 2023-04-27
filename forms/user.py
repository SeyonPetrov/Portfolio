from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, IntegerField, \
    RadioField
from wtforms.validators import DataRequired
from фнекдот import joke
import requests
import random
from deep_translator import GoogleTranslator


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()],
                       render_kw={'placeholder': 'ВАША ПОЧТА'})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={'placeholder': 'ВАШ ПАРОЛЬ'})
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()],
                                   render_kw={'placeholder': 'ВАШ ПАРОЛЬ ЕЩЕ РАЗ'})
    name = StringField('Имя пользователя', validators=[DataRequired()],
                       render_kw={'placeholder': 'ВАШЕ ИМЯ'})
    place_job_study = StringField("Место работы/учёбы", validators=[DataRequired()],
                                  render_kw={'placeholder': 'МЕСТО РАБОТЫ / УЧЕБЫ'})
    address = StringField("Город", validators=[DataRequired()],
                          render_kw={'placeholder': 'ВАШ ГОРОД'})
    age = IntegerField("ВОЗРАСТ", validators=[DataRequired()])
    phone_num = StringField('Номер телефона', validators=[DataRequired()],
                            render_kw={'placeholder': 'ВАШ НОМЕР ТЕЛЕФОНА'})
    sex = RadioField('ПОЛ', choices=['Женский', 'Мужской'])
    submit = SubmitField('ВОЙТИ')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()],
                       render_kw={'placeholder': 'ВАША ПОЧТА'})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={'placeholder': 'ВАШ ПАРОЛЬ'})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('ВОЙТИ')


class IDForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()],
                      render_kw={'placeholder': 'ПОИСК ПОРТФОЛИО ПО ID'})
    submit = SubmitField('Поиск')


class AnecForm(FlaskForm):
    text = TextAreaField('', render_kw={'placeholder': joke()})


def transfer(mytext):
    trns = GoogleTranslator(source='auto', target='ru').translate(mytext)
    return trns


class TextApiForm(FlaskForm):
    fact = requests.get(f'http://numbersapi.com/random/{random.choice(["trivia", "math"])}?json').json()
    trans_f = transfer(str(fact['text']))
    text = TextAreaField(f'', render_kw={
        'placeholder': f'{trans_f}'
    })


class JustForm(FlaskForm):
    pass


