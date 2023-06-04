
paddleclas --build_gallery=True --model_name="PP-ShiTuV2" \
	-o IndexProcess.image_root=/home/liukun/work/jiubu/pp_backend/resource/jiubu_dataset/gallery/images \
	-o IndexProcess.index_dir=/home/liukun/work/jiubu/pp_backend/resource/jiubu_dataset/index/ \
	-o IndexProcess.data_file=/home/liukun/work/jiubu/pp_backend/resource/jiubu_dataset/gallery/images_map.txt


CURRENT_DIR=$( cd "$(dirname "$0")"; pwd)
echo $CURRENT_DIR
streamlit run web_front/扫码识别.py $CURRENT_DIR

