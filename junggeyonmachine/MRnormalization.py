import os
import numpy as np
import matplotlib.pyplot as plt
import skimage
from PIL import Image

basepath = r'D:\MRSIM_abdomen_data\npy\MR/'

mr_npy_list = os.listdir(basepath)

norm_val_list = []
number_of_patients = 50
for idx in range(number_of_patients):
    
    #####read voxel#####
    mr_volume = np.load(basepath + mr_npy_list[idx])
    mr_one_dim = np.ravel(mr_volume)

    #####normalization#####
    max_pixel_value = 2000
    mrnorm_hyperparam = 1000
    counts_list, bin_locations, patches = plt.hist(mr_one_dim, max_pixel_value, (0, max_pixel_value))
    plt.ylim((0, 1e5))
    plt.xlim((0, 2000))
    plt.xlabel("Pixel Value")
    plt.ylabel("Number of Pixels")
    plt.show()
    
    for idx_val in range(max_pixel_value-1, -1, -1):
        if counts_list[idx_val] > mrnorm_hyperparam:
            val_norm = idx_val+1
            print(mr_npy_list[idx] + ': ' + str(val_norm))
            norm_val_list.append(val_norm)
            break
    
    mr_volume = np.where(mr_volume > val_norm, val_norm, mr_volume)

    #####rescaling and make image#####
    mr_volume = mr_volume.astype('float64')
    max_ = np.max(mr_volume)
    min_ = np.min(mr_volume)

    mr_volume -= min_
    mr_volume /= max_-min_

    mr_volume *= 255
    mr_volume = mr_volume.astype('uint8')
    
    #np.save(r'D:\junggeyon\pelvic_MR_pic_npy/'+r'P%03dMR_pic_volume.npy' %(idx+1), mr_volume)
    mr_volume_re = skimage.transform.resize(mr_volume, (len(mr_volume), 256, 256))
    mr_volume_re *= 255
    mr_volume_re = mr_volume_re.astype('uint8')

    for i in range(len(mr_volume)):
        #if i < 40 and len(mr_volume) > 100:
        #    continue
        image = Image.fromarray(mr_volume_re[i])
        image.save(r"D:\teeest1/P%03d_MR_slice%03d.jpg" %(idx+1,i+1))
        
        #if len(mr_volume) - i == 21 and len(mr_volume) > 100:
        #    break
       #image.save(r'D:\test_pic/'+ r'P03%d_MR_slice%d.jpg' %(idx+1, i), 'JPEG')
#해당 pixel값 저장해놓고, 그것으로 normalization 해주기...

