import os
import sys
sys.path.append('..')
from shitu.shitu import ShiTu

gallary_path = '/home/liukun/work/jiubu/shitu/gallery'
index_path = '/home/liukun/work/jiubu/shitu/index'

shitu_op = ShiTu(gallary_path, index_path)

test_image_path = '/home/liukun/work/jiubu/test_shitu/images/微信图片_20230504214236.jpg'
test_tag = 'A0104'

# res = shitu_op.add_record(test_tag, test_image_path)
# print('[DEBUG] main add:', res)


res = shitu_op.get_tag_by_image(test_image_path)
print('[DEBUG] main find:', res)





