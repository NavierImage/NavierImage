import os
from PIL import Image

image_path = r'C:\Users\Desktop\Downloads\mri2ct_200epoch_abdomenYH_first\samples_testing_valid\B2A'
img_list = os.listdir(image_path)

for img in img_list:
    image = Image.open(image_path + '/' + img)
    crop_image = image.crop((0, 0, 256, 256))
    crop_image.save(r'C:\Users\Desktop\Downloads\mri2ct_200epoch_abdomenYH_first\samples_testing_valid\realCT/realCT' + img)
    