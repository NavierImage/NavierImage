import numpy as np
from numpngw import write_png
ctvox = np.load(r"D:\junggeyon\Unity\Unity CT MR registered\Aligned256\train_cyclegan_2d\ct\P01_slice040_CT_tform.npy")
ctvox = ctvox.astype('int32')
ctvox += np.min(ctvox)
ctvox *= int((2**16)/(2**12))
ctvox = ctvox.astype('uint16')
write_png(r'D:\junggeyon\Unity\Unity CT MR registered\Aligned256\cc.png', ctvox)