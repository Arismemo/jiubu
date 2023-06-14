import base64
import streamlit as st
from PIL import Image
import re
import os
import time
import sys
import io
from PIL import Image, ImageDraw
from utils.shitu_wrapper import *
from streamlit_modal import Modal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.table_commodity import ProductInfo, search_product

sys.path.append('..')
sys.path.append('../utils')
sys.path.append('../pages')

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
Base = orm.declarative_base()


placeholder =  st.empty()

def compare_images(new_image, existed_image):
    confirm_modal = Modal(title="图片比较", key="confirm_images", max_width=300)
    with confirm_modal.container():
        with st.container():
            col1, col2 = st.columns(2)
            col1.image(new_image)
            col2.image(existed_image)


def try_add_record(tag, upload_file):
    search_result = search_image(upload_file)
    if search_result['find_result']:
        exist_photo_path = search_result['photo_path']
        exist_image = Image.open(exist_photo_path)
        compare_images(upload_file, exist_image)
    else:
        add_record(tag, upload_file)


def show_product_info(info: dict):
    with st.container():
        st.title('查找结果')
        lib_pic_path = info['photo_path']
        product_code = info['rec_docs']

        product = search_product(product_code)
        if len(product) == 1:
            product[0].show_product_info()
            st.image(lib_pic_path, width=100)
        else:
            st.error("库中存在两个相同产品编号的产品，请联系管理员")



def comfirm_add_product(uploaded_file):
    st.info('未找到商品，请前往【新建商品】页面进行新建')
    st.image(uploaded_file, width=100)

def search_product_by_code():
    with st.form('通过产品ID查找'):
        product_code = st.text_input('产品编号', '')
        submitted = st.form_submit_button("开始查找")
    if submitted:
        obj_list = search_product(product_code)
        if len(obj_list) == 1:
            obj_list[0].show_product_info()
            st.success('查找成功')
        elif len(obj_list) == 0:
            st.warning('未查到编号对应的产品')
        else:
            st.error("产品库中存在编号相同的产品，请联系管理员")

def save_image(uploaded_file):
    # file_contents = uploaded_file.read()
    # image = Image.open(io.BytesIO(file_contents))
    image = Image.open(uploaded_file)
    # photo_path = os.path.join(upload_photo_path, time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time())) + '.jpg')
    photo_path = os.path.join(upload_photo_path, uploaded_file.name)
    image.save(photo_path)
    return photo_path

def search_product_by_image():
    with st.form("通过图片查找"):
        uploaded_file = st.file_uploader(
            label="上传图片",
            type=["jpg", "png", "jpeg"])
        submitted = st.form_submit_button("开始查找")
    
    if submitted:
        if uploaded_file:
            with st.spinner('图像分析中'):
                upload_photo_path = save_image(uploaded_file)
                info = search_image(upload_photo_path)
            if info['find_result'] == True:
                confirm_modal = Modal(title="", key="confirm_modal", max_width=400)
                with confirm_modal.container():
                    st.info("确定是这个商品吗")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(uploaded_file, caption='上传图片', width=100)
                    with col2:
                        lib_image = Image.open(info['photo_path'])
                        st.image(lib_image, caption="库中图片", width=100)

                        col1, col2 = st.columns(2)
                        with col1:
                                st.button('是', key="confirm", on_click=show_product_info, args=(info,))
                        with col2:
                                st.button('不是', key="not_confirm", on_click=comfirm_add_product, args=(uploaded_file,))
            else:
                st.info('未找到商品，请前往【新建商品】页面进行新建')
                st.image(uploaded_file, width=100)
        else:
            st.warning("请先上传图片")
            st.stop()
           

if __name__ == "__main__":
    # 设置页面属性
    # st.set_page_config(page_title="九步", page_icon="🍀", layout="centered", menu_items={"about":"none"})

    # 初始化数据库
    engine = create_engine(
        "mysql+pymysql://jiubu:Trainlk100@localhost:3306/database_jiubu",
        # encoding= "utf-8",
        echo=True
    )
    Base.metadata.create_all(engine)
    print('Create table successfully!')

    tab_search_product_by_code, tab_search_product_by_image = st.tabs(["通过编号查找", "通过图片查找"])
    with tab_search_product_by_code:
        search_product_by_code()

    with tab_search_product_by_image:
        search_product_by_image()

        



