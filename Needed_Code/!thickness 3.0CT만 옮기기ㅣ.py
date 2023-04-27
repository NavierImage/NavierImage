import os 
import shutil
bp = r"D:\junggeyon\!!!JG_newCT"
dest_bp = r"D:\junggeyon\!!!JG_new_CT_3.0"
sub_p = os.listdir(bp)

idx = 0
for sp in range(len(sub_p)):
    folder_name = sub_p[sp]
    if "Body.3.0" in folder_name and "00000" in folder_name:
        idx += 1
        shutil.copytree(os.path.join(bp, folder_name), os.path.join(dest_bp, folder_name))
        
        print(folder_name)
print(idx)
        