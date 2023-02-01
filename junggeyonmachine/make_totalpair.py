import os
from PIL import Image

image1_path = r"C:\plastimatch_tester\nomind_bicubic_comset3\realMR"
image2_path = r"D:\AAAAmrsim\results\MRSIM_CECT_npy_nomind_v100\test_latest\fakeCT_gray"
image3_path = r"C:\plastimatch_npy2\defcut"
image4_path = r"D:\AAAAmrsim\results\MRSIM_CECT_npy_nomind_v100\test_latest\fusion"
image5_path = r"D:\AAAAmrsim\results\MRSIM_CECT_npy_nomind_v100\test_latest\mae"

save_path = r"D:\AAAAmrsim\results\MRSIM_CECT_npy_nomind_v100\test_latest"
slash = r"/"
img1_list = os.listdir(image1_path)
img2_list = os.listdir(image2_path)
img3_list = os.listdir(image3_path)
img4_list = os.listdir(image4_path)
img5_list = os.listdir(image5_path)

assert len(img2_list) == len(img1_list), 'set the fileidx'
for i in range(len(img1_list)):
    
    image1 = Image.open(image1_path + slash + img1_list[i])
    image2 = Image.open(image2_path + slash + img2_list[i])
    image3 = Image.open(image3_path + slash + img3_list[i])
    image4 = Image.open(image4_path + slash + img4_list[i])
    image5 = Image.open(image5_path + slash + img5_list[i])
    image1_size = image1.size
    image2_size = image2.size
    image3_size = image3.size
    new_image = Image.new('RGB', (3*image1_size[0], 2*image1_size[1]), (0, 0, 0))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_size[0], 0))
    new_image.paste(image3, (2*image1_size[0], 0))
    new_image.paste(image4, (0, image1_size[1]))
    new_image.paste(image5, (image1_size[0], image1_size[1]))
    new_image.save(save_path + slash + (img1_list[i][:4]) + (img1_list[i][6:-8]) +'totalpair.jpg', 'JPEG')
    
        