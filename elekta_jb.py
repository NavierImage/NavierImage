import os
import re
import random
import numpy as np
import pydicom
from skimage.draw import line as lin




    
def contour_info_from_elekta(pt_dir):
    contournames_path = os.path.join(pt_dir, "contournames")
    contour_dict = get_contournames_info(contournames_path)
    # contour_dict = {"test" : 9}
    
    color_dict = {}
    for key, val in contour_dict.items():
        color_dict[int(val)] = rand_color_generator()
    
    dcm_fol_path = os.path.join(pt_dir, "DCMData")
    
    file_list = os.listdir(pt_dir)


    wc_file_sort_list = []
    for i in range(len(file_list)):
        if file_list[i][-2:] == "WC":
            
            wc_file_path = os.path.join(pt_dir, file_list[i])
            with open(wc_file_path, "r") as wc_file:
                wc_file_readlines = wc_file.readlines()
            
            wc_file_z_coord = re.sub("\n", "", wc_file_readlines[5].split(",")[2])
            wc_file_z_coord=  float(wc_file_z_coord)
            wc_file_sort_list.append((file_list[i], wc_file_z_coord))
            
    wc_file_sort_list.sort(key=lambda x: x[1])
    
    dcm_list = ct_dcm_data(dcm_fol_path)
    assert len(dcm_list) == len(wc_file_sort_list), "match file size"
    
    ct_3d_arr = get_dcm_3d_arr(dcm_list)
    
    ##visualization##
    win_min = np.min(ct_3d_arr)
    win_max = np.max(ct_3d_arr) * 0.01
    
    ct_3d_arr[ct_3d_arr > win_max] = win_max
    ct_3d_arr[ct_3d_arr < win_min] = win_min
    ct_3d_arr = 255 * (ct_3d_arr - win_min)/(win_max - win_min)
    ct_3d_arr = ct_3d_arr.astype('uint8')
    ct_3d_arr = np.stack((ct_3d_arr, ) * 3 , axis = -1)
    
    for i in range(len(dcm_list)):
        coord_dict = transfer_pixelspace_contouring(dcm_list[i][0], os.path.join(pt_dir, wc_file_sort_list[i][0]), contour_dict)
        for key, val in coord_dict.items():
            if np.all(val) == None:
                continue
            color = color_dict[key]
            for j in range(len(val)-1):
                x1 = val[j][0]
                y1 = val[j][1]
                x2 = val[j+1][0]
                y2 = val[j+1][1]
                ry, cx = lin(y1, x1, y2, x2)
                ct_3d_arr[i, ry, cx] = color
            ry,cx = lin(y2, x2, val[0][1], val[0][0])
            ct_3d_arr[i, ry, cx] = color
            
    from PIL import Image
    for i in range(len(ct_3d_arr)):
        img = Image.fromarray(ct_3d_arr[i])
        img.save(r"D:\!JUNG_newdata_prostate\img/%d.png" %i)
    
def get_contournames_info(contournames_path):
    with open(contournames_path, "r") as contournames:
        cnames_line_list = contournames.readlines()
    
    contour_dict = {}
    for idx, line in enumerate(cnames_line_list):
        line_str = line
        if "\n" in line_str:
            line_str = re.sub("\n", "", line_str)
        
        if line_str.isspace(): # space
            continue 
        elif line_str == "": # null
            continue
        
        number_det = re.findall(r"\d+", line_str) #Zn case except ex) Z8, Z1 ...
        check = 0
        if len(number_det) > 0:
            pass
        elif "gtv" in line_str.lower():
            check = 1
        else:
            if   line_str.lower() == "imported":
                pass
            elif line_str.lower() == "mrlcouch":
                pass
            elif line_str.lower() == "study ct":
                pass
            elif line_str.lower() == "mm":
                pass
            elif line_str.lower() == "patient":
                pass
            elif line_str.lower() == "general":
                pass
            elif line_str.lower() == "isocenter":
                pass
            else:
                check = 1
                
        
        if check == 1 and idx != len(cnames_line_list) -1:
            next_line = cnames_line_list[idx+1]
            contour_dict[line_str.lower()] = next_line.split(",")[0]
    return contour_dict

    

def transfer_pixelspace_contouring(dcm, wc_file_path, contour_dict):
    with open(wc_file_path, "r") as wc_file:
        wc_file_readlines = wc_file.readlines()
    #start index is 7
    idx = 7
    # translation_arr = np.array([float(wc_file_readlines[4].split(",")[0]), float(wc_file_readlines[4].split(",")[1])])
    # elekta_orientation_arr = np.array([float(wc_file_readlines[6].split(",")[0:3]), float(wc_file_readlines[6].split(",")[3:6])])
    
    origin_arr = np.array(dcm.ImagePositionPatient[:2])
    
    
    # spacing = dcm.PixelSpacing
    spacing_arr = np.array(dcm.PixelSpacing)
    
    coord_dict = {}
    for key, val in contour_dict.items():
        coord_dict[int(val)] = None
    
    while idx < len(wc_file_readlines):
        ctr_meta_coord = wc_file_readlines[idx]
        ctr_meta = wc_file_readlines[idx+1]
        if "\n" in ctr_meta_coord:
            ctr_meta_coord = re.sub("\n", "", ctr_meta_coord)
            ctr_meta = re.sub("\n", "", ctr_meta)
        
        if ctr_meta_coord == "isocenter":
            break
        
        ctr_coord_amount = int(ctr_meta_coord)
        ctr_target = int(ctr_meta)
        
        if ctr_coord_amount == 0 and ctr_target == 0: #NEED TO CHECK
            break
        
        ctr_coord_start_idx = idx + 2
        
        # 5 set unit
        length = ctr_coord_amount // 5
        if ctr_coord_amount % 5 != 0:
            length += 1
        
        if ctr_target not in coord_dict:
            idx = idx + length + 2
            continue
        
        
        ctr_coord_list = []
        for ctr_line_idx in range(ctr_coord_start_idx, ctr_coord_start_idx + length):
            ctr_line =re.sub("\n", "",  wc_file_readlines[ctr_line_idx])
            ctr_line_list = ctr_line.split(",")
            temp_ctr_coord_list = [float(i) for i in ctr_line_list]
            ctr_coord_list.extend(temp_ctr_coord_list)
        ctr_coord_arr = np.array(ctr_coord_list)
        ctr_coord_arr = np.reshape(ctr_coord_arr, (len(ctr_coord_arr)//2, 2))
        #all???
        # if elekta_orientation_arr[0][1] == 1.0:
        ctr_coord_arr[:, 1] *= -1
        
        ctr_pixcd_arr = (ctr_coord_arr - origin_arr) /spacing_arr 
        
        ctr_pixcd_arr_int = ctr_pixcd_arr.astype("int32")
        ctr_pixcd_arr_int = ctr_pixcd_arr_int.astype("float64")
        ctr_pixcd_arr_alpha = ctr_pixcd_arr - ctr_pixcd_arr_int
        ctr_pixcd_arr_alpha[ctr_pixcd_arr_alpha >= 0.5] = 1
        ctr_pixcd_arr_alpha[ctr_pixcd_arr_alpha <0.5] = 0
        ctr_pixcd_arr_int += ctr_pixcd_arr_alpha
        ctr_pixcd_arr_int = ctr_pixcd_arr_int.astype("int32")
        coord_dict[ctr_target] = ctr_pixcd_arr_int
        
        idx = idx + length + 2
        
    return coord_dict
    
    
def ct_dcm_data(dcm_dir):
    dcm_fol_list = os.listdir(dcm_dir)
    dcm_list = []
    for idx, dcm_path in enumerate(dcm_fol_list):
        dcm_path_ = os.path.join(dcm_dir, dcm_path)
        dcm = pydicom.dcmread(dcm_path_, force=True)
        dcm.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
        dcm_list.append((dcm, dcm.ImagePositionPatient[2]))
    dcm_list.sort(key=lambda x:x[1])
    
    return dcm_list

def get_dcm_3d_arr(dcm_list):
    arr_list = []
    for i, dcm in enumerate(dcm_list):
        dcm_slice = dcm[0].pixel_array * dcm[0].RescaleSlope + dcm[0].RescaleIntercept
        arr_list.append(dcm_slice)
    dcm_3d_arr = np.array(arr_list)
    return dcm_3d_arr

def rand_color_generator():
    rand_color = [random.randrange(100, 256), random.randrange(100, 256), random.randrange(100, 256)]
    return rand_color

# contour_info_from_elekta(pt_dir)
    

ct_path = r"D:\!JUNG_newdata_T23D_mr\abdomenCT1"
ct_list = os.listdir(ct_path)
for i in range(len(ct_list)):
    pt_dir = os.path.join(ct_path, ct_list[i])
    contour_info_from_elekta(pt_dir)