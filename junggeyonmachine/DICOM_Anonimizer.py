import os
import pydicom
from tqdm import tqdm
import time
 
# get dcm_file_list
def get_file_list(dcm_paths) :
    try :
        list_path = []
        list_file = []
        list_full = []   
        
        for (path, _, file) in os.walk(dcm_paths):
            for each_file in file:
                if each_file[-4:] == '.dcm':
                    list_path.append(path)    
                    list_file.append(each_file)
                    list_full.append(os.path.join(os.getcwd(),path,each_file))
        return list_full
    except : 
        return 'get_file_list error.'    
 
 
# de-identifier for multi
def de_identifier_for_multi(filename):
    try:
        Metadata = pydicom.filereader.dcmread(str(filename))
    except: return 'de_identifier // file reading error. '
    try:            
        # de-identify
        Metadata.PatientName = ''
        Metadata.PatientBirthDate = ''
        Metadata.PatientSex = ''
        Metadata.OtherPatientIDs = ''
        Metadata.PatientAge = ''
        Metadata.RequestingPhysician = ''
        Metadata.InstitutionName = ''
        Metadata.InstitutionAddress = ''
        Metadata.ReferringPhysicianName = ''
        Metadata.StationName = ''
        Metadata.PhysiciansofRecord = ''
 
        Metadata.save_as(str(filename))
 
            # TODO - revive
            # sql_query(True)  
 
    except:            
 
            # TODO - revive
            # sql_query(False)  
            return 'de_identifier error'

f_list = get_file_list(r"D:\!Oncosoft\!MRprostate_anon")
for idx, filename in enumerate(f_list):
    de_identifier_for_multi(filename)
