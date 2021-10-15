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


@app.route('/')
def index():
    return render_template('index2.html')


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
                return redirect(url_for("login_page_client"))

            if cred[0][2] == psw:
                session['user'] = email
                session['first_name'] = cred[0][3]
                session['last_name'] = cred[0][4]
                session['id'] = cred[0][0]
                return redirect(url_for('therapist_index'))
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
    return redirect(url_for('login_page_client'))


@app.route('/register_client_page')
def register_client_page():
    return render_template('register.html')


@app.route('/register_client', methods=['POST'])
def register_client():
    if request.method == 'POST':
        username, password, database, hostname, port = parse()
        email = request.form.get("email")
        psw = request.form.get("psw")
        psw_repeat = request.form.get("psw_repeat")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
        cursor = dbconn.cursor()
        cursor.execute(f"""INSERT INTO client_cred (email, password, status,first_name,last_name) VALUES (%s,%s,%s,%s,%s);""",(email,psw,'empty',first_name,last_name))
        dbconn.commit()
        return redirect('login_page_client')


@app.route('/user_index')
def user_index():
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f"""SELECT * FROM client_cred WHERE email = %s""",[session['user']])
    client_info = cursor.fetchall()
    session['firstname'] = client_info[0][3]
    session['lastname'] = client_info[0][4]
    for i in client_info[0]:
        if i == 'empty':
            session['profile_complete'] = False
        else:
            session['profile_complete'] = True
            session['client_info'] = client_info

    if session['profile_complete']:
        description = 'We will let you know when a therapist accepts your profile'
    else:
        description = 'Please Complete Profile'

    return render_template('user_index.html', email = session['user'], client_info = client_info, description = description, profile_complete = session['profile_complete'])


@app.route('/user_profile')
def user_profile():
    client_info = session['client_info']
    return render_template('user_profile.html' ,client_info = client_info)


@app.route('/edit_profile')
def edit_profile():
    if 'user' in session:
        client_info = session['client_info']
        return render_template('edit_profile.html', client_info = client_info)
    else:
        return redirect(url_for('login_page_client'))


@app.route('/edit_info', methods=['POST'])
def edit_info():
    if request.method == 'POST':
        phone = request.form.get('phone')
        age = request.form.get('age')
        print(age)
        city = request.form.get('city')
        occupation = request.form.get('occupation')
        concerns = request.form.get('concerns')
        relationship_status = request.form.get('relationship_status')
        timeperiod = request.form.get('timeperiod')
        username, password, database, hostname, port = parse()
        dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
        cursor = dbconn.cursor()
        cursor.execute(f"""UPDATE client_cred SET phonenumber = %s WHERE email = %s;""",(phone,session['user']))
        cursor.execute(f"""UPDATE client_cred SET age = %s WHERE email = %s;""",(age,session['user']))
        cursor.execute(f"""UPDATE client_cred SET city = %s WHERE email = %s;""",(city,session['user']))
        cursor.execute(f"""UPDATE client_cred SET occupation = %s WHERE email = %s;""",(occupation,session['user']))
        cursor.execute(f"""UPDATE client_cred SET concerns = %s WHERE email = %s;""",(concerns,session['user']))
        cursor.execute(f"""UPDATE client_cred SET relationship_status = %s WHERE email = %s;""",(relationship_status,session['user']))
        cursor.execute(f"""UPDATE client_cred SET timeperiod = %s WHERE email = %s;""",(timeperiod,session['user']))
        cursor.execute(f"""UPDATE client_cred SET status = %s WHERE email = %s;""",('free',session['user']))
        cursor.execute(f"""UPDATE client_cred SET therapist = %s WHERE email = %s;""",('free',session['user']))
        dbconn.commit()
        return redirect(url_for('user_index'))


@app.route('/therapist_index')
def therapist_index():
    email = session['user']
    arr = email.split('@')
    arr_2 = arr[1].split('.')
    arr_3 = [arr[0],arr_2[0]]
    table_name = ''.join(arr_3)
    session['table_name'] = table_name
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f"""SELECT * FROM client_cred;""")
    client_info = cursor.fetchall()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {session['table_name']} ( id serial PRIMARY KEY, date VARCHAR NOT NULL, status VARCHAR, client VARCHAR);")
    dbconn.commit()
    return render_template('therapist_index.html', client_info = client_info, session = session)


@app.route('/accepted_clients')
def accepted_clients():
    username, password, database, hostname, port = parse()
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f"""SELECT * FROM {session['table_name']};""")
    client_info = cursor.fetchall()
    dbconn.commit()
    return render_template('therapist_index.html', client_info = client_info, session = session)


@app.route('/accept_client/<ref_email>')
def accept_client(ref_email):
    username, password, database, hostname, port = parse()
    arr = ref_email.split('@')
    arr_2 = arr[1].split('.')
    arr_3 = [arr[0],arr_2[0]]
    ref_email_arr = ''.join(arr_3)
    dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
    cursor = dbconn.cursor()
    cursor.execute(f"""UPDATE client_cred SET status = %s WHERE email = %s;""",('accepted',ref_email))
    cursor.execute(f"""UPDATE client_cred SET therapist = %s WHERE email = %s;""",(session['user'],ref_email))
    cursor.execute(f"""INSERT INTO {session['table_name']} (date,status,client) VALUES (%s,%s,%s);""",(date.today(),'accepted',ref_email_arr))
    dbconn.commit()

    return redirect(url_for('therapist_index'))

if __name__ == "__main__":
	app.run(debug=True)