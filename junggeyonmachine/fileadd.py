import os
import shutil
file_list = os.listdir(r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_aug\trainA")

for i in range(len(file_list)):
    shutil.copyfile(r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_aug\trainA" + '/' + file_list[i], r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_aug\trainA1" +  '/' + file_list[i][:-4]+'_1.jpg')
    shutil.copyfile(r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_aug\trainA" + '/' + file_list[i], r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_aug\trainA2" +  '/' + file_list[i][:-4]+'_2.jpg')
    shutil.copyfile(r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_aug\trainA" + '/' + file_list[i], r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_aug\trainA3" +  '/' + file_list[i][:-4]+'_3.jpg')
    shutil.copyfile(r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_aug\trainA" + '/' + file_list[i], r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_aug\trainA4" +  '/' + file_list[i][:-4]+'_4.jpg')
    shutil.copyfile(r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_aug\trainA" + '/' + file_list[i], r"D:\DLnetwork\traindata_MRSIM_CECT_totalMR_aug\trainA5" +  '/' + file_list[i][:-4]+'_5.jpg')