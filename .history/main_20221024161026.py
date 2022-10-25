import pymysql
from app import app
from config import mysql
from flask import jsonify, request, make_response
from math import ceil

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