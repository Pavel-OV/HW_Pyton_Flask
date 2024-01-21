'''Создать форму для регистрации пользователей на сайте. Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться". При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.'''

from flask import Flask, render_template, request, redirect, url_for
from hashlib import sha256
from flask_wtf.csrf import CSRFProtect
from models import db, User
from forms import RegistrationForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '.pol,mkijnuhbytghjhjkk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdatabase.db'
db.init_app(app)
csrf = CSRFProtect


@app.cli.command("init_db")
def init_db():
    db.create_all()
    
   

@app.route('/', methods=['GET', 'POST'])
def index():
    return  render_template('index.html')


@app.route('/base/', methods=['GET', 'POST'])
def register():    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(user_name=form.user_name.data,
                   user_surname=form.user_surname.data,
                   email=form.email.data, 
                   password=sha256(form.password.data.encode(encoding='utf-8')).hexdigest())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('register'))
    return  render_template('register.html', form=form)


if __name__ == '__main__':  
    app.run(debug=True)


    
