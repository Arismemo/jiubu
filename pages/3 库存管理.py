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


from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder


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

df.rename(columns = {'description' : '描述',
                     'goods_position' : '货架位置',
                     'model_position' : '模具位置',
                     'color_list' : '颜色序列',
                     'classify' : '分类',
                     'count' : '库存数量',
                     'create_time' : '创建时间',
                     'last_update_time' : '最后修改时间',
                     }, inplace = True)


with st.container():
    st.experimental_data_editor(df,
                                num_rows='dynamic',
                                key="data_editor",
                                # hide_index=True,
                                use_container_width=True)

connection.close()
if st.button('提交修改'):
   df.to_sql(name='商品信息表', con=connection,if_exists='replace')