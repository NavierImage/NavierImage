import os
import shutil
import openpyxl

file_source_CT = r"D:\DLnetwork\traindata_MRSIM_windowed_2\valB"
file_destination_CT = r"D:\MRSIM_abdomen_data\traindata_MRSIM_CNC\CT_nc"


CT_file_list = os.listdir(file_source_CT)

work_xl = openpyxl.load_workbook(r"D:\MRSIM_abdomen_data\Patient_data\properties\data_prop_.xlsx", data_only=True)
worksheet = work_xl["Sheet1"]

#get_cells = worksheet["A2" : "A51"]
#for row in get_cells:
#    for cell in row:
#        print(cell.value)

for i in range(len(CT_file_list)):
    if CT_file_list[i][3] != "0":
        patient_num = CT_file_list[i][1:4].strip("0")
    else:
        patient_num = CT_file_list[i][1:4].lstrip("0")
    
    if worksheet["B" + str(int(patient_num)+1)].value == "con":
        pass
        #shutil.copyfile(file_source_CT + '/' + CT_file_list[i], file_destination_CT +  '/' + CT_file_list[i])
        #shutil.copyfile(file_source_MR + '/' + MR_file_list[i], file_destination_MR  + '/' + MR_file_list[i])
    else:
        shutil.copyfile(file_source_CT + '/' + CT_file_list[i], file_destination_CT +  '/' + CT_file_list[i])