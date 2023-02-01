import os
import numpy as np
import pydicom
import openpyxl
workbook = openpyxl.load_workbook(r"D:\MRSIM_abdomen_data\Patient_data\properties\MRSIM_CT_aligned_dcm_properties.xlsx")
worksheet = workbook['Sheet1']
basepath = r"D:\MRSIM_abdomen_data\Patient_data"
patient_data = os.listdir(basepath)
cont_cnt = 0
noncont_cnt = 0
gastro_cnt = 0
null_cnt = 0
for i in range(len(patient_data)):
    if patient_data[i] == "properties":
        continue
    number_patientID = os.listdir(basepath + "/" + patient_data[i])
    for j in range(len(number_patientID)):
        if number_patientID[j] == "CT":
            moda = number_patientID[j]

    personal = os.listdir(basepath + "/" + patient_data[i] + "/" + moda)
    
    charming_dicom = []
    for j in range(len(personal)):
        find = 0 ##한개만 할수 있도록
        if "npy" in personal[j]:
            continue
        the_path = basepath + "/" + patient_data[i] + "/" + moda + "/" + personal[j]

        dicom = os.listdir(the_path)
        
        for k in range(len(dicom)):
            dicominfo = pydicom.dcmread(the_path + "/" + dicom[k])
            if dicominfo.InstanceNumber == 1:
                #charming_dicom.append(dicominfo)
                #print(dicominfo.StudyDescription)
                #print(dicominfo.PixelSpacing[0], dicominfo.PixelSpacing[1])
                #print(dicominfo.SliceThickness)
                #print(dicominfo.ManufacturerModelName)
                #print(dicominfo.PatientID)
                #print(dicominfo.ScanOptions)
                #print(dicominfo.ProtocolName)
                #print(patient_data[i])
                #print(dicominfo.Rows, dicominfo.Columns)
                find = 1
                break
        if find: break
    if "non" in dicominfo.StudyDescription:
        cont = "Non-contrast"
        noncont_cnt += 1
    elif "Gastrografin" in dicominfo.StudyDescription:
        cont = "Gastrografin"
        cont_cnt += 1
    elif "Contrast" in dicominfo.StudyDescription:
        cont_cnt += 1
        cont = "Contrast"
    else:
        cont = "null"
        null_cnt += 1

    worksheet[chr(65)+"%d" %(i+2)] = patient_data[i]
    worksheet[chr(66)+"%d" %(i+2)] = dicominfo.StudyDate
    worksheet[chr(67)+"%d" %(i+2)] = dicominfo.StudyDescription
    worksheet[chr(68)+"%d" %(i+2)] = dicominfo.SeriesDescription
    worksheet[chr(69)+"%d" %(i+2)] = cont
    worksheet[chr(70)+"%d" %(i+2)] = dicominfo.PatientSex
    worksheet[chr(71)+"%d" %(i+2)] = dicominfo.ManufacturerModelName
    worksheet[chr(72)+"%d" %(i+2)] = dicominfo.ScanOptions
    worksheet[chr(73)+"%d" %(i+2)] = dicominfo.KVP
    worksheet[chr(74)+"%d" %(i+2)] = dicominfo.ProtocolName
    worksheet[chr(75)+"%d" %(i+2)] = dicominfo.Rows
    worksheet[chr(76)+"%d" %(i+2)] = dicominfo.Columns
    ps1 = dicominfo.PixelSpacing[0]
    ps2 = dicominfo.PixelSpacing[1]
    worksheet[chr(77)+"%d" %(i+2)] = f'{ps1:.6f}'
    worksheet[chr(78)+"%d" %(i+2)] = f'{ps2:.6f}'
    worksheet[chr(79)+"%d" %(i+2)] = dicominfo.SliceThickness

worksheet[chr(65)+"%d" %1] = "Patients"
worksheet[chr(66)+"%d" %1] = "StudyDate"
worksheet[chr(67)+"%d" %1] = "StudyDescription"
worksheet[chr(68)+"%d" %1] = "SeriesDescription"
worksheet[chr(69)+"%d" %1] = "Contrast"
worksheet[chr(70)+"%d" %1] = "PatientSex"
worksheet[chr(71)+"%d" %1] = "ManufacturerModelName"
worksheet[chr(72)+"%d" %1] = "ScanOptions"
worksheet[chr(73)+"%d" %1] = "KVP"
worksheet[chr(74)+"%d" %1] = "ProtocolName"
worksheet[chr(75)+"%d" %1] = "Rows"
worksheet[chr(76)+"%d" %1] = "Columns"
worksheet[chr(77)+"%d" %1] = "PixelSpacing[0](X)"
worksheet[chr(78)+"%d" %1] = "PixelSpacing[1](Y)"
worksheet[chr(79)+"%d" %1] = "SliceThickness(Z)"
workbook.save(r"D:\MRSIM_abdomen_data\Patient_data\properties\MRSIM_CT_aligned_dcm_properties.xlsx")

print(cont_cnt, noncont_cnt, null_cnt)