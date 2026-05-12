class PatientData:
    def __init__(self,  sub_num, DCM="", ID="", date="", age="", sex=""):
        self.sesList = []
        self.modality_list = []
        self.Details_List = []
        self.CohortList = []
        self.Sub_tag_num = int(sub_num)

        if DCM == "":
            self.PatientID = str(ID)
            if not date=="":
                self._Create_ses_entry(date)
            self.age = str(age)
            self.sex = str(sex)
        else:
            self._Create_ses_entry(DCM.StudyDate)
            self.PatientID = str(DCM.PatientID)
            self.age = str(DCM.PatientAge)
            self.sex = str(DCM.PatientSex)

    def Get_Sub_Tag(self):
        """Creates a string with the 'sub-' tag, with 0 added
        for numbers below 10"""
        if self.Sub_tag_num >= 10:
            return "sub-" + str(self.Sub_tag_num)
        else:
            return "sub-0" + str(self.Sub_tag_num)

    def Get_Ses_Tag(self, S_date):
        """Input: Studdy Date\n
        If the studdy date is logged with a 'ses-' tag returns 'ses-' str.
        Else it loggs the new studdy date with a new session tag, 
        and returns that"""
        BExists = False
        for s in self.sesList:
            if s.get('ses_date') == str(S_date):
                BExists = True
        if BExists == False:
            self._Create_ses_entry(S_date)
        for s in self.sesList:
            if s.get('ses_date') == str(S_date):
                if s.get('ses_tag_nr') >= 10:
                    ses_tag_str = ("ses-" + 
                                   str(s.get('ses_tag_nr')))
                else:
                    ses_tag_str = ("ses-0" + 
                                   str(s.get('ses_tag_nr')))
                return ses_tag_str
    
    def _Create_ses_entry(self, new_S_date):
        """Input: Studdy Date\n
        Loggs the new studdy date with a new tag"""
        tempmax = 1
        if not self.sesList == []:
            for s in self.sesList:
                if s.get('ses_tag_nr') >= tempmax:
                    tempmax = s.get('ses_tag_nr') + 1

        tempDict = {'ses_date'  : str(new_S_date), 
                    'ses_tag_nr': tempmax}
        self.sesList.append(tempDict)
    
    def Append_Mod_List(self, modality, descript, ses_date):
        """Input: str modality, descrtiption, and StuddyDate\n
        Key is modality, value is protocol name. Adds the pair to
        the list as a dict.
        The dict also has the key 'date' with the str ses_tag as value"""
        inListB = False
        for d in self.modality_list:
            if (modality == d.get("mod") 
                and descript == d.get("desc") 
                and ses_date == d.get("date")):
                inListB = True
        if inListB == False:
            self.modality_list.append({"mod" :modality, 
                                       "desc":descript,
                                       "date":self.Get_Ses_Tag(ses_date)})

    def Append_Details_List(self, new_dict):
        """Input: dict with keys: 
        ["Modality","Avbildning","Options","ses_tag"].\n
        Adds it to the list as long as an identical dict is not 
        already added"""
        existsBool = False
        for d in self.Details_List:
            if (d.get("Modality")   == new_dict.get("Modality")   and
                d.get("Avbildning") == new_dict.get("Avbildning") and
                d.get("Options")    == new_dict.get("Options")    and 
                d.get("ses_tag")    == new_dict.get("ses_tag")    ):
                existsBool = True
        if existsBool == False:
            self.Details_List.append(new_dict)

    def Append_Cohort_list(self, c_dict, ses_date):
        """Input: dict to add, session date\n
        Takes the dict to add, adds the session tag, appends the list"""
        tempDict = c_dict.copy()
        tempDict["session"] = self.Get_Ses_Tag(ses_date)
        self.CohortList.append(tempDict)

    def Get_personal_Data(self):
        tempSesDir = {}
        for s in self.sesList:
            tempSesDir[str(self.Get_Ses_Tag(s.get('ses_date')))] = (str(s.
                                                         get('ses_date')))

        return {str(self.Get_Sub_Tag()): str(self.PatientID), 
                "sessions":tempSesDir}



class PatientList:
    import BIDS_Program.func_getCohort_tabell as funcCohort

    def __init__(self):
        self.SubList = []
        self.Total_mod_list = []

    def _getList(self):
        """Returns sub list"""
        return self.SubList

    def Patient_Exists(self, E_ID):
        """Input: Patient ID string\n
        Iterates over all PatientData object, and returns true if any that
        exist match the given ID"""
        existsBool = False
        for p in self.SubList:
            if p.PatientID == str(E_ID):
                existsBool = True
        return existsBool

    def Get_P_sub_tag(self, DCM):
        """Input: dicom object\n
        Uses the PatientID of the dcm file to find the coresponding 
        subject, and then calls that objects 'Get_sub_tag' method"""
        p_ID = DCM.PatientID
        for p in self.SubList:
            if p.PatientID == p_ID:
                return p.Get_Sub_Tag()
        return False

    def Get_P_ses_tag(self, DCM="", Date="", ID= ""):
        """Input: dicom object or (string for date and id)\n
        Uses the PatientID of the dcm file to find the coresponding 
        subject, and then calls that objects 'Get_ses_tag' method"""
        if not DCM=="":
            p_ID = DCM.PatientID
            for p in self.SubList:
                if p.PatientID == p_ID:
                    return p.Get_Ses_Tag(DCM.StudyDate)
        else:
            for p in self.SubList:
                if p.PatientID == ID:
                    return p.Get_Ses_Tag(Date)
        return False
    
    def add_To_List(self, p_DCM="", n_ID="", n_Date="", 
                    n_number=1, n_age="", n_sex=""):
        """Input: dicom object\n
        Initiates a new PatientData object, with a sub number one higher
        than the highest current in the list. Then adds to list"""
        if p_DCM == "":
            temp_Patient = PatientData(n_number, ID=n_ID, date=n_Date, 
                                       age=n_age, sex=n_sex)
        else:
            temp_Patient = PatientData(self.highest_Num() + 1, DCM=p_DCM)
        self.SubList.append(temp_Patient)

    def highest_Num(self):
        """Returns the highest int sub-number in the list"""
        maxNum = 0
        if not self._getList() == []:
            for p in self._getList():
                if p.Sub_tag_num >= maxNum:
                    maxNum = int(p.Sub_tag_num)
        return int(maxNum)

    def Uppdate_MODS(self, DCM, modality):
        """Input: dicom object to read value from, str modality to use\n
        Finde the correct Patient in list form dicom object, calls
        the append_mod method"""
        p_ID = DCM.PatientID
        p_desc = DCM.SeriesDescription
        p_date = DCM.StudyDate
        for p in self.SubList:
            if p.PatientID == p_ID:
                # Update patient specific list
                p.Append_Mod_List(modality, p_desc, p_date)
                # Update total list
                inListB = False
                for d in self.Total_mod_list:
                    if (d.get("mod") == modality 
                        and d.get("desc") == p_desc):
                            inListB = True
                            d["NR"] += 1
                if inListB == False:
                    self.Total_mod_list.append({"mod"  : modality, 
                                                "desc" : p_desc,
                                                "NR"   : 1})
                
    def Update_Details(self, DCM, d_dict):
        """Inputn: DCM objetct, details dict\n
        Identefies the target PatientData object in the list
        from the DCM object, and calls the 'Append_Details_List'
        method in that object to add the d_dict"""
        p_ID = DCM.PatientID
        for p in self.SubList:
            if p.PatientID == p_ID:
                # Update detail list
                p.Append_Details_List(d_dict)
    
    def Update_Cohort(self, DCM):
        """Input: dicom object\n
        Takes a dcm object to both identify the right PatientData object,
        and to analyse with getCohort(), then updates the patient"""
        p_ID = DCM.PatientID
        for p in self.SubList:
            if p.PatientID == p_ID:
                # Update detail list
                p.Append_Cohort_list(self.funcCohort.getCohort(DCM), 
                                     DCM.StudyDate)
                    
    def Append_Total_Mod_List(self, modality, desc):
        inListB = False
        for d in self.Total_mod_list:
            if (d.get("mod") == modality and d.get("desc") == desc):
                    inListB = True
                    d["NR"] += 1
        if inListB == False:
            self.Total_mod_list.append({"mod":modality, 
                                        "desc":desc, 
                                        "NR":0})

    def Get_All_Personal_Data(self):
        tempAllList = []
        for p in self._getList():
            tempAllList.append(p.Get_personal_Data())
        return tempAllList

    def Compile_Cohort(self):
        tc_list = [] # total cohort list
        for pat in self.SubList:
            for ses in pat.sesList.copy():
                sestag = pat.Get_Ses_Tag(ses.get('ses_date'))
                wholeSes = []
                for scan in pat.CohortList.copy():
                    if scan.get("session") == sestag:
                        wholeSes.append(scan)
                if not wholeSes == []:
                    tc_list.append(self.funcCohort.getTotal(wholeSes))

        col0 = {"Anat":2,"T1 utan kontrast":3,"T1 med kontrast":4,
                "T2 utan kontrast":5,"T2 med kontrast":6,"FLAIR":7,
                "SWI":8,"Func":9, "DWI":10, "ASL":11,"DSC":12,"DCE":13,"CBF":14,
                "CBV":15,"MS":16,"SVS":17,"MRSI":18}
        col1 = {}
        col2 = {}
        col3 = {}
        for key, value in col0.items():
            if not key == "header":
                col1[key] = 0
                col2[key] = 0
                col3[key] = 0
        amount_FDG = 0
        amount_met = 0
        amount_rest = 0

        for en in tc_list: # en short for entries
            if en.get("Tracer") == "FDG":
                if not key == "Tracer":
                    amount_FDG += 1

            elif en.get("Tracer") == "metionin":
                if not key == "Tracer":
                    amount_met += 1
            elif en.get("Tracer") == "resterande":
                if not key == "Tracer":
                    amount_rest += 1

            for key, value in en.items():
                if en.get("Tracer") == "FDG":
                    if not key == "Tracer":
                        col1[key] += 1
                elif en.get("Tracer") == "metionin":
                    if not key == "Tracer":
                        col2[key] += 1
                elif en.get("Tracer") == "resterande":
                    if not key == "Tracer":
                        col3[key] += 1
        return [col0, col1, col2, col3, amount_FDG ,amount_met ,amount_rest]
