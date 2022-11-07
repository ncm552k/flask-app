import pymysql
from app import app
from config import mysql,sql_statement
from flask import jsonify, request, make_response, redirect
from math import ceil
from functools import wraps
import jwt
from datetime import datetime, timedelta
from predictor import Predictor

model = Predictor()
model.initModel()

#check token
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
        data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
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



#lấy ra danh sách xe
@app.route("/api/cars", methods=["GET"])
def get_cars():
    page=int(request.args.get("page"))
    search=request.args.get("search")
    if search:
        search=search.split(' ')
        search='%'.join(search).lower()
    limit = (page-1)*20
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
                    WHERE LOWER(CONCAT(carinfo.HangXe,' ', carinfo.DongXe,' ',carinfo.NamSX))\
                    LIKE '%{search}%'"

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
        
        if HangXe and DongXe and NamSX and XuatXu and KieuDang and SoKm and NgoaiThat and NoiThat and NhienLieu and DongCo and HopSo and DanDong and Gia:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO carinfo VALUES(NULL,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            bindData = (HinhAnh, HangXe, DongXe, NamSX, XuatXu, KieuDang, SoKm, NgoaiThat, NoiThat, NhienLieu, DongCo, HopSo, DanDong, Gia)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify({"message": "OK"})
            response.status_code = 200
            return response
        else:
            return showMessage(e)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()


@app.route("/api/get-car-by-id/<int:id>", methods=["GET"])
def get_car_by_id(id):
    try:  
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)		
        sqlQuery = "SELECT * FROM carinfo WHERE ID=%s"        
        cursor.execute(sqlQuery, id)
        res = cursor.fetchone()
        response = jsonify(res)
        response.status_code = 200
        return response
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
        
        if _id and HangXe and DongXe and NamSX and XuatXu and KieuDang and SoKm and NgoaiThat and NoiThat and NhienLieu and DongCo and HopSo and DanDong and Gia:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "UPDATE carinfo SET HinhAnh=%s, HangXe=%s, DongXe=%s, NamSX=%s,\
                        XuatXu=%s, KieuDang=%s, SoKm=%s, NgoaiThat=%s, NoiThat=%s, NhienLieu=%s, DongCo=%s, HopSo=%s, DanDong=%s, Gia=%s \
                        WHERE ID=%s"
            bindData = (HinhAnh, HangXe, DongXe, NamSX, XuatXu, KieuDang, SoKm, NgoaiThat, NoiThat, NhienLieu, DongCo, HopSo, DanDong, Gia, _id)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify({"message": "OK"})
            response.status_code = 200
            return response
        else:
            return showMessage(e)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
        



#xoá thông tin xe
@app.route('/api/delete-car/<int:id>', methods=['POST'])
@token_required
def delete_car(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM carinfo WHERE id =%s", id)
        conn.commit()
        response = jsonify({"message":'Car Information deleted successfully!'})
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
    


#lấy thông tin các field
@app.route("/api/get-field-info",methods=["GET"])
def get_field_info():
    try:
        HangXe =[]
        XuatXu=[]
        KieuDang=[]
        NgoaiThat=[]
        NoiThat=[]
        NhienLieu=[]
        HopSo=[]
        DanDong=[]

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute(sql_statement['HangXe'])
        HangXeData= cursor.fetchall()
        for data in HangXeData:
            HangXe.append(data['HangXe'])
        
        cursor.execute(sql_statement['XuatXu'])
        XuatXuData= cursor.fetchall()
        for data in XuatXuData:
            XuatXu.append(data['XuatXu'])

        cursor.execute(sql_statement['KieuDang'])
        KieuDangData= cursor.fetchall()
        for data in KieuDangData:
            KieuDang.append(data['KieuDang'])

        cursor.execute(sql_statement['NgoaiThat'])
        NgoaiThatData= cursor.fetchall()
        for data in NgoaiThatData:
            NgoaiThat.append(data['NgoaiThat'])

        cursor.execute(sql_statement['NoiThat'])
        NoiThatData= cursor.fetchall()
        for data in NoiThatData:
            NoiThat.append(data['NoiThat'])

        cursor.execute(sql_statement['NhienLieu'])
        NhienLieuData= cursor.fetchall()
        for data in NhienLieuData:
            NhienLieu.append(data['NhienLieu'])

        cursor.execute(sql_statement['HopSo'])
        HopSoData= cursor.fetchall()
        for data in HopSoData:
            HopSo.append(data['HopSo'])

        cursor.execute(sql_statement['DanDong'])
        DanDongData= cursor.fetchall()
        for data in DanDongData:
            DanDong.append(data['DanDong'])

        res =[
            {
                "label": "Hãng xe",
                "data": HangXe,
                "key": "HangXe"
            },
            {
                "label": "Xuất xứ",
                "data": XuatXu,
                "key":"XuatXu"
            },
            {
                "label": "Kiểu dáng",
                "data": KieuDang,
                "key": "KieuDang"
            },
            {
                "label": "Ngoại thất",
                "data": NgoaiThat,
                "key": "NgoaiThat"
            },
            {
                "label": "Nội thất",
                "data": NoiThat,
                "key": "NoiThat"
            },
            {
                "label": "Nhiên liệu",
                "data": NhienLieu,
                "key":"NhienLieu"
            },
            {
                "label": "Hộp số",
                "data": HopSo,
                "key":"HopSo"
            },
            {
                "label": "Dẫn động",
                "data": DanDong,
                "key": "DanDong"
            }
        ]
        response=jsonify(res)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

#lấy các dòng xe dựa vào hãng
@app.route("/api/get-model-by-brand",methods=["POST"])
def get_model_by_brand():
    try:
        body=request.json
        HangXe=body['HangXe']

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute('SELECT DISTINCT DongXe from carinfo WHERE HangXe=%s',(HangXe))
        DongXeData= cursor.fetchall()
        DongXe=[]
        for data in DongXeData:
            DongXe.append(data['DongXe'])

        response=jsonify({"DongXe":DongXe})
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 


#update model dự đoán
@app.route("/api/update-model", methods=["GET"])
@token_required
def update_model():
    try:
        model.initModel()
        response = jsonify({"message": "OK"})
        response.status_code = 200
        return response
    except Exception as e:
        return showMessage(e)



# Đưa ra giá trị dự đoán
@app.route("/api/predict", methods=["POST"])
def predict_price():
    
    body = request.json
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
    
    if HangXe and DongXe and NamSX and XuatXu and KieuDang and SoKm and NgoaiThat and NoiThat and NhienLieu and DongCo and HopSo and DanDong :
        input =[HangXe, DongXe, NamSX, XuatXu, KieuDang, SoKm, NgoaiThat, NoiThat, NhienLieu, DongCo, HopSo, DanDong]
        # data=getDataFrame()
        res = model.predictPrice(input)

        response = jsonify({"price": res})
        response.status_code = 200
        return response
    else:
        return showMessage()
    



#đăng nhập
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
        }, app.config['SECRET_KEY']
        ,algorithm="HS256")
    return make_response(jsonify({'token' : token}), 201)

#check-manage
@app.route('/manage', methods =['GET'])
@token_required
def checked():
    return make_response(jsonify({'message' : "OK"}),200)


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)