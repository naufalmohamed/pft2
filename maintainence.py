from urllib.parse import urlparse
import psycopg2

def parse():
	result = urlparse("postgres://civgirukxfttcp:5c09e3778935987955c7940bb61c6eb918bed4c82e0e58f838fdf87dd26b8edd@ec2-52-45-238-24.compute-1.amazonaws.com:5432/d5paujj6a5bkhp")
	username = result.username
	password = result.password
	database = result.path[1:]
	hostname = result.hostname
	port = result.port
	return username, password, database, hostname, port


username, password, database, hostname, port = parse()
dbconn = psycopg2.connect(database = database,user = username,password = password,host = hostname,port = port)
cursor = dbconn.cursor()
sql = open("db.sql", "r").read()
cursor.execute(sql)
dbconn.commit()
