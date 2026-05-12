import xlsxwriter
import pathlib
import pandas

def Write_Patient_Data(Patient_List, out_path):
    """Input: PatientList object, pathlib object for output\n
    Reads the list of modalities in PatientList and writes
    it to an excel (xlsx) file, with every key being a column\n
    Does the same for the lists in every individual patient"""
    
    headers = ["pet"  , "cbf", "cbv", "asl" , "dsc", "dce", "dwi", 
               "FLAIR", "T1w", "T2w", "mrsi", "svs", "swi"]
    
    ### Overarching table
    # Creates tools for formating empty columns
    recordEmptyCols = []
    for titels in headers:
        recordEmptyCols.append(False)

    ### Modality table for entire dataset
    table_path = out_path / "Modality_Table.xlsx"  
    book = xlsxwriter.Workbook(str(table_path))
    all_List = Patient_List.Total_mod_list.copy()
    with book as workbook:
        # Add worksheet
        worksheet = workbook.add_worksheet("MainTable")
        colInt = 0
        for head in headers:
            cf_2 = book.add_format({'bold':True, 
                                    'bg_color':'gray'})
            worksheet.write(0, colInt, str(head), cf_2)
            worksheet.write(0, colInt + 1, (str(head) + ": nr"), cf_2)
            colInt += 2
        colInt = 0
        for col in headers:
            rowInt = 1
            for pairs in all_List:
                if col == pairs.get("mod"):
                    worksheet.write(rowInt, colInt, 
                                    str(pairs.get("desc")))
                    worksheet.write(rowInt, colInt + 1, 
                                    str(pairs.get("NR")))
                    if rowInt == 1:
                        recordEmptyCols[int(colInt/2)] = True
                    rowInt += 1
            colInt += 2
        for rec in range(len(recordEmptyCols)):
                    if recordEmptyCols[rec] == False: 
                        # Cell format 1
                        cf_1 = book.add_format({'bold':True, 
                                                    'bg_color':'Red'})
                        worksheet.write(1, rec, "- - - - -", cf_1)
        worksheet.autofit()
  
    ### Cohort tabel
    table_path = out_path / "Cohort_Table.xlsx"  
    book = xlsxwriter.Workbook(str(table_path))
    all_List = Patient_List.Total_mod_list.copy()
    with book as workbook:
        # Add worksheet
        worksheet = workbook.add_worksheet("CohortTable")
        ###_Format_Styles_
        head_style = book.add_format({'bold':True, 
                                      'bg_color':("#BEBEBE")})
        head_style2 = book.add_format({'bold':True, 
                                      'bg_color':'gray'})
        ###_Extract_Data_
        cohortData = Patient_List.Compile_Cohort()
        amount_FDG = cohortData[4]
        amount_met = cohortData[5]
        amount_rest = cohortData[6]

        ###_Reading_Data_From_Existing_Table_
        if pathlib.Path.exists(table_path):
            df = pandas.read_excel(table_path)
            amount_FDG += df["FDG"][0]
            amount_met += df["metionin"][0]
            amount_rest += df["resterande"][0]
            for key, value in cohortData[0].items():
                cohortData[1][key] += df["FDG"][value-1]
                cohortData[2][key] += df["metionin"][value-1]
                cohortData[3][key] += df["resterande"][value-1]
        ###_Headers______
        worksheet.write(0, 0, "Cohort", head_style2)
        worksheet.write(0, 1, "FDG", head_style2)
        worksheet.write(0, 3, "metionin", head_style2)
        worksheet.write(0, 5, "resterande", head_style2)
        ###_Amount tab___
        worksheet.write(1, 0, "", head_style2)
        worksheet.write(1, 1, amount_FDG, head_style2)
        worksheet.write(1, 2, "", head_style2)
        worksheet.write(1, 3, amount_met, head_style2)
        worksheet.write(1, 4, "", head_style2)
        worksheet.write(1, 5, amount_rest, head_style2)
        worksheet.write(1, 6, "", head_style2)
        ###_Iterate_over_data
        for key, value in cohortData[0].items():
            if key == "Func" or key == "MS" or key == "Anat":
                ### Paint section row
                worksheet.write(value, 0, key, head_style)
                worksheet.write(value, 1, "", head_style)
                worksheet.write(value, 2, "", head_style)
                worksheet.write(value, 3, "", head_style)
                worksheet.write(value, 4, "", head_style)
                worksheet.write(value, 5, "", head_style)
                worksheet.write(value, 6, "", head_style)
            else:
                ### Save Data
                # If statments to write 0 instead of the fraction
                # To avoid division by 0
                worksheet.write(value, 0, key,)
                worksheet.write(value, 1, cohortData[1].get(key))
                if amount_FDG == 0:
                    worksheet.write(value, 2, f"({0:06.2f}%)")
                else:
                    worksheet.write(value, 2,
                        f"({(cohortData[1]
                             .get(key)/amount_FDG)*100:06.2f}%)")
                worksheet.write(value, 3, cohortData[2].get(key))
                if amount_met == 0:
                    worksheet.write(value, 4, f"({0:06.2f}%)")
                else:
                    worksheet.write(value, 4,
                        f"({(cohortData[2]
                             .get(key)/amount_met)*100:06.2f}%)")
                worksheet.write(value, 5, cohortData[3].get(key))
                if amount_rest == 0:
                    worksheet.write(value, 6, f"({0:06.2f}%)")
                else:
                    worksheet.write(value, 6,
                        f"({(cohortData[3]
                             .get(key)/amount_rest)*100:06.2f}%)")         
        # ###_Add_Borders____________________
        # border_style = book.add_format({"Border"      :  2,
        #                                 'border_color': 'black'})
        # worksheet.conditional_format('B2:B20', {'type'  : 'noblanks',
        #                                         'format': border_style})
        # worksheet.conditional_format('C2:D20', {'type'  : 'noblanks',
        #                                         'format': border_style})
        # worksheet.conditional_format('E2:F20', {'type'  : 'noblanks',
        #                                         'format': border_style})
        # worksheet.conditional_format('G2:H20', {'type'  : 'noblanks',
        #                                         'format': border_style})
        # ###_Final_Styling___________________
        worksheet.autofit()
        worksheet.ignore_errors({"number_stored_as_text": 
                                 "C4:C19 E5:E19 G4:G19"})

    
    ### Individual tables
    for pat in Patient_List.SubList:
        all_List = pat.modality_list.copy()
        # Writes a table for every session, only adds entries if 
        # the stored ses-tag matches with session table
        for ses in pat.sesList:
            ### Individual modality
            sestag = pat.Get_Ses_Tag(ses.get('ses_date'))
            sesTableName = (out_path / pat.Get_Sub_Tag() 
                            / str(pat.Get_Sub_Tag() + "_" 
                                  + sestag + "_Modality.xlsx"))
            # Checks if the necesary folders exist, and if the 
            # table is missing
            if (pathlib.Path.exists(out_path / pat.Get_Sub_Tag()) 
                and pathlib.Path.exists(out_path / pat.Get_Sub_Tag() 
                                                 / sestag)
                and not pathlib.Path.exists(sesTableName)):

                # ses table modality
                recordEmptyCols = []
                for titels in headers:
                    recordEmptyCols.append(False)
                book = xlsxwriter.Workbook(out_path / pat.Get_Sub_Tag() 
                                                    / str(pat.Get_Sub_Tag() 
                                                        + "_" + sestag
                                                        + "_Modality.xlsx"))
                with book as workbook:
                    # Add worksheet
                    worksheet = workbook.add_worksheet("Patient table")
                    colInt = 0
                    for head in headers:
                        cf_2 = book.add_format({'bold':True, 
                                    'bg_color':'gray'})
                        worksheet.write(0, colInt, str(head), cf_2)
                        colInt += 1
                    colInt = 0
                    for col in headers:
                        rowInt = 1
                        for pairs in all_List:
                            if col == pairs.get("mod"):
                                # If the data was saved
                                if pairs.get("date") == sestag:
                                    worksheet.write(rowInt, colInt, 
                                                    str(pairs.get("desc")))
                                    if rowInt == 1:
                                        recordEmptyCols[colInt] = True
                                    rowInt += 1
                        colInt += 1
                    for rec in range(len(recordEmptyCols)):
                        if recordEmptyCols[rec] == False: 
                            # Cell format 1
                            cf_1 = book.add_format({'bold':True, 
                                                        'bg_color':'Red'})
                            worksheet.write(1, rec, "- - - - -", cf_1)
                    worksheet.autofit()
                
                # ses details table
                book = xlsxwriter.Workbook(out_path / pat.Get_Sub_Tag() 
                                                    / str(pat.Get_Sub_Tag() 
                                                        + "_" + sestag
                                                        + "_Details.xlsx"))
                with book as workbook:
                    worksheet = workbook.add_worksheet("Details table")
                    detai_list = pat.Details_List
                    column_heads = ["ses_tag"   , "Modality", 
                                    "Avbildning", "Options" ]
                    cf_1 = book.add_format({'bold':True, 
                                                'bg_color':'gray'})
                    colInt = 0
                    for ch in column_heads:
                        worksheet.write(0, colInt, str(ch), cf_1)
                        colInt += 1
                    rowInt = 0
                    for head in headers:
                        for det in detai_list:
                            if (det.get("Modality") == str(head) and
                                det.get("ses_tag" ) == str(sestag)):
                                rowInt += 1
                                colInt = 0
                                for col in column_heads:
                                    worksheet.write(rowInt, colInt, 
                                                    det.get(col))
                                    colInt += 1
                            worksheet.write(0, 5, "Vikt", cf_1)
                            worksheet.write(1, 5, det.get("Weight"))
                    worksheet.autofit()
