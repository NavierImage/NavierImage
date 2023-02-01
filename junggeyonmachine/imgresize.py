from unittest import TestResult
import numpy as np
from PIL import Image
from skimage.transform import rescale, resize, downscale_local_mean

pic1_path = r"C:\Users\Desktop\Desktop\대한방사선종양학회증빙\IMG_4450.JPG"
pic2_path = r"C:\Users\Desktop\Desktop\대한방사선종양학회증빙\IMG_4451.JPG"

pic1 = Image.open(pic1_path)
pic2 = Image.open(pic2_path)
arr1 = np.array(pic1)
arr2 = np.array(pic2)
pic1_resized = resize(arr1, (arr1.shape[0] // 4 , arr1.shape[1] //4 ), anti_aliasing = TestResult)
pic2_resized = resize(arr2, (arr1.shape[0] // 4, arr1.shape[1] //4 ), anti_aliasing = TestResult)

pic1_resized *= 255
pic2_resized *= 255
pic1_resized = pic1_resized.astype('uint8')
pic2_resized = pic2_resized.astype('uint8')

img1 = Image.fromarray(pic1_resized)
img2 = Image.fromarray(pic2_resized)

img1.save(r"C:\Users\Desktop\Desktop\대한방사선종양학회증빙/img1.jpg")
img2.save(r"C:\Users\Desktop\Desktop\대한방사선종양학회증빙/img2.jpg")