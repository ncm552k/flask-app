from sqlalchemy import create_engine
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor

db_connection_str = 'mysql+pymysql://root:Minh!2000@localhost/car'
db_connection = create_engine(db_connection_str)



def getDataFrame():
    df = pd.read_sql('SELECT * FROM carinfo', con=db_connection)
    df=df.drop("ID", axis=1)
    df=df.drop("HinhAnh", axis=1)
    
    X = df.iloc[:,:12]
    y = df.iloc[:,-1]
   
    return {"X":X,"y":y}



def initModel():
    data= getDataFrame()
    le = LabelEncoder()
    mn = MinMaxScaler()
    text_cols=['HangXe','DongXe','XuatXu','KieuDang','NgoaiThat','NoiThat','NhienLieu','HopSo','DanDong']
    X=data['X']
    y=data['y']
    x_test= pd.DataFrame([input], columns=['HangXe','DongXe','NamSX','XuatXu','KieuDang','SoKm','NgoaiThat','NoiThat','NhienLieu','DongCo','HopSo','DanDong'])
    for col in text_cols:
        le.fit(X[col])
        X[col] = le.transform(X[col])
        # x_test[col] = le.transform(x_test[col])

    X= pd.DataFrame(mn.fit_transform(X))
    # x_test=pd.DataFrame(mn.transform(x_test))

    predictor=RandomForestRegressor()
    predictor.fit(X,y)
    # res=model.predict(x_test)
    # return res[0]
    return {
        "le": le,
        "mn": mn,
        "predictor": predictor
    }


def predict(model,input):
    le=model['le']
    mn=model['mn']
    predictor=model['predictor']
    text_cols=['HangXe','DongXe','XuatXu','KieuDang','NgoaiThat','NoiThat','NhienLieu','HopSo','DanDong']
    x_test= pd.DataFrame([input], columns=['HangXe','DongXe','NamSX','XuatXu','KieuDang','SoKm','NgoaiThat','NoiThat','NhienLieu','DongCo','HopSo','DanDong'])
    for col in text_cols:
        x_test[col] = le.transform(x_test[col])

    x_test=pd.DataFrame(mn.transform(x_test))
    res = predictor.predict(x_test)
    return res[0]


model= initModel()
res=predict(model,['Nissan','Navara',2020,'Nhập khẩu','Bán tải / Pickup',41000,'Trắng','Kem','Dầu',2.5,'Số tự động','4WD - Dẫn động 4 bánh'])
print(res)
