import os
import shutil
import openpyxl
file_source_MR = r"D:\DLnetwork\traindata_MRSIM_windowed_2\valA"
file_source_CT = r"D:\DLnetwork\traindata_MRSIM_windowed_2\valB"
file_destination_CT = r"D:\DLnetwork\traindata_MRSIM_CNC\testCT"
file_destination_MR = r"D:\DLnetwork\traindata_MRSIM_CNC\testMR_contrast"
file_destination_MR_2 = r"D:\DLnetwork\traindata_MRSIM_CNC\testMR_noncontrast"

CT_file_list = os.listdir(file_source_CT)
MR_file_list = os.listdir(file_source_MR)
work_xl = openpyxl.load_workbook(r"D:\MRSIM_abdomen_data\Patient_data\properties\MRSIM_MR_dcm_properties.xlsx", data_only=True)
worksheet = work_xl["Sheet1"]

#get_cells = worksheet["A2" : "A51"]
#for row in get_cells:
#    for cell in row:
#        print(cell.value)

for i in range(len(MR_file_list)):
    if MR_file_list[i][3] != "0":
        patient_num = MR_file_list[i][1:4].strip("0")
    else:
        patient_num = MR_file_list[i][1:4].lstrip("0")
    
    if worksheet["E" + str(int(patient_num)+1)].value == "Contrast":
        shutil.copyfile(file_source_MR + '/' + MR_file_list[i], file_destination_MR  + '/' + MR_file_list[i])
    elif worksheet["E" + str(int(patient_num)+1)].value == "Non-contrast":
        shutil.copyfile(file_source_MR + '/' + MR_file_list[i], file_destination_MR_2  + '/' + MR_file_list[i])