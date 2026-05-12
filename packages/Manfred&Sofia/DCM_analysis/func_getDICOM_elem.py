
#import func_getWhichMod
from BIDS_Program import func_getWhichMod

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


# DEN HÄR HANTERAR FLER MODALITETER SOM EJ SKA TAS HÄNSYN TILL
def getSpecifics(modality,mod=0):
    """input str m. modalitet -> oputut lista m. specifics för modalitet, 
    input str m. modalitet och mod = dicom-objekt -> oputput dict m. ifyllda
      specifics"""
    
    infosAll = ["StudyDate","ImageType","PhotometricInterpretation"]
    infosPT = ["Radiopharmaceutical","RadiopharmaceuticalTotalDose"]
    infosMR = (["EchoTime","RepetitionTime","InversionTime","ScanningSequence",
                "SequenceVariant","FlipAngle","MRAcquisitionType",
                "MagneticFieldStrength","ImagedNucleus","ContrastBolusAgent",
                "SliceThickness","PixelSpacing"])

    if modality == 'pet':
        if mod == 0:
            return infosAll+infosPT
        else:
            return _priv(mod,infosAll+infosPT)
    
    else:
        if mod != 0:
            pr = _priv(mod,infosAll+infosMR)
        if modality == 'asl' or 'cbf':
            if mod == 0:
                return infosAll+infosMR+["ASLType"]
            else:
                if (0x004310A3) in mod:
                    pr.update({"ASLType":mod[0x004310A3].value})
                    return pr
                elif (0x0019109E) in mod:
                    pr.update({"ASLType":mod[0x0019109E].value})
                else:
                    pr.update({"ASLType":False})
                    return pr
                #return _priv(mod,infosAll+infosMR).update({"ASLType":mod[0x004310A3].value})
        elif modality == 'dsc' or modality == 'dce':
            if mod == 0:
                return infosAll+infosMR+["TheContrastBolusAgent"]
            else:
                if "Gd" in mod.SeriesDescription:
                    #return _priv(mod,infosAll+infosMR).update({"ContrastBolusAgent":"Gd"})
                    pr.update({"TheContrastBolusAgent":"Gd"})
                    return pr
                else:
                    #return _priv(mod,infosAll+infosMR).update({"ContrastBolusAgent":"Unknown"})
                    pr.update({"TheContrastBolusAgent":False})
                    return pr
        elif modality == 'svs' or modality == 'mrsi':
            if mod == 0:
                return infosAll+infosMR+["CSIType"]
            else:
                #pr = _priv(mod,infosAll+infosMR)
                if (0x0019109E) in mod:
                    pr.update({"CSIType":mod[0x0019109E].value})
                    return pr
                    #return _priv(mod,infosAll+infosMR).update({"CSIType":[0x0019109E].value})
                else:
                    pr.update({"CSIType":False})
                    return pr
                    #return _priv(mod,infosAll+infosMR).update({"CSIType":"Unknown"})
        elif modality == 'T1w' or modality == 'T2w' or modality == 'FLAIR':
            if mod == 0:
                return infosAll+infosMR+["Sequencename"]
            else:
                #pr = _priv(mod,infosAll+infosMR)
                if (0x0019109C) in mod:
                    #return ( _priv(mod,infosAll+infosMR).update({"Sequencename":mod[0x0019109C].value}) )
                    #pr = _priv(mod,infosAll+infosMR)
                    #return pr
                    pr.update({"Sequencename":mod[0x0019109C].value})
                else:
                    #return _priv(mod,infosAll+infosMR).update({"Sequencename":"Unknown"})
                    pr.update({"Sequencename":"False"})
                return pr
            
        elif modality == 'dwi' : 
            if mod == 0:
                return infosAll+infosMR+["PLD"]
            else:
                if 'InversionTime' in mod:
                    pr.update({"PLD":mod.InversionTime})
                else:
                    pr.update({"PLD":False})
                return pr
                
        elif (modality == 'ADC' or modality == 'isoDWI' or modality == 'FA' 
              or modality == 'trace' or modality == 'dwi' or modality == 'swi' 
              or modality == 'cbv'):
            if mod == 0:
                return infosAll+infosMR
            else:
                return _priv(mod,infosAll+infosMR)
        else:
            print("ERROR : WENT THROUGH getSpecifics XXX")
            return False
    

# TROR EJ ATT DEN HÄR ANVÄNDS
def getSpecifics2(modality,modfir=0,modlas=0):
    """testar igen"""
    infosAll = ["StudyDate","ImageType"]
    infosPT = ["Radiopharmaceutical","RadionuclideTotalDose"]
    infosMR = (["EchoTime","RepetitionTime","ScanningSequence",
                "SequenceVariant","MRAcquisitionType","MagneticFieldStrength",
                "ImagedNucleus","SliceThickness","PixelSpacing"])

    if modality == 'pet' : 
        if modfir == 0 : 
            return infosAll+infosPT
        else : 
            #temp = _priv(modfir,infosAll+infosPT)
            temp = _priv(modfir,infosAll+["RadionuclideTotalDose"])
            #temp = temp.update({"Radiopharmaceutical":modfir.Radiopharmaceutical})
            #if 'Radiopharmaceutical' in modfir:
            #    temp.update({"Radiopharmaceutical":modfir.Radiopharmaceutical})
            #elif (0x00180031) in modfir:
            #    temp.update({"Radiopharmaceutical":modfir[0x00180031].value})
            
            if (0x00091036) in modfir : 
                temp.update({"Radiopharmaceutical":modfir[0x00091036].value})
            else : 
                temp.update({"Radiopharmaceutical":False})

            if (0x00091038) in modfir : 
                (temp.update({"RadionuclideTotalDose":(10**6)
                              *int(modfir[0x00091038].value)}))
            else : 
                temp.update({"RadionuclideTotalDose":False})
            return temp
        
    else : 
        temp = _priv(modfir,infosAll+infosMR)
    
    if modality == 'T1w' or modality == 'T2w' or modality == 'FLAIR' : 
        if modfir == 0 : 
            return infosAll+infosMR+["InversonTime","FlipAngle"]
        else : 
            temp = temp | _priv(modfir,["InversionTime","FlipAngle"])
            return temp
    
    if modality == 'dsc' or modality == 'dce' or modality == 'swi' : 
        if modfir == 0 : 
            return infosAll+infosMR+["FlipAngle"]
        else : 
            temp = temp | _priv(modfir,["FlipAngle"])
            return temp
    
    if modality == 'asl' : 
        if modfir == 0 or modlas == 0 : 
            return infosAll+infosMR+["PLD","FlipAngle"]
        else : 
            temp = temp | _priv(modfir,["FlipAngle"])
            if 'InversionTime' in modfir : 
                temp.update({"PLD":modfir.InversionTime})
            elif 'InversionTime' in modlas : 
                temp.update({"PLD":modlas.InversionTime})
            else : 
                temp.update({"PLD":False})
            return temp
    
    if modality == 'svs' or modality == 'mrsi' : 
        if modfir == 0 : 
            return infosAll+infosMR+["CSIType"]
        else : 
            if ((0x0019109E) in modfir 
                and 'PRESS' in modfir[0x0019109E].value.upper()) : 
                temp.update({"CSIType":"PRESS"})
            elif ((0x0019109E) in modfir 
                  and 'STEAM' in modfir[0x0019109E].value.upper()) : 
                temp.update({"CSIType":"STEAM"})
            else : 
                temp.update({"CSIType":False})
            return temp
    
    if modality == 'dwi' or modality == 'cbf' or modality == 'cbv' : 
        if modfir == 0 or modlas == 0 : 
            return infosAll+infosMR
        else : 
            return temp
        
    return "WENT WRONG"

# MÅSTE FIXA DELEN FÖR PRIVAT ELEMENT!!!
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
        return ["Modality","Avbildning","Options"]
    
    temp = dict({"Modality":"","Avbildning":"","Options":""})
    temp["Modality"] = func_getWhichMod.getMod(modfir)
    
    if modfir.Modality == 'PT' : 
        temp["Avbildning"] = (" ".join([temp["Avbildning"],
            _privGetBasics(["Radiopharmaceutical","0x00091036"],
                          modfir,modlas)]))
        temp["Options"] = (" ".join([temp["Options"],
            str(int(_privGetBasics(["RadionuclideTotalDose"],
                                  modfir,modlas))),"Bq/μmol"]))
        
        if 'MAC' in modfir.SeriesDescription : 
            temp["Options"] = (" ".join([temp["Options"],
                str(int(_privGetBasics(["0x000910BB"],modfir,modlas))),"mm"]))
            
        if 'PatientWeight' in modfir and 'NAC' in modfir.SeriesDescription : 
            #temp["Options"] = (" ".join([temp["Options"],str(int(modfir.PatientWeight)),"kg"]))
            temp.update({"Weight":" ".join([str(int(modfir.PatientWeight)),"kg"])})
    
    else : 

        # BRAVO / CUBE / PROP
        if 'BRAVO' in modfir.SeriesDescription : 
            temp["Avbildning"] = " ".join([temp["Avbildning"],"BRAVO"])
        elif 'CUBE' in modfir.SeriesDescription.upper() : 
            temp["Avbildning"] = " ".join([temp["Avbildning"],"CUBE"])
        elif 'PROP' in modfir.SeriesDescription.upper() : 
            temp["Avbildning"] = " ".join([temp["Avbildning"],"PROPELLER"])
            temp["Options"] = (" ".join([temp["Options"],
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
            temp["Avbildning"] = " ".join([temp["Avbildning"],"ASL"])
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
            temp["Avbildning"] = " ".join([temp["Avbildning"],"Coil",modfir.ReceiveCoilName[modfir.ReceiveCoilName.find("[")+1:][:modfir.ReceiveCoilName.find("]")-1]])
            temp["Options"] = " ".join([temp["Options"],"Window center",str(int(modfir.WindowCenter))])

    if len(temp["Avbildning"]) > 1 : 
        temp["Avbildning"] = temp["Avbildning"][1:]
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

# används ej
#def _privGetBasicsList(thelist,modfir,modlas):
#    """input lista av dicom-objekt, output värde av dicom-objekt, om ej finns 
#    är output False, som tidigare, men returnerar allt som en lista"""
#    templist = []
#    for i in thelist:
#        if i[:2] == "0x":
#            if (i) in modfir :
#                templist.append(modfir[i].value)
#            if (i) in modlas : 
#                templist.append(modlas[i].value)
#        else : 
#            if i in modfir : 
#                templist.append(modfir.i)
#            if i in modlas : 
#                templist.append(modlas.i)
#    if len(templist) == 0 :
#        return False
#    else : 
#        return templist
    

