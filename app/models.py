from sqlalchemy.orm import sessionmaker, declarative_base, validates
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum, Float
import datetime
from sqlalchemy.sql.schema import Table


class MyBase:
    engine = None
    Session = None
    Base = None

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.Base = declarative_base()
        metadata = self.Base.metadata

        # 定义商品模型类
        class Product(self.Base):
            __tablename__ = '商品信息表'
            id = Column(String(256), primary_key=True, comment="商品ID")
            name = Column(String(256), primary_key=True, comment="名称")
            description = Column(String(256), primary_key=True, comment="描述")
            goods_position = Column(String(256), nullable=False, comment="货架位置")
            model_position = Column(String(256), comment="模具位置")
            color_list = Column(String(256), nullable=False, comment="颜色序列")
            classify = Column(String(256), nullable=False, comment="分类")
            count =  Column(Integer, nullable=False, comment="库存")
            photo_path = Column(Integer, nullable=False, comment="图片路径")

            create_time = Column(
                DateTime, default=datetime.datetime.now, comment="创建时间")

            last_update_time = Column(
                DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment="最后更新时间")

            # @validates('color')
            # def validate_color(self, key, color):
            #     allowed_colors = ["紅", "綠", "藍", "黃", "黑", "灰"]
            #     if color not in allowed_colors:
            #         raise ValueError(f"invalid color, allowed values are {allowed_colors}")
            #     return color

            # @validates('size')
            # def validate_size(self, key, size):
            #     allowed_sizes = ["S", "M", "L", "2L", "XL", "XXL"]
            #     if size not in allowed_sizes:
            #         raise ValueError(f"invalid size, allowed values are {allowed_sizes}")
            #     return size


        self.product = Product
        self.create_db()

    def create_db(self):
        self.Base.metadata.create_all(self.engine)

    def reset_db(self):
        self.Base.metadata.drop_all(self.engine)
        self.create_db()