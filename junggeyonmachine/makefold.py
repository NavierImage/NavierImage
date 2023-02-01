import os
import shutil
file_path = r'C:\pelvic_unity/'
patient_file_list = os.listdir(file_path)
for folder in patient_file_list:
    folder_file_list = os.listdir(file_path+folder)
    #1. 이거 실행
    #os.mkdir(file_path + folder + '/' + "CT")
    #os.mkdir(file_path + folder + '/' + "MR")
    #os.mkdir(file_path + folder + '/' + "CT_aligned")
    #os.mkdir(file_path + folder + '/' + "MR_RTst")
    #os.mkdir(file_path + folder + '/' + "CT_RTst")
    #2. 이거 실행
    dcm_folder_list = os.listdir(file_path + folder + '/' + folder_file_list[0])
    print(dcm_folder_list)
    for dcm_folder in dcm_folder_list:
        if "CT" and "Align" in dcm_folder :
            shutil.move(file_path + folder+ '/' + folder_file_list[0]+'/' + dcm_folder , file_path + folder + '/'+ dcm_folder) 
        elif "CT" in dcm_folder and "Align" not in dcm_folder:
            shutil.move(file_path + folder+ '/' + folder_file_list[0]+'/' + dcm_folder , file_path + folder + '/'+ dcm_folder)
        elif "MR" in dcm_folder:
            shutil.move(file_path +folder+ '/' + folder_file_list[0]+'/' + dcm_folder, file_path + folder + '/'+ dcm_folder)
    #    elif "RTst" in dcm_folder and "MR" not in dcm_folder:
    #        shutil.move(file_path +folder+ '/' + folder_file_list[0]+'/' + dcm_folder, file_path + folder + '/'+ folder_file_list[3])
    #    elif "RTst" in dcm_folder and "MR" in dcm_folder:
    #        shutil.move(file_path +folder+ '/' + folder_file_list[0]+'/' + dcm_folder, file_path + folder + '/'+ folder_file_list[5])

    #if "MR" == folder:
    #    CT_folder_list = os.listdir(file_path + folder)
    #    if len(CT_folder_list)>1:
    #        for RTst in CT_folder_list:
    #            if "RTst" in RTst:
    #                shutil.move(file_path+folder+'/'+RTst, file_path+folder + '/' +'MR_RTst')