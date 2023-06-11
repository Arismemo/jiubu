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
from utils.table_commodity import ProductInfo, add_product, search_product
from utils.shitu_wrapper import *


def get_cache_data():
    try:
        return pd.read_pickle('data/cache.pkl')
    except:
        df = pd.DataFrame(
            dict(
                name=[],
                color=[],
                size=[],
                id=[]
            )
        )
        df.to_pickle('data/cache.pkl')
        return df

def add_cache_data(data:pd.DataFrame):
    df = get_cache_data()
    if data['id'].tolist()[0] not in df['id'].tolist():
        pd.concat([df, data]).to_pickle('data/cache.pkl')

def reset_cache_data():
    pd.DataFrame(
        dict(
            name=[],
            color=[],
            size=[],
            id=[]
        )
    ).to_pickle('data/cache.pkl')


def submit_goods_confirm():
    st.session_state['submit_goods_confirm'] = True

def comfirm_add_product(product: ProductInfo, upload_file):
    st.spinner("添加中")
    # 添加商品到库中
    try:
        add_product(product)
    except:
        product
        st.stop()
    # 添加图片到库中
    add_record(product.id, upload_file)


def page_add_new_product():
    with st.form("新增商品"):
        id = get_product_code()
        st.write('商品ID\t{}'.format(id))
        st.markdown('---')
        
        upload_file = st.file_uploader("图片", type=["jpg", "png", "jpeg"])
        goods_position = st.text_input('货架位置')

        col1, col2 = st.columns(2)
        with col1:
            if st.button('加入清单'):
                add_cache_data(pd.DataFrame([df]))
        with col2:
            if st.button(f'清空清單', use_container_width=True):
                reset_cache_data()

        with st.expander('详细选项'):
            col1, col2 = st.columns(2)
            with col1:
                description = st.text_input("描述")
                color_list = st.text_input('颜色序列')
                classify = "未分类"
                classify = st.selectbox('分类', ('混批', '系列', '未分类'))
                
            with col2:
                model_position = st.text_input('模具位置')
                count = st.number_input('库存数量', step=10)

        submitted = st.form_submit_button("提交")
    

    if submitted:
        if upload_file is None:
            st.error("请上传商品图片")
            st.stop()
        if goods_position == "":
            st.error("请指定商品货位")
            st.stop()
        
        with st.spinner("判断图片是否存在库中"):
            info = search_image(upload_file)

        with st.container():
            if info['find_result'] == True: # 图片已在库中
                product_list = search_product(info['rec_docs'])
                if not len(product_list) == 1:
                    product_list
                    st.error('产品库有问题，请联系管理员') 
                    st.stop()
                st.info("从库中中找到一张类似图片，仍要添加新的商品吗?")
                col1, col2 = st.columns(2)
                with col1:
                    st.image(upload_file, caption='上传图片')
                with col2:
                    lib_image = Image.open(info['image_path'])
                    st.image(lib_image, caption="库中图片")
                    product_list[0].show_product_info()
                st.button("仍要添加", key="double_confirm", on_click=submit_goods_confirm)
                
            else:
                comfirm_add_product(product, upload_file)
                product.show_product_info()
                st.image(upload_file, width=100)
                st.button("确认提交", key="confirm", on_click=submit_goods_confirm)
            
                    
            
    # 这里通过session_state判断弹窗里的确定按钮被点击了，就进行你想要的逻辑操作。
    if st.session_state["submit_goods_confirm"]:
        comfirm_add_product(product, upload_file)
        st.session_state["submit_goods_confirm"] = False    # 恢复session_state为False
        with confirm_modal.container():
            st.success("加入商品成功")
        st.experimental_rerun()  # 重刷页面


if __name__ == "__main__":
    page_add_new_product()
        
            
