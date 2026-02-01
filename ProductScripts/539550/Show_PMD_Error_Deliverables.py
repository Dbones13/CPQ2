tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
Product.Attr('Error_Message_1').AssignValue('')
if 'Labor Deliverables' in tabs or 'General Inputs' in tabs:
    deliverables = Product.GetContainerByName('PMD Engineering Labor Container').Rows
    gesLocation = Product.GetContainerByName('PMD_Labour_Details').Rows[0].GetColumnByName('PMD_Ges_Location').Value
    count = count1 = count2 = 0
    Labor_Message = Labor_Message2 = Labor_Message3 = ""

    for row in deliverables:
        deliverable = row.GetColumnByName('Deliverable')
        GES_Eng = FO1_Eng = FO2_Eng = FO1_Eng_Cost = FO2_Eng_Cost = GES_Eng_Cost = 0
        if row.GetColumnByName('GES Eng % Split').Value not in ('','0') and (gesLocation != "None" or gesLocation != ''):
            GES_Eng = float(row.GetColumnByName('GES Eng % Split').Value)
        if row.GetColumnByName('FO Eng 1 % Split').Value not in ('','0'):
            FO1_Eng = float(row.GetColumnByName('FO Eng 1 % Split').Value)
        if row.GetColumnByName('FO Eng 2 % Split').Value not in ('','0'):
            FO2_Eng = float(row.GetColumnByName('FO Eng 2 % Split').Value)
        if row.GetColumnByName('FO_Eng_1_Unit_Regional_Cost').Value not in ('','0'):
            FO1_Eng_Cost = float(row.GetColumnByName('FO_Eng_1_Unit_Regional_Cost').Value)
        if row.GetColumnByName('FO_Eng_2_Unit_Regional_Cost').Value not in ('','0'):
            FO2_Eng_Cost = float(row.GetColumnByName('FO_Eng_2_Unit_Regional_Cost').Value)
        if row.GetColumnByName('GES_Unit_Regional_Cost').Value not in ('','0'):
            GES_Eng_Cost = float(row.GetColumnByName('GES_Unit_Regional_Cost').Value)
        GES_Eng_Val = row.GetColumnByName('GES Eng').Value
        split = float(GES_Eng + FO1_Eng + FO2_Eng)
        if split != 100 and row["Final Hrs"] not in ('','0'):
            count +=1
            Labor_Message = Labor_Message + " - " +str(deliverable.Value) + "<br>"

        #CXCPQ-23786
        FO_Eng_1_val = row.GetColumnByName('FO Eng 1').DisplayValue
        FO1_Eng = float(row.GetColumnByName('FO Eng 1 % Split').Value)

        FO_Eng_2_val = row.GetColumnByName('FO Eng 2').DisplayValue
        FO2_Eng = float(row.GetColumnByName('FO Eng 2 % Split').Value)
        finalHrs = row.GetColumnByName('Final Hrs').Value


        if (finalHrs not in ('','0','0.0') and (((FO_Eng_2_val == '' or FO_Eng_2_val == 'None') and FO2_Eng > 0) or ((FO_Eng_1_val == '' or FO_Eng_1_val == 'None') and FO1_Eng > 0))):
            count1 = count1 + 1
            Labor_Message2 = Labor_Message2 + " - " +str(deliverable.Value) + "<br>"
        if (finalHrs not in ('','0','0.0') and ((FO_Eng_2_val != '' and FO_Eng_2_val != 'None' and FO2_Eng_Cost == 0 and FO2_Eng > 0) or (FO_Eng_1_val != '' and FO_Eng_1_val != 'None' and FO1_Eng_Cost == 0 and FO1_Eng > 0) or (GES_Eng_Val != '' and GES_Eng_Val != 'None' and GES_Eng_Cost == 0 and GES_Eng > 0))):
            count2 = count2 + 1
            Labor_Message3 = Labor_Message3 + " - " +str(deliverable.Value) + "<br>"

    if count > 0:
        Labor_Message = "<b>"+'Hours distribution among resources is not 100%. Please adjust the % Split column value to get the total 100% <br>'+"</b>" + Labor_Message
        Product.Attr('ErrorMessage').AssignValue('True')
    else :
        Product.Attr('ErrorMessage').AssignValue('False')

    if count1 > 0:
        Labor_Message2 = "<b>"+'Resource is not selected for deliverable. Please select respective Eng or change the Eng % Split to 0% <br>'+"</b>" + Labor_Message2
        if Labor_Message != "":
			Labor_Message += "<br>" + Labor_Message2
        else:
            Labor_Message = Labor_Message2
    if count2 > 0:
        Labor_Message3 = "<b>"+'Cost is not available for selected resource in PMD Engineering Labor Container.Please select different resource or different Execution Country.Deliverables to look into: <br>'+"</b>" + Labor_Message3
        if Labor_Message != "":
            Labor_Message += "<br>" + Labor_Message3
        else:
            Labor_Message = Labor_Message3
    if Labor_Message != "":
        Product.Attr('Error_Message_1').AssignValue(Labor_Message)


    #Error Message for PMD Labor Additional Custom Deliverable
    PMD_Error_Message_val = ""
    deliverables = Product.GetContainerByName('PMD Labor Additional Custom Deliverable')
    count = count2 = 0
    Labor_Message3 = ''
    for row in deliverables.Rows:
        deliverable = row["Deliverable Name"] if row["Deliverable Name"] else row['Standard Deliverable']
        GES_Eng = FO1_Eng = FO1_Eng_Cost = GES_Eng_Cost = 0
        if row.GetColumnByName('GES Eng % Split').Value not in ('','0'):
            GES_Eng = float(row.GetColumnByName('GES Eng % Split').Value)
        if row.GetColumnByName('FO Eng % Split').Value not in ('','0'):
            FO1_Eng = float(row.GetColumnByName('FO Eng % Split').Value)
        if row.GetColumnByName('FO_Eng_1_Unit_Regional_Cost').Value not in ('','0'):
            FO1_Eng_Cost = float(row.GetColumnByName('FO_Eng_1_Unit_Regional_Cost').Value)
        if row.GetColumnByName('GES_Unit_Regional_Cost').Value not in ('','0'):
            GES_Eng_Cost = float(row.GetColumnByName('GES_Unit_Regional_Cost').Value)
        GES_Eng_Val = row.GetColumnByName('GES Eng').Value
        FO_Eng_1_val = row.GetColumnByName('FO Eng').DisplayValue
        finalHrs = row.GetColumnByName('Final Hrs').Value
        split = float(GES_Eng + FO1_Eng )
        if split != 100 and row["Final Hrs"] not in ('','0'):
            count +=1
            PMD_Error_Message_val = PMD_Error_Message_val + " - " +str(deliverable) + "<br>"
        if (finalHrs not in ('','0','0.0') and ((FO_Eng_1_val != '' and FO_Eng_1_val != 'None' and FO1_Eng_Cost == 0 and FO1_Eng > 0) or (GES_Eng_Val != '' and GES_Eng_Val != 'None' and GES_Eng_Cost == 0 and GES_Eng > 0))):
            count2 = count2 + 1
            Labor_Message3 = Labor_Message3 + " - " +str(deliverable) + "<br>"

    if count > 0:
        PMD_Error_Message_val =  "<b>"+'Hours distribution among resources is not 100%. Please adjust the % Split column value to get the total 100% <br>'+"</b>" + PMD_Error_Message_val
        Product.Attr('PMD_Error_Message_Custom').AssignValue('True')
    else:
        Product.Attr('PMD_Error_Message_Custom').AssignValue('False')
    if count2 > 0:
        Labor_Message3 = "<b>"+'Cost is not available for selected resource in Additional Custom Deliverables. Please select different resource or different Execution Country.Deliverables to look into: <br>'+"</b>" + Labor_Message3
        if Labor_Message != "":
            Labor_Message += "<br>" + Labor_Message3
        else:
            Labor_Message = Labor_Message3
    if Labor_Message != "":
        Product.Attr('Error_Message_1').AssignValue(Labor_Message)
    if PMD_Error_Message_val != "":
        Product.ErrorMessages.Add(str(PMD_Error_Message_val))