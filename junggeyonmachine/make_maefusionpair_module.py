from importlib.resources import path
import os 
import numpy as np
from PIL import Image
from sklearn.metrics import mean_absolute_error
#result_name_path = r"D:\DLnetwork\MRSIM_checkpoints_2\results\MRSIM_CECT_totalMR_CUT_v2"
basepath = r"C:\plastimatch_npy2\!swinunetr_encode3"
img1_path = basepath + r"\syncut" #fake CT path

img2_path = basepath + r"\defcut" #ref CT path
img3_path = basepath + r"\realMR_gray" #ref MR path

img4_path = basepath + r'\fusion'
img5_path = basepath + r'\mae'
three_pair_save_path = basepath + r'\threepair'
total_pair_save_path = basepath + r'\totalpair'
slash = r'/'
img1_list = os.listdir(img1_path)
img2_list = os.listdir(img2_path)

try: os.mkdir(basepath + r"\fusion")
except: pass
try: os.mkdir(basepath + r"\mae")
except: pass
try: os.mkdir(basepath + r"\threepair")
except:pass
try: os.mkdir(basepath + r"\totalpair")
except: pass

assert len(img1_list) == len(img2_list)

##make MAE images##
for i in range(len(img1_list)):
    imarr1 = np.array(Image.open(img1_path + slash + img1_list[i]), 'int16')
    imarr2 = np.array(Image.open(img2_path + slash + img2_list[i]), 'int16')
    mae_arr = imarr1 - imarr2
    mae_arr = np.where(mae_arr < 0, -1 * mae_arr, mae_arr)
    mae_arr = mae_arr.astype('uint8')
    mae_img = Image.fromarray(mae_arr)
    #mae_img.save(basepath + r"\mae/"+
    #                img1_list[i][:4] + 
    #                "mae_slice"+
    #                img1_list[i][13:16]+
    #                '.jpg')
    # mae_img.save(basepath + r'\mae/'+
    # img1_list[i][:4]+
    # "mae_slice"+
    # img1_list[i][-7:-4]+
    # '.jpg')
    mae_img.save(basepath + r'\mae/'+
    img1_list[i][:4]+
    "mae_slice"+
    "%03d"%(i+1)+
    '.jpg')


img1_list = os.listdir(img1_path)
img3_list = os.listdir(img3_path)

assert len(img1_list) == len(img3_list)
##make Fusion images##
for i in range(len(img1_list)): 
    
    img1 = Image.open(img1_path + slash + img1_list[i])
    img2 = Image.open(img3_path + slash + img3_list[i])

    imgarr1 = np.array(img1)
    imgarr2 = np.array(img2)

    rgbarr1 = np.stack((imgarr1, ) * 3, axis = -1)
    rgbarr2 = np.stack((imgarr2, ) * 3, axis = -1)
    print(img1_list[i], img3_list[i])
    assert rgbarr1.shape == rgbarr2.shape, "you need to match the size of images"

    rgbarr1[:, :, 0] = 0
    rgbarr1[:, :, 2] = 0
    rgbarr2[:, :, 1] = 0

    fusion_arr = rgbarr1 + rgbarr2
    fusion_arr = fusion_arr.astype('uint8')
    fusion_pic = Image.fromarray(fusion_arr)
    #fusion_pic.save(basepath + r"\fusion" + slash+
    #                img1_list[i][:4] + 
    #                "fusion_slice"+
    #                img1_list[i][13:16]+
    #                '.jpg')
    # fusion_pic.save(basepath + r'\fusion/'+
    # img1_list[i][:4]+
    # "fusion_slice"+
    # img1_list[i][-7:-4]+
    # '.jpg')
    fusion_pic.save(basepath + r'\fusion/'+
    img1_list[i][:4]+
    "fusion_slice"+
    "%03d" %(i+1)+
    '.jpg')

for i in range(len(img1_list)):
    image1 = Image.open(img3_path + slash + img3_list[i])
    image2 = Image.open(img1_path + slash + img1_list[i])
    image3 = Image.open(img2_path + slash + img2_list[i])
    image1_size = image1.size
    image2_size = image2.size
    image3_size = image3.size
    new_image = Image.new('L', (3*image1_size[0], image1_size[1]), (250))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_size[0], 0))
    new_image.paste(image3, (2*image1_size[0], 0))
    new_image.save(three_pair_save_path + slash + str(i) + (img1_list[i][:4]) + (img1_list[i][6:-8]) +'3pair.jpg', 'JPEG')
    

img4_list = os.listdir(img4_path)
img5_list = os.listdir(img5_path)

assert len(img2_list) == len(img1_list), 'set the fileidx'
for i in range(len(img1_list)):
    
    image1 = Image.open(img3_path + slash + img3_list[i])
    image2 = Image.open(img1_path + slash + img1_list[i])
    image3 = Image.open(img2_path + slash + img2_list[i])
    image4 = Image.open(img4_path + slash + img4_list[i])
    image5 = Image.open(img5_path + slash + img5_list[i])
    image1_size = image1.size
    image2_size = image2.size
    image3_size = image3.size
    new_image = Image.new('RGB', (3*image1_size[0], 2*image1_size[1]), (0, 0, 0))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_size[0], 0))
    new_image.paste(image3, (2*image1_size[0], 0))
    new_image.paste(image4, (0, image1_size[1]))
    new_image.paste(image5, (image1_size[0], image1_size[1]))
    new_image.save(total_pair_save_path + slash+ str(i)  + (img1_list[i][:4]) + (img1_list[i][6:-8]) +'totalpair.jpg', 'JPEG')

