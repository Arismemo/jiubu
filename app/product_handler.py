from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum, Float
from sqlalchemy.orm import sessionmaker, declarative_base, validates
import pandas as pd
from app.models import MyBase

import sys
sys.path.append('../utils')
from utils.shitu_wrapper import *

class ProductHandler(MyBase):
    def __init__(self) -> None:
        super().__init__('mysql+pymysql://jiubu:Trainlk100@localhost:3306/database_jiubu')

    # 创建商品记录的函数
    def create_product(self,
                       id:str,
                       name:str,
                       goods_position:str,
                       description:str,
                       model_position:str=None,
                       color_list:str=None,
                       classify:str=None,
                       count:str=None,
                       photo_path:str=None) -> None:
        with self.Session() as session:
            # 检查主键是否存在
            product = session.query(self.product).filter_by(id=id).first()
            if product is not None:
                print('product id existed')
                return False # 如果存在就跳过
            try:
                product = self.product(id=id,
                                        name=name,
                                        description=description,
                                        goods_position=goods_position,
                                        model_position=model_position,
                                        color_list=color_list,
                                        classify=classify,
                                        count=count,
                                        photo_path=photo_path,
                                       )
                session.add(product)
                session.commit()
            except Exception as e:
                print(str(e))
                print('database error')
                return False
            
            if not add_record(id, photo_path):
                return False
            return True

    # 根据商品 ID 查找商品记录的函数
    def get_product_by_id(self, id:str):
        with self.Session() as session:
            p = session.query(self.product).filter_by(id=id).first()
            session.commit()
            df = pd.DataFrame([(p.id, p.description, p.goods_position, p.model_position, p.color_list, p.classify)],
                            columns=['ID', '描述', '货架位置', '模具位置', '颜色序列', '分类',])
            return df

    # 更新商品记录的函数
    def update_product(self, id, name=None, color=None, size=None, photo_path=None):
        with self.Session() as session:
            product = session.query(self.product).filter_by(id=id).first()
            if name:
                product.name = name
            if color:
                product.color = color
            if size:
                product.size = size
            if photo_path:
                product.photo_path = photo_path
            session.commit()
            return product

    # 删除商品记录的函数
    def delete_product(self, id):
        with self.Session() as session:
            product = session.query(self.product).filter_by(id=id).first()
            session.delete(product)
            session.commit()
            return product

    def get_product_data(self):
        with self.Session() as session:
            results = session.query(self.product).all()
        df = pd.DataFrame([(p.id, os.path.basename(p.photo_path), p.classify,  p.goods_position, p.name, p.description,  p.model_position, p.color_list,  p.count, p.create_time, ) for p in results],
                        columns=['ID', '图片', '分类', '库存位置', '名称', '描述',  '模具位置', '颜色序列',  '库存', '创建时间'])
        return df

    # 创建商品记录的函数
    def create_product_detail(self, id, quantity, price, type, supplier, note=None, detail_ts:pd.Timestamp=None):
        with self.Session() as session:
            if detail_ts is None:
                t = pd.Timestamp.now()
            else:
                t = detail_ts
            # t -= pd.Timedelta(pd.Series(range(3000)).sample(1).values[0], 'day')
            # t += pd.Timedelta(pd.Series(range(3000)).sample(1).values[0], 'day')
            detail = self.detail(detail_ts=t , id=id, quantity=quantity, price=price, type=type, supplier=supplier, note=note)
            session.add(detail)
            session.commit()
            return detail

    # 根据商品 ID 查找商品记录的函数
    def get_product_detail_by_id(self, id):
        with self.Session() as session:
            results = session.query(self.detail).filter_by(id=id).all()
        df = pd.DataFrame([(d.id, d.detail_ts, d.quantity, d.price, d.type, d.supplier, d.note) for d in results], 
                        columns=['id', 'detail_ts', 'quantity', 'price', 'type', 'supplier', 'note'])
        return df

    def get_detail_data(self):
        with self.Session() as session:
            results = session.query(self.detail).all()
        df = pd.DataFrame([(d.id, d.detail_ts, d.quantity, d.price, d.type, d.supplier, d.note) for d in results], 
                        columns=['id', 'detail_ts', 'quantity', 'price', 'type', 'supplier', 'note'])
        return df.sort_values('detail_ts', ascending=False)

    # 删除商品记录的函数
    def delete_detail(self, ts):
        with self.Session() as session:
            detail = session.query(self.detail).filter_by(detail_ts=ts).delete()
            # session.delete(detail)
            session.commit()
            return detail

    def gen_random_data(self):
        ph = self
        for g in ['男', '女', '中性']:
            for pt in ['長褲', '瑜珈褲', '壓力褲','短褲','上衣','排汗衣']:
                ph.create_product(g+pt)

        type = ['IN', 'OUT']
        supplier = ['柏國', '蝦皮']
        days = pd.Series(range(1, 700, 3))
        for _ in range(50):
            for i in ph.get_product_data().id.sample(10).values:
                for t in type:
                    for s in supplier:
                        m = 5 if t == 'IN' else 6
                        ph.create_product＿detail(i, 
                                                 pd.Series([50,100,150]).sample(1).values[0] * m, 
                                                 pd.Series([100,500,1500]).sample(1).values[0], 
                                                 t, 
                                                 s,
                                                 detail_ts=pd.Timestamp.now() - pd.Timedelta(days.sample(1).values[0]*m, 'day')
                                                 )
