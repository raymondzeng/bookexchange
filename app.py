import os, json
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session, abort
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required, user_logged_in
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail, Message
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR
from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, SelectField, TextAreaField, ValidationError
from wtforms.validators import Required, Length, EqualTo, Email
from datetime import datetime
from amazon import get_amazon_info, get_amazon_image
import time
from threading import Thread
import requests
import re


app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] 
sender = os.environ['DEF_SENDER']

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = '/login'

mail = Mail(app)

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
        mailgun = requests.get(
            "https://api.mailgun.net/v2/address/validate",
            auth=("api", "pubkey-0qte70295e2fb293-3prii8dcijm0cu3"),
            params={"address": field.data})
        if not mailgun.json()['is_valid']:
            raise ValidationError('Invalid Email')


    def validate_fb_url(form, field):
        s = field.data.find('facebook.com')
        if s == -1:
            field.data = ''
        else:
            url = field.data[s:]
            field.data = url

class PostForm(Form):
    isbn = TextField('isbn', validators = [Required()])
    price = TextField('price')
    condition = SelectField('condition', choices=[
        ('Used - Like New', 'Used - Like New'),         
        ('Used - Very Good', 'Used - Very Good'), 
        ('Used - Good', 'Used - Good'), 
        ('Used - Acceptable', 'Used - Acceptable'),
        ('Used - Unacceptable', 'Used - Unacceptable'),
        ('New', 'New')])
    comments = TextAreaField('comments')
    courses = TextField('courses')

    def validate_price(form, field):
        if field.data == '':
            return

        if not field.data.replace('.','',1).isdigit():
            raise ValidationError('Price must be a number')
        
    def validate_isbn(form, field):
        isbn = field.data.strip().replace('-','').replace(' ','')
        if len(isbn) != 10 and len(isbn) != 13:
            raise ValidationError('Invalid ISBN')
        form.isbn = field

def send_email(msg):
    mail.send(msg)

def email_subbers(post):
    recip = post.book.subscribers.all()
    if len(recip) == 0:
        return
    recip = map(lambda x: x.user, recip)
    subj = 'New Offer for "%s"'%(str(post.book.title))
    html = render_template('email.html',
                           post=post)
    msg = Message(subj, sender=sender, recipients=recip)
    msg.html = html
    thr = Thread(target = send_email, args = [msg])
    thr.start()

def process_string(s):
    new_s = s.strip()
    if len(new_s) == 14 and '-' in new_s:
        new_s = new_s.replace('-','')
    return new_s

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET','POST'])
def index():
    if not current_user.is_authenticated():
        return render_template('index.html')
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        remember_me = form.remember_me.data
        login_user(form.user,remember=remember_me)
        session['logged_in'] = True
        return redirect(request.args.get("next") or url_for("index"))
        
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
    return user

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = register_user(form)
        login_user(user, remember=False)
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

@app.route('/search')
def search():
    searchterms = request.args.get('q')
    if searchterms is None:
        return redirect(url_for('index'))
    searchterms = process_string(searchterms)
    results = Book.query.filter("setweight(to_tsvector(coalesce(isbn::text,'')), 'A')    || setweight(to_tsvector(coalesce(title,'')), 'B')  || setweight(to_tsvector(coalesce(array_to_string(author,', '),'')), 'B') || setweight(to_tsvector(coalesce(array_to_string(courses,', '),'')), 'B') @@ plainto_tsquery(:ss)").params(ss=searchterms).all()
    #results = Book.query.filter("tsv @@ plainto_tsquery(:ss)").params(ss=searchterms).all()
    
    # for flexible course code search: ABCD##, ABCD### -> ABCD0###
    regex_s = re.search('[A-Z]{4}\d{2,3}',str(searchterms).upper())
    if regex_s is not None:
        s_num = re.search('\d{2,3}', regex_s.group()).group()
        if len(s_num) == 2:
            s_num = s_num + '0'
        s_num = regex_s.group()[:4] + '0' + s_num
        course_search = Book.query.filter("to_tsvector(coalesce(array_to_string(courses,', '),'')) @@ plainto_tsquery(:ss)").params(ss=s_num).all()
        if course_search:
            if results:
                results = list(set(course_search.extend(results)))
            results = course_search
    results = sorted(results, key=lambda x: x.posts.count(), reverse=True)
    results = map(lambda x: x.info_dict(), results)
    return render_template('results.html',
                           results = results,
                           query = searchterms)

@app.route('/book/<isbn>', methods=['GET','POST'])
def book(isbn):
    if not isbn.isdigit():
        return abort(404)
    b = Book.query.filter_by(isbn=isbn).first()
    if b is None:
        return abort(404)
    if current_user.is_authenticated():
        user_subs = current_user.subscriptions
        subbed = any(str(sub.isbn) == isbn for sub in user_subs)
    else:
        subbed = False
    return render_template('book.html',
                           book=b.info_dict(),
                           posts=b.get_posts(),
                           subbed=subbed)

@app.route('/post', methods=['GET','POST'])
@login_required
def post():
    form = PostForm()
    if request.method == 'GET':
        if request.args.get('isbn'):
            form.isbn.data = request.args.get('isbn')
    if form.validate_on_submit():
        isbn = form.isbn.data.strip().replace('-','').replace(' ','')
        price = form.price.data
        if price == '':
            price = None
        cond = form.condition.data
        comments = form.comments.data
        courses = form.courses.data.strip().replace(' ','').upper()
        if len(courses) > 9:
            courses = ''
        if not Book.query.get(isbn):
            info = get_amazon_info(isbn)
            image = get_amazon_image(isbn)
            b = Book(isbn=isbn, title=info['title'], author=info['author'], amazon_url=info['url'], image=image, courses=[courses])
            db.session.add(b)
            db.session.commit()
        else:
            b = Book.query.get(isbn)
            old_courses = list(b.courses)
            old_courses.append(courses)
            b.courses = list(set(old_courses))
            db.session.commit()
        p = Post(uid=current_user.id, timestamp=datetime.utcnow(), isbn=isbn, price=price,condition=cond,comments=comments)
        db.session.add(p)
        db.session.commit()
        email_subbers(p)
        return redirect(url_for('book',isbn=isbn))
    return render_template('post.html',
                           post_form = form)

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    pid = request.form['id']
    post = Post.query.get(pid)
    if post.seller.id == current_user.id:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/editpost', methods=['POST'])
@login_required
def edit_post():
    price = request.form['editprice']
    comments = request.form['editcomments']
    pid = request.form['editid']
    post = Post.query.get(pid)
    if post.seller.id == current_user.id:
        if price != '' and price.isdigit():
            post.price = price
        if comments != '':
            if comments == 'NONE':
                comments = ''
            post.comments = comments
        post.timestamp = datetime.utcnow()
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/subscribe', methods=['POST'])
@login_required
def subscribe():
    isbn = request.form['isbn']
    email = current_user.email
    s = Subscription(timestamp=datetime.utcnow(), user=email, isbn=isbn)
    db.session.add(s)
    db.session.commit()
    return redirect(request.referrer)

@app.route('/unsubscribe',methods=['POST'])
@login_required
def unsubscribe():
    isbn = request.form['isbn']
    email = current_user.email
    s = Subscription.query.filter_by(isbn=isbn,user=email).first()
    db.session.delete(s)
    db.session.commit()
    return redirect(request.referrer)

@app.route('/info/<isbn>')
@login_required
def info(isbn):
    isbn = isbn.strip().replace('-','').replace(' ','')
    if len(isbn) != 13 or not isbn.isdigit():
        return jsonify(data=None)
    i = Book.query.get(isbn)
    if i:
        return jsonify(
            title=i.title,
            image=i.image,
            author=i.author,
            courses=i.courses)
    time.sleep(1)
    img = get_amazon_image(isbn)
    time.sleep(1)
    info = get_amazon_info(isbn)
    if info:
        return jsonify(
            title=info['title'],
            image=img,
            author=info['author'])
    return jsonify(title=None)

@app.route('/settings', methods=['GET','POST'])
@login_required
def settings():
    choice = request.args.get('myselect')
    fb = request.args.get('myinput')
    i = fb.find('facebook.com')
    if i == -1:
        fb = ''
    else:
        fb = fb[i:]
    current_user.fb_url = fb
    current_user.pref = choice
    db.session.commit()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)

