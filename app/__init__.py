from flask import Flask
from flask_mysql_connector import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = "127.0.0.1"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "abonitalla123"
app.config['MYSQL_DB'] = "crude_studentdb"
app.secret_key = "mysecretkey"

mysql = MySQL(app)

from app import routes