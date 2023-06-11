import base64
import streamlit as st
from PIL import Image
import re
import os
import time
import sys
import io
from PIL import Image, ImageDraw
from shitu.shitu import ShiTu


gallary_path = '/home/liukun/work/jiubu/shitu/gallery'
index_path = '/home/liukun/work/jiubu/shitu/index'
upload_image_path = '/home/liukun/work/jiubu/media/temp' # 待识别的图片的目录
shitu_operator = ShiTu(gallary_path, index_path)

def add_record(tag, upload_file):
    upload_image = Image.open(upload_file)
    # gallary_image_path = os.path.join(gallary_path, 'images', tag + '.jpg')

    image_path = os.path.join(upload_image_path, upload_file.name)

    upload_image.save(image_path)
    try:
        shitu_operator.add_record(tag, image_path)
    except Exception as e:
        st.error("添加图片失败,请联系管理员,reason: " + str(e))
    



def search_image(uploaded_file):
    file_contents = uploaded_file.read()
    image = Image.open(io.BytesIO(file_contents))
    image_path = os.path.join(upload_image_path, time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time())) + '.jpg')
    image.save(image_path)
    info = shitu_operator.get_tag_by_image(image_path)
    return info