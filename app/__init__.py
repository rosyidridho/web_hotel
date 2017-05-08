from flask import Flask
import MySQLdb as mysql

app = Flask(__name__)
app.secret_key='some_secret'
from app import views
