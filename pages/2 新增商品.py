import base64
import streamlit as st
from PIL import Image

import sys 
sys.path.append('..')
sys.path.append('../utils')
sys.path.append('../app')

from shitu.shitu import ShiTu
from streamlit_modal import Modal
import pandas as pd
from utils.product_code_generator import *
from utils.table_commodity import ProductInfo, add_product, search_product
from utils.shitu_wrapper import *
from app.product_handler import ProductHandler


@st.cache_resource
def ph():
    ph = ProductHandler()
    return ph

def continue_add(record):
    if record is None or not ph().create_product(**record):
        st.error('添加商品到数据库失败')
        st.stop()
    else:
        st.success(f'新建商品成功！')

def cancle_add():
    st.info('请重新上传商品')  # 重刷页面

def save_image(uploaded_file):
    image = Image.open(uploaded_file)
    photo_path = os.path.join(upload_photo_path, uploaded_file.name)
    image.save(photo_path)
    return photo_path

def page_add_new_product():

    info = None
    record  = None

    with st.form('提交数据'):

        upload_file = st.file_uploader("图片", type=["jpg", "png", "jpeg"])
        goods_position = st.text_input('货架位置')
        id = get_product_code()
        with st.expander('详细选项'):

            st.write('商品ID\t{}'.format(id))
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input('名称')
                description = st.text_input("描述")
                classify = "未分类"
                classify = st.selectbox('分类', ('未分类', '混批', '系列'))
                
            with col2:
                model_position = st.text_input('模具位置')
                count = st.number_input('库存数量', step=10)
                color_list = st.text_input('颜色序列')

        submit = st.form_submit_button(f'新增商品', use_container_width=True)

    if submit:
        if upload_file is None:
            st.error("请上传商品图片")
            st.stop()
        if goods_position == "":
            st.error("请指定商品货位")
            st.stop()

        photo_path = save_image(upload_file)
        info = None
        with st.spinner('比对数据库图片中.....'):
            info = search_image(photo_path)

        record = dict(
            id = id,
            name = name,
            goods_position = goods_position,
            description = description,
            model_position = model_position,
            color_list = color_list,
            classify = classify,
            count = count,
            photo_path = photo_path
        )
        
        if info is not None and info['find_result'] == True:
            confirm_modal = Modal(title="库中已有类似图片", key="confirm_images", max_width=300)
            with confirm_modal.container():
                col1, col2 = st.columns(2)
                with col1:
                    new_image = Image.open(photo_path)
                    col1.image(new_image, caption='上传图片', width=100)
                with col2:
                    lib_image = Image.open(info['photo_path'])
                    col2.image(lib_image, caption="库中图片", width=100)

                col1, col2 = st.columns(2)
                with col1:
                    st.button('继续添加', key="confirm", on_click=continue_add, args=(record, ))
                with col2:
                    st.button('取消添加', key="not_confirm", on_click=cancle_add)            
        else:
            continue_add(record)


if __name__ == "__main__":
    page_add_new_product()



# def get_cache_data():
#     try:
#         return pd.read_pickle('data/cache.pkl')
#     except:
#         df = pd.DataFrame(
#             dict(
#                 id = [],
#                 name = [],
#                 goods_position = [],
#                 description = [],
#                 model_position = [],
#                 color_list = [],
#                 classify = [],
#                 count = [],
#                 photo_path = []
#             )
#         )
#         df.to_pickle('data/cache.pkl')
#         return df

# def add_cache_data(data:pd.DataFrame):
#     df = get_cache_data()
#     if data['photo_path'].tolist()[0] not in df['photo_path'].tolist():
#         pd.concat([df, data]).to_pickle('data/cache.pkl')

# def reset_cache_data():
#     pd.DataFrame(
#         dict(
#             id = [],
#             name = [],
#             goods_position = [],
#             description = [],
#             model_position = [],
#             color_list = [],
#             classify = [],
#             count = [],
#             photo_path = []
#         )
#     ).to_pickle('data/cache.pkl')


# def comfirm_add_product(product: ProductInfo, upload_file):
#     st.spinner("添加中")
#     # 添加商品到库中
#     try:
#         add_product(product)
#     except:
#         product
#         st.stop()
#     # 添加图片到库中
#     add_record(product.id, upload_file)

# def comfirm_product(photo_path):
#     # 确认库中已有图片
#     st.spinner('比对图片中......')
#     search_result = search_image(photo_path)
#     search_result
#     if search_result['find_result']:
#         confirm_modal = Modal(title="图片比较", key="confirm_images", max_width=300)
#         with confirm_modal.container():
#             col1, col2 = st.columns(2)
#             with col1:
#                 new_image = Image.open(photo_path)
#                 col1.image(new_image)
#                 st.button('继续添加', key="confirm", on_click=continue_add)
#             with col2:
#                 lib_image = Image.open(search_result['photo_path'])
#                 col2.image(lib_image)
#                 st.button('取消添加', key="not_confirm", on_click=cancle_add)





