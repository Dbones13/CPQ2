tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
scope = Product.Attr('CE_Scope_Choices').GetValue()
Product.Attr('ErrorMessage1').AssignValue('')
if (('Labor Deliverables' in tabs or 'General Inputs' in tabs) and scope == 'HW/SW + LABOR'):
    gesLocation = Product.Attr('MXPro_GES_Location').GetValue()
    count = count1 = count2 = 0
    Labor_Message = Labor_Message2 = Labor_Message3 = ""

    #Error Message for MXPro_Labor_Additional_Cust_Deliverables_con
    mxproline_Error_Message_val = mxproline_Error_Message_val2 = ""
    deliverables = Product.GetContainerByName('MXPro_Labor_Additional_Cust_Deliverables_con')
    count = count1 = 0
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
        split = 100.0
        FO1_Eng_New = 0
        if(GES_Eng in range(101)):
            split = float(GES_Eng + FO1_Eng )
            FO1_Eng_New = float(100 - GES_Eng)
        if split != 100.0 and row.GetColumnByName('Final Hrs').Value not in ('','0','0.0') and deliverable != '':
            count +=1
            mxproline_Error_Message_val = mxproline_Error_Message_val + " - " +str(deliverable) + "<br>"
        FO_Eng_1_val = row.GetColumnByName('FO Eng').DisplayValue
        FO1_Eng = float(row.GetColumnByName('FO Eng % Split').Value)
        finalHrs = row.GetColumnByName('Final Hrs').Value

        if (finalHrs not in ('','0','0.0') and ((FO_Eng_1_val == '' or FO_Eng_1_val == 'None') and FO1_Eng_New > 0)):
            count1 = count1 + 1
            mxproline_Error_Message_val2 = mxproline_Error_Message_val2 + " - " +str(deliverable) + "<br>"
        if (finalHrs not in ('','0','0.0') and ((FO_Eng_1_val != '' and FO_Eng_1_val != 'None' and FO1_Eng_Cost == 0 and FO1_Eng > 0) or (GES_Eng_Val != '' and GES_Eng_Val != 'None' and GES_Eng_Cost == 0 and GES_Eng > 0))):
            count2 = count2 + 1
            Labor_Message3 = Labor_Message3 + " - " +str(deliverable) + "<br>"
    #if count > 0:
        #mxproline_Error_Message_val =  "<b>"+'Hours distribution among resources is not 100%. Please adjust the % Split column value to get the total 100% <br>'+"</b>" + mxproline_Error_Message_val
        #if Labor_Message != "":
            #Labor_Message += "<br>" + mxproline_Error_Message_val
        #else:
            #Labor_Message = mxproline_Error_Message_val

    if count1 > 0:
        mxproline_Error_Message_val2 = "<b>"+'Resource is not selected for deliverable. Please select respective Eng or change the Eng % Split to 0% <br>'+"</b>" + mxproline_Error_Message_val2
        if Labor_Message != "":
            Labor_Message += "<br>" + mxproline_Error_Message_val2
        else:
            Labor_Message = mxproline_Error_Message_val2
    if count2 > 0:
        Labor_Message3 = "<b>"+'Cost is not available for selected resource in Additional Custom Deliverables. Please select different resource or different Execution Country.Deliverables to look into: <br>'+"</b>" + Labor_Message3
        if Labor_Message != "":
            Labor_Message += "<br>" + Labor_Message3
        else:
            Labor_Message = Labor_Message3
    if Labor_Message != '':
        Product.Attr('ErrorMessage1').AssignValue(Labor_Message)