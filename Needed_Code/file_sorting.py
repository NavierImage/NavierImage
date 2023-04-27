import os 
import shutil
bp = r"D:\junggeyon\junggeyon_additional_data"
sub_p = os.listdir(bp)
pa_num_dict = {}
for sp in range(len(sub_p)):
    patient_path = os.listdir(os.path.join(bp, sub_p[sp]))
    for idx in range(len(patient_path)):
        pa_list = patient_path[idx].split("_")
        pa_num_dict[str(pa_list[1])] = 1

ct_bp = r"D:\junggeyon\junggeyon_additional_data_CT"

sub_p = os.listdir(ct_bp)
pa_num_list = []
done = []
for sp in range(len(sub_p)):
    t1 = os.path.join(ct_bp, sub_p[sp])
    patient_path = os.listdir(t1)
    for idx in range(len(patient_path)):
        pa_list = patient_path[idx].split("_")
        t2 = os.path.join(t1, patient_path[idx])
        try:
            pa_num_dict[pa_list[1]]
            done.append(pa_list[1])
            shutil.copytree(t2, r"D:\junggeyon\!!!JG_newCT/" + patient_path[idx])
        except:
            pass