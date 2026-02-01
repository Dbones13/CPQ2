gesLocation = TagParserProduct.ParseString('<* Value(C300_GES_Location) *>')
laborCont = Product.GetContainerByName('eServer_Labor_Container')
tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_NEGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_NEGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from eServer_Labor_Deliverables')
if laborCont.Rows.Count > 0:
    for new_row in laborCont.Rows:
        for row in tableLabor:
            if  new_row["Deliverable"]  ==  row.Deliverable:
                if gesLocation == "None" or gesLocation == '':
                    Product.Attr('eServer_labor_GES_check').AssignValue('None')
                    new_row["GES Eng % Split"]= row.GES_Eng_1_No
                    new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
                    new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
                    new_row.GetColumnByName('FO Eng 1').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_1_NoGES)
                    new_row.GetColumnByName('FO Eng 2').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_2_NoGES)
                    new_row['FO Eng 1']=row.FO_Eng_1_NoGES
                    new_row['FO Eng 2']=row.FO_Eng_2_NoGES
                    #new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                    #new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                else:
                    if Product.Attr('eServer_labor_GES_check').GetValue() != "Country":
                        new_row["GES Eng % Split"]= row.GES_Eng
                        new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
                        new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
                        new_row.GetColumnByName('FO Eng 1').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_1_NEGES)
                        new_row.GetColumnByName('FO Eng 2').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_2_NEGES)
                        new_row['FO Eng 1']=row.FO_Eng_1_NEGES
                        new_row['FO Eng 2']=row.FO_Eng_1_NEGES
                    Product.Attr('eServer_labor_GES_check').AssignValue('Country')
    laborCont.Calculate()
    ScriptExecutor.Execute('PS_Populate_Prices')