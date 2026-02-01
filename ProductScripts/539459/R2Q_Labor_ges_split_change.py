def R2Q_Replace_GES_values(gesLocation):
    Trace.Write("SM Event Run start")
    gesLocation=gesLocation
    laborCont = Product.GetContainerByName('SM_SSE_Engineering_Labor_Container')
    tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Execution_Country from SAFETY_MANAGER_LABOR_SSE_ENGINEERING_LABOR')
    if laborCont.Rows.Count > 0:
        for new_row in laborCont.Rows:
            for row in tableLabor:
                if  new_row["Deliverable"]  ==  row.Deliverable:
                    if gesLocation == "None" or gesLocation == '':
                        new_row["GES Eng % Split"]= row.GES_Eng_1_No
                        new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
                        new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
                        new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                        new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                        new_row['FO Eng 1']=row.FO_Eng_1_NoGES
                        new_row['FO Eng 2']=row.FO_Eng_2_NoGES
                    else:
                        if gesLocation !="None":
                            new_row["GES Eng % Split"]= row.GES_Eng
                            new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
                            new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
                            new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                            new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                            new_row['FO Eng 1']=row.FO_Eng_1_NoGES
                            new_row['FO Eng 2']=row.FO_Eng_2_NoGES
        laborCont.Calculate()
    laborCont1 = Product.GetContainerByName('SM Safety System - ESD/FGS/BMS/HIPPS Container')
    tableLabor1 = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Execution_Country from SAFETY_MANAGER_LABOR_SSE_ENGINEERING_LABOR_TWO')
    if laborCont1.Rows.Count > 0:
        for new_row in laborCont1.Rows:
            for row in tableLabor1:
                if  new_row["Deliverable"]  ==  row.Deliverable:
                    if gesLocation == "None" or gesLocation == '':
                        new_row["GES Eng % Split"]= row.GES_Eng_1_No
                        new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
                        new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
                        new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                        new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                        new_row["FO Eng 1"]= row.FO_Eng_1_NoGES
                        new_row["FO Eng 2"]= row.FO_Eng_2_NoGES
                    else:
                        if gesLocation !="None" :
                            new_row["GES Eng % Split"]= row.GES_Eng
                            new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
                            new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
                            new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                            new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                            new_row["FO Eng 1"]= row.FO_Eng_1_NoGES
                            new_row["FO Eng 2"]= row.FO_Eng_2_NoGES
                        Trace.Write("SM Event Run end")
        laborCont1.Calculate()
gesLocation=''
if Product.GetContainerByName('SM_Labor_Cont').Rows.Count > 0 :
    gesLocation = Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('GES_Location').Value
    if gesLocation not in ["None",""] and Product.Attr('R2Q_GES_Change').GetValue()=="None" and Quote.GetCustomField("isR2QRequest").Content:
        run=R2Q_Replace_GES_values(gesLocation)