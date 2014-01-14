import app
from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required, Length, EqualTo

class User(app.db.Model):

    id = app.db.Column(app.db.Integer, primary_key=True)
    email = app.db.Column(app.db.String(120), unique=True)
    password = app.db.Column(app.db.String(120))
    fb_url = app.db.Column(app.db.Text, default=None)
    posts = app.db.relationship('Post', backref='seller', lazy='dynamic')

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

class Book(app.db.Model):
    isbn = app.db.Column(app.db.Integer, primary_key=True)
    title = app.db.Column(app.db.String(140))
    author = app.db.Column(app.db.String(140))
    amason_url = app.db.Column(app.db.Text)
    classes = app.db.Column(app.db.String(20))
    posts = app.db.relationship('Post', backref='book', lazy='dynamic')

class Post(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    uid = app.db.Column(app.db.Integer, app.db.ForeignKey('user.id'))
    timestamp = app.db.Column(app.db.DateTime)
    book_isbn = app.db.Column(app.db.Integer, app.db.ForeignKey('book.isbn'))
    price = app.db.Column(app.db.Integer)
    condition = app.db.Column(app.db.Integer)
    
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
