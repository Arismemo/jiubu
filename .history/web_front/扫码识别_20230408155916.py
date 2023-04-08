import base64
import streamlit as st
from PIL import Image
import re
import os

# @st.cache_data
def run_pp_shitu():
    import subprocess
    # exit_status, output = commands.getstatusoutput("paddleclas --model_name=PP-ShiTuV2 --predict_type=shitu -o Global.infer_imgs='https://image.buy.ccb.com/merchant/201909/1189826382/1594017506908.jpg' -o IndexProcess.index_dir='./drink_dataset_v2.0/index''")
    command = "paddleclas --model_name=PP-ShiTuV2 --predict_type=shitu -o Global.infer_imgs='" + temp_upload_image_path + "' -o IndexProcess.index_dir='./drink_dataset_v2.0/index'"
    # command = "paddleclas --model_name=PP-ShiTuV2 --predict_type=shitu -o Global.data_file=image -o IndexProcess.index_dir='./drink_dataset_v2.0/index'"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=pp_shitu_path)
    exec_output, unused_err = p.communicate()
    return exec_output


def shitu(target):
    # image = base64.b64encode(target)

    upload_image = Image.open(file)
    upload_image.save(temp_upload_image_path)
    col1.write("待识别的图片")
    col1.image(upload_image)

    exec_output = run_pp_shitu()
    find_group = re.findall('\[\{.+\]',exec_output.decode())
    result_write = col2.title("识别结果：" + '......')
    if not find_group:
        result_write.write("识别结果：" + '对不起，识别失败，请更换要识别的图片！')
        result_write.write(exec_output)
        return

    img_recognition_dic = eval(find_group[0])[0]
    # st.write(type(img_recognition_dic[0]))
    # st.write('debug', img_recognition_dic)
    print(img_recognition_dic)
    result_write.title("识别结果：" + img_recognition_dic['rec_docs'])



project_dir = os.getenv("CURRENT_DIR")
pp_shitu_path = os.path.join(project_dir, 'pp_backend') # pp_shitu后端的目录
pp_shitu_gallary_path = os.path.join(project_dir, 'pp_backend') # pp_shitu图片的目录
upload_image_path = os.path.join(project_dir, 'assets/images')  # 上传的图片的目录

print(project_dir)
print(pp_shitu_path)
print(pp_shitu_gallary_path)
print(upload_image_path)



st.set_page_config(page_title="九步", page_icon="🍀", layout="wide")

col1, col2 = st.columns(2)
file = col1.file_uploader("请上传要识别的图片", type=["jpg", "png", "jpeg"])

if file is not None:
    shitu(file.read())