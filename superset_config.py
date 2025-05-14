import os
import pymysql
pymysql.install_as_MySQLdb()
from datetime import timedelta

SECRET_KEY = os.environ.get('SUPERSET_SECRET_KEY', 'supersecretkey777')