# def page_show_data():
#     all_data = ph().get_product_data().sort_values('创建时间', ascending=False)
#     all_data.insert(0, '刪除', False)
#     col1, col2 = st.columns([1, 1])
#     st.subheader('所有商品')
#     edited_df = st.experimental_data_editor(all_data, use_container_width=True)
    # st.write('---')
    # st.subheader('刪除商品')
    # goods_tab, update_tab, delete_tab = st.tabs(['庫存', '更新', '刪除'])
    # update_tab, delete_tab = st.tabs(['更新', '刪除'])

    # # with goods_tab:
    # #     all_detail_data = ph().get_detail_data().sort_values('detail_ts', ascending=False)
    # #     all_detail_data = all_detail_data[all_detail_data.id.isin(edited_df[edited_df['刪除']].id.tolist())]
    # #     all_detail_data.insert(0, '刪除', False)
    # #     edited_detail = st.experimental_data_editor(all_detail_data, use_container_width=True)
    #     # st.dataframe(edited_detail[edited_detail['刪除']], use_container_width=True)

    # with delete_tab:
    #     st.dataframe(edited_df[edited_df['刪除']], use_container_width=True)
    #     id = edited_df[edited_df['刪除']]['id'].tolist()

    #     col1, col2, col3 = st.columns([1, 1, 4])
    #     with col1:
    #         if st.button(f'確定刪除'):
    #             for i in id:
    #                 ph().delete_product(id=i)
    #             with col2:
    #                 if st.button(f'重新整理'):
    #                     pass
    #             with col3:
    #                 st.success(f'刪除成功\n{id} ')



    # if info is not None and info['find_result'] == True:
    #     'check info'
    #     confirm_modal = Modal(title="", key="comfirm_product", max_width=400)
    #     with confirm_modal.container():
    #         st.info("确定是这个商品吗")
    #         col1, col2 = st.columns(2)
    #         with col1:
    #             upload_image = Image.open(photo_path)
    #             st.image(upload_image, caption='上传图片', width=100)
    #         with col2:
    #             lib_image = Image.open(info['photo_path'])
    #             st.image(lib_image, caption="库中图片", width=100)

    #         col1, col2 = st.columns(2)
    #         with col1:
    #                 st.button('是', key="confirm", on_click=continue_add)
    #         with col2:
    #                 st.button('不是', key="not_confirm", on_click=cancle_add)

    # import streamlit.components.v1 as components


    # modal = Modal("", '确认添加商品')
    # open_modal = st.button("Open")
    # if open_modal:
    #     modal.open()

    # if modal.is_open():
    #     with modal.container():
    #         st.write("库中已存在相似图片，确认添加新商品吗")

    #         # html_string = '''
    #         # <h1>HTML string in RED</h1>

    #         # <script language="javascript">
    #         # document.querySelector("h1").style.color = "red";
    #         # </script>
    #         # '''
    #         # components.html(html_string)

    #         # st.write("Some fancy text")
    #         value = st.checkbox("Check me")
    #         st.write(f"Checkbox checked: {value}")
    #         st.button()
            


    # if upload_file is not None:
    #     photo_path = save_image(upload_file)
    #     comfirm_product(photo_path)


    # if st.session_state["continue_add"] == False:
    #     upload_file = None
    #     st.session_state["continue_add"] = True

        

    # df = dict(
    #     id = id,
    #     name = name,
    #     goods_position = goods_position,
    #     description = description,
    #     model_position = model_position,
    #     color_list = color_list,
    #     classify = classify,
    #     count = count,
    #     photo_path = photo_path
    # )

    # col1, col2 = st.columns(2)
    # with col1:
    #     if st.button('加入清单') and st.session_state["continue_add"] == True:
    #         add_cache_data(pd.DataFrame([df]))
    # with col2:
    #     if st.button(f'清空清单', use_container_width=True):
    #         reset_cache_data()

    # 将清单数据加入数据库
    # all_data = get_cache_data()
    # if len(all_data) > 0:
    #     st.dataframe(all_data, use_container_width=True)
    # else:
    #     st.info(':blue[清单无商品]')

    # if len(all_data) > 0:
    #     # all_data = all_data.drop(columns=['id'], axis=1).to_dict('records')
    #     all_data = all_data.to_dict('records')

    #     if st.button(f'新增所有商品', use_container_width=True):
    #         for v in all_data:
    #             if not ph().create_product(**v):
    #                 st.error('create_product failed')
    #                 st.stop()
    #             # 添加图片到shitu库中
    #             add_record(v['id'], v['photo_path'])
    #         reset_cache_data()
    #         if st.button(f'重新整理', use_container_width=True):
    #             pass
    #         st.success(f'新建商品成功！')

    # if submitted:
    #     if upload_file is None:
    #         st.error("请上传商品图片")
    #         st.stop()
    #     if goods_position == "":
    #         st.error("请指定商品货位")
    #         st.stop()
        
    #     with st.spinner("判断图片是否存在库中"):
    #         info = search_image(upload_file)

    #     with st.container():
    #         if info['find_result'] == True: # 图片已在库中
    #             product_list = search_product(info['rec_docs'])
    #             if not len(product_list) == 1:
    #                 product_list
    #                 st.error('产品库有问题，请联系管理员') 
    #                 st.stop()
    #             st.info("从库中中找到一张类似图片，仍要添加新的商品吗?")
    #             col1, col2 = st.columns(2)
    #             with col1:
    #                 st.image(upload_file, caption='上传图片')
    #             with col2:
    #                 lib_image = Image.open(info['photo_path'])
    #                 st.image(lib_image, caption="库中图片")
    #                 product_list[0].show_product_info()
    #             st.button("仍要添加", key="double_confirm", on_click=submit_goods_confirm)
                
    #         else:
    #             comfirm_add_product(product, upload_file)
    #             product.show_product_info()
    #             st.image(upload_file, width=100)
    #             st.button("确认提交", key="confirm", on_click=submit_goods_confirm)
            

    # # 这里通过session_state判断弹窗里的确定按钮被点击了，就进行你想要的逻辑操作。
    # if not st.session_state["continue_add"]  == False:
    #     st.session_state["continue_add"] = True    # 恢复session_state为False
    #     st.experimental_rerun()  # 重刷页面



        
            
