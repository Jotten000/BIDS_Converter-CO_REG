
def getIfAccept(mod):
    """input dicom-objekt, returnerar True/False ifall avbildningen ska vara 
    med i BIDS-datan"""
   
    imagetypes = ['SCREEN SAVE','ACMAP','DIXON']
    seriesdescs = ['UNIVERSAL','SEGMENTATION','PETMR','ORIG']
    protcnames = ['DTI FA','IMAGE QC']
        
    if not getNotInkl(imagetypes,'ImageType',mod):
        return False
    if not getNotInkl(seriesdescs,'SeriesDescription',mod):
        return False
    if not getNotInkl(protcnames,'ProtocolName',mod):
        return False
    
    needforpet = ['NAC','MAC']
    if 'PT' in mod.Modality and getNotInkl(needforpet,'SeriesDescription',mod):
        return False
    
    return True
    
def getNotInkl(thelist,place,mod):
    """privat modul, ge lista m. strings, string för dicom-element, dicom 
    objekt, returnerar True om ingen del i listan finns i dicom-elementet"""
    if place in mod:
        for i in thelist:
            if i in str(mod.data_element(place)).upper():
                return False
    return True

def getMod(mod=0):
    """input dicom-objekt, output str() vilken modalitet, ifall inget 
    input-argument returneras lista m. alla giltiga modaliteter"""

    if mod == 0 : 
        return (["pet","T1w","T2w","FLAIR","asl","dsc","dce","dwi","swi",
                 "cbf","cbv","svs","mrsi"])
    
    if not getIfAccept(mod):
        return "ERROR"
    
    # PET
    if getIfIn('PT',mod,publ='Modality'):
        return "pet"
    # CBF, rCBF, rCBV
    if (getIfIn('CBF',mod,publ='SeriesDescription') 
        and getIfIn('ASL',mod,priv='0x0019109C') 
        or getIfIn('RCBF',mod,publ='SeriesDescription')):
        return "cbf"
    if getIfIn('RCBV',mod,publ='SeriesDescription'):
        return "cbv"
    # ASL
    if (getIfIn('ASL',mod,publ='ImageType') 
        and getIfIn('ASL',mod,priv='0x0019109C')):
        return "asl"
    # DSC
    if (getIfIn('PERFUSION',mod,publ='SeriesDescription') 
        and getIfIn('Y',mod,publ='ContrastBolusAgent')):
        return "dsc"
    # DCE
    if getIfIn('FSPGR',mod,publ='SeriesDescription'):
        return "dce"
    # DWI
    if getIfIn('DWI',mod,publ='SeriesDescription'):
        return "dwi"
    # FLAIR
    if (getIfIn('FLAIR',mod,publ='SeriesDescription') 
        or getIfIn('FLAIR',mod,priv='0x0019109C')):
        return "FLAIR"
    # T1w
    if (getIfIn('T1',mod,publ='SeriesDescription') 
        or getIfIn('BRAVO',mod,priv='0x0019109C')):
        return "T1w"
    # T2w
    if (getIfIn('T2',mod,publ='SeriesDescription') 
        or getIfIn('T2',mod,priv='0x0019109C')):
        return "T2w"
    # CSI
    if (getIfIn('CSI',mod,priv='0x0019109E') 
        and getIfIn('CSI',mod,publ='SeriesDescription')):
        return "mrsi"
    # SVS
    if (getIfIn('CSI',mod,priv='0x0019109E') 
        and getIfIn('SV',mod,publ='SeriesDescription')):
        return "svs"
    # SWI
    if getIfIn('SWI',mod,publ='SeriesDescription'):
        return "swi"
    print("XX NO MOD")
    return False

def getDatatype(modality=0,mod=0):
    """input modalitet, eller mod=dicomobjekt, output vilken datatyp"""
    if modality == 0:
        modality = getMod(mod)
    
    if modality == 'T1w' or modality == 'T2w' or modality == 'FLAIR':
        return "anat"
    if modality == 'asl' or modality == 'dsc' or modality == 'dce':
        return "perf"
    if modality == 'mrsi' or modality == 'svs':
        return "mrs"
    if modality == 'swi':
        return "swi"
    if modality == 'dwi':
        return "dwi"
    if modality == 'pet':
        return "pet"
    if modality == 'cbf' or modality == 'cbv':
        return "DERIV_perfusion"
    print("XX NO DATATYPE")
    return False
    

def getIfIn(item,mod,publ=0,priv=0):
    """privat funktion, för getMod"""
    if publ != 0 and publ in mod:
        if item in str(mod.data_element(publ)).upper():
            return True
        else:
            return False
    if priv !=0 and (priv) in mod:
        if item in mod[priv].value.upper():
            return True
        else:
            return False
    return False
