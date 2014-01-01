import os

from flask import Flask, request, render_template, jsonify
from database import email_in_use, add_user

app = Flask(__name__)

@app.route("/validate_email", methods= ['GET','POST'])
def validate_email():
    e = request.args.get('e')
    taken = email_in_use(e)
    return jsonify(result = taken)

@app.route("/register", methods= ['GET', 'POST'])
def register():
    #e = request.args.get('e','')
    #p = request.args.get('p','')
    #add_user(e,p)
    return render_template('register.html')


@app.route("/")
def home():
    return render_template("index.html")

