from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Minh!2000'
app.config['MYSQL_DATABASE_DB'] = 'car'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY']='minh123'
mysql.init_app(app)


sql_statement={
    "HangXe": "SELECT DISTINCT HangXe from carinfo",
    "XuatXu": "SELECT DISTINCT XuatXu from carinfo",
    "KieuDang": "SELECT DISTINCT KieuDang from carinfo",
    "NgoaiThat": "SELECT DISTINCT NgoaiThat from carinfo",
    "NoiThat": "SELECT DISTINCT NoiThat from carinfo",
    "NhienLieu": "SELECT DISTINCT NhienLieu from carinfo",
    "HopSo": "SELECT DISTINCT HopSo from carinfo",
    "DanDong": "SELECT DISTINCT DanDong from carinfo",
}