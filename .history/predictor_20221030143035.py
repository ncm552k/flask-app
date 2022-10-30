from sqlalchemy import create_engine
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor

db_connection_str = 'mysql+pymysql://root:Minh!2000@localhost/car'
db_connection = create_engine(db_connection_str)



class Predictor:
    def __init__(self):
        self.text_cols = ['HangXe','DongXe','XuatXu','KieuDang','NgoaiThat','NoiThat','NhienLieu','HopSo','DanDong']
        self.num_cols = ['NamSX','SoKm','DongCo']
        self.label_encoder = {}
        self.minmax_scaler = None


    def initModel(self):
        #get dataframe from database
        df = pd.read_sql('SELECT * FROM carinfo', con=db_connection)
        df=df.drop("ID", axis=1)
        df=df.drop("HinhAnh", axis=1)  
        X = df.iloc[:,:12]
        y = df.iloc[:,-1]

        for col in self.text_cols:
            le = LabelEncoder()
            # le.fit(X[col])
            X[col] = le.fit_transform(X[col])
            self.label_encoder[col] = le

        mn = MinMaxScaler()
        X= pd.DataFrame(mn.fit_transform(X))
        self.minmax_scaler = mn 

        print(X)
        print(y)
        _model=RandomForestRegressor()
        _model.fit(X,y)
        self.model = _model


    def predictPrice(self,input):
        x_test= pd.DataFrame([input], columns=['HangXe','DongXe','NamSX','XuatXu','KieuDang','SoKm','NgoaiThat','NoiThat','NhienLieu','DongCo','HopSo','DanDong'])
        for col in self.text_cols:
            x_test[col] = self.label_encoder[col].transform(x_test[col])
        x_test=pd.DataFrame(self.minmax_scaler.transform(x_test))
        # print(x_test)
        res=self.model.predict(x_test)
        return res[0]
    



# model = Predictor()
# model.initModel()
# res = model.predictPrice(['Nissan','Navara',2020,'Nhập khẩu','Bán tải / Pickup',41000,'Trắng','Kem','Dầu',2.5,'Số tự động','4WD - Dẫn động 4 bánh'])
# print(res)
