import shutil
import os
file_source = r'D:\DLnetwork\traindata_MRSIM_windowed_2\CT_window_manipulate2_256[600, -160]/'
file_destination = r'D:\DLnetwork\traindata_MRSIM_windowed_2\testB/'

get_files = os.listdir(file_source)

for name in get_files:
    if 'P002' in name or 'P003' in name or 'P015' in name or 'P019' in name or 'P021' in name or 'P027' in name or 'P028' in name or 'P031' in name or 'P037' in name or 'P042' in name:
        shutil.move(file_source + name, file_destination)