import subprocess
import os
import re

class ShiTu:
    def __init__(self, gallary_path, project_dir, index_path):
        self._project_dir = project_dir
        self._gallary_path = gallary_path
        self._index_path = index_path
        return

    # 输入图像路径，输出识别结果
    def run(self, image_path):
        result_list = []

        command = '''
            paddleclas \
            --model_name=PP-ShiTuV2 \
            --predict_type=shitu \
            -o Global.infer_imgs='{}' \
            -o IndexProcess.index_dir={}'''.format(image_path, self._index_path)
        print(command)

        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=self._project_dir)
        exec_output, unused_err = p.communicate()

        print('[DEBUG] exec_output.decode()  ', exec_output.decode())
        find_group = re.findall('\[\{.+\]',exec_output.decode())
        if not find_group:
            return result_list

        result_list = eval(find_group[0])

        print('[DEBUG] result_list  ', result_list)
        return result_list


    # 输入图像路径，和图像唯一标识；返回值bool，是否添加成功
    def update_index_lib(self):
        # 重新构建文件的对应表
        index_images_path = os.path.join(self._gallary_path, 'images')
        index_name_list = os.listdir(index_images_path)
        with open(os.path.join(self._gallary_path, 'images_map.txt'), 'w') as f:
            for file_name in index_name_list:
                position = file_name.split('.')[0]
                f.write("{}\t{}\n".format(file_name, position))


        images_path = os.path.join(self._gallary_path, 'images')
        
        command = '''
            paddleclas \
            --build_gallery=True \
            --model_name='PP-ShiTuV2' \
            -o IndexProcess.image_root={} \
            -o IndexProcess.index_dir={} \
            -o IndexProcess.data_file={}
            '''.format(
                images_path,
                self._index_path,
                os.path.join(self._gallary_path, 'images_map.txt')
            )

        print(command)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=self._project_dir)
        exec_output, unused_err = p.communicate()
        print('[DEBUG]', unused_err)
        return True