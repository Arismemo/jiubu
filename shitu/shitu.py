import subprocess
import os
import re
import shutil
import wget

class ShiTu:
    def __init__(self, gallary_path, index_path):
        self._gallary_path = gallary_path
        self._index_path = index_path
        self._images_dir = os.path.join(self._gallary_path, 'images')
        self._images_map_path = os.path.join(self._gallary_path, 'images_map.txt')
        # 如果初始状态库里没有文件，则从网上下载一张，生成默认index
        if not os.path.exists(os.path.join(self._index_path, 'vector.index')):
            if not os.listdir(self._images_dir): # 若文件夹为空，则从网上下载一张图片进行数据库初始化
                url1 = 'https://alifei04.cfp.cn/creative/vcg/veer/1600water/veer-303764513.jpg'
                wget.download(url1, out=os.path.join(self._images_dir, 'test001.jpg'))
                with open(self._images_map_path, 'w') as f:
                    f.write('test001.jpg\ttest001\n')
            self._rebuild_library()


    def _run_subprocess_cmd(self, cmd):
        try:
            ret_line_list = []
            return_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while True:
                next_line = return_info.stdout.readline()
                return_line = next_line.decode("utf-8", "ignore")
                if return_line == '' and return_info.poll() != None:
                    break
                ret_line_list.append(return_line)

            returncode = return_info.wait()
            if returncode:
                raise subprocess.CalledProcessError(returncode, return_info)
            return ret_line_list
        except Exception as e:
            print(ret_line_list)
            print(e)
            raise e


    def _rebuild_library(self):
        # todo: 捕捉subprocess.Popen执行的错误
        command = '''
            paddleclas \
            --build_gallery=True \
            --model_name='PP-ShiTuV2' \
            -o IndexProcess.image_root={} \
            -o IndexProcess.index_dir={} \
            -o IndexProcess.data_file={}
            '''.format(
                self._images_dir,
                self._index_path,
                self._images_map_path
            )

        print(command)
        self._run_subprocess_cmd(command)


    
    def get_image_by_tag(self, tag: str) -> str:
        # 通过tag获取图片路径
        match_path = ''
        name_list = os.listdir(self._images_dir)
        for name in name_list:
            if name.split('.')[0] == tag:
                match_path = os.path.join(self._images_dir, name)

        return match_path
    
    def get_tag_by_image(self, img_path: str) -> str:
        ret = dict()
        command = '''
            paddleclas \
            --model_name=PP-ShiTuV2 \
            --predict_type=shitu \
            -o Global.infer_imgs='{}' \
            -o IndexProcess.index_dir={}'''.format(img_path, self._index_path)
        print(command)
        try:
            exec_output = self._run_subprocess_cmd(command)
        except Exception as e:
            raise e
        
        predict_result_line = ''
        for line in exec_output:
            if 'bbox' in line:
                predict_result_line = line
        
        if not predict_result_line:
            ret['find_result'] = False
            return ret

        print('[DEBUG] predict_result_line', predict_result_line)
        find_group = re.findall('\[\{.+\]', predict_result_line)

        if find_group:
            ret = eval(find_group[0])[0]
            ret['find_result'] = True
        else:
            ret['find_result'] = False

        # 通过tag找出库中图片的路径, 以进行和原图的对比确认
        tag = ret['rec_docs']
        find_image_name = ""
        with open(self._images_map_path) as f:
            while True:
                line = f.readline()
                # print('[{}], [{}]'.format(line, tag))
                if not line:
                    break
                else:
                    pair = re.split('\t|\n', line)
                    file_name = pair[0]
                    file_id = pair[1]
                    # print('[{}], [{}]'.format(file_name, file_id))
                    if tag == file_id:
                        find_image_name = file_name
                        break

        ret['image_path'] = os.path.join(
            self._gallary_path,
            'images',
            find_image_name
        )
        print('[DEBUG] (get_tag_by_image) tag:  ', ret)
        return ret

    # 添加record之前,需要先search,保证数据库中没有重复object
    def add_record(self, tag: str, img_path: str) -> bool:
        try:
            info = self.get_tag_by_image(img_path)
            if info['find_result']:
                raise e
        except Exception as e:
            raise e

        # 将图片移动到gallary/images中, 且在map中添加记录
        image_name = os.path.basename(img_path)
        target_path = os.path.join(self._images_dir, image_name)
        shutil.copy(img_path, target_path)
        with open(self._images_map_path, 'a+') as f:
            f.write("{}\t{}\n".format(image_name, tag))

        # 重新构建库
        self._rebuild_library()




    
    # todo :添加批量加入索引的方法
    def add_batch_record(self, tags: dict) -> bool:
            return

    def delete_record_by_image(self, img_path: str) -> bool:
        # 通过图片路径去删除记录
        tag = self.get_tag_by_image(img_path)
        if not tag: return False # 图片不存在于库中，添加失败

        had_delete = False
        map_dic = {}
        with open(self._images_map_path) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                else:
                    pair = line.split('\t')
                    file_name = pair[0]
                    file_id = pair[1]
                    if tag == file_id: # 如果是要删除的图片，则删除图片
                        os.remove(os.path.join(self._images_dir, file_name))
                        had_delete = True
                        break
                    map_dic[file_name] = file_id

        # 重新写回map文件内容
        with open(self._images_map_path) as f:
            for line in map_dic:
                f.write("{}\t{}\n".format(map_dic[0], map_dic[1]))
        
        # 重新编译索引库
        self._rebuild_library()
        return had_delete
    
    def delete_record_by_tag(self, tag: str) -> bool:
        # 通过tag去删除记录
        self._rebuild_library()
        return
    
    def replace_tag_by_image(self, img_path) -> bool:
        return