import base64
import streamlit as st
from PIL import Image
import re
import os
import time
import sys
import subprocess
import shutil

project_dir = sys.argv[1]
# project_dir = os.getenv("CURRENT_DIR")
pp_shitu_path = os.path.join(project_dir, 'pp_backend') # pp_shitu后端的目录
pp_shitu_gallary_path = os.path.join(project_dir, 'pp_backend/gallery/') # pp_shitu图片的目录
upload_image_path = os.path.join(project_dir, 'assets/images/to_recognize')  # 待识别的图片的目录
add_lib_image_path = os.path.join(project_dir, 'assets/images/to_add_to_lib')  # 待识别的图片的目录
# print(project_dir)
# print(pp_shitu_path)
# print(pp_shitu_gallary_path)
# print(upload_image_path)


def pp_add_inex():

    # 将新增文件从缓存区移动到index区
    file_name_list = os.listdir(add_lib_image_path)
    from_dir = add_lib_image_path
    to_dir = os.path.join(pp_shitu_gallary_path, 'index_images')
    for file_name in file_name_list:
        file_path = os.path.join(from_dir, file_name)
        try:
            shutil.move(file_path, to_dir)
        except:
            st.write('{}文件已存在库中, 是否覆盖或者取消操作'.format(file_name))


    # 重新构建文件的对应表
    index_name_list = os.listdir(to_dir)
    with open(os.path.join(pp_shitu_gallary_path, 'file_map.txt'), 'w') as f:
        for file_name in index_name_list:
            position = file_name.split('.')[0]
            f.write("{}\t{}\n".format(file_name, position))

    IndexProcess_image_root = to_dir
    IndexProcess_index_dir = os.path.join(pp_shitu_gallary_path, 'index')
    IndexProcess_data_file = os.path.join(pp_shitu_gallary_path, 'file_map.txt')
    
    command = "paddleclas --build_gallery=True --model_name='PP-ShiTuV2' -o IndexProcess.image_root={} -o IndexProcess.index_dir={} -o IndexProcess.data_file={}".format(IndexProcess_image_root, IndexProcess_index_dir, IndexProcess_data_file)
    print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=pp_shitu_path)
    exec_output, unused_err = p.communicate()
    # st.write(exec_output)

def save_images_for_index(image_path):
    upload_image.save(image_path)

if __name__ == "__main__":

    product_code = st.text_input('请输入商品位置或编号', 'A0101')
    file = st.file_uploader("请上传商品编号对应的图片", type=["jpg", "png", "jpeg"])

    if file is not None:
        upload_image = Image.open(file)
        image_path = os.path.join(add_lib_image_path, product_code + '.jpg')
        st.image(upload_image)

        if st.button('保存图片待入库', on_click=save_images_for_index, args=(image_path,)):
            st.write('已保存')

        if st.button('添加所有图片到库', on_click=pp_add_inex):
            st.write('已添加')