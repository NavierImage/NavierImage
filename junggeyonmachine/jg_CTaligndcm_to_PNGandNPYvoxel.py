import os
import numpy as np
import pydicom
import skimage
from numpngw import write_png
from PIL import Image

#from PIL import Image #PIL은 8bit image만 다룰수 있음.
#https://stackoverflow.com/questions/62739851/convert-rgb-arrays-to-pil-image
#CT폴더 불러오기
#Contour파일 불러오기
basepath = r'D:\MRSIM_abdomen_data\Patient_data/'
dir_list = os.listdir(basepath)
for i in range(1, 51):    
    if i < 10:number_str = '00' + str(i)
    else: number_str = '0' + str(i)
    
    for patient in dir_list:
        
        if number_str == patient[:3]:
            
            sub_dir_list = os.listdir(basepath + patient)
            
            for ct in sub_dir_list:
                if 'CT_aligned' == ct:
                    sub_sub_dir_list = os.listdir(basepath + patient +'/' + ct)
                    
                    for destination in sub_sub_dir_list:
                        CT_folder_path = basepath + patient + '/' + ct +'/'+destination
                        if 'npy' in CT_folder_path:
                            continue
                        break
            break
            
    def PNGandNPYsave(dir_list, idx, CT_png_voxel, CT_voxel):
        print(np.min(CT_voxel), np.max(CT_voxel))
        
        #np.save(r'D:\junggeyon\pelvic_CT_pic_npy/P%03dCT_pic_volume.npy' %idx, CT_png_voxel)
        #npy_save_path = r'C:\pelvic_unity\npy\CT'
        #print(CT_voxel.dtype)
        #np.save(npy_save_path + "/P%03dCTvolume.npy", CT_voxel)
        pic_save_path = r"D:\DLnetwork\MRSIM_checkpoints_2\results\CT_[-280, 800]"
        CT_png_voxel = CT_png_voxel.astype('float64')
        CT_png_voxel *= 255/65535
        CT_png_voxel = CT_png_voxel.astype('uint8')
        CT_png_voxel_re = skimage.transform.resize(CT_png_voxel, (len(CT_png_voxel), 256, 256))
        CT_png_voxel_re *= 255
        CT_png_voxel_re = CT_png_voxel_re.astype('uint8')
        for i in range(int(CT_png_voxel.shape[0])):
            #if i < 40 and len(CT_png_voxel) > 100:
            #    continue
            CT_pic_img = Image.fromarray(CT_png_voxel_re[i])
            CT_pic_img.save(pic_save_path + "/P%03d_CT_slice%03d[-280, 800].jpg" %(idx, i+1))
            

            #if int(CT_png_voxel.shape[0]) - i == 21 and len(CT_png_voxel) > 100:
            #    break
        

        
    def GetCTinfo(CT_folder_path):
        CT_dcm_files = []
        fileidx = []
        for top, dir, file in os.walk(CT_folder_path):
            for filename in file:
                if filename[-3:] != 'dcm':
                    continue
                temp_ct_slice = pydicom.dcmread(CT_folder_path + '/' + filename)
                CT_dcm_files.append(temp_ct_slice)
                idxnum = temp_ct_slice.InstanceNumber
                fileidx.append(idxnum)
            break

        fileidx = np.array(fileidx)
        fileorder = np.argsort(fileidx)

        sorted_CT_file = []

        for i in range(len(fileidx)):
            sorted_CT_file.append(CT_dcm_files[fileorder[i]])

        return sorted_CT_file, len(fileidx)

    sorted_CT_file, zsize = GetCTinfo(CT_folder_path)
    
    print(len(sorted_CT_file))

    def GetWindowMaxandMin(ct_dicomdata):

        if type(ct_dicomdata.WindowCenter) == pydicom.valuerep.DSfloat:
            window_center = ct_dicomdata.WindowCenter
            window_width = ct_dicomdata.WindowWidth
        else:
            window_center = ct_dicomdata.WindowCenter[0]
            window_width = ct_dicomdata.WindowWidth[0]

        img_max = window_center + window_width // 2
        img_min = window_center - window_width // 2

        return img_max, img_min

    def GetSlopeandIntercept(ct_dicomdata):
        slope = float(ct_dicomdata.RescaleSlope)
        intercept = float(ct_dicomdata.RescaleIntercept)
        return slope, intercept

    def GraytoRGB(arr_slice):
        pixel_rgb = np.stack((arr_slice, )*3, axis = -1)
        return pixel_rgb

    #########window 기본 세팅 - extra_norm = True, 아니면 그냥 False#########
    def MakeCTvoxel(sorted_CT_file, zsize, gray2rgb = 0, extra_norm = True):
        row = sorted_CT_file[0].Rows
        col = sorted_CT_file[0].Columns
        print(row, col)
        if gray2rgb == 1:
            CT_voxel = np.zeros((zsize, row, col, 3), 'int32')
            CT_png_voxel = np.zeros((zsize, row, col, 3), 'int32')
        else:
            CT_voxel = np.zeros((zsize, row, col), 'int32')
            CT_png_voxel = np.zeros((zsize, row, col), 'int32')

        ####Set normalization####
        img_min = -280; img_max = 800
        for i in range(len(sorted_CT_file)):
            ct_dicomdata = sorted_CT_file[i]
            convert_coeff = 2**(ct_dicomdata.BitsAllocated-1)
            slope, intercept = GetSlopeandIntercept(ct_dicomdata)
            
            if extra_norm == False:
                img_max, img_min = GetWindowMaxandMin(ct_dicomdata)
                print(img_max, img_min)
            else:
                assert img_max != None and img_min != None, "You have to set window max and min"

            temp_arr_slice = slope * ct_dicomdata.pixel_array + intercept
            temp_arr_slice = temp_arr_slice.astype('int32')
            CT_voxel[i] = (temp_arr_slice)
            
            temp_arr_slice[temp_arr_slice < img_min] = img_min
            temp_arr_slice[temp_arr_slice > img_max] = img_max

            temp_arr_slice *= round(convert_coeff/(img_max-img_min))
            if gray2rgb == 1:
                CT_png_voxel[i] = GraytoRGB(temp_arr_slice)
            else:
                CT_png_voxel[i] = (temp_arr_slice)
        
        return CT_voxel, CT_png_voxel

    CT_voxel, CT_png_voxel = MakeCTvoxel(sorted_CT_file, zsize)

    def CT_rescaling_to_show(sorted_CT_file, CT_png_voxel):
        convert_coeff = 2**(sorted_CT_file[0].BitsAllocated-1)
        CT_png_voxel += int(convert_coeff) - abs(np.min(CT_png_voxel))
        ### unsigned 16bit ##
        CT_png_voxel = CT_png_voxel.astype('float64')
        min_ = np.min(CT_png_voxel)
        max_ = np.max(CT_png_voxel)
        ### how to CT showing => (bit value) * (value - min)/(max - min)
        CT_png_voxel -= min_
        CT_png_voxel /= (max_ - min_)
        CT_png_voxel *= round(2**sorted_CT_file[0].BitsAllocated-1)
        CT_png_voxel = CT_png_voxel.astype('uint16')

        return CT_png_voxel

    CT_png_voxel = CT_rescaling_to_show(sorted_CT_file, CT_png_voxel)

    PNGandNPYsave(dir_list,i, CT_png_voxel, CT_voxel)