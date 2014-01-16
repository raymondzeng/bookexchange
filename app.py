import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required, user_logged_in
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, SelectField, ValidationError
from wtforms.validators import Required, Length, EqualTo, Email


app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/localdb'  
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] 


db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = '/login'

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
    author = db.Column(ARRAY(db.Text))
    amazon_url = db.Column(db.Text)
    image = db.Column(db.Text)
    courses = db.Column(ARRAY(db.String(140)))
    amazon_price = db.Column(db.Numeric)
    posts = db.relationship('Post', backref='book', lazy='dynamic')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime)
    book_isbn = db.Column(db.BigInteger, db.ForeignKey('book.isbn'))
    price = db.Column(db.Numeric)
    condition = db.Column(db.Integer)
    

class LoginForm(Form):
    email = TextField('email', validators = [Required(), Email()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

    def validate(self):
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
    email = TextField('email', validators = [Required(), Email()])
    password = PasswordField('password', validators = [Required()])
    confirm = PasswordField('confirm', validators = [
        Required(),
        EqualTo('password', message='Passwords must match')])
    fb_url = TextField('facebook')

    def validate_email(form, field):
        user = User.query.filter_by(
            email=field.data).first()
        
        if user is not None:
            raise ValidationError('Email already in use')


class PostForm(Form):
    isbn = TextField('isbn', validators = [Required()])
    price = TextField('price')
    condition = SelectField('condition', choices=[('new', 'New'), 
                                                ('uln', 'Used - Like New'), 
                                                ('uvg', 'Used - Very Good'), 
                                                ('ug', 'Used - Good'), 
                                                ('ua', 'Used - Acceptable'),
                                                ('uua', 'Used - Unacceptable')])
    
    def validate_isbn(form, field):
        if len(field.data) != 10 and len(field.data) != 13:
            raise ValidationError('ISBN must be 10 or 13 digits')

            
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET','POST'])
def index():
    if not current_user.is_authenticated():
        return render_template('home_logged_out.html')
    return render_template('base.html')

@app.route('/sell' , methods=['GET', 'POST'])
def sell():
    form = PostForm()
    if form.validate_on_submit():
        flash('post received')
        return redirect(url_for('index'))
    return render_template('post.html',
                        title = 'Sell Books',
                        user_email = current_user.email,
                        post_form = form)
    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        remember_me = form.remember_me.data
        login_user(form.user,remember=remember_me)
        session['logged_in'] = True
        return redirect(url_for('index'))
        
    return render_template('login.html', 
                           title = 'Sign In',
                           login_form = form)


def register_user(form):
    email = form.email.data
    password = form.password.data
    fb_url = form.fb_url.data
    user = User(email=email, password=password, fb_url=fb_url)
    db.session.add(user)
    db.session.commit()

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        register_user(form)
        login_user(user, remember=True)
        return redirect(url_for('index'))

    return render_template('register.html',
                           title = 'Register',
                           register_form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/book/<isbn>', methods=['GET','POST'])
def get_book(isbn):
    if not isbn.isdigit():
        return jsonify(data='invalid isbn')
    b = Book.query.filter_by(isbn=isbn).first()
    if b is None:
        return jsonify(data='invalid isbn')
    return jsonify(data="%s<br>%s<br>%s<br>%s<br><a href='%s'>amazon</a><br><a href='%s'>image</a>"%(b.isbn,b.title,b.author,b.courses,b.amazon_url,b.image))

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)

