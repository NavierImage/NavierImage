import os 
basepath = r"D:\!JUNG_newdata_T23D_mr\abdomenCT1\10079813"

file_dir_list = os.listdir(basepath)

wc_list = []


for i in range(len(file_dir_list)):
    if "WC" in file_dir_list[i]:
        wc_list.append(float(file_dir_list[i][2:8]))

print(wc_list[115])