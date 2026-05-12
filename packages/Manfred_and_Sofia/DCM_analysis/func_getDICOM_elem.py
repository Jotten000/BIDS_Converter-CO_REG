
#import func_getWhichMod
from packages.Manfred_and_Sofia.DCM_analysis import func_getWhichMod

"""Alla funktioner i filen tar ett dicom-objekt (FileDataset) som input, och 
ger en patientspecifik eller modulspecifik dict() som output, värden som ej 
finns med returneras som False ifall ingen input skickas, returneras en lista 
med parametrar som läses från dicom-objektet"""

# Använder
def getNamePersNr(mod=0):
    """input dicom-objekt, output dict() personnummer, datum för bildtagning, 
    kön, vikt, ifall ingen input returneras lista m. parametrar för 
    dict()-en"""
    infos = (["StudyDate","PatientName","PatientID","PatientSex",
              "PatientWeight","PatientAge"])
    if mod == 0:
        return infos
    return _priv(mod,infos)

def _priv(mod,thelist):
    """privat funktion, används för iterering"""
    theses = dict()
    for i in thelist:
        if i in mod:
            theses.update({i:mod.data_element(i).value})
        else:
            theses.update({i:False})
    return theses

def getBasics(modfir=0, modlas=0):
    """input första och sista dicom-objektet i serien, output dict() m. basic 
    information, om ingen input -> output lista m. vilken basic information 
    som ska returneras"""

    if modfir == 0 :
        return ["Modalitet","Avbildning","Alternativ"]
    
    temp = dict({"Modalitet":"","Avbildning":"","Alternativ":""})
    temp["Modalitet"] = func_getWhichMod.getMod(modfir)
    
    if modfir.Modality == 'PT' : 
        temp["Avbildning"] = (" ".join([temp["Avbildning"],
            _privGetBasics(["Radiopharmaceutical","0x00091036"],
                          modfir,modlas)]))
        temp["Alternativ"] = (" ".join([temp["Alternativ"],
            str(int(_privGetBasics(["RadionuclideTotalDose"],
                                  modfir,modlas))),"Bq"]))
        
        if 'MAC' in modfir.SeriesDescription : 
            temp["Alternativ"] = (" ".join([temp["Alternativ"],
                str(int(_privGetBasics(["0x000910BB"],modfir,modlas))),"mm"]))
            
        if 'PatientWeight' in modfir and 'NAC' in modfir.SeriesDescription : 
            temp.update({"Vikt":" ".join([str(int(modfir.PatientWeight)),"kg"])})
    
    else : 

        # BRAVO / CUBE / PROP
        if 'BRAVO' in modfir.SeriesDescription : 
            temp["Avbildning"] = " ".join([temp["Avbildning"],"BRAVO"])
        elif 'CUBE' in modfir.SeriesDescription.upper() : 
            temp["Avbildning"] = " ".join([temp["Avbildning"],"CUBE"])
        elif 'PROP' in modfir.SeriesDescription.upper() : 
            temp["Avbildning"] = " ".join([temp["Avbildning"],"PROPELLER"])
            temp["Alternativ"] = (" ".join([temp["Alternativ"],
                str(int(_privGetBasics(["SliceThickness"],modfir,modlas))),
                "mm"]))

        # Sekvens
        if 'EP' in modfir.ScanningSequence : 
            temp["Avbildning"] = " ".join([temp["Avbildning"],"echo planar"])

        if (0x0019109E) in modfir and 'EFGRE' in modfir[0x0019109E].value : 
            temp["Avbildning"] = (" ".join([temp["Avbildning"],
                                            "fast gradient echo"]))
        elif 'GR' in modfir.ScanningSequence : 
            temp["Avbildning"] = " ".join([temp["Avbildning"],"gradient echo"])
        
        if (0x0019109E) in modfir and 'FSE' in modfir[0x0019109E].value : 
            temp["Avbildning"] = (" ".join([temp["Avbildning"],
                                            "fast spin echo"]))
        elif 'SE' in modfir.ScanningSequence : 
            temp["Avbildning"] = " ".join([temp["Avbildning"],"spin echo"])

        # FS och K
        if 'FS' in modfir.ScanOptions or ' FS' in modfir.SeriesDescription : 
            temp["Alternativ"] = " ".join([temp["Alternativ"],"fat saturated"])
        if 'DYN' in modfir.SeriesDescription : 
            temp["Alternativ"] = " ".join([temp["Alternativ"],"dynamic"])
        if ('+K' in modfir.SeriesDescription 
            or '_K' in modfir.SeriesDescription 
            or '+ K' in modfir.SeriesDescription 
            or ' K' in modfir.SeriesDescription) : 
            temp["Alternativ"] = " ".join([temp["Alternativ"],"with contrast"])
        elif 'Gd' in modfir.SeriesDescription : 
            temp["Alternativ"] = " ".join([temp["Alternativ"],"with contrast"])
        if 'FSPGR' in modfir.SeriesDescription : 
            temp["Alternativ"] = (" ".join([temp["Alternativ"],"flip angle",
                                         str(int(modfir.FlipAngle))]))

        # ASL
        if ((0x0019109E) in modfir 
            and 'ASL' in modfir[0x0019109E].value.upper()) : 
            temp["Avbildning"] = " ".join([temp["Avbildning"],"ASL"])
            if 'InversionTime' in modfir : 
                temp["Alternativ"] = (" ".join([temp["Alternativ"],
                                "PLD =",str(int(modfir.InversionTime)),"ms"]))
            elif 'InversionTime' in modlas : 
                temp["Alternativ"] = (" ".join([temp["Alternativ"],
                                "PLD =",str(int(modlas.InversionTime)),"ms"]))
            else : 
                temp["Alternativ"] = " ".join([temp["Alternativ"],"PLD =","Unknown"])
        
        # SWI
        if func_getWhichMod.getMod(modfir) == 'swi' : 
            temp["Avbildning"] = " ".join([temp["Avbildning"],"Coil",modfir.ReceiveCoilName[modfir.ReceiveCoilName.find("[")+1:][:modfir.ReceiveCoilName.find("]")-1]])
            temp["Alternativ"] = " ".join([temp["Alternativ"],"Window center",str(int(modfir.WindowCenter))])

    if len(temp["Avbildning"]) > 1 : 
        temp["Avbildning"] = temp["Avbildning"][1:]
    if len(temp["Alternativ"]) > 1 : 
        temp["Alternativ"] = temp["Alternativ"][1:]

    return temp
                
def _privGetBasics(thelist, modfir, modlas):
    """input lista av dicom-objekt, output värde av dicom-objekt, om ej finns 
    är output False"""
    for i in thelist:
        if i[:2] == "0x":
            if (i) in modfir : 
                return modfir[i].value
            if (i) in modlas : 
                return modlas[i].value
        else : 
            if i in modfir : 
                return modfir.data_element(i).value
            if i in modlas : 
                return modlas.data_element(i).value
    return False

    

