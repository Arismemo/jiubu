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
upload_photo_path = '/home/liukun/work/jiubu/media/temp' # 待识别的图片的目录
shitu_operator = ShiTu(gallary_path, index_path)

def add_record(tag, photo_path):
    try:
        shitu_operator.add_record(tag, photo_path)
        return True
    except Exception as e:
        st.error("添加图片失败,请联系管理员,reason: " + str(e))
        return False
    

def search_image(photo_path):
    info = shitu_operator.get_tag_by_image(photo_path)
    return info