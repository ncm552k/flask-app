import pymysql
from app import app
from config import mysql
from flask import jsonify, request, make_response
from math import ceil
from functools import wraps
import jwt

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


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user_id = 
            current_user = User.query\
                .filter_by(public_id = data['id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
    return decorated


@app.route('/api/login', methods =['POST'])
def login():
    # creates dictionary of form data
    auth = request.form
  
    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
  
    user = User.query\
        .filter_by(email = auth.get('email'))\
        .first()
  
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
  
    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
  
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )

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