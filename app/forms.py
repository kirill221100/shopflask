from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, RadioField, IntegerRangeField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_login import current_user
from app import db
from app.models import User

def is_mail_exist(form, field):
    if db.session.query(User).filter(User.mail == field.data).first():
        raise ValidationError('Аккаунт с такой почтой уже есть')

def is_phone(form, field):
    if field.data < 79000000000 or field.data > 79999999999:
        raise ValidationError('Не телефон')

def is_mail_exist_auth(form, field):
    if not db.session.query(User).filter(User.mail == field.data).first():
        raise ValidationError('Аккаунт с такой почтой не существует')

def is_mail_exist_order(form, field):
    if current_user.mail != field.data:
        raise ValidationError('Это не ваша почта')

class OrderForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    mail = StringField('Электропочта', validators=[DataRequired(), Email(), is_mail_exist_order])
    phone = IntegerField('Телефон (с 7 без +)', validators=[DataRequired(), is_phone])
    submit = SubmitField('Оформить заказ')

class RegisterForm(FlaskForm):
    mail = StringField('', validators=[DataRequired(), Email(message='хуета'), is_mail_exist])
    password = StringField('', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Зарегистрироваться')

class AuthForm(FlaskForm):
    mail = StringField('', validators=[DataRequired(), Email(), is_mail_exist_auth])
    password = StringField('', validators=[DataRequired()])
    submit = SubmitField('Авторизоваться')