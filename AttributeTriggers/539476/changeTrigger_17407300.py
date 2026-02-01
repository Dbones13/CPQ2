gesLocation = Product.Attr("FDM_GES_Location").GetValue()
laborCont = Product.GetContainerByName('FDM Engineering Labor Container')
tableLabor = SqlHelper.GetList('select Deliverable,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1_NoGES,FO_Eng_1_GES,FO1_Eng_NoGES,FO1_Eng_GES,FO_Eng_2_NoGES,FO_Eng_2_GES,FO2_Eng_NoGES,FO2_Eng_GES,Rank,Execution_Country from FDM_ENGINEERING_DELIVERABLES')
if laborCont.Rows.Count > 0:
    for new_row in laborCont.Rows:
        for row in tableLabor:
            if  new_row["Deliverable"]  ==  row.Deliverable:
                if gesLocation == "None" or gesLocation == '':
                    new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                    new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                    new_row['FO Eng 1']=row.FO_Eng_1_NoGES
                    new_row['FO Eng 2']=row.FO_Eng_2_NoGES
                    new_row["GES Eng % Split"]= row.GES_Eng_NoGES
                    new_row["FO Eng 1 % Split"]= row.FO1_Eng_NoGES
                    new_row["FO Eng 2 % Split"]= row.FO2_Eng_NoGES
                elif TagParserProduct.ParseString('<*CTX( Container(FDM Engineering Labor Container).Column(GES Eng).GetPermission )*>') == "Hidden":
                    Trace.Write("if")
                    new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_GES)
                    new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_GES)
                    new_row['FO Eng 1']=row.FO_Eng_1_GES
                    new_row['FO Eng 2']=row.FO_Eng_2_GES
                    new_row["GES Eng % Split"]= row.GES_Eng_GES
                    new_row["FO Eng 1 % Split"]= row.FO1_Eng_GES
                    new_row["FO Eng 2 % Split"]= row.FO2_Eng_GES
    if gesLocation != "None":
        TagParserProduct.ParseString('<*CTX( Container(FDM Engineering Labor Container).Column(GES Eng).SetPermission(Editable) )*>')
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
    laborCont.Calculate()