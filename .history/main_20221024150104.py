import pymysql
from app import app
from config import mysql
from flask import jsonify, request, make_response
from math import ceil

@app.route("/api/cars", methods=["GET"])
def get_cars():
    page=int(request.args.get("page"))
    search=request.args.get("search").split('+')
    
    print(search)
    search="q"
    limit = str((page-1)*20)
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = f"SELECT * FROM carinfo LIMIT 20 OFFSET {limit}"
        sqlQuery2 = f"SELECT COUNT(ID) as totalPages FROM carinfo"

        if search:
            sqlQuery = f"SELECT * FROM car.carinfo\
                    WHERE CONCAT(carinfo.HangXe,' ', carinfo.DongXe,' ',carinfo.NamSX)\
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




if __name__ == "__main__":
    app.run(debug=True)