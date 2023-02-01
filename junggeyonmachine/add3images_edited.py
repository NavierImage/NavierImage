import os
from PIL import Image
ct_img_list = os.listdir(r'D:\CT_norm_im')
mr_img_list = os.listdir(r'D:\MR_norm_im')
fu_img_list = os.listdir(r'D:\DeepMaster\MRSIM_total\CTMR_fusion')

for i in range(len(ct_img_list)):
    image1 = Image.open(r'D:\CT_norm_im/' + ct_img_list[i])
    image2 = Image.open(r'D:\MR_norm_im/' + mr_img_list[i])
    image3 = Image.open(r'D:\DeepMaster\MRSIM_total\CTMR_fusion/' + fu_img_list[i])
    image1 = image1.resize((512, 512))
    image2 = image2.resize((512, 512))
    image3 = image3.resize((512, 512))
    image1_size = image1.size
    image2_size = image2.size
    image3_size = image3.size
    new_image = Image.new('RGB', (3*image1_size[0], image1_size[1]), (250, 250, 250))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_size[0], 0))
    new_image.paste(image3, (2*image1_size[0], 0))
    new_image.save(r'D:\ctmrfu/' + ct_img_list[i][:4] + 'ctmrfusion_slice' + ct_img_list[i][-8:-5] + '.jpg')