import numpy as np
from numpngw import write_png
from PIL import Image
import os
basepath = r'D:\DeepMaster\MRSIM\aligned256'
voxel_file_list = os.listdir(basepath + r'\MR_png_npy')
for file in range(len(voxel_file_list)):
    voxel = np.load(basepath + r'\MR_png_npy' + r'\\'+voxel_file_list[file])
    voxel = voxel.astype('float64')
    voxel *= 255/65535
    voxel = voxel.astype('uint8')

    for i in range(voxel.shape[0]):
        im = Image.fromarray(voxel[i])
        if int(voxel_file_list[file][:3]) < 10:
            if i < 9:
                im.save(basepath + r'\MR'+ r'\train/'+ r'00%dMR_slice00%d.jpeg' %(int(voxel_file_list[file][:3]), i+1))
            else:
                im.save(basepath + r'\MR'+ r'\train/'+ r'00%dMR_slice0%d.jpeg' %(int(voxel_file_list[file][:3]), i+1))
        else:
            if i < 9:
                im.save(basepath + r'\MR'+ r'\train/'+ r'0%dMR_slice00%d.jpeg' %(int(voxel_file_list[file][:3]), i+1))
            else:
                im.save(basepath + r'\MR'+ r'\train/'+ r'0%dMR_slice0%d.jpeg' %(int(voxel_file_list[file][:3]), i+1))