import base64
import streamlit as st
from PIL import Image
import sys 
sys.path.append('..')
sys.path.append('../utils')

from shitu.shitu import ShiTu
from streamlit_modal import Modal
import pandas as pd

from utils.product_code_generator import *
from utils.table_commodity import ProductInfo, add_product
from utils.shitu_wrapper import *


def submit_goods_confirm():
    st.session_state['submit_goods_confirm'] = True

def comfirm_add_product(product: ProductInfo, upload_file):
    st.spinner("添加中")
    # 添加图片到库中
    add_record(product.id, upload_file)
    # 添加商品到库中
    add_product(product)

def page_add_new_product(external_upload_file=None):
    confirm_modal = Modal(title="确认提交", key="confirm_modal", max_width=300)
    if "submit_goods_confirm" not in st.session_state:
        st.session_state['submit_goods_confirm'] = False

    with st.form("新增商品"):
        goods_position = "None"
        model_position = "None"
        color_list = "None"
        classify = "未分类"
        count = "0"

        col1, col2 = st.columns(2)
        if external_upload_file is None:
            upload_file = st.file_uploader("图片", type=["jpg", "png", "jpeg"])
        else:
            upload_file = external_upload_file
            st.image(external_upload_file, width=50)

        with col1:
            description = st.text_input("描述")
            goods_position = st.text_input('货架位置')
            model_position = st.text_input('模具位置')

        with col2:
            color_list = st.text_input('颜色序列')
            classify = "未分类"
            classify = st.selectbox('分类', ('混批', '系列', '未分类'))
            count = st.number_input('库存数量', step=10)


        # Every form must have a submit button.
        submitted = st.form_submit_button("提交")
    id = get_product_code()
    product = ProductInfo(id,
                          description,
                          goods_position,
                          model_position,
                          color_list,
                          classify)

    if submitted:
        if upload_file is None:
            st.error("请上传商品图片")
            st.stop()
        else:
            with confirm_modal.container():
                with st.container():
                    product.show_product_info()
                    st.image(upload_file, width=100)
                    st.button("确定", key="confirm", on_click=submit_goods_confirm)
                    
            
    # 这里通过session_state判断弹窗里的确定按钮被点击了，就进行你想要的逻辑操作。
    if st.session_state["submit_goods_confirm"]:
        # 判断商品是否已在库中
        st.spinner("判断图片是否存在库中")
        info = search_image(upload_file)
        if info['find_result'] == True: # 图片已在库中
            with confirm_modal.container():
                st.info("从库中中找到一张类似图片，仍要添加新的商品吗?")
                col1, col2 = st.columns(2)
                with col1:
                    st.image(upload_file, caption='上传图片')
                with col2:
                    lib_image = Image.open(info['image_path'])
                    st.image(lib_image, caption="库中图片")

                if st.button('仍要添加'):
                    comfirm_add_product(upload_file, upload_file)
        else:
            comfirm_add_product(upload_file, upload_file)
            # delete_cases(t[0])    # 删除用例
        st.session_state["submit_goods_confirm"] = False    # 恢复session_state为False
        st.info("加入商品成功")
        st.experimental_rerun()  # 重刷页面


if __name__ == "__main__":
    page_add_new_product()
        
            
