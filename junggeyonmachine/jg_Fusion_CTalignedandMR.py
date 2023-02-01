import numpy as np
from PIL import Image
from numpngw import write_png
import os
#for i in range(48):
#    try:
#        os.makedirs('D:\junggeyon\CT_MR_fusion/P%03d' %(i+1))
#    except:
#        pass

basepath = r'D:\junggeyon'
for i in range(1, 21):
    ctvoxel_resized = np.load(basepath + r'\CT_aligned_resized_png\Patient%d\patient%dCTvoxel_imagation_resized.npy' %(i, i))
    mrvoxel = np.load(basepath + r'\MR_png\Patient%d\patient%dMRvoxel.npy' %(i, i))

    ctvoxel_resized = np.transpose(ctvoxel_resized, (3, 1, 2, 0))
    mrvoxel = np.transpose(mrvoxel, (3, 1, 2, 0))

    RGB = 3
    for _ in range(RGB-1):
        ctvoxel_resized = np.delete(ctvoxel_resized, 0,axis = 0)
        mrvoxel = np.delete(mrvoxel, 0, axis = 0)

    padder = np.zeros_like(ctvoxel_resized)
    ct_green = np.append(padder, ctvoxel_resized, axis = 0)
    ct_green = np.append(ct_green, padder, axis = 0)

    mr_pink = np.append(mrvoxel, padder, axis = 0)
    mr_pink = np.append(mr_pink, mrvoxel, axis = 0)

    ct_green = np.transpose(ct_green, (3, 1, 2, 0))
    mr_pink = np.transpose(mr_pink, (3, 1, 2, 0))

    fusion_voxel = ct_green + mr_pink
    fusion_voxel = fusion_voxel.astype('uint16')
    