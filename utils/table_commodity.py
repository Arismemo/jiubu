# -*- coding: utf-8 -*-
# author: Jclian91
# place: Sanya, Hainan
# time: 12:52

import datetime
import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Enum,
    DECIMAL,
    DateTime,
    Boolean,
    UniqueConstraint,
    Index
)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class ProductInfo(Base):
    __tablename__ = '商品信息表'

    id = Column(String(256), primary_key=True, comment="商品ID")
    description = Column(String(256), primary_key=True, comment="描述")
    goods_position = Column(String(256), nullable=False, comment="货架位置")
    model_position = Column(String(256), comment="模具位置")
    color_list = Column(String(256), nullable=False, comment="颜色序列")
    classify = Column(String(256), nullable=False, comment="分类")
    count =  Column(Integer, nullable=False, comment="库存")

    create_time = Column(
        DateTime, default=datetime.datetime.now, comment="创建时间")

    last_update_time = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment="最后更新时间")

    def __init__(self, id, description, goods_position, model_position, color_list, classify, ):
        self.id = id
        self.description = description
        self.goods_position = goods_position
        self.model_position = model_position
        self.color_list = color_list
        self.classify = classify
        self.count = 0


    def __str__(self):
        return f"object : <id:{self.id} name:{self.description}>"
    
    def show_product_info(self):
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.write('产品编号: {}'.format(self.id))
        with col2:
            st.write('货架位置: {}'.format(self.goods_position))

        with st.expander('详细信息'):
            st.write('模具位置: {}'.format(self.model_position))
            st.write('库存数量: {}'.format(self.count))
            st.write('颜色序列: {}'.format(self.color_list))
            st.write('分类: {}'.format(self.classify))
        # st.markdown('''
        #             | 产品编号| 货架位置 | 模具位置 |库存数量 | 颜色序列 |分类|
        #             | --- | ----------- |---|--- | ----------- |---|
        #             | {} | {} | {} | {} | {} | {} |
        #             '''.format(self.id, self.goods_position, self.model_position, self.count, self.color_list, self.classify))
        st.markdown("---")

def add_product(product: ProductInfo):
    # 初始化数据库连接
    engine = create_engine(
        "mysql+pymysql://jiubu:Trainlk100@localhost:3306/database_jiubu",
        # encoding= "utf-8",
        echo=True
    )    
    # 创建DBSession类型
    DBSession = sessionmaker(bind=engine)

    # 创建session对象
    session = DBSession()
    # 插入单条数据
    # 添加到session
    session.add(product)
    # 提交即保存到数据库
    session.commit()
    # 关闭session
    session.close()
    print('insert into db successfully!')

def search_product(product_code):
    # 初始化数据库连接
    engine = create_engine(
        "mysql+pymysql://jiubu:Trainlk100@localhost:3306/database_jiubu",
        # encoding= "utf-8",
        echo=True
    )    # 创建DBSession类型
    # 创建DBSession类型 
    DBSession = sessionmaker(bind=engine)
    # 创建session对象
    session = DBSession()

    query_obj_list = session.query(ProductInfo).filter(ProductInfo.id==product_code).all()
    return query_obj_list




# class DatabaseConnection():
#     def __init__()
        
# def get_connection():
#     if st.session_state[]
# conn = DatabaseConnection()

# if __name__ == '__main__':
#     add_product()