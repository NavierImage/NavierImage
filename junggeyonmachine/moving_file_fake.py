import shutil
import os
file_source = r"D:\DLnetwork\MRSIM_windowed_checkpoints\results\MRSIM_CT_con_MR_non_v1\test_latest\images/"
file_destination = r"D:\DLnetwork\MRSIM_windowed_checkpoints\results\MRSIM_CT_con_MR_non_V1\test_latest\fakeCT/"

get_files = os.listdir(file_source)

for name in get_files:
    if 'fake' in name:
        shutil.move(file_source + name, file_destination)
