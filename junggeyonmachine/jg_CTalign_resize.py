import numpy as np
from numpngw import write_png
from skimage.transform import resize
from PIL import image
import os


basepath = r'D:\DeepMaster\MRSIM'
for k in range(39, 48):
    ctvoxel = np.load(basepath + r'\aligned\CT_png_npy\0%dMR_png_voxel.npy' %(k))
    ctvoxel_resized = np.zeros((len(ctvoxel), 256, 256))

    for i in range(len(ctvoxel)):
        ctvoxel_slice_resized = resize(ctvoxel[i], (256, 256))
        ctvoxel_resized[i] = ctvoxel_slice_resized
    ctvoxel_resized *= (2**16-1)
    ctvoxel_resized = ctvoxel_resized.astype('uint16')
    np.save(basepath+ r'\aligned256\CT_png_npy\0%dMR_256png_voxel.npy' %(k), ctvoxel_resized)

    #for i in range(len(ctvoxel_resized)):
    #    write_png(basepath +r'\CT_aligned_resized_png\Patient%d\pa%dctresized%d.png' %(k, k, i), ctvoxel_resized[i])