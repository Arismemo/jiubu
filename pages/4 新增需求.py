import streamlit as st
from utils.shitu_wrapper import *
from streamlit_modal import Modal


if __name__ == "__main__":
    with st.form('提交需求'):
        uploaded_file = st.file_uploader('拍照获取产品编号')

        if uploaded_file is None:
            col1, col2 = st.columns(2)
            with col1:
                product_code = st.text_input('*产品编号')
                price = st.text_input('产品单价')
            with col2:
                require_count = st.number_input('*需求数量', min_value=0)
            submitted = st.form_submit_button("提交")
        else:
            product_code = ''
            with st.spinner('图像分析中'):
                info = search_image(uploaded_file)

            if info['find_result'] == True:
                confirm_modal = Modal(title="", key="confirm_modal", max_width=400)
                with confirm_modal.container():
                    st.info("确定是这个商品吗")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(uploaded_file, caption='上传图片', width=100)
                    with col2:
                        lib_image = Image.open(info['image_path'])
                        st.image(lib_image, caption="库中图片", width=100)

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button('是', key="confirm"):
                                    product_code = info['ret_docs']
                        with col2:
                            if st.button('不是', key="not_confirm"):
                                    product_code = ''
            else:
                confirm_modal = Modal(title="", key="confirm_modal_not_found", max_width=300)
                with confirm_modal.container():
                    st.warning('未找到商品')

            col1, col2 = st.columns(2)
            
            with col1:
                product_code = st.text_input('*产品编号', value=product_code)
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