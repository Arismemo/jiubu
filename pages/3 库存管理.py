from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import pymysql
from st_aggrid import AgGrid,ColumnsAutoSizeMode

# engine = create_engine(
#     "mysql+pymysql://jiubu:Trainlk100@localhost:3306/database_jiubu",
#     # encoding= "utf-8",
#     echo=True
# )    

# sql = 'select * from 商品信息表;'
# df = pd.read_sql(sql, engine)

st.set_page_config(layout='wide')
connection = pymysql.connect(
    host='localhost',
    user='jiubu',
    password='Trainlk100',
    db='database_jiubu',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

sql = 'SELECT * FROM 商品信息表'
df = pd.read_sql(sql=sql, con=connection, index_col='id', columns=['id'])

connection.close()
with st.container():
    AgGrid(
        df,
        # fit_columns_on_grid_load=True,
        editable=True,
        # height=500,
        theme='streamlit',
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        enable_enterprise_modules=True
        )
# st.dataframe(df)


if st.button('提交修改'):
    df.to_sql(name='商品信息表', con=connection,if_exists='replace')