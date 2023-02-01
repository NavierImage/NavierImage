import os
from PIL import Image
mr_file_list = os.listdir(r'D:\junggeyon\Unity\Unity CT MR registered - img\Aligned256\valid_cyclegan_2d\mr')
ct_file_list = os.listdir(r'D:\junggeyon\Unity\Unity CT MR registered - img\Aligned256\valid_cyclegan_2d\ct')


for i in range(len(mr_file_list)):
    
        image1 = Image.open(r'D:\junggeyon\Unity\Unity CT MR registered - img\Aligned256\valid_cyclegan_2d\mr/' + mr_file_list[i])
        image2 = Image.open(r'D:\junggeyon\Unity\Unity CT MR registered - img\Aligned256\valid_cyclegan_2d\ct/' + ct_file_list[i])
        #image3 = Image.open('D:\junggeyon\Fusion\Patient1/pa1fusion%d' %i)
        
        image1_size = image1.size
        image2_size = image2.size
        new_image = Image.new('RGB', (2*image1_size[0], image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1_size[0], 0))
        new_image.save(r'D:\junggeyon\Unity\Unity CT MR registered - img\Aligned256\valid_cyclegan_2d\zzzmr_ct_valid/'+ mr_file_list[i][:12] + 'mrct.jpg', 'JPEG')
    