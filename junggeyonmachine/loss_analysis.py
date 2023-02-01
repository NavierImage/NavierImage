from itertools import cycle
import os
import re
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
loss_txt = pd.read_csv(r"D:\AAAAmrsim\!swinUnetr_who_v4\loss_log.txt", 'r')
loss_arr = np.array(loss_txt)

D_A_loss = [] #3
G_A_loss = [] #4
cycle_A_loss = [] #5
idt_A_loss = [] #6
D_B_loss = [] #7
G_B_loss = [] #8
cycle_B_loss = [] #9
idt_B_loss = [] #10
X = []
for i in range(len(loss_arr)):
    a = loss_arr[i]
    epoch = re.findall(r'\d+', a[0])
    
    temp = re.findall(r'\d+.\d+', a[1])
    if len(temp) != 11:
        temp.insert(0, 123)
        if len(temp)<9:
            continue
    
    D_A_loss.append(float(temp[3]))
    G_A_loss.append(float(temp[4]))
    cycle_A_loss.append(float(temp[5]))
    idt_A_loss.append(float(temp[6]))
    D_B_loss.append(float(temp[7]))
    G_B_loss.append(float(temp[8]))
    cycle_B_loss.append(float(temp[9]))
    idt_B_loss.append(float(temp[10]))

print(np.max(G_A_loss), np.max(G_B_loss), np.max(D_A_loss), np.max(D_B_loss), np.max(cycle_A_loss), np.max(cycle_B_loss), np.max(idt_A_loss), np.max(idt_B_loss))
save_path = r"D:\MRSIM_abdomen_data\result_[720, -100]/"
y_list = []
D_refline = [0.25]
for i in range(0, 11):
    y_list.append(i / 10)
plt.subplots(constrained_layout=True)
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 15 # 개별적용 - plt.yticks(fontsize=20)
plt.rcParams['font.style'] = 'normal'

plt.subplot(2, 4, 1)
plt.plot(G_A_loss)
plt.hlines(0.25, 0, len(G_A_loss), colors="red", linestyles="solid")
plt.hlines(0.251, 0, len(G_A_loss), colors="red", linestyles="solid")
plt.hlines(0.249, 0, len(G_A_loss), colors="red", linestyles="solid")
plt.xticks([0, len(G_A_loss)//6, 2*len(G_A_loss)//6, 3*len(G_A_loss)//6, 4*len(G_A_loss)//6, 5*len(G_A_loss)//6, len(G_A_loss)] , 
            [0, 50, 100, 150, 200, 250, 300])

plt.yticks(y_list)
plt.xlabel("epochs")
plt.ylabel("CT generator loss")
plt.ylim((0, 1))

plt.subplot(2, 4, 2)
plt.plot(G_B_loss)
plt.hlines(0.25, 0, len(G_A_loss), colors="red", linestyles="solid")
plt.hlines(0.251, 0, len(G_A_loss), colors="red", linestyles="solid")
plt.hlines(0.249, 0, len(G_A_loss), colors="red", linestyles="solid")
plt.xticks([0, len(G_B_loss)//6, 2*len(G_B_loss)//6, 3*len(G_B_loss)//6, 4*len(G_B_loss)//6, 5*len(G_B_loss)//6, len(G_B_loss)] , 
            [0, 50, 100, 150, 200, 250, 300])
plt.yticks(y_list)
plt.xlabel("epochs")
plt.ylabel("MR generator loss")
plt.ylim((0, 1))

plt.subplot(2, 4, 3)
plt.plot(D_A_loss)
plt.hlines(0.25, 0, len(G_A_loss), colors="red", linestyles="solid")
plt.hlines(0.251, 0, len(G_A_loss), colors="red", linestyles="solid")
plt.hlines(0.249, 0, len(G_A_loss), colors="red", linestyles="solid")
plt.xticks([0, len(D_A_loss)//6, 2*len(D_A_loss)//6, 3*len(D_A_loss)//6, 4*len(D_A_loss)//6, 5*len(D_A_loss)//6, len(D_A_loss)] , 
            [0, 50, 100, 150, 200, 250, 300])
plt.yticks(y_list)
plt.xlabel("epochs")
plt.ylabel("CT discriminator loss")
plt.ylim((0, 1))

plt.subplot(2, 4, 4)
plt.plot(D_B_loss)
plt.hlines(0.25, 0, len(G_A_loss), colors="red", linestyles="solid")
plt.hlines(0.251, 0, len(G_A_loss), colors="red", linestyles="solid")
plt.hlines(0.249, 0, len(G_A_loss), colors="red", linestyles="solid")
plt.xticks([0, len(D_B_loss)//6, 2*len(D_B_loss)//6, 3*len(D_B_loss)//6, 4*len(D_B_loss)//6, 5*len(D_B_loss)//6, len(D_B_loss)] , 
            [0, 50, 100, 150, 200, 250, 300])
plt.yticks(y_list)
plt.xlabel("epochs")
plt.ylabel("MR discriminator loss")
plt.ylim((0, 1))

plt.subplot(2, 4, 5)
plt.plot(cycle_A_loss)
plt.xticks([0, len(cycle_A_loss)//6, 2*len(cycle_A_loss)//6, 3*len(cycle_A_loss)//6, 4*len(cycle_A_loss)//6, 5*len(cycle_A_loss)//6, len(cycle_A_loss)] , 
            [0, 50, 100, 150, 200, 250, 300])
plt.yticks(y_list)
plt.xlabel("epochs")
plt.ylabel("cyclic MR loss ( rec MR, real MR )")
plt.ylim((0, 1))

plt.subplot(2, 4, 6)
plt.plot(cycle_B_loss)
plt.xticks([0, len(cycle_B_loss)//6, 2*len(cycle_B_loss)//6, 3*len(cycle_B_loss)//6, 4*len(cycle_B_loss)//6, 5*len(cycle_B_loss)//6, len(cycle_B_loss)] , 
            [0, 50, 100, 150, 200, 250, 300])
plt.yticks(y_list)
plt.xlabel("epochs")
plt.ylabel("cyclic CT loss ( rec CT, real CT )")
plt.ylim((0, 1))

plt.subplot(2, 4, 7)
plt.plot(idt_A_loss)
plt.xticks([0, len(idt_A_loss)//6, 2*len(idt_A_loss)//6, 3*len(idt_A_loss)//6, 4*len(idt_A_loss)//6, 5*len(idt_A_loss)//6, len(idt_A_loss)] , 
            [0, 50, 100, 150, 200, 250, 300])
plt.yticks(y_list)
plt.xlabel("epochs")
plt.ylabel("identity CT loss ( real CT in CT generator )")
plt.ylim((0, 1))

plt.subplot(2, 4, 8)
plt.plot(idt_B_loss)
plt.xticks([0, len(idt_B_loss)//6, 2*len(idt_B_loss)//6, 3*len(idt_B_loss)//6, 4*len(idt_B_loss)//6, 5*len(idt_B_loss)//6, len(idt_B_loss)] , 
            [0, 50, 100, 150, 200, 250, 300])
plt.yticks(y_list)
plt.xlabel("epochs")
plt.ylabel("identity MR loss ( real MR in MR generator )")
plt.ylim((0, 1))
#plt.savefig(save_path+"idt_B_loss.png")

#plt.ylim((0, 1))

plt.show()