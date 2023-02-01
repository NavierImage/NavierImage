import os
path1 = r"D:\DLnetwork\traindata_MRSIM_windowed\trainA"
path2 = r"D:\DLnetwork\traindata_MRSIM_windowed_2\trainA"
img_list1 = os.listdir(path1)
img_list2 = os.listdir(path2)

standard1 = "P001"
standard2 = "P001"
a = []
b = []
cnt1= 0;cnt2=0
iter = len(img_list1)
if iter > len(img_list2):
    iter = len(img_list2)
for i in range(iter):
    if img_list1[i][:4] != standard1:
        standard1= img_list1[i][:4]
        a.append((img_list1[i-1][:4], cnt1))
        cnt1= 0
    if img_list2[i][:4] != standard2:
        standard2= img_list2[i][:4]
        b.append((img_list2[i-1][:4], cnt2))
        cnt2= 0
    cnt1 += 1
    cnt2 += 1
print(a)
print(b)
print(sum(a), sum(b))