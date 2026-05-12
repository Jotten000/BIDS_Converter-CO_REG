from packages.Manfred_and_Sofia.DCM_analysis import func_getWhichMod
def getCohort(hms) : 
    """input dicom-objekt, output dict m. vilken modalitet är True"""


    td = dict({"T1":True})

    thedict = dict({"Tracer":None,"T1 utan kontrast":False,"T1 med kontrast":False,"T2 utan kontrast":False,"T2 med kontrast":False,"FLAIR":False,"SWI":False,"DWI":False,"ASL":False,"DSC":False,"DCE":False,"CBF":False,"CBV":False,"SVS":False,"MRSI":False})
    
    if func_getWhichMod.getMod(hms) == 'pet' : 
        if 'Radiopharmaceutical' in hms and ('METHIONINE' in hms.Radiopharmaceutical.upper() or 'METIONIN' in hms.Radiopharmaceutical.upper()) or ((0x00091036) in hms and ('METHIONINE' in hms[0x00091036].value.upper() or 'METIONIN' in hms[0x00091036].value.upper())) or 'ProtocolName' in hms and ('METHIONINE' in hms.ProtocolName.upper() or 'METIONIN' in hms.ProtocolName.upper()) : 
            thedict["Tracer"] = 'metionin'
        elif 'Radiopharmaceutical' in hms and ('FDG' in hms.Radiopharmaceutical.upper() or 'FLUORODEOXYGLUCOSE' in hms.Radiopharmaceutical.upper()) or ((0x00091036) in hms and ('FDG' in hms[0x00091036].value.upper() or 'FLUORODEOXYGLUCOSE' in hms[0x00091036].value.upper())) or 'ProtocolName' in hms and ('FDG' in hms.ProtocolName.upper() or 'FLUORODEOXYGLUCOSE' in hms.ProtocolName.upper()) :
            thedict["Tracer"] = 'FDG'
        elif thedict["Tracer"] == None : 
            thedict["Tracer"] = 'resterande'

    elif func_getWhichMod.getMod(hms) == 'T1w' and ('+K' in hms.SeriesDescription or '_K' in hms.SeriesDescription or '+ K' in hms.SeriesDescription or ' K' in hms.SeriesDescription) : 
        thedict["T1 med kontrast"] = True
    elif func_getWhichMod.getMod(hms) == 'T1w' : 
        thedict["T1 utan kontrast"] = True
    elif func_getWhichMod.getMod(hms) == 'T2w' and ('+K' in hms.SeriesDescription or '_K' in hms.SeriesDescription or '+ K' in hms.SeriesDescription or ' K' in hms.SeriesDescription) : 
        thedict["T2 med kontrast"] = True
    elif func_getWhichMod.getMod(hms) == 'T2w' : 
        thedict["T2 utan kontrast"] = True

    elif func_getWhichMod.getMod(hms) != 'ERROR' : 
        thedict[func_getWhichMod.getMod(hms).upper()] = True
    
    return thedict

def getTotal(hms): 
    """input lista m. dicts för 1 session, output dict m. summering och True"""
    temp = dict()
    for i in hms : 
        # i är en dict
        if i["Tracer"] is not None and "Tracer" not in temp.keys():
            temp.update({"Tracer":i["Tracer"]})
        else : 
            for j in i : 
                # j är nyckeln, i[j] är värdet (true//false)
                if i[j] == True and j not in temp.keys() : 
                    temp.update({j:i[j]})
    # Kontroll att Tracer finns med
    if "Tracer" not in temp.keys() : 
        temp.update({"Tracer":"resterande"})
    return temp

def getHeaders(header) : 
    """input 'H' för hoistontell header eller 'V' för vertikal header, output lista med strings av alla headers"""
    if header == 'H' : 
        return ["FDG","metionin","resterande"]
    if header == 'V' : 
        return ["Anat","T1 utan kontrast","T1 med kontrast","T2 utan kontrast","T2 med kontrast","FLAIR","swi","Func","dwi","asl","dsc","dce","cbf","cbv","MS","svs","mrsi"]



