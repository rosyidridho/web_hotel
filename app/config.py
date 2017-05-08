import MySQLdb as mysql
import json
import os

DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
FILE_CONFIG = os.path.join(DIR, 'config.json')

try:
    with open(FILE_CONFIG) as config:
        data_json = json.loads(config.read())
except Exception as e:
    raise e

koneksi = mysql.connect(
    host = data_json["db"]["db_host"],
    user = data_json["db"]["db_user"],
    passwd = data_json["db"]["db_password"],
    db = data_json["db"]["db_name"]
)

UPLOAD_FOLDER = os.path.join(DIR, data_json["upload_folder"])

ALLOWED_EXTENSIONS = data_json["allowed_extensions"]
