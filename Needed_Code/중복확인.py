import os 
import shutil
bp = r"D:\junggeyon\!!!JG_new_CT_3.0"
patient_path = os.listdir(bp)
pa_num_dict = {}
for sp in range(len(patient_path)):
    # patient_path = os.listdir(os.path.join(bp, patient_path[sp]))
    pa_list = patient_path[sp].split("_")
    try:
        pa_num_dict[str(pa_list[1])]
        shutil.move(os.path.join(bp, patient_path[sp]), os.path.join(r"D:\junggeyon\!!!JG_new_CT_3.0_중복", patient_path[sp]))
    except:
        pa_num_dict[str(pa_list[1])] = 1

