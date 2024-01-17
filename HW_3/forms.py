'''Создать форму для регистрации пользователей на сайте. Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться". При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    user_name = StringField('User_name', validators=[DataRequired()])
    user_surname = StringField('User_surname', validators=[DataRequired()])
    email = EmailField('User_email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('ConfirmPassword', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')



