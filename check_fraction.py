import os 
import numpy as np
import matplotlib.pyplot as plt
basepath = r"E:\gangnam_data"
fx_dir_list = os.listdir(basepath)
fraction_cnt_list = []
for i in range(len(fx_dir_list)):
    fx_path = os.path.join(basepath, fx_dir_list[i])
    
    fol_dir_list = os.listdir(fx_path)
    
    fraction_cnt = 0
    
    for j in range(len(fol_dir_list)):
        if "xT" in fol_dir_list[j]:
            fraction_cnt += 1
    if fraction_cnt >= 30:
        print(fx_dir_list[i])
    fraction_cnt_list.append(fraction_cnt)


print(np.median(fraction_cnt_list))
print(np.mean(fraction_cnt_list))
print(np.max(fraction_cnt_list))
print(np.min(fraction_cnt_list))
# x = [i for i in range(len(fraction_cnt_list))]
plt.plot(fraction_cnt_list)
plt.xlabel('Patients', fontsize=10)
plt.ylabel('Fraction', fontsize=10)
# plt.show()
