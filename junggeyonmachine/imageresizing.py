import os
from PIL import Image
path = r'D:\MR_norm_im'
save_path = r'D:\MR_norm_im_256'
im_file_list = os.listdir(path)

for filename in im_file_list:
    im = Image.open(path + '/' + filename)
    im = im.resize((256, 256))
    im.save(save_path +'/'+filename+'_256.jpg')
