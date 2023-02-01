import os
import numpy as np

path = r'D:\junggeyon\Unity\Unity CT MR registered\raw\PN 07'
file_list = os.listdir(path)

first = -1
mr_volume = np.zeros((300, 512, 512))
for i in range(len(file_list)):
    if file_list[i][-3:] == 'npy' and 'MR' in file_list[i]:
        first += 1
        mr_slice = np.load(path + '/'+ file_list[i])
        mr_volume[first] = mr_slice
mr_volume = mr_volume.astype('uint16')
print(mr_volume.shape)
np.save('D:/mr7unityvolume.npy', mr_volume)