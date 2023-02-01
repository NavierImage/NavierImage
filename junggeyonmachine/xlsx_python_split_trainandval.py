import os
import re
import shutil
import openpyxl

modal1_path = r"D:\DLnetwork\MRSIM_checkpoints_2\results\sorted"


excel_path = r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_aug\data_prop_CECT_totalMR.xlsx"

file_destination_val = r"D:\DLnetwork\MRSIM_checkpoints_2\results\testreal"
workbook = openpyxl.load_workbook(excel_path)
worksheet = workbook["Total_data_prop"]
modal1_list = os.listdir(modal1_path)

for i in range(len(modal1_list)):
    nums = re.findall(r"\d+", modal1_list[i])
    patients_n, slice_n = int(nums[0]), int(nums[1])
    print(worksheet["E%d" %(patients_n+1)].value)
    if worksheet["E%d" %(patients_n+1)].value == "val":
        shutil.move(modal1_path + '/' + modal1_list[i], file_destination_val+'/' +modal1_list[i])

