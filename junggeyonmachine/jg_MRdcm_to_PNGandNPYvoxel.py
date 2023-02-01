import os
import numpy as np
import pydicom
from numpngw import write_png
from PIL import Image
import matplotlib.pyplot as plt
###for 16bit image
basepath = r'D:\MRSIM_abdomen_data\Patient_data/'
dir_list = os.listdir(basepath)
for i in range(1, 51):    
    if i < 10:number_str = '00' + str(i)
    else: number_str = '0' + str(i)
    
    for patient in dir_list:
        if number_str == patient[:3]:
            print(patient)
            sub_dir_list = os.listdir(basepath + patient)
            
            for mr in sub_dir_list:
                if 'MR' == mr:
                    sub_sub_dir_list = os.listdir(basepath + patient +'/' + mr)
                    for destination in sub_sub_dir_list:
                        if destination[-3:] != 'npy':
                            MR_folder_path = basepath + patient + '/' + mr +'/'+destination
                            break
            break
            
    def PNGandNPYsave(dir_list, idx, MR_voxel):
        save_path = r'D:\MRSIM_abdomen_data\npy\MR'
        np.save(r'D:\MRSIM_abdomen_data\npy\MR\P%03d_MR_volume.npy' %idx, MR_voxel)
        
        
        #pic_save_path = r'D:\junggeyon\pelvic_MR_pic'
        #MR_png_voxel = MR_png_voxel.astype('float64')
        #MR_png_voxel *= 255/65535
        #MR_png_voxel = MR_png_voxel.astype('uint8')
        #for i in range(int(MR_png_voxel.shape[0])):
        #    MR_pic_img = Image.fromarray(MR_png_voxel[i])
        #    MR_pic_img.save(pic_save_path + "/P%03dMR_slice%03d.jpg" %(idx, i+1))

    def GetMRinfo(MR_folder_path):
        MR_dcm_files = []
        fileidx = []
        for top, dir, file in os.walk(MR_folder_path):
            for filename in file:
                if filename[-3:] != 'dcm':
                    continue
                temp_mr_slice = pydicom.dcmread(MR_folder_path + '/' + filename)
                MR_dcm_files.append(temp_mr_slice)
                idxnum = temp_mr_slice.InstanceNumber
                fileidx.append(idxnum)
            break

        fileidx = np.array(fileidx)
        fileorder = np.argsort(fileidx)

        sorted_MR_file = []

        for i in range(len(fileidx)):
            sorted_MR_file.append(MR_dcm_files[fileorder[i]])

        return sorted_MR_file, len(fileidx)

    sorted_MR_file, zsize = GetMRinfo(MR_folder_path)

    def GetSlopeandIntercept(mr_dicomdata):
        slope = float(mr_dicomdata.RealWorldValueMappingSequence[0].RealWorldValueSlope)
        intercept = float(mr_dicomdata.RealWorldValueMappingSequence[0].RealWorldValueIntercept)
        return slope, intercept

    def GetWindowMaxandMin(mr_dicomdata):

        if type(mr_dicomdata.WindowCenter) == pydicom.valuerep.DSfloat:
            window_center = mr_dicomdata.WindowCenter
            window_width = mr_dicomdata.WindowWidth
        else:
            window_center = mr_dicomdata.WindowCenter[0]
            window_width = mr_dicomdata.WindowWidth[0]
        img_max = window_center + window_width / 2
        img_min = window_center - window_width / 2
        return img_max, img_min

    def GraytoRGB(arr_slice):
        pixel_rgb = np.stack((arr_slice, )*3, axis = -1)
        return pixel_rgb

    def MakeMRvoxel(sorted_MR_file, zsize, gray2rgb = 0):
        column = sorted_MR_file[0].Columns
        row = sorted_MR_file[0].Rows
        if gray2rgb == 1:
            MR_voxel = np.zeros((zsize, row, column, 3), 'float64')
            MR_png_voxel = np.zeros((zsize, row, column, 3), 'float64')
        else:
            MR_voxel = np.zeros((zsize, row, column), 'float64')
            MR_png_voxel = np.zeros((zsize, row, column), 'float64')

        for i in range(len(sorted_MR_file)):
            mr_dicomdata = sorted_MR_file[i]
            #slope, intercept = GetSlopeandIntercept(mr_dicomdata)
            
            temp_arr_slice = mr_dicomdata.pixel_array
            
            MR_voxel[i] = temp_arr_slice
            
            if gray2rgb == 1:
                MR_png_voxel[i] = GraytoRGB(temp_arr_slice)
            else:
                MR_png_voxel[i] = temp_arr_slice

        return MR_voxel, MR_png_voxel

    MR_voxel, MR_png_voxel = MakeMRvoxel(sorted_MR_file, zsize)

    def RefineMRvoxel(MR_voxel):
        print(np.min(MR_voxel))
        print(np.max(MR_voxel))
        MR_voxel = MR_voxel.astype('uint16')

        return MR_voxel

    

    def MR_rescaling_to_show(sorted_MR_file, MR_png_voxel):
        min_ = np.min(MR_png_voxel)
        max_ = np.max(MR_png_voxel)
        mr_dicom_firstdata = sorted_MR_file[0]
        try:
            slope, intercept = GetSlopeandIntercept(mr_dicom_firstdata) 
        except:
            slope = 1; intercept = 0
        print(slope, intercept)
        ##windowing section##
        window_high, window_low = GetWindowMaxandMin(mr_dicom_firstdata)
        MR_png_voxel = np.where(MR_png_voxel >= window_high, window_high, MR_png_voxel)
        MR_png_voxel = np.where(MR_png_voxel <= window_low, window_low, MR_png_voxel)
        MR_png_voxel *= slope
        MR_png_voxel += intercept
        MR_png_voxel = MR_png_voxel.astype('float64')
        #MR_png_voxel -= min_
        #MR_png_voxel /= max_ - min_
        #MR_png_voxel *= 2**16-1
        ##rescaling section##
        min_ = np.min(MR_png_voxel)
        max_ = np.max(MR_png_voxel)
        MR_png_voxel -= min_
        MR_png_voxel /= max_ - min_
        MR_png_voxel *= 2**16-1
        MR_png_voxel = MR_png_voxel.astype('uint16')
        print(np.max(MR_png_voxel), np.min(MR_png_voxel))
        return MR_png_voxel

    
    #MR_png_voxel = MR_rescaling_to_show(sorted_MR_file, MR_png_voxel)
    MR_voxel = RefineMRvoxel(MR_voxel)
    PNGandNPYsave(dir_list, i, MR_voxel)