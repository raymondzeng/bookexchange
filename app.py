import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, g
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required, user_logged_in
from flask.ext.sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config.from_object('config')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/localdb'  
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] 


db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = '/'

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET','POST'])
def index():
    if not current_user.is_authenticated():
        return redirect(url_for('login'))
    return current_user.email

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        remember_me = form.remember_me.data
        login_user(form.user,remember=remember_me)
        return redirect(url_for('index'))
        
    return render_template('login.html', 
        title = 'Sign In',
        login_form = form)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        fb_url = form.fb_url.data
        user = User(email=email, password=password, fb_url=fb_url)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('index'))

    return render_template('register.html',
        title = 'Register',
        register_form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)

