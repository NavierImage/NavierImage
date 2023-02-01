import os
import shutil
import openpyxl
import numpy as np
excel_path = r"D:\DLnetwork\traindata_MRSIM_CNC_2\data_prop_2_homo.xlsx"

workbook = openpyxl.load_workbook(excel_path)
each_mode = 1
#개별모드...
if each_mode == 1:
    worksheet = workbook["Total_data_prop"]

    get_pa_num = worksheet["A2" : "A55"]


    pa_num_list = []
    i = 1
    for row in get_pa_num:
        i += 1
        for cells in row:
            isval = worksheet["H%d" %i]
            if isval.value == "val":
                pass
            else:
                worksheet["H%d" %i] = "train"

    workbook.save(r"D:\DLnetwork\traindata_MRSIM_CNC_2\data_prop_2_homo.xlsx")
else:
    worksheet = workbook["Total_data_prop"]
    get_cells = worksheet["E2" : "H52"]
    start_row = 0; start_col = 0
    end_row = 52-2 + 1; end_col = int(ord("H")) - int(ord("E")) + 1
    data_array = np.zeros((end_row, end_col))
    print(data_array.shape)
    #for row in get_cells:
    #    for cells in row:
    #        if cells.value == "val":
    #            pass
    #        else:
    #            cells.value = "train"
    #workbook.save(r"D:\CNC_train_data\data_prop.xlsx")            