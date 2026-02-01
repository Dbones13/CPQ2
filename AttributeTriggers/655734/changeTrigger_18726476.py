gesLocation = Product.Attr("Terminal_Ges_Location_Labour").GetValue()
laborCont = Product.GetContainerByName('Terminal Engineering Labor Container')
tableLabor = SqlHelper.GetList('select Deliverable,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1_NoGES,FO_Eng_1_GES,FO1_Eng,FO_Eng_2,FO2_Eng,Rank,Execution_Country from TERMINAL_ENGINEERING_DELIVERABLES')
if laborCont.Rows.Count > 0:
    for new_row in laborCont.Rows:
        for row in tableLabor:
            if  new_row["Deliverable"]  ==  row.Deliverable:
                if gesLocation == "None" or gesLocation == '':
                    new_row["GES Eng % Split"]= row.GES_Eng_NoGES
                    new_row["FO Eng 1 % Split"]= row.FO_Eng_1_NoGES
                    new_row["FO Eng 2 % Split"]= "0"
                elif TagParserProduct.ParseString('<*CTX( Container(Terminal Engineering Labor Container).Column(GES Eng).GetPermission )*>') == "Hidden":
                    new_row["GES Eng % Split"]= row.GES_Eng_GES
                    new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
                    new_row["FO Eng 2 % Split"]= "0"
    if gesLocation != "None" or gesLocation != "":
        TagParserProduct.ParseString('<*CTX( Container(Terminal Engineering Labor Container).Column(GES Eng).SetPermission(Editable) )*>')
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
    laborCont.Calculate()