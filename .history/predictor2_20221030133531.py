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
    

def predictPrice(data, input):
    le = LabelEncoder()
    mn = MinMaxScaler()
    text_cols=['HangXe','DongXe','XuatXu','KieuDang','NgoaiThat','NoiThat','NhienLieu','HopSo','DanDong']
    num_cols=['NamSX','SoKm','DongCo']
    X=data['X']
    y=data['y']
    x_test= pd.DataFrame([input], columns=['HangXe','DongXe','NamSX','XuatXu','KieuDang','SoKm','NgoaiThat','NoiThat','NhienLieu','DongCo','HopSo','DanDong'])
    for col in text_cols:
        le.fit(X[col])
        X[col] = le.transform(X[col])
        x_test[col] = le.transform(x_test[col])
    
    # X[num_cols]= mn.fit_transform(X[num_cols])
    # x_test[num_cols]=mn.transform(x_test[num_cols])

    X= pd.DataFrame(mn.fit_transform(X))
    x_test=pd.DataFrame(mn.transform(x_test))

    model=RandomForestRegressor()
    model.fit(X,y)
    res=model.predict(x_test)
    return res[0]


# data=getDataFrame()
# res=predictPrice(data,['Nissan','Navara',2020,'Nhập khẩu','Bán tải / Pickup',41000,'Trắng','Kem','Dầu',2.5,'Số tự động','4WD - Dẫn động 4 bánh'])
# print(res)
