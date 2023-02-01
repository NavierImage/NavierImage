import os
from PIL import Image

de_list = os.listdir(r"C:\plastimatch_tester\deformed")
sy_list = os.listdir(r"C:\plastimatch_tester\syned")

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


for i in range(len(de_list)):
    #try:
    image1 = Image.open(r"C:\plastimatch_tester\deformed" +'/' + de_list[i])
    image2 = Image.open(r"C:\plastimatch_tester\syned" +'/' + sy_list[i])
    
    image1_size = image1.size
    image2_size = image2.size
    
    new_image = Image.new("RGB", (2*image1_size[0], image1_size[1]))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_size[0], 0))
    
    new_image.save(r"C:\plastimatch_tester\pair\%d.jpg" %(i), 'JPEG')
    #except:
    #    break