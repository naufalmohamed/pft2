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


@app.route('/login_page_client')
def login_page_client():
    return render_template('login_page_client.html')
   

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        username, password, database, hostname, port = parse()
        email = request.form.get("email")
        psw = request.form.get("psw")
        login_type = request.form.get("login_type")
        if login_type == "therapist":
            try:
                dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
                cursor = dbconn.cursor()
                cursor.execute(f"SELECT * FROM therapist_cred WHERE email = %s;",[email])
                cred = cursor.fetchall()
                dbconn.commit()
            except:
                return redirect(url_for("login_page"))

            if cred[0][2] == psw:
                session['user'] = email
                session['first_name'] = cred[0][3]
                session['last_name'] = cred[0][4]
                session['id'] = cred[0][0]
                return redirect(url_for('therapist'))
            else:
                return redirect(url_for('login_page'))     
        else:
            try:
                dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
                cursor = dbconn.cursor()
                cursor.execute(f"SELECT password FROM client_cred WHERE email = %s;",[email])
                cred = cursor.fetchall()
                dbconn.commit()
            except:
                    return redirect(url_for("login_page_client"))

            if cred[0][0] == psw:
                session['user'] = email
                return redirect(url_for('user_index'))
            else:
                return redirect(url_for('login_page_client'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/user_index')
def user_index():
    return render_template('user_index.html', email = session['user'])


@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')


@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')


if __name__ == "__main__":
	app.run(debug=True)