

from packages.Manfred_and_Sofia.DCM_analysis import func_getWhichMod

"""Alla funktioner i filen tar ett dicom-objekt (FileDataset) som input, och 
ger en patientspecifik eller modulspecifik dict() som output, värden som ej 
finns med returneras som False ifall ingen input skickas, returneras en lista 
med parametrar som läses från dicom-objektet"""

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
        return ["Modality","Sequence","Options","Weight"]
    
    temp = dict({"Modality":"","Sequence":"","Options":"","Weight":""})
    temp["Modality"] = func_getWhichMod.getMod(modfir)
    if 'PatientWeight' in modfir : 
        temp.update({"Weight":" ".join([str(int(modfir.PatientWeight)),"kg"])})
    
    if modfir.Modality == 'PT' : 
        temp["Sequence"] = (" ".join([temp["Sequence"],
            _privGetBasics(["Radiopharmaceutical","0x00091036"],
                          modfir,modlas)]))
        #temp["Options"] = (" ".join([temp["Options"],
        #    str(int(_privGetBasics(["RadionuclideTotalDose"],
        #                          modfir,modlas))),"Bq"]))
        
        if 'RadionuclideTotalDose' in modfir :
            temp["Options"] = (" ".join([temp["Options"],str(int(modfir.RadionuclideTotalDose)),"Bq"]))
        elif (0x00091038) in modfir : 
            temp["Options"] = (" ".join([temp["Options"],str(int(modfir[0x00091038].value)),"MBq"]))
        elif 'RadionuclideTotalDose' in modlas :
            temp["Options"] = (" ".join([temp["Options"],str(int(modlas.RadionuclideTotalDose)),"Bq"]))
        elif (0x00091038) in modlas : 
            temp["Options"] = (" ".join([temp["Options"],str(int(modlas[0x00091038].value)),"MBq"]))
        

        if 'MAC' in modfir.SeriesDescription and ((0x000910BB) in modfir or (0x000910BB) in modlas) : 
            temp["Options"] = (" ".join([temp["Options"],
                str(int(_privGetBasics(["0x000910BB"],modfir,modlas))),"mm"]))
        if 'NAC' in modfir.SeriesDescription :
            temp["Options"] = (" ".join([temp["Options"],"NAC"]))

    else : 

        # BRAVO / CUBE / PROP
        if 'BRAVO' in modfir.SeriesDescription : 
            temp["Sequence"] = " ".join([temp["Sequence"],"BRAVO"])
        elif 'CUBE' in modfir.SeriesDescription.upper() : 
            temp["Sequence"] = " ".join([temp["Sequence"],"CUBE"])
        elif 'PROP' in modfir.SeriesDescription.upper() : 
            temp["Sequence"] = " ".join([temp["Sequence"],"PROPELLER"])
            temp["Options"] = (" ".join([temp["Options"],
                str(int(_privGetBasics(["SliceThickness"],modfir,modlas))),
                "mm"]))

        # Sekvens
        if 'EP' in modfir.ScanningSequence : 
            temp["Sequence"] = " ".join([temp["Sequence"],"echo planar"])

        if (0x0019109E) in modfir and 'EFGRE' in modfir[0x0019109E].value : 
            temp["Sequence"] = (" ".join([temp["Sequence"],
                                            "fast gradient echo"]))
        elif 'GR' in modfir.ScanningSequence : 
            temp["Sequence"] = " ".join([temp["Sequence"],"gradient echo"])
        
        if (0x0019109E) in modfir and 'FSE' in modfir[0x0019109E].value : 
            temp["Sequence"] = (" ".join([temp["Sequence"],
                                            "fast spin echo"]))
        elif 'SE' in modfir.ScanningSequence : 
            temp["Sequence"] = " ".join([temp["Sequence"],"spin echo"])

        # FS och K
        if 'FS' in modfir.ScanOptions or ' FS' in modfir.SeriesDescription : 
            temp["Options"] = " ".join([temp["Options"],"fat saturated"])
        if 'DYN' in modfir.SeriesDescription : 
            temp["Options"] = " ".join([temp["Options"],"dynamic"])
        if ('+K' in modfir.SeriesDescription 
            or '_K' in modfir.SeriesDescription 
            or '+ K' in modfir.SeriesDescription 
            or ' K' in modfir.SeriesDescription) : 
            temp["Options"] = " ".join([temp["Options"],"with contrast"])
        elif 'Gd' in modfir.SeriesDescription : 
            temp["Options"] = " ".join([temp["Options"],"with contrast"])
        if 'FSPGR' in modfir.SeriesDescription : 
            temp["Options"] = (" ".join([temp["Options"],"flip angle",
                                         str(int(modfir.FlipAngle))]))

        # ASL
        if ((0x0019109E) in modfir 
            and 'ASL' in modfir[0x0019109E].value.upper()) : 
            temp["Sequence"] = " ".join([temp["Sequence"],"ASL"])
            if 'InversionTime' in modfir : 
                temp["Options"] = (" ".join([temp["Options"],
                                "PLD =",str(int(modfir.InversionTime)),"ms"]))
            elif 'InversionTime' in modlas : 
                temp["Options"] = (" ".join([temp["Options"],
                                "PLD =",str(int(modlas.InversionTime)),"ms"]))
            else : 
                temp["Options"] = " ".join([temp["Options"],"PLD =","Unknown"])
        
        # SWI
        if func_getWhichMod.getMod(modfir) == 'swi' : 
            temp["Sequence"] = " ".join([temp["Sequence"],"Coil",modfir.ReceiveCoilName[modfir.ReceiveCoilName.find("[")+1:][:modfir.ReceiveCoilName.find("]")-1]])
            temp["Options"] = " ".join([temp["Options"],"Window center",str(int(modfir.WindowCenter))])

    if len(temp["Sequence"]) > 1 : 
        temp["Sequence"] = temp["Sequence"][1:]
    if len(temp["Options"]) > 1 : 
        temp["Options"] = temp["Options"][1:]

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

    

