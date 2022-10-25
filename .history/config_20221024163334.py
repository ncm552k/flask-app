from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Minh!2000'
app.config['MYSQL_DATABASE_DB'] = 'car'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY']='minh123'
mysql.init_app(app)