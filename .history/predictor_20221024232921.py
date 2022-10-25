from sqlalchemy import create_engine
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor

db_connection_str = 'mysql+pymysql://root:Minh!2000@localhost/car'
db_connection = create_engine(db_connection_str)

def initModel():
    df = pd.read_sql('SELECT * FROM carinfo', con=db_connection)
    df=df.drop("ID", axis=1)
    df=df.drop("HinhAnh", axis=1)
    
    X = df.iloc[:,:12]
    y = df.iloc[:,-1]
    print(X)
    print(y)

    le = LabelEncoder()
    hangXeEncoder=X['HangXe']=le.fit_transform(X['HangXe'])
    X['DongXe']=le.fit_transform(X['DongXe'])
    X['XuatXu']=le.fit_transform(X['XuatXu'])
    X['KieuDang']=le.fit_transform(X['KieuDang'])
    X['NgoaiThat']=le.fit_transform(X['NgoaiThat'])
    X['NoiThat']=le.fit_transform(X['NoiThat'])
    X['NhienLieu']=le.fit_transform(X['NhienLieu'])
    X['HopSo']=le.fit_transform(X['HopSo'])
    X['DanDong']=le.fit_transform(X['DanDong'])

    mm = MinMaxScaler()
    x_encoded = pd.DataFrame(mm.fit_transform(X))
    print(x_encoded)

initModel()