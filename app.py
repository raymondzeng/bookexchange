import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, g
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required, user_logged_in
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required, Length, EqualTo


app = Flask(__name__)
app.config.from_object('config')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/localdb'  
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] 


db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = '/'

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    fb_url = db.Column(db.Text, default=None)
    posts = db.relationship('Post', backref='seller', lazy='dynamic')

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

class Book(db.Model):
    isbn = db.Column(db.BigInteger, primary_key=True, unique=True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    amazon_url = db.Column(db.Text)
    image = db.Column(db.Text)
    courses = db.Column(db.String(140))
    posts = db.relationship('Post', backref='book', lazy='dynamic')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime)
    book_isbn = db.Column(db.BigInteger, db.ForeignKey('book.isbn'))
    price = db.Column(db.Integer)
    condition = db.Column(db.Integer)
    
class LoginForm(Form):
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

    def validate(self):
        print 'ui'
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            email=self.email.data).first()
        
        if user is None:
            self.email.errors.append('Invalid email')
            return False

        if not user.password == self.password.data:
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True

class RegisterForm(Form):
    email = TextField('email', validators = [
        Required(),
        Length(min=6, max=35)])
    password = PasswordField('password', validators = [Required()])
    confirm = PasswordField('confirm', validators = [
        Required(),
        EqualTo('password', message='Passwords must match')])
    fb_url = TextField('facebook')

    def validate(self):
        print 'ui'
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            email=self.email.data).first()
        
        if user is not None:
            self.email.errors.append('Email already in use')
            return False

        return True

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


@app.route('/book/<isbn>')
def get_book(isbn):
    b = Book.query.filter_by(courses=isbn).first()
    if b is None:
        return 'invalid isbn'
    return "%s<br>%s<br>%s<br>%s<br><a href='%s'>amazon</a><br><a href='%s'>image</a>"%(b.isbn,b.title,b.author,b.courses,b.amazon_url,b.image)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)

