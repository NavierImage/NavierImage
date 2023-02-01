
import os
import re
import openpyxl
import shutil
file_path = r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_512\CT"
xlsx_path = r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR\data_prop_1_hetero.xlsx"
wb = openpyxl.load_workbook(xlsx_path)
worksheet = wb["Total_data_prop"]
get_mode = 1
if get_mode:
    slice_list = os.listdir(file_path)
    counter = 0
    start_idx = re.findall(r"\d+", slice_list[0])
    for i in range(len(start_idx)):
        print(int(start_idx[i]))

    patient_idx = int(start_idx[0])
    slice_idx = int(start_idx[1])
    worksheet["J2"] = slice_idx
    counter = 2
    for i in range(len(slice_list)):
        idx_list = re.findall(r"\d+", slice_list[i])
        p_idx = int(idx_list[0])
        s_idx = int(idx_list[1])
        print(p_idx, s_idx)
        if patient_idx != p_idx:
            counter += 1
            worksheet["K%d" %(counter-1)] = s_idx_pre
            worksheet["J%d" %(counter)] = s_idx

            patient_idx = p_idx
        s_idx_pre = s_idx

    wb.save(xlsx_path)

    