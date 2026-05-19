from packages.Manfred_and_Sofia.File_handling.Analyze_and_Convert_Subject import iterate_Patient_Folders as Navigate
from packages.Manfred_and_Sofia.File_handling.patient_classes import PatientList, PatientData
from packages.Manfred_and_Sofia.File_handling.Excel_Print import Write_Patient_Data
import pathlib
import pandas
import json
import time

def PH_is_dead():
    """Placeholder for a function that returns if the thread should
    be killed"""
    return False

def prepAndConvert(Drive_Path   =pathlib.Path(""),
                   Output_Folder=pathlib.Path(""),
                   ThreadCount  =2, 
                   ZippIt       =False,
                   Run_Name     =False,
                   Check_DCM    =True,
                   Update_Status=print,
                   Print_Func   =print,
                   Check_broken =PH_is_dead):
    try:
        if (pathlib.Path.is_dir(Drive_Path)       and 
            pathlib.Path.is_dir(Output_Folder)    and
            not Drive_Path    == pathlib.Path("") and
            not Output_Folder == pathlib.Path("")  ):

            tick = time.time() ### Starting the stopwatch
            Subject_list = PatientList()
            FileName = "Personal_Data_BIDS.json"
            psd_path = (Output_Folder.resolve().parents[0] / "Private_Data_BIDS")
            
            # Reading "participants.tsv" and creating entries from the data
            Update_Status("Reading existing data")
            if pathlib.Path.exists(Output_Folder / "participants.tsv"):
                ptcpt_r = pandas.read_csv((Output_Folder / "participants.tsv"), 
                                            sep='\t')
                for i in range(len(ptcpt_r)):
                    if pathlib.Path.exists(psd_path / FileName):
                        with open(str(psd_path / FileName)) as file:
                            priv_data = json.load(file)
                        loadDict = {}
                        for sub in priv_data:
                            for key, value in sub.items():
                                if key == ptcpt_r["partisipant_id"][i]:
                                    loadDict = sub.copy()
                        (Subject_list.
                        add_To_List(n_number=int(ptcpt_r["partisipant_id"][i][4:]),
                                    n_age=ptcpt_r["age"][i],
                                    n_sex=ptcpt_r["sex"][i],
                                    n_ID=loadDict.get(ptcpt_r["partisipant_id"][i])))
                        for ses in loadDict.get("sessions"):
                            Subject_list.Get_P_ses_tag(ID=loadDict.
                                                get(ptcpt_r
                                                    ["partisipant_id"][i]),
                                                Date=loadDict.get("sessions")
                                                            .get(ses))
                    else:
                        (Subject_list.
                        add_To_List(n_number=int(ptcpt_r["partisipant_id"][i][4:]),
                                    n_age=ptcpt_r["age"][i],
                                    n_sex=ptcpt_r["sex"][i]))
            # Reading "Modality_Table.xlsx" 
            # and adding all modalities to total list
            if pathlib.Path.exists(Output_Folder / "Modality_Table.xlsx"):
                ex_r = pandas.read_excel(Output_Folder / "Modality_Table.xlsx")
                headers = ["pet"  , "cbf", "cbv", "asl" , "dsc", "dce", "dwi", 
                        "FLAIR", "T1w", "T2w", "mrsi", "svs", "swi"]
                for mods in headers:
                    mod_row_count = 0
                    for value in ex_r[mods]:
                        if (not value == ""          and 
                            not value == "- - - - -" and
                            not pandas.isna(value)):
                            for i in range(int(ex_r[mods + ": nr"][mod_row_count])):
                                Subject_list.Append_Total_Mod_List(modality=mods,
                                                                desc=value)
                            mod_row_count += 1
            
            try:
                Navigate(Patient_Path      = (Drive_Path),
                        Output_Path       = Output_Folder, 
                        Sub_List          = Subject_list,
                        Number_of_threads = ThreadCount,
                        zippIt            = ZippIt,
                        name_run          = Run_Name,
                        CheckDCM          = Check_DCM,
                        update_status     = Update_Status,
                        Print_func        = Print_Func,
                        is_killed         = Check_broken)
            except Exception as e:
                Update_Status("Failed")
                Print_Func("Encountered unexpected error in: Navigate")
                Print_Func(str(e))
                
            if not Subject_list.SubList == []:
                Update_Status("Writing Metadata & Tables")
                ### Writing excel
                #try:
                if pathlib.Path.exists(psd_path / FileName):
                    with open(str(psd_path / FileName)) as file:
                        priv_data = json.load(file)
                        Write_Patient_Data(Patient_List=Subject_list, 
                                            out_path=Output_Folder,
                                            Exsisting_PD=priv_data)
                else:
                    Write_Patient_Data(Patient_List=Subject_list, 
                                    out_path=Output_Folder)
                # except Exception as e:
                #     Update_Status("Failed")
                #     Print_Func("Encountered unexpected error in: Excel_Print")
                #     Print_Func(str(e))
                ### Replaced with valid patient metadata 
                parti_d = {"partisipant_id":[], "age":[], "sex":[]}
                for p in Subject_list.SubList.copy():
                    parti_d.get("partisipant_id").append(str(p.Get_Sub_Tag()))
                    parti_d.get("age"           ).append(str(p.age          ))
                    parti_d.get("sex"           ).append(str(p.sex          ))
                pts_tsv = pandas.DataFrame(parti_d)
                pts_tsv.to_csv(str(Output_Folder / "participants.tsv"), sep="\t")
            
                ### Writing encrypted personal data to seperate file
                # psd: personal data
                if not psd_path.exists():
                    psd_path.mkdir(parents=True, exist_ok=False)

                psd_list = Subject_list.Get_All_Personal_Data()
                with open((psd_path / FileName), "w") as psd_json:
                    json.dump(psd_list, psd_json)

                ## Writing bidsignore
                path = Output_Folder /".bidsignore"
                with open(str(path), "w") as f:
                    f.write("**/swi/\n")
                    f.write("**/dce/\n")
                    f.write("**/dsc/\n")
                    f.write("**/cbf/\n")
                    f.write("**/cbv/\n")

            
            Update_Status("Finished Process")


            tock = time.time() # Stopping stopwatch
            total_sec = int(tock - tick)
            if total_sec >= 60:
                minutes = int(total_sec / 60)
            else:
                minutes =int(0)
            sec = int(total_sec % 60)
            Print_Func("\n\nTotal time : " + str(total_sec) + " s")
            Print_Func("The entire process took: " + str(minutes) 
                    + " min, " + str(sec)     + " sec")

        else:
            Update_Status("Must give path")
    except Exception as e:
        Update_Status("Failed")
        Print_Func("Encountered unexpected error in: Convert_Handler")
        Print_Func(str(e))
          