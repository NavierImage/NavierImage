import os
from PIL import Image

#for i in range(20):
#    try:
#        os.makedirs('D:\junggeyon\sup/concapatient%d' %(i+1))
#    except:
#        pass

#for file_idx in range(1, 21):
#    for i in range(1, 100):
#        try:
#            image1 = Image.open('D:\junggeyon\CT_aligned_png\Patient%d/pa%dCT%d.png' %(file_idx, file_idx, i))
#            image2 = Image.open('D:\junggeyon\MR_png\Patient%d/pa%dMR%d.png' %(file_idx, file_idx, i))
#            image1 = image1.resize((512, 512))
#            image2 = image2.resize((512, 512))
#
#            image1_size = image1.size
#            image2_size = image2.size
#
#            new_image = Image.new('RGB', (2*image1_size[0], image1_size[1]), (250, 250, 250))
#            new_image.paste(image1, (0, 0))
#            new_image.paste(image2, (image1_size[0], 0))
#            new_image.save('D:\junggeyon\good_mr\concapatient%d/ctmr%d.jpg' %(file_idx, i), 'JPEG')
#        except:
#            break
#image1_path = r'D:\junggeyon_results\pelvic_unpaired_e250_testrlt\test_latest\realMR/'
#image2_path = r'D:\junggeyon_results\pelvic_unpaired_e250_testrlt\test_latest\fakeCT_gray/'
#image3_path = r'D:\junggeyon_results\pelvic_unpaired_e250_testrlt\test_latest\realCT/'
#save_path = r'D:\junggeyon_results\pelvic_unpaired_e250_testrlt\test_latest\threepair/'
image1_path = r"C:\plastimatch_npy2\syncut/"
image2_path = r"C:\plastimatch_npy2\refcut/"
image3_path = r"C:\plastimatch_npy2\defcut/"
#image3_path = r"C:\plastimatch_tester\nomind_bicubic_comset3\def_ref_fusion/"
save_path = r"C:\plastimatch_npy2\mrrefdef_pair/"
img1_list = os.listdir(image1_path)
img2_list = os.listdir(image2_path)
img3_list = os.listdir(image3_path)

assert len(img2_list) == len(img1_list), 'set the fileidx'
for i in range(len(img1_list)):
    
    image1 = Image.open(image1_path + img1_list[i] )
    image2 = Image.open(image2_path + img2_list[i])
    image3 = Image.open(image3_path + img3_list[i])
    
    #image1 = image1.resize((512, 512))
    #image2 = image2.resize((512, 512))
    #image3 = image3.resize((512, 512))
    image1_size = image1.size
    image2_size = image2.size
    image3_size = image3.size
    new_image = Image.new('RGB', (3*image1_size[0], image1_size[1]), (250))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_size[0], 0))
    new_image.paste(image3, (2*image1_size[0], 0))
    new_image.save(save_path + '%s' %img1_list[i][:4] +'_%s_3pair.jpg' %(img1_list[i][:-4].split("slice")[1]), 'JPEG')
    
        