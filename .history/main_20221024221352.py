import pymysql
from app import app
from config import mysql
from flask import jsonify, request, make_response, redirect
from math import ceil
from functools import wraps
import jwt
from datetime import datetime, timedelta

#lấy ra danh sách xe
@app.route("/api/cars", methods=["GET"])
def get_cars():
    page=int(request.args.get("page"))
    search=request.args.get("search").split(' ')
    search='%'.join(search).lower()
    limit = str((page-1)*20)
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = f"SELECT * FROM carinfo LIMIT 20 OFFSET {limit}"
        sqlQuery2 = f"SELECT COUNT(ID) as totalPages FROM carinfo"

        if search:
            sqlQuery = f"SELECT * FROM car.carinfo\
                    WHERE LOWER(CONCAT(carinfo.HangXe,' ', carinfo.DongXe,' ',carinfo.NamSX))\
                    LIKE '%{search}%' LIMIT 20 OFFSET {limit}"
            sqlQuery2 = f"SELECT COUNT(ID) as totalPages FROM carinfo\
                    WHERE CONCAT(carinfo.HangXe,' ', carinfo.DongXe,' ',carinfo.NamSX)\
                    LIKE '%{search}%' LIMIT 20 OFFSET {limit}"

        cursor.execute(sqlQuery2)
        pages_num = cursor.fetchone()
        cursor.execute(sqlQuery)
        dataRows = cursor.fetchall()
        res = {"data": dataRows, "totalPages":ceil(pages_num["totalPages"]/20)}
        response = jsonify(res)
        response.status_code=200
        return response 	
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

#thêm thông tin xe mới
@app.route("/api/add-car", methods=["POST"])
@token_required
def add_car():
    try:
        body = request.json
        print(body)
        HinhAnh = body['HinhAnh']
        HangXe = body['HangXe']
        DongXe = body['DongXe']
        NamSX = int(body['NamSX'])
        XuatXu = body['XuatXu']
        KieuDang = body['KieuDang']
        SoKm = int(body['SoKm'])
        NgoaiThat = body['NgoaiThat']
        NoiThat = body['NoiThat']
        NhienLieu = body['NhienLieu']
        DongCo = float(body['DongCo'])
        HopSo = body['HopSo']
        DanDong = body['DanDong']
        Gia = int(body['Gia'])
        
        if HinhAnh and HangXe and DongXe and NamSX and XuatXu and KieuDang and SoKm and NgoaiThat and NoiThat and NhienLieu and DongCo and HopSo and DanDong and Gia:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO carinfo VALUES(NULL,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            bindData = (HinhAnh, HangXe, DongXe, NamSX, XuatXu, KieuDang, SoKm, NgoaiThat, NoiThat, NhienLieu, DongCo, HopSo, DanDong, Gia)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Car information added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()    

#xoá thông tin xe
@app.route('/api/delete-car/<int:id>', methods=['POST'])
@token_required
def delete_emp(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM carinfo WHERE id =%s", id)
		conn.commit()
		respone = jsonify('Car Information deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#cập nhật thông tin xe
@app.route("/api/update-car", methods=["POST"])
@token_required
def update_car():
    try:
        body = request.json
        print(body)
        _id = body['ID']
        HinhAnh = body['HinhAnh']
        HangXe = body['HangXe']
        DongXe = body['DongXe']
        NamSX = int(body['NamSX'])
        XuatXu = body['XuatXu']
        KieuDang = body['KieuDang']
        SoKm = int(body['SoKm'])
        NgoaiThat = body['NgoaiThat']
        NoiThat = body['NoiThat']
        NhienLieu = body['NhienLieu']
        DongCo = float(body['DongCo'])
        HopSo = body['HopSo']
        DanDong = body['DanDong']
        Gia = int(body['Gia'])
        
        if _id and HinhAnh and HangXe and DongXe and NamSX and XuatXu and KieuDang and SoKm and NgoaiThat and NoiThat and NhienLieu and DongCo and HopSo and DanDong and Gia:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "UPDATE carinfo SET HinhAnh=%s, HangXe=%s, DongXe=%s, NamSX=%s,\
                        XuatXu=%s, KieuDang=%s, SoKm=%s, NgoaiThat=%s, NoiThat=%s, NhienLieu=%s, DongCo=%s, HopSo=%s, DanDong=%s, Gia=%s \
                        WHERE ID=%s"
            bindData = (HinhAnh, HangXe, DongXe, NamSX, XuatXu, KieuDang, SoKm, NgoaiThat, NoiThat, NhienLieu, DongCo, HopSo, DanDong, Gia, _id)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Car information updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 





@app.route('/api/login', methods =['POST'])
def login():
    body = request.json
    username=body['username']
    password=body['password']
  
    if not username and not password:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT ID FROM account WHERE username=%s AND password=%s", (username, password))
    data = cursor.fetchone()
    cursor.close() 
    conn.close()

    if not data:
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate' : 'Basic realm ="Wrong Username or Password !!"'}
        )

    token = jwt.encode({
            'user_id': data['ID'],
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
  
    return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)

#check-manage
@app.route('/manage', methods =['GET'])
def check_user():
    try:
        token= request.headers['x-access-token']
        if not token:
            return redirect('localhost:3000/login', 401)
        
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user_id = data['user_id']
        cursor.execute("SELECT ID FROM account WHERE ID=%s", (user_id))
        result = cursor.fetchone()

        if not result:
            return redirect('localhost:3000/login', 401)

    except Exception as e:
        print(e)
    finally:    
        cursor.close() 
        conn.close()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return redirect('localhost:3000/login', 401)
        
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user_id = data['user_id']
        cursor.execute("SELECT ID FROM account WHERE ID=%s", (user_id))
        result = cursor.fetchone()
        cursor.close() 
        conn.close() 

        if not result:
            return redirect('localhost:3000/login', 401)

        # returns the current logged in users context to the routes
        return  f(*args, **kwargs)
    return decorated


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.run(debug=True)