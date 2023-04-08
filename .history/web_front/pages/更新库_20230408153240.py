import base64
import streamlit as st
from PIL import Image
import re
import os

pp_shitu_path = '/Users/liukun/pp/demo_test'
temp_upload_image_path = os.path.join(pp_shitu_path, 'temp_image.jpg')


def pp_add_inex(tag, gallary_path):
    import subprocess

    index_file_path = os.path.join(gallary_path, "shows_flower.txt")
    command = "echo '{}\t{}' >> {}".format(tag + '.jpg', tag, index_file_path)
    st.write(command)
    subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=pp_shitu_path)

    command = "paddleclas --build_gallery=True --model_name='PP-ShiTuV2' -o IndexProcess.image_root=./drink_dataset_v2.0/gallery/ -o IndexProcess.index_dir=./drink_dataset_v2.0/index -o IndexProcess.data_file=./drink_dataset_v2.0/gallery/shows_flower.txt"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=pp_shitu_path)
    exec_output, unused_err = p.communicate()
    # st.write(exec_output)


product_code = st.text_input('请输入商品位置或编号', 'A0101')
upload_file = st.file_uploader("请上传商品编号对应的图片", type=["jpg", "png", "jpeg"])

if upload_file is not None:
    product_pic = Image.open(upload_file)
    gallary_path = os.path.join(pp_shitu_path, 'drink_dataset_v2.0/gallery/')
    image_path = os.path.join(gallary_path, product_code + '.jpg')
    st.write(gallary_path)
    product_pic.save(image_path)
    st.image(product_pic)
    # st.write(type(product_pic))

    if st.button('添加到库', on_click=pp_add_inex, args=(product_code, gallary_path,)):
        st.write('已添加')