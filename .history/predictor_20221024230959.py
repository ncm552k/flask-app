from sqlalchemy import create_engine
import pandas as pd

db_connection_str = 'mysql+pymysql://root:Minh!2000@localhost/car'
db_connection = create_engine(db_connection_str)

def initModel():
    df = pd.read_sql('SELECT * FROM carinfo', con=db_connection)
    df=df.drop("ID", axis=1)
    df=df.drop("HinhAnh", axis=1)
    print(df)

initModel()