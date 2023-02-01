import os

basepath = r'D:\junggeyon\Patient_data_2'
folder_list = os.listdir(basepath)
print(folder_list)
name = ['CT', 'CT_aligned', 'CT_RTst', 'MR', 'MR_RTst']
for foldername in folder_list:
    for modality_folder_name in name:
        try:os.makedirs(basepath +'/'+ foldername+ '/' + modality_folder_name)
        except:pass