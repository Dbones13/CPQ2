tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
scope = ''
if Product.GetContainerByName('CE_SystemGroup_Cont').Rows.Count > 0:
    scope = Product.GetContainerByName('CE_SystemGroup_Cont').Rows[0].GetColumnByName('Scope').Value
def getfloat(var):
    if var:
        return float(var)
    return 0.0
    
Product.Attr('ErrorMessage1').AssignValue('')
Product.Attr('ErrorMessage4').AssignValue('')
Product.Attr('ErrorMessage5').AssignValue('')
Product.Attr('ErrorMessage6').AssignValue('')

if (('PM Labor Deliverables' in tabs or 'General Inputs' in tabs) and scope == 'HWSWLABOR'):
    #Error Message for Safety Manager Engineering Labor Container
    try: #script was replecating error in R2Q quote
        gesLocation = Product.GetContainerByName('Labor_Details_New/Expansion_Cont').Rows[0].GetColumnByName('GES_Location').Value
    except:
        gesLocation = "None"
    #gesLocation = Product.GetContainerByName('Labor_Details_New/Expansion_Cont').Rows[0].GetColumnByName('GES_Location').Value
    containers = {
        'Labor_Container': 'ErrorMessage1',
        'Project_management_Labor_Container': 'ErrorMessage4',
        'PLE_Labor_Container': 'ErrorMessage5'
    }
    for container_name, error_message_attr in containers.items():
        deliverables = Product.GetContainerByName(container_name).Rows
        count = count1 = count2 = 0
        Labor_Message = Labor_Message1 = Labor_Message2 = Labor_Message3 =Labor_Message4 = ""
        for row in deliverables:
            deliverable = row.GetColumnByName('Deliverable')
            GES_Eng = FO1_Eng = FO2_Eng = FO1_Eng_Cost = FO2_Eng_Cost = GES_Eng_Cost = 0
            if row.GetColumnByName('GES Eng % Split').Value not in ('','0') and (gesLocation != "None" or gesLocation != ''):
                GES_Eng = float(row.GetColumnByName('GES Eng % Split').Value)
            if row.GetColumnByName('FO Eng 1 % Split').Value not in ('','0'):
                FO1_Eng = float(row.GetColumnByName('FO Eng 1 % Split').Value)
            if row.GetColumnByName('FO Eng 2 % Split').Value not in ('','0'):
                FO2_Eng = float(row.GetColumnByName('FO Eng 2 % Split').Value)
            if row.GetColumnByName('FO Eng 2 % Split').Value not in ('','0'):
                FO2_Eng = float(row.GetColumnByName('FO Eng 2 % Split').Value)
            if row.GetColumnByName('FO_Eng_1_Unit_Regional_Cost').Value not in ('','0'):
                FO1_Eng_Cost = float(row.GetColumnByName('FO_Eng_1_Unit_Regional_Cost').Value)
            if row.GetColumnByName('FO_Eng_2_Unit_Regional_Cost').Value not in ('','0'):
                FO2_Eng_Cost = float(row.GetColumnByName('FO_Eng_2_Unit_Regional_Cost').Value)
            if row.GetColumnByName('GES_Unit_Regional_Cost').Value not in ('','0'):
                GES_Eng_Cost = float(row.GetColumnByName('GES_Unit_Regional_Cost').Value)
            GES_Eng_Val = row.GetColumnByName('GES Eng').Value
            FO1_Eng_New = 0
            if(GES_Eng in range(101) and FO2_Eng in range(101)):
                
                FO1_Eng_New = float(100 - GES_Eng - FO2_Eng)
            if FO1_Eng_New < 0:
                count +=1
                Labor_Message = Labor_Message + " - " +str(deliverable.Value) + "<br>"
                Trace.Write("DP2 " +str(Labor_Message))

            FO_Eng_1_val = row.GetColumnByName('FO Eng 1').DisplayValue
            FO1_Eng = getfloat(row.GetColumnByName('FO Eng 1 % Split').Value)

            FO_Eng_2_val = row.GetColumnByName('FO Eng 2').DisplayValue
            FO2_Eng = getfloat(row.GetColumnByName('FO Eng 2 % Split').Value)
            finalHrs = row.GetColumnByName('Final Hrs').Value

            #if ((FO_Eng_2_val == '' or FO_Eng_2_val == 'None') and FO2_Eng > 0 ) or ((FO_Eng_1_val == '' or FO_Eng_1_val == 'None') and FO1_Eng > 0):
            if (finalHrs not in ('','0','0.0') and (((FO_Eng_2_val == '' or FO_Eng_2_val == 'None') and FO2_Eng > 0) or ((FO_Eng_1_val == '' or FO_Eng_1_val == 'None') and FO1_Eng > 0))):
                count1 = count1 + 1
                Labor_Message2 = Labor_Message2 + " - " +str(deliverable.Value) + "<br>"
            if (finalHrs not in ('','0','0.0') and ((FO_Eng_2_val != '' and FO_Eng_2_val != 'None' and FO2_Eng_Cost == 0 and FO2_Eng > 0) or (FO_Eng_1_val != '' and FO_Eng_1_val != 'None' and FO1_Eng_Cost == 0 and FO1_Eng > 0) or (GES_Eng_Val != '' and GES_Eng_Val != 'None' and GES_Eng_Cost == 0 and GES_Eng > 0))):
                count2 = count2 + 1
                Labor_Message3 = Labor_Message3 + " - " +str(deliverable.Value) + "<br>"
        if count > 0:
            Labor_Message = "<b>"+'Hours distribution among resources is not 100%. Please adjust the % Split column value to get the total 100% <br>'+"</b>" + Labor_Message

        if count1 > 0:
            Labor_Message2 = "<b>"+'Resource is not selected for deliverable. Please select respective Eng or change the Eng % Split to 0% <br>'+"</b>" + Labor_Message2
            if Labor_Message != "":
                Labor_Message += "<br>" + Labor_Message2
            else:
                Labor_Message = Labor_Message2
        if count2 > 0:
            Labor_Message3 = "<b>"+'Cost is not available for selected resource in '+ str(Product.Attr(container_name).LabelFormula) +'. Please select different resource or different Execution Country.Deliverables to look into: <br>'+"</b>" + Labor_Message3
            if Labor_Message != "":
                Labor_Message += "<br>" + Labor_Message3
            else:
                Labor_Message = Labor_Message3
        if Labor_Message != '':
            Product.Attr(error_message_attr).AssignValue(Labor_Message)
    
    #PS_Additional_Error_Message
    deliverables = Product.GetContainerByName('PM_Additional_Custom_Deliverables_Labor_Container').Rows
    count = count1 = count2 = 0
    Labor_Message = Labor_Message2 = Labor_Message3 = ""
    for row in deliverables:
        deliverable = row["Deliverable Name"] if row["Deliverable Name"] else row['Standard Deliverable']
        GES_Eng = FO1_Eng = FO1_Eng_Cost = GES_Eng_Cost = 0
        if row.GetColumnByName('GES Eng % Split').Value not in ('','0') and (gesLocation != "None" or gesLocation != ''):
            GES_Eng = float(row.GetColumnByName('GES Eng % Split').Value)
        if row.GetColumnByName('FO Eng % Split').Value not in ('','0'):
            FO1_Eng = float(row.GetColumnByName('FO Eng % Split').Value)
        if row.GetColumnByName('FO_Eng_1_Unit_Regional_Cost').Value not in ('','0'):
            FO1_Eng_Cost = float(row.GetColumnByName('FO_Eng_1_Unit_Regional_Cost').Value)
        if row.GetColumnByName('GES_Unit_Regional_Cost').Value not in ('','0'):
            GES_Eng_Cost = float(row.GetColumnByName('GES_Unit_Regional_Cost').Value)
        GES_Eng_Val = row.GetColumnByName('GES Eng').Value
        split = 100
        FO1_Eng_New = 0
        if(GES_Eng in range(101)):
            split = float(GES_Eng + FO1_Eng )
            FO1_Eng_New = float(100 - GES_Eng)
        if FO1_Eng_New < 0:
            count +=1
            Labor_Message = Labor_Message + " - " +str(deliverable.Value) + "<br>"

        FO_Eng_1_val = row.GetColumnByName('FO Eng').DisplayValue
        FO1_Eng = getfloat(row.GetColumnByName('FO Eng % Split').Value)
        finalHrs = row.GetColumnByName('Final Hrs').Value
        if ((FO_Eng_1_val == '' or FO_Eng_1_val == 'None') and FO1_Eng_New > 0 and deliverable != ''):
            count1 = count1 + 1
            Labor_Message2 = Labor_Message2 + " - " +str(deliverable) + "<br>"
        if (finalHrs not in ('','0','0.0') and ((FO_Eng_1_val != '' and FO_Eng_1_val != 'None' and FO1_Eng_Cost == 0 and FO1_Eng > 0) or (GES_Eng_Val != '' and GES_Eng_Val != 'None' and GES_Eng_Cost == 0 and GES_Eng > 0))):
            count2 = count2 + 1
            Labor_Message4 = Labor_Message4 + " - " +str(deliverable) + "<br>"
    if count1 > 0:
        Labor_Message2 = "<b>"+'Resource is not selected for deliverable. Please select respective Eng or change the Eng % Split to 0% <br>'+"</b>" + Labor_Message2
        if Labor_Message != "":
            Labor_Message += "<br>" + Labor_Message2
        else:
            Labor_Message = Labor_Message2
    if count2 > 0:
        Labor_Message3 = "<b>"+'Cost is not available for selected resource in Additional Custom Deliverables. Please select different resource or different Execution Country.Deliverables to look into: <br>'+"</b>" + Labor_Message3
        if Labor_Message != "":
            Labor_Message += "<br>" + Labor_Message3
        else:
            Labor_Message = Labor_Message3
    if Labor_Message != '':
        Trace.Write("Labor_Message"+str(Labor_Message))
        Product.Attr('ErrorMessage6').AssignValue(Labor_Message)
