from logging import error
from flask import Flask, render_template, url_for, redirect, request, session
from urllib.parse import urlparse
import psycopg2
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer 
import random
from datetime import date

app = Flask(__name__)
app.secret_key = 'hello'

app.config.from_pyfile('config.cfg')

mail = Mail(app)

s = URLSafeTimedSerializer('secret')

    
def parse():
	result = urlparse("postgres://civgirukxfttcp:5c09e3778935987955c7940bb61c6eb918bed4c82e0e58f838fdf87dd26b8edd@ec2-52-45-238-24.compute-1.amazonaws.com:5432/d5paujj6a5bkhp")
	username = result.username
	password = result.password
	database = result.path[1:]
	hostname = result.hostname
	port = result.port
	return username, password, database, hostname, port


@app.route('/user_index')
def user_index():
    return render_template('user_index.html')


@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')


if __name__ == "__main__":
	app.run(debug=True)