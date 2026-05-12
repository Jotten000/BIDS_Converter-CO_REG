###___________________Column marker________________________________________79|_________________99|_________________120|
##                                                                           |                   |                    |
import pathlib
import pydicom
import subprocess
import os
import sys
import bids_validator
import time
import pigz_python
from BIDS_Program.func_getWhichMod import getMod, getDatatype, getIfAccept
from BIDS_Program.func_getDICOM_elem import getBasics
from BIDS_Program.getName import getFileName

def unique_Name(sub_tag_str, ses_tag_str, file_path, dicom_file,
                run_in_name, Target_Folder, Print_Func):
    Bids_File_Name = getFileName(sub      = str(sub_tag_str), 
                                 ses      = str(ses_tag_str), 
                                 suffix   = str(getMod(dicom_file)), 
                                 mod      = dicom_file, 
                                 runIndex = 1,
                                 ifRun    = run_in_name)
    if not "_run" in Bids_File_Name:
        ### OBS: checks .json, because that file is created near instantly,
        #  .nii and .nii.gz takes far longer to generate
        if pathlib.Path(str(file_path / Bids_File_Name) + ".json").is_file():
            Print_Func("____________ OBS: Duplicate name!!! ____________")
            Print_Func("Subject: " + sub_tag_str 
                + " | Sub: " + ses_tag_str 
                + " | Dupelicate name: " + Bids_File_Name)
            Print_Func("Source Folder: " + str(Target_Folder.stem))
            Print_Func("______________________________________________")
            return False
        else:
            not_uniqe_run = False
    elif "_run" in Bids_File_Name:
        runcounter = 1
        not_uniqe_run = True
        while not_uniqe_run == True:
            Bids_File_Name = getFileName(
                                 sub      = str(sub_tag_str), 
                                 ses      = str(ses_tag_str), 
                                 suffix   = str(getMod(dicom_file)), 
                                 mod      = dicom_file, 
                                 runIndex = int(runcounter),
                                 ifRun    = run_in_name)
            
            ### OBS: checks .json, because that file is created near instantly,
            #   .nii and .nii.gz takes far longer to generate
            if not pathlib.Path(str(file_path / Bids_File_Name) + ".json").is_file():
                not_uniqe_run = False
            runcounter += 1  
    return Bids_File_Name          

def validate_new_bids(sub_tag_str, ses_tag_str, Bids_Name, target_DCM,
                      Target_Folder, Print_Func):
    """OBS: UPPDATE!!!"""

    DataType_tag = getDatatype(getMod(target_DCM))

    validator = bids_validator.BIDSValidator()
    is_it_valid = ("/" + str(sub_tag_str) + "/" + str(ses_tag_str) 
                    + "/" + str(DataType_tag) + "/" + Bids_Name)

    # Does not validate files that vill be covered by .bidsignore
    if not validator.is_bids((is_it_valid + ".nii")):
        if (not str(getMod(target_DCM)) == "swi" and 
            not str(getMod(target_DCM)) == "dce" and 
            not str(getMod(target_DCM)) == "dsc" and
            not str(getMod(target_DCM)) == "cbv" and
            not str(getMod(target_DCM)) == "cbf"):
            # Writes a log for filenames that are not valid
            Print_Func("____________ OBS: Invalid name!!! ____________")
            Print_Func("Subject: " + sub_tag_str 
                + " | Sub: " + ses_tag_str 
                + " | Invalid name: " + Bids_Name)
            Print_Func("Source Folder: " + str(Target_Folder.stem))
            Print_Func("______________________________________________")

def create_BIDS_path(Sub_tag_str, Ses_tag_str, target_dcm, 
                     path_hierachy_start):
    DataType_tag = getDatatype(getMod(target_dcm))
    path_BIDS = (path_hierachy_start 
                    / str(Sub_tag_str) 
                    / str(Ses_tag_str) 
                    / str(DataType_tag))
    return path_BIDS

def iterate_Patient_Folders(Patient_Path , Output_Path, 
                            Sub_List, Number_of_threads, 
                            zippIt, name_run, CheckDCM, update_status, Print_func, 
                            is_killed):
    """Takes a path object to root folder, and a path object to the output
    folder. Takes a bool for if the function should double check 
    if all items in a folders are dicom. This makes the program slower.
    Takes a bool for if the function shoulkd convert data. 
    If False creates empty placeholder .txt. Used for debugging.
    Takes a bool for the conversion zip .nii files to .nii.gz. 
    Recomended, but much slower.
    
      
    Iterates over all folders in the given path. 
    If a folder only has files inside it: 
    checks the first file in the folder, and extracts subject id and 
    studdy date. If these don't exist in Subs_dict they will be added 
    with an accosiated tag. Will return a new updated subs_dict. With 
    the file and acociated sub/ses tags it will gennerate a bids path, 
    create the folders. Then generates a filename, checks and logs if 
    it's unique, and starts a conversion subprocess"""
    
    ### Threading variables
    Threads_Active_subprocess = []

    
    # Iterates over all folders in the hierarchy, and adds folders that 
    # contains either .dcm or .img files.
    path_list = []
    update_status("Finding all folders to convert")
    #update_other_status_text("Finding all folders to convert")
    for Paths, FolderNames, Files in Patient_Path.walk():
        if is_killed() == True:
            break
        tempFileListLog = []
        tempBool = False

        ### ______File validation__________________________________
        ### A new version that is less rigorous but has better
        ### performance. Change back if performance is not needed
        for x in Paths.iterdir():
            if x.suffix == ".dcm" or x.suffix == ".img":
                tempFileListLog.append(x)
    
        if not tempFileListLog == []:
            if CheckDCM == True:
                tempBool = (all(pydicom.misc.is_dicom(str(d)) 
                                for d in tempFileListLog))
            else:
                tempBool = True
        ### _______________________________________________________

        bool_bids_include = False
        if tempBool:
            dcmTemp = pydicom.dcmread(tempFileListLog[0])
            bool_bids_include = getIfAccept(dcmTemp) 
        if tempBool == True and bool_bids_include == True:
            pathDict = {"path":str(Paths), 
                        "date":int(dcmTemp.StudyDate)}
            path_list.append(pathDict)
            Print_func("From date: " + dcmTemp.StudyDate 
                  + "|   Added path: " + str(Paths))
    
    # sort the list based on the StuddyDate tag in the first dcm file
    update_status("Sorting the list of folders in chronological order")
    #update_other_status_text("Sorting the list of folders in chronological order")
    path_list.sort(key=lambda x: x.get("date"))

    if path_list == []:
        Print_func("No valid folders found")
    
    update_status("Converting to bids")
    Print_func("\n")
    count_Conversions_Started = 0
    for pd in path_list:
        if is_killed() == True: 
            break
        File_List_Conv = []
        FolderPaths = pathlib.Path(pd.get("path"))
        for x in FolderPaths.iterdir():
            if x.suffix == ".dcm" or x.suffix == ".img":
                File_List_Conv.append(x)
        tempDicom = pydicom.dcmread(File_List_Conv[0])

        # Check if either patient ID or Studdy date is unique, 
        # creates new entries in Subs_dict if needed
        if not Sub_List.Patient_Exists(tempDicom.PatientID):
            Sub_List.add_To_List(tempDicom)
            Print_func("New subject added: "
                        + Sub_List.Get_P_sub_tag(tempDicom))

        Sub_tag = Sub_List.Get_P_sub_tag(tempDicom)
        Ses_tag = Sub_List.Get_P_ses_tag(tempDicom)

        # Creates an apropriate path for the bids nii/json files
        temp_BIDS_Path = create_BIDS_path(Sub_tag, Ses_tag, 
                                          tempDicom, Output_Path)

        # Checks if path already exist, if not creates it
        if not temp_BIDS_Path.exists():
            temp_BIDS_Path.mkdir(parents=True, exist_ok=False)

        ### Generates name
        bf_Name = unique_Name(Sub_tag, Ses_tag, temp_BIDS_Path, 
                              tempDicom, name_run, FolderPaths, Print_func)
        if not bf_Name == False:
            ### Validate Bids
            validate_new_bids(Sub_tag, Ses_tag, bf_Name, tempDicom, 
                              FolderPaths, Print_func)
            
            # Uptdates the PatientLisat and PatientData with the mods
            # of this file
            Sub_List.Uppdate_MODS(tempDicom, getMod(tempDicom))

            # Updates the specifics table list
            detailsDict_temp = getBasics(tempDicom, 
                                         pydicom.dcmread(File_List_Conv[-1]))

            # Update the Cohort Tabel
            Sub_List.Update_Cohort(tempDicom)

            detailsDict_temp["ses_tag"] = Ses_tag
            Sub_List.Update_Details(tempDicom, detailsDict_temp)

            # ### ___________ Threading ____________________
            # # Searches the list of active subprocesses, kills and 
            # # removes finished ones.
            # # Then, if the list is shorter then max amount, 
            # # adds a new suprocess.
            
            # # The segment will loop with a timer untill 
            # # a free slott is found
            # # _____________________________________________
            count_Conversions_Started += 1
            temp_Found_Empty_Thread = False
            try:
                while not temp_Found_Empty_Thread:
                    for r_tas in reversed(Threads_Active_subprocess):
                        if r_tas.poll() is not None:
                            Threads_Active_subprocess.remove(r_tas)
                            r_tas.terminate()
                    if len(Threads_Active_subprocess) <= Number_of_threads:

                        # if getattr(sys, 'frozen', False):
                        #     base_path = sys._MEIPASS
                        # else:
                        #     base_path = os.path.dirname(os.path.abspath(__file__))

                        # dcm2niix_path = os.path.join(base_path, "dcm2niix")
                        dcm2niix_path = "dcm2niix"

                        if zippIt:
                            ### Exports .nii.gz
                            # strst = " ".join([str(dcm2niix_path), " -ba y -z y","-f",
                            #                   bf_Name,"-o",str(temp_BIDS_Path),
                            #                   str(FolderPaths)])

                            strst = [str(dcm2niix_path), 
                                    "-ba",
                                    "y",
                                    "-z",
                                    "y",
                                    "-f",
                                    bf_Name,
                                    "-o",
                                    str(temp_BIDS_Path),
                                    str(FolderPaths)]
                            
                            tempSubPros = subprocess.Popen(strst)
                            Threads_Active_subprocess.append(tempSubPros)
                        else:
                            ### Exports .nii
                            # strst = " ".join([str(dcm2niix_path), " -ba y","-f",bf_Name,
                            #                   "-o",str(temp_BIDS_Path),
                            #                   str(FolderPaths)])
                            strst = [str(dcm2niix_path), 
                                    "-ba", 
                                    "y",
                                    "-f",
                                    bf_Name,
                                    "-o",
                                    str(temp_BIDS_Path),
                                    str(FolderPaths)]
                            
                            tempSubPros = subprocess.Popen(strst)
                            Threads_Active_subprocess.append(tempSubPros)
                        temp_Found_Empty_Thread = True
                        update_status("Converting to bids | Started conversion nr: " 
                                    + str(count_Conversions_Started))
                        time.sleep(0.1)
                    time.sleep(0.001)
            except Exception as e:
                Print_func("Error in converter")
                Print_func(str(e))

                    
    for tas in Threads_Active_subprocess:
        tas.communicate()