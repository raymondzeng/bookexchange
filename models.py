from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    fb_url = db.Column(db.Text, default=None)
    pref = db.Column(db.Text, default='e')
    posts = db.relationship('Post', backref='seller', lazy='dynamic')
    subscriptions = db.relationship('Subscription', backref='subscriber', lazy='dynamic')

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
    tsv = db.Column(TSVECTOR)
    posts = db.relationship('Post', backref='book', lazy='dynamic')
    subscribers = db.relationship('Subscription', backref='book', lazy='dynamic')
    def info_dict(self):
        return {'isbn': self.isbn,
                'title': self.title,
                'author': self.author,
                'amazon_url': self.amazon_url,
                'image': self.image,
                'courses': self.courses,
                'post_count': self.posts.count()}

    def get_posts(self):
        return self.posts


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime)
    isbn = db.Column(db.BigInteger, db.ForeignKey('book.isbn'))
    price = db.Column(db.Numeric)
    condition = db.Column(db.Text)
    comments = db.Column(db.Text)
    
    
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    user = db.Column(db.String(120), db.ForeignKey('user.email'))
    isbn = db.Column(db.BigInteger, db.ForeignKey('book.isbn'))
