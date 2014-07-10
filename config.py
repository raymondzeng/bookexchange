import os

CSRF_ENABLED = True
SECRET_KEY = os.environ['SECRET_KEY']
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ['GMAIL_U']
MAIL_PASSWORD = os.environ['GMAIL_P']
DEFAULT_MAIL_SENDER = os.environ['DEF_SENDER']
DATABASE_URI = 'postgresql://localhost/localdb'  
