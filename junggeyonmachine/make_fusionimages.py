import os
import numpy as np
from PIL import Image
img1_path = r"C:\plastimatch_tester\mind30_bilinear_comset3\syncut"
img2_path = r"C:\plastimatch_tester\defcut"
slash = r"/"
img1_list = os.listdir(img1_path)
img2_list = os.listdir(img2_path)

assert len(img1_list) == len(img2_list)

for i in range(len(img1_list)): 
    
    img1 = Image.open(img1_path + slash + img1_list[i])
    img2 = Image.open(img2_path + slash + img2_list[i])

    imgarr1 = np.array(img1)
    imgarr2 = np.array(img2)

    rgbarr1 = np.stack((imgarr1, ) * 3, axis = -1)
    rgbarr2 = np.stack((imgarr2, ) * 3, axis = -1)

    assert rgbarr1.shape == rgbarr2.shape, "you need to match the size of images"

    rgbarr1[:, :, 0] = 0
    rgbarr1[:, :, 2] = 0
    rgbarr2[:, :, 1] = 0

    fusion_arr = rgbarr1 + rgbarr2
    fusion_arr = fusion_arr.astype('uint8')
    fusion_pic = Image.fromarray(fusion_arr)
    fusion_pic.save(r"C:\plastimatch_tester\fusion" + slash+ "%d.jpg" %(i))
                    #img1_list[i][:4] + 
                    #"fusion_slice"+
                    #img1_list[i][13:16]+
                    #'.jpg')
