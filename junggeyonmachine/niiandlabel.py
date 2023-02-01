import nibabel as nib
import numpy as np
from collections import deque 
from PIL import Image
ct = nib.load(r"C:\tasktable\RawData\RawData\Training\label\label0035.nii.gz").get_fdata()
label_np = np.load(r"D:\DLnetwork\research-contributions-main\SwinUNETR\BTCV\outputs\checkyes\0.npy")
save_path = r"D:\DLnetwork\research-contributions-main\SwinUNETR\BTCV\outputs\checkyes\img"

ct = np.transpose(ct, (2, 1, 0))
label_np = np.transpose(label_np, (2, 1, 0))
ct = np.stack((ct, ) * 3, axis = -1)
arr = np.stack((label_np, ) * 3, axis = -1)
pic = np.zeros_like(ct[i])
plate = np.zeros_like(arr[i])
for i in range(ct.shape[0]):
    
    plate[i] = np.where(arr[i] == 1, [255, 255, 0], plate[i])
    plate[i] = np.where(arr[i] == 2, [0, 255, 0], plate[i])
    plate[i] = np.where(arr[i] == 3, [0, 0, 255], plate[i])
    plate[i] = np.where(arr[i] == 4, [255, 255, 0], plate[i])
    plate[i] = np.where(arr[i] == 5, [255, 0, 255], plate[i])
    plate[i] = np.where(arr[i] == 6, [0, 255, 255], plate[i])
    plate[i] = np.where(arr[i] == 7, [255, 255, 255], plate[i])
    plate[i] = np.where(arr[i] == 8, [185, 255, 0], plate[i])
    plate[i] = np.where(arr[i] == 9, [255, 185, 0], plate[i])
    plate[i] = np.where(arr[i] == 10, [255, 0, 185], plate[i])
    plate[i] = np.where(arr[i] == 11, [0, 185, 255], plate[i])
    plate[i] = np.where(arr[i] == 12, [185, 0, 255], plate[i])
    plate[i] = np.where(arr[i] == 13, [255, 185, 0], plate[i])

    ct[i] = np.where(plate == [0, 0, 0], ct, plate)
    img = Image.fromarray(ct[i])
    img.save(save_path + "%d.jpg" %(i+1))


                        
