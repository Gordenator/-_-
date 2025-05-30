from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

# Инициализация БД
db = SQLAlchemy(app)

# Настройка Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Главная страница
@app.route('/')
def home():
    return render_template('index.html')

# О нас
@app.route('/about')
def about():
    return render_template('about.html')

# Меню
@app.route('/menu')
def menu():
    return render_template('menu.html')

# Галерея
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

# Бронирование
@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        # Обработка бронирования
        return render_template('reservation.html', success=True)
    return render_template('reservation.html')

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        flash('Вы успешно вошли!', 'success')
        return redirect(url_for('account'))
    return render_template('login.html')

# Выход
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Личный кабинет
@app.route('/account')
@login_required
def account():
    return render_template('account.html')

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Здесь может быть обработка данных формы
        return redirect(url_for('login'))
    return render_template('register.html')

# Добавляем недостающий роут для восстановления пароля
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('reset_password.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)