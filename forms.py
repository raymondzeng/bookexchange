from flask_wtf import Form
from wtforms.validators import Required, Length, EqualTo, Email
from wtforms import TextField, BooleanField, PasswordField, SelectField, TextAreaField, ValidationError

from models import *

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
