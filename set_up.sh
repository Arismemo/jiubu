pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 初始化pp识图
cd pp_backend
wget https://paddle-imagenet-models-name.bj.bcebos.com/dygraph/rec/models/inference/picodet_PPLCNet_x2_5_mainbody_lite_v1.0_infer.tar
wget https://paddle-imagenet-models-name.bj.bcebos.com/dygraph/rec/data/drink_dataset_v2.0.tar && tar -xf drink_dataset_v2.0.tar
paddleclas --build_gallery=True --model_name="PP-ShiTuV2" \
-o IndexProcess.image_root=./drink_dataset_v2.0/gallery/ \
-o IndexProcess.index_dir=./drink_dataset_v2.0/index \
-o IndexProcess.data_file=./drink_dataset_v2.0/gallery/drink_label.txt


cd ..
