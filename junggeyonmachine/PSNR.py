import os 
import numpy as np
from PIL import Image
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import skimage
import math


total_mae_list = []
total_mse_list = []
total_psnr_list = []
image1_path = r"C:\plastimatch_tester\deformed"
image2_path = r"C:\plastimatch_tester\syned"
#image1_path = r'D:\junggeyon\pelvic_unpaired_e250_valrlt\test_latest\fakeCT'
#image2_path = r'D:\junggeyon\pelvic_val'

#image1_path = r'D:\mrsim_cycleGAN\mrsim_ct'
#image2_path = r'D:\mrsim_cycleGAN\mrsim_real_ct'

image1_list = os.listdir(image1_path)
image2_list = os.listdir(image2_path)

assert len(image1_list) == len(image2_list), "파일 갯수 같아야"

def compute_psnr(img1, img2):
    img1 = img1.astype(np.float64) / 255.
    img2 = img2.astype(np.float64) / 255.
    mse = np.mean((img1 - img2) ** 2)
    print(mse)
    if mse == 0:
        return "Same Image"
    return 10 * math.log10(1. / mse)
hu_value = 760/255
for idx in range(len(image1_list)):
    img1 = Image.open(image1_path + '/' + image1_list[idx])
    img2 = Image.open(image2_path + '/' + image2_list[idx])
    
    
    imarr1 = np.array(img1)
    #imarr1_gray = imarr1[:, :, 0]
    #imarr1_gray = np.squeeze(imarr1_gray)
    #gray = Image.fromarray(imarr1_gray)
    #gray.save(r"D:\junggeyon_results\pelvic_unpaired_e250_testrlt\test_latest\fakeCT_gray/" + image1_list[idx][:-3] + 'jpg')
    imarr2 = np.array(img2)
    
    #imarr1_gray = imarr1_gray.astype("float64")
    imarr2 = imarr2.astype("float64")

    MAE = mean_absolute_error(imarr2, imarr1)
    print(MAE)
    #MSE = mean_squared_error(imarr2, imarr1_gray)
    PSNR = skimage.metrics.peak_signal_noise_ratio(imarr2, imarr1, data_range = 255)
    
    total_mae_list.append(MAE * hu_value)
    #total_mse_list.append(MSE)
    total_psnr_list.append(PSNR)


print("mean mae: %f" %(np.mean(total_mae_list)))
print("std mae: %f" %(np.std(total_mae_list) * hu_value))
print("median mae:%f" %(np.median(total_mae_list) * hu_value))
print("max mae: %f" %(np.max(total_mae_list) * hu_value))
print("min mae: %f" %(np.min(total_mae_list) * hu_value))
print()
#print("mean mse: %f" %(np.mean(total_mse_list)))
#print("std mse: %f" %(np.std(total_mse_list)))
#print("median mse:%f" %(np.median(total_mse_list)))
#print()
print("mean psnr: %f" %(np.mean(total_psnr_list)))
print("std psnr: %f" %(np.std(total_psnr_list)))
print("median psnr:%f" %(np.median(total_psnr_list)))
print("max psnr: %f" %(np.max(total_psnr_list)))
print("min psnr: %f" %(np.min(total_psnr_list)))