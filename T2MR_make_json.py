import os
import json
from collections import OrderedDict
import numpy as np
file_data = OrderedDict()

# file_data["info"] = {[]}
# file_data["licenses"] ={[]}
basepath = r"D:\chanwoong\JUNG_T2sMR_Seg\traindata"
oar_name = "./Spleen/"
where_list = os.listdir(basepath)




file_data["description"] = "challengedata"
file_data["labels"] = {"0" : "background", "1": "bbox"}
file_data["licence"] = "hand off!"
file_data["modality"] = {"0" : "CT"}
file_data["name"] = "segrap"
file_data["numTest"] = 20
file_data["numTraining"] = 120
file_data["reference"] = ""
file_data["release"] = "0.0"
file_data["tensorImageSize"] = "4D"
file_data["test"] = []
file_data["training"] = []
file_data["validation"] = []
train_im_path = os.path.join(basepath, "imagesTr")

train_im_path_list = os.listdir(train_im_path)
train_la_path = os.path.join(basepath, oar_name)
train_la_path_list = os.listdir(train_la_path)

val_cnt = 0



for idx in range(len(train_im_path_list)):
    if 80<= idx < 100:
        file_data["validation"].append({"image": "./imagesTr/" + train_im_path_list[idx],
                                    "label": os.path.join(oar_name, train_la_path_list[idx])})
    else:                           
        file_data["training"].append({"image": "./imagesTr/" + train_im_path_list[idx],
                                    "label": os.path.join(oar_name, train_la_path_list[idx])})
file_path = os.path.join(basepath, r"dataset_0.json")
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(file_data, file, indent=4)
