import os
import shutil
import openpyxl

file_path = r'D:\DLnetwork\traindata_MRSIM_CECT_totalMR_512\CT'
file_destination = r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_512\trashCT"
xlsx_path = r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_512\data_prop_1_hetero.xlsx"

wb = openpyxl.load_workbook(xlsx_path)
worksheet = wb["Total_data_prop"]
patient_num = worksheet["A2":"A51"]
pa_num = []
for row in patient_num:
    for celldata in row:
        pa_num.append(int(celldata.value))


get_cell_1 = worksheet["L2" : "L51"]

elim_start = []
for row in get_cell_1:
    for celldata in row:
        try:
            elim_start.append(int(celldata.value))
        except:
            pass
elim_end = []
get_cell_2 = worksheet["M2" : "M51"]
for row in get_cell_2:
    for celldata in row:
        try:
            elim_end.append(int(celldata.value))
        except:
            pass

file_list = os.listdir(file_path)

for i in range(len(pa_num)):
    for j in range(len(file_list)):
        if pa_num[i] == int(file_list[j][1:4].lstrip("0")):
            done = 0
            for k in range(elim_start[i], elim_end[i]):
                shutil.move(file_path+'/'+file_list[j][:-7] +"%03d.jpg" %k, file_destination +'/' +file_list[j][:-7] +"%03d.jpg" %k)
                done = 1
            if done == 1:
                break

