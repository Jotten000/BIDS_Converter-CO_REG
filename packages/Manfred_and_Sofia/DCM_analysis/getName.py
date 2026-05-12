"""modulen har funktioner som returnerar namnet för avbildningen"""
from pathlib import Path
from pydicom import dcmread

from packages.Manfred_and_Sofia.DCM_analysis import func_getWhichMod

def getWhole(mod, runIndex, ifRun):
    """input dicom-objekt, 
    output dict() m. alla entities av filnamnet enligt BIDS"""

    modtype = func_getWhichMod.getDatatype(mod=mod)
    modality = func_getWhichMod.getMod(mod)

    if mod.Modality == 'PT':
        if 'NAC' in mod.SeriesDescription : 
            return dict({"rec":"None"})

        else :
            nots = ["DECY","DTIM","RANSNG","DCAL","SLSENS","NORM"]
            ises = mod.CorrectedImage
            istot = ""
            for ist in ises:
                if ist not in nots:
                    istot = "".join([istot,ist])
            
            if (0x000910BB) in mod : 
                istot = "".join([istot,str(int(mod[0x000910BB].value)),"mm"])
            elif ('mm' in mod.SeriesDescription and mod.SeriesDescription
                  [mod.SeriesDescription.find("mm")-1] == " ") : 
                istot = ("".join([istot,"".join([mod.SeriesDescription
                                [mod.SeriesDescription.find("mm")-2],"mm"])]))
            elif 'mm' in mod.SeriesDescription : 
                istot = ("".join([istot,"".join([mod.SeriesDescription
                                [mod.SeriesDescription.find("mm")-1],"mm"])]))
      
            return dict({"rec":istot[1:],"run":str(runIndex)})
    
    elif modtype == 'anat':
        entities = dict()

        if 'CUBE' in mod[0x0019109C].value.upper():
            entities.update({"rec":"CUBE"})
        elif ('FSE' in mod[0x0019109C].value.upper() 
              and 'XL' in mod[0x0019109C].value.upper()):
            entities.update({"rec":"FSEXL"})
        else:
            entities.update({"rec":mod[0x0019109C].value.upper()})

        tst = []
        if 'K' in mod.SeriesDescription:
            tst.append("K")
        if 'DYN' in mod.SeriesDescription:
            tst.append("DYN")
        if 'FS' in mod.ScanOptions:
            tst.append("FS")
            
        if len(tst) > 0:
            entities.update({"acq":"+".join(tst)})
        
        if 'mm' in mod.SeriesDescription:
            entities.update({"echo":int(mod.EchoTime)})
        
    elif modtype == 'mrs':
        entities = dict({"acq":int(mod.SliceThickness)})
        if (modality == 'svs' and ('DX' in mod.SeriesDescription.upper() 
                                or 'DEX' in mod.SeriesDescription.upper())) : 
            entities.update({"voi":"Dx"})
        elif modality == 'svs' and 'SIN' in mod.SeriesDescription.upper() : 
            entities.update({"voi":"Sin"})
    
    elif modtype == 'dwi' : 
        entities = dict()
    
    elif modtype == 'perf' : 
        entities = dict()
        if modality == 'dce' : 
            entities.update({"flip":int(mod.FlipAngle)})

            tst = []
            if 'K' in mod.SeriesDescription:
                tst.append("K")
            if 'DYN' in mod.SeriesDescription:
                tst.append("DYN")
            if 'FS' in mod.ScanOptions:
                tst.append("FS")
            if len(tst) > 0:
                entities.update({"acq":"+".join(tst)})
        
        #return entities
    
    elif modtype == 'swi' : 
        if 'phase' in mod.SeriesDescription : 
            #return 
            entities = dict({"part":"phase"})
        else : 
            #return 
            entities = dict({"acq":int(mod.WindowWidth)})
        
    elif modtype == 'DERIV_perfusion' : 
        if ('RCBF' in mod.SeriesDescription.upper() 
            or 'RCBV' in mod.SeriesDescription.upper()):
            return dict({"acq":"REL","run":str(runIndex)})
        elif ('CBF' in mod.SeriesDescription.upper() 
              or 'CBV' in mod.SeriesDescription.upper()):
            return dict({"acq":"ABS","run":str(runIndex)})
    else : 
        print("XXX")
        entities = dict()
    
    if ifRun : 
        entities.update({"run":str(runIndex)})
    return entities
    
def getFileName(sub:str,ses:str,suffix:str,mod, runIndex, ifRun):
    """input str sub, str ses, str suffix, int/str run index, d
    icom-objekt, output filnamn"""

    if ('SCREEN SAVE' in mod.ImageType or 'REFORMAT' in mod.ImageType 
        or 'Processed Images' in mod.SeriesDescription) :
        return "IGNORE"
    
    dict = getWhole(mod, runIndex,ifRun)


    parts = []
    parts.append(sub)
    parts.append(ses)
    # BIDS entity ordering (per BIDS 1.9 spec)
    entity_order = ["task", "acq", "ce", "trc", "voi", "rec", "run", 
                    "echo", "flip", "inv", "part"]
    for key in entity_order:
        if key in dict:
            parts.append(f"{key}-{dict[key]}")
    parts.append(suffix)
    name = "_".join(parts)

    return name
