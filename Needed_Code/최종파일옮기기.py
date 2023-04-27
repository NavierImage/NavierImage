import os 
import shutil
bp = r"D:\junggeyon\!!!JG_new_CT_3.0"
patient_path = os.listdir(bp)
pa_num_dict = {}
for sp in range(len(patient_path)):
    # patient_path = os.listdir(os.path.join(bp, patient_path[sp]))
    pa_list = patient_path[sp].split("_")
    pa_num_dict[str(pa_list[1])] = 1

bp2 = r"D:\junggeyon\!!!JG_new_MR"
patient_path = os.listdir(bp2)

for sp in range(len(patient_path)):
    # patient_path = os.listdir(os.path.join(bp, patient_path[sp]))
    pa_list = patient_path[sp].split("_")
    
    try:
        
        pa_num_dict[str(pa_list[1])]
        print("ya")
        shutil.copytree(os.path.join(bp2, patient_path[sp]), r"D:\junggeyon\!!!JG_new_MR_3.0/" + patient_path[sp])
    except:
        pass