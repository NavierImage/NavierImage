"edge detection"
import os
import numpy as np
from skimage import filters
from PIL import Image
import scipy

ct_img_path = r'D:\CT_norm_im/'
mr_img_path = r'D:\MR_norm_im/'
ct_save_path = r'D:\CT_norm_im_edge/'
mr_save_path = r'D:\MR_norm_im_edge/'

ct_img_list = os.listdir(ct_img_path)
mr_img_list = os.listdir(mr_img_path)

assert len(ct_img_list) == len(mr_img_list), 'set the fileidx'
for idx in range(len(ct_img_list)):
    ct_img = Image.open(ct_img_path + ct_img_list[idx])
    mr_img = Image.open(mr_img_path + mr_img_list[idx])
    ct_arr = np.array(ct_img)
    mr_arr= np.array(mr_img)
    ct_edge = filters.sobel(ct_arr) * 255
    mr_edge = filters.sobel(mr_arr) * 255

    ct_edge = ct_edge.astype('uint8')
    mr_edge = mr_edge.astype('uint8')
    
    #ct_threshold = filters.threshold_otsu(ct_edge, nbins = 256, hist =None)
    #mr_threshold = filters.threshold_otsu(mr_edge, nbins = 256, hist =None)
    block_size_ct= 205
    block_size_mr = 155
    #ct_local_thresh = filters.threshold_local(ct_edge, block_size_ct, offset = 0, mode = 'wrap')
    #mr_local_thresh = filters.threshold_local(mr_edge, block_size_mr, offset = 0, mode ='wrap')
    
    #print(np.min(ct_local_thresh), np.max(ct_local_thresh))
    #ct_edge = np.where(ct_edge > ct_threshold, 255, 0)
    #mr_edge = np.where(mr_edge > mr_threshold, 255, 0)

    #ct_edge = np.where(ct_edge > ct_local_thresh, 255, 0)
    #mr_edge = np.where(mr_edge > mr_local_thresh, 255, 0)

    ct_edge = ct_edge.astype('uint8')
    mr_edge = mr_edge.astype('uint8')
    ct_edge_img = Image.fromarray(ct_edge)
    mr_edge_img = Image.fromarray(mr_edge)
    
    ct_edge_img.save(ct_save_path + ct_img_list[idx][:4] +'CTedge_slice' + ct_img_list[idx][-8:-5] +'.jpg')
    mr_edge_img.save(mr_save_path + mr_img_list[idx][:4] +'MRedge_slice' + mr_img_list[idx][-7:-4] + '.jpg')