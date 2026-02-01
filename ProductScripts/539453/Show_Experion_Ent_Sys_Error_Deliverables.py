tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
scope = Product.Attr('CE_Scope_Choices').GetValue()
Product.Attr('ErrorMessage').AssignValue('')
if (('Labor Deliverables' in tabs or 'General Inputs' in tabs) and scope == 'HW/SW + LABOR'):
    
    #Error Message for Experion Enterprise Sys Hardware Engineering Labor Container
    deliverables = Product.GetContainerByName('Hardware Engineering Labour Container').Rows
    gesLocation = gesLocation = Product.Attr("Experion_HS_Ges_Location_Labour").GetValue()
    count = count1 = 0
    Labor_Message = Labor_Message2 = ""

    for row in deliverables:
        deliverable = row.GetColumnByName('Deliverable')
        GES_Eng = FO1_Eng = FO2_Eng = 0
        if row.GetColumnByName('GES Eng % Split').Value not in ('','0') and (gesLocation != "None" or gesLocation != ''):
            GES_Eng = float(row.GetColumnByName('GES Eng % Split').Value)
        if row.GetColumnByName('FO Eng 1 % Split').Value not in ('','0'):
            FO1_Eng = float(row.GetColumnByName('FO Eng 1 % Split').Value)
        if row.GetColumnByName('FO Eng 2 % Split').Value not in ('','0'):
            FO2_Eng = float(row.GetColumnByName('FO Eng 2 % Split').Value)

        FO1_Eng_New = 0
        if(GES_Eng in range(101) and FO2_Eng in range(101)):
            FO1_Eng_New = float(100 - GES_Eng - FO2_Eng)

        if FO1_Eng_New < 0 and row.GetColumnByName('Final Hrs').Value not in ('','0','0.0'):
            #Trace.Write("GES_Eng:{} FO1_Eng:{} FO2_Eng:{} diff:{} Final Hrs:{}".format(GES_Eng, FO1_Eng, FO2_Eng, diff,row["Final Hrs"]))
            count +=1
            Labor_Message = Labor_Message + " - " +str(deliverable.Value) + "<br>"

        FO_Eng_1_val = row.GetColumnByName('FO Eng 1').DisplayValue
        FO1_Eng = float(row.GetColumnByName('FO Eng 1 % Split').Value)

        FO_Eng_2_val = row.GetColumnByName('FO Eng 2').DisplayValue
        FO2_Eng = float(row.GetColumnByName('FO Eng 2 % Split').Value)
        finalHrs = row.GetColumnByName('Final Hrs').Value

        #if ((FO_Eng_2_val == '' or FO_Eng_2_val == 'None') and FO2_Eng > 0 ) or ((FO_Eng_1_val == '' or FO_Eng_1_val == 'None') and FO1_Eng > 0):
        if (finalHrs not in ('','0','0.0') and ((FO_Eng_2_val == '' or FO_Eng_2_val == 'None') and FO2_Eng > 0 and FO2_Eng <= 100) or ((FO_Eng_1_val == '' or FO_Eng_1_val == 'None') and FO1_Eng_New > 0)):
            count1 = count1 + 1
            Labor_Message2 = Labor_Message2 + " - " +str(deliverable.Value) + "<br>"

    if count > 0:
        Labor_Message = "<b>"+'Hours distribution among resources is not 100%. Please adjust the % Split column value to get the total 100% <br>'+"</b>" + Labor_Message

    if count1 > 0:
        Labor_Message2 = "<b>"+'Resource is not selected for deliverable. Please select respective Eng or change the Eng % Split to 0% <br>'+"</b>" + Labor_Message2
        if Labor_Message != "":
            Labor_Message += "<br>" + Labor_Message2
        else:
            Labor_Message = Labor_Message2

    #Error Message for Experion Enterprise sys Additional Custom Deliverables
    Experion_Error_Message_val = Experion_Error_Message_val2 = ""
    deliverables = Product.GetContainerByName('Additional_CustomDev_Labour_Container')
    count = count1 = 0
    for row in deliverables.Rows:
        deliverable = row["Deliverable Name"] if row["Deliverable Name"] else row['Standard Deliverable']
        GES_Eng = FO1_Eng = 0
        if row.GetColumnByName('GES Eng % Split').Value not in ('','0'):
            GES_Eng = float(row.GetColumnByName('GES Eng % Split').Value)
        if row.GetColumnByName('FO Eng % Split').Value not in ('','0'):
            FO1_Eng = float(row.GetColumnByName('FO Eng % Split').Value)
        split = 100
        FO1_Eng_New = 0
        if(GES_Eng in range(101)):
            split = float(GES_Eng + FO1_Eng )
            FO1_Eng_New = float(100 - GES_Eng)
        if split != 100 and row.GetColumnByName('Final Hrs').Value not in ('','0','0.0') and deliverable != '':
            count +=1
            Experion_Error_Message_val = Experion_Error_Message_val + " - " +str(deliverable) + "<br>"
        FO_Eng_1_val = row.GetColumnByName('FO Eng').DisplayValue
        FO1_Eng = float(row.GetColumnByName('FO Eng % Split').Value)
        finalHrs = row.GetColumnByName('Final Hrs').Value

        if (finalHrs not in ('','0','0.0') and (FO_Eng_1_val == '' or FO_Eng_1_val == 'None') and FO1_Eng_New > 0):
            count1 = count1 + 1
            Experion_Error_Message_val2 = Experion_Error_Message_val2 + " - " +str(deliverable) + "<br>"
            
    """

    if count > 0:
        Experion_Error_Message_val =  "<b>"+'Hours distribution among resources is not 100%. Please adjust the % Split column value to get the total 100% <br>'+"</b>" + Experion_Error_Message_val
        if Labor_Message != "":
            Labor_Message += "<br>" + Experion_Error_Message_val
        else:
            Labor_Message = Experion_Error_Message_val"""

    if count1 > 0:
        Experion_Error_Message_val2 = "<b>"+'Resource is not selected for deliverable. Please select respective Eng or change the Eng % Split to 0% <br>'+"</b>" + Experion_Error_Message_val2
        if Labor_Message != "":
            Labor_Message += "<br>" + Experion_Error_Message_val2
        else:
            Labor_Message = Experion_Error_Message_val2

    if Labor_Message != '':
        Product.Attr('ErrorMessage').AssignValue(Labor_Message)