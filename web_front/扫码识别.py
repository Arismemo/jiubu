import base64
import streamlit as st
from PIL import Image
import re
import os
import time
import sys
import io
from PIL import Image, ImageDraw
from shitu import ShiTu


project_dir = sys.argv[1]
gallary_path = '/home/liukun/work/jiubu/pp_backend/resource/jiubu_dataset/gallery/'
index_path = '/home/liukun/work/jiubu/pp_backend/resource/jiubu_dataset/index/'
shitu_operator = ShiTu(gallary_path, project_dir, index_path)


pp_shitu_path = os.path.join(project_dir, './pp_backend') # pp_shitu后端的目录
upload_image_path = os.path.join(project_dir, 'assets/images/to_recognize')  # 待识别的图片的目录


def handle_uploaded_file(file_list):
    # 创建一个空列表，用于保存所有上传的图片
    images = []
    # 遍历所有上传的文件
    for new_file in file_list:
        # 读取文件内容并将其转换为图像格式
        file_contents = new_file.read()
        image = Image.open(io.BytesIO(file_contents))
        # 将图像添加到列表中
        images.append(image)
    
    # 按行排列所有图像
    num_images = len(images)
    row_width = 500
    num_cols = int(row_width / 100)
    num_rows = int(num_images / num_cols) + (1 if num_images % num_cols > 0 else 0)
    for row in range(num_rows):
        # 创建一个新的行
        col_widths = [100] * min(num_images - row * num_cols, num_cols)
        cols = st.columns(col_widths)
        # 在行中显示图像
        for i, col in enumerate(cols):
            if i + row * num_cols < num_images:
                ig = images[i + row * num_cols]
                
                image_path = os.path.join(upload_image_path, time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time())) + '.jpg')
                ig.save(image_path)

                col.image(ig, use_column_width=True)

                info_list = shitu_operator.run(image_path)
                print(info_list)
                if info_list:
                    for info in info_list:
                        bbox_point_list = info['bbox']
                        x1, y1, x2, y2 = bbox_point_list
                        draw = ImageDraw.Draw(ig)
                        draw.rectangle(((x1, y1), (x2, y2)), outline="red", width=50)
                        col.write(info['rec_docs'])
                else:
                    col.write('未找到')
                
                

if __name__ == "__main__":

    # 设置页面属性
    st.set_page_config(
        page_title="九步", 
        page_icon="🍀", 
        layout="wide"
    )

    # 文件上传组件
    file_list = st.file_uploader(
        label="😘",
        type=["jpg", "png", "jpeg"],
        label_visibility="hidden",
        accept_multiple_files=True,
        help='test help')

    # 处理上传的文件
    if file_list is not None:
        handle_uploaded_file(file_list)