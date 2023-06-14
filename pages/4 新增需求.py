import streamlit as st
from utils.shitu_wrapper import *
from streamlit_modal import Modal

def get_product_code(uploaded_file):

    if 'requirement_pruduct_code' not in st.session_state:
        if uploaded_file is not None:
            with st.spinner('图像分析中'):
                info = search_image(uploaded_file)
            if info['find_result'] == True:
                st.session_state['pass_file'] = False
                confirm_modal = Modal(title="", key="confirm_modala", max_width=400)
                with confirm_modal.container():
                    st.info("确定是这个商品吗")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(uploaded_file, caption='上传图片', width=100)
                    with col2:
                        lib_image = Image.open(info['photo_path'])
                        st.image(lib_image, caption="库中图片", width=100)

                    if st.button('是', key="confirm1"):
                        st.session_state['requirement_pruduct_code'] = info['rec_docs']
                    else:
                            st.session_state['requirement_pruduct_code'] = ""

if __name__ == "__main__":
    uploaded_file = st.file_uploader('拍照获取产品编号')
    if uploaded_file is not None:
        get_product_code(uploaded_file)
    with st.form('提交需求'):
        col1, col2 = st.columns(2)
        with col1:
            product_code = st.text_input('*产品编号', key='requirement_pruduct_code')
            price = st.text_input('产品单价')
        with col2:
            require_count = st.number_input('*需求数量', min_value=0)
            
        submitted = st.form_submit_button("提交")

        if submitted:
            if product_code == '':
                st.error("请输入产品编号")
                st.stop()
            
            if require_count == 0:
                st.error("请输入需求数量")
                st.stop()

            "todo: 插入数据库"
            st.success("提交成功")