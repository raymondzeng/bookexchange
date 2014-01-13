import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, g
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required, user_logged_in
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] #'postgresql://localhost/localdb' 


db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.email)


class LoginForm(Form):
    email = TextField('email', validators = [Required()])
    password = TextField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)



@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods = ['GET', 'POST'])
def login():

    if current_user is not None and current_user.is_authenticated():
        return "logged in rem"

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                login_user(user,remember=remember_me)
                flash("sucess")
                return str(remember_me)
            else:
                flash("incorrect password")
        else:
            flash('user does not exist')
        
    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)

