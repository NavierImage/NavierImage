import os
import re
from PIL import Image
data_path = r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR"

trainA = "trainA"
trainB = "trainB"
testA = "testA"
testB = "testB"

another_trainA = "another_trainA"
another_trainB = "another_trainB"
another_testA = "another_testA"
another_testB = "another_testB"

pre_trainA_paths = os.listdir(os.path.join(data_path, trainA))
pre_trainB_paths = os.listdir(os.path.join(data_path, trainB))
pre_testA_paths = os.listdir(os.path.join(data_path, testA))
pre_testB_paths = os.listdir(os.path.join(data_path, testB))

aft_trainA_paths = os.path.join(data_path, another_trainA)
aft_trainB_paths = os.path.join(data_path, another_trainB)
aft_testA_paths = os.path.join(data_path, another_testA)
aft_testB_paths = os.path.join(data_path, another_testB)

pre_paths_list = [pre_trainA_paths, pre_trainB_paths, pre_testA_paths, pre_testB_paths]
aft_paths_list = [aft_trainA_paths, aft_trainB_paths, aft_testA_paths, aft_testB_paths]
pre = [trainA, trainB, testA, testB]
aft = [another_trainA, another_trainB, another_testA, another_testB]

pre_a = ["001"]
for i, split_set in enumerate(pre_paths_list):
    cnt = 0
    for idx, img_path in enumerate(split_set):
        cnt += 1
        a = re.findall(r'\d+', img_path)
        if pre_a[0] != a[0]:
            cnt = 1
            pre_a = a[:]
        img = Image.open(os.path.join(os.path.join(data_path, pre[i]), img_path))
        img.save(os.path.join(aft_paths_list[i], "P%s" %(a[0]) +img_path[4:8]+"slice%03d.jpg"  %(cnt)))