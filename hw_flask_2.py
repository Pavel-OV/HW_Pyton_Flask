'''Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой будет создан cookie-файл с данными пользователя, а также будет произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл с данными пользователя и произведено перенаправление на страницу ввода имени и электронной почты.'''

from multiprocessing import context
from flask import Flask, render_template, request, redirect, url_for, make_response, session

app = Flask(__name__)


app.secret_key = "asrtyh123hkilklfswsr"

@app.get('/')
def submit_get():
    context = {
        'login': 'Авторизация'
    }
    return render_template('index.html', **context)


@app.post('/')
def submit_post():
    session['login'] = request.form.get('login')
    session['email'] = request.form.get('email')
    return redirect(url_for('success'))


@app.route('/user_login/', methods=['GET', 'POST'])
def success():
    if 'login' in session:
        context = {
            'login': session['login'],
            'email': session['email'],
        }
        if request.method == 'POST':
            session.pop('login', None)
            session.pop('email', None)
            return redirect(url_for('submit_get'))
        return render_template('user_login.html', **context)
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)