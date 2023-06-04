import base64
import streamlit as st
from PIL import Image
import re
import os
import time
import sys
import subprocess
import shutil
import sys 

sys.path.append("..") 
from shitu import ShiTu

import logging

logging.basicConfig(
    format = '%(asctime)s - %(levelname)s - %(message)s - %(funcName)s',
    level=logging.DEBUG
)

project_dir = sys.argv[1]
gallary_path = '/home/liukun/work/jiubu/pp_backend/resource/jiubu_dataset/gallery/'
index_path = '/home/liukun/work/jiubu/pp_backend/resource/jiubu_dataset/index/'
shitu_operator = ShiTu(gallary_path, project_dir, index_path)


# project_dir = os.getenv("CURRENT_DIR")
pp_shitu_path = os.path.join(project_dir, 'pp_backend') # pp_shitu后端的目录
upload_image_path = os.path.join(project_dir, 'assets/images/to_recognize')  # 待识别的图片的目录
add_lib_image_path = os.path.join(project_dir, 'assets/images/to_add_to_lib')  # 待识别的图片的目录



def pp_add_inex():
    shitu_operator.update_index_lib()


def check_img_existed(product_code):
    return

if __name__ == "__main__":

    logging.debug('logger test')

    product_code = st.text_input('货位', '')
    file = st.file_uploader("上传图片", type=["jpg", "png", "jpeg"])

    existed, info = check_img_existed(file)

    if file and not existed:
        upload_image = Image.open(file)
        if product_code:
            gallary_image_path = os.path.join(gallary_path, 'images', product_code + '.jpg')
        
            logging.debug('gallary_image_path: ', gallary_image_path)
            logging.debug('save image to gallary')

            upload_image.save(gallary_image_path)
            st.image(upload_image)
            if st.button('添加', on_click=pp_add_inex):
                st.write('已添加')
        else:
            st.write('请输入货位')

