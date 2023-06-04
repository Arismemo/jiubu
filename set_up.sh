pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

paddleclas --build_gallery=True --model_name="PP-ShiTuV2" \
	-o IndexProcess.image_root=/home/liukun/work/jiubu/pp_backend/resource/jiubu_dataset/gallery/ \
	-o IndexProcess.index_dir=/home/liukun/work/jiubu/pp_backend/resource/jiubu_dataset/index/ \
	-o IndexProcess.data_file=/home/liukun/work/jiubu/pp_backend/resource/jiubu_dataset/gallery/images_map.txt

cd ../ # 回到主目录

mkdir -p assets/images/to_recognize
mkdir -p assets/images/to_add_to_lib

# 初始化streamlit
cd ../web_front
