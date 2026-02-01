tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
scope = ''
if Product.GetContainerByName('CE_SystemGroup_Cont').Rows.Count > 0:
    scope = Product.GetContainerByName('CE_SystemGroup_Cont').Rows[0].GetColumnByName('Scope').Value
Trace.Write("Scope= "+str(scope))
Product.Attr('ErrorMessage5').AssignValue('')
def getfloat(var):
    if var:
        return float(var)
    return 0.0
if (('PM Labor Deliverables' in tabs or 'General Inputs' in tabs) and scope == 'HWSWLABOR'):
    #Error Message for Safety Manager Engineering Labor Container
    Trace.Write("dp")
    deliverables = Product.GetContainerByName('PLE_Labor_Container').Rows
    gesLocation = Product.GetContainerByName('Labor_Details_New/Expansion_Cont').Rows[0].GetColumnByName('GES_Location').Value
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
        Trace.Write("DP2 " +str(FO1_Eng_New))
        if FO1_Eng_New < 0:
            #Trace.Write("GES_Eng:{} FO1_Eng:{} FO2_Eng:{} diff:{} Final Hrs:{}".format(GES_Eng, FO1_Eng, FO2_Eng, diff,row["Final Hrs"]))
            count +=1
            Labor_Message = Labor_Message + " - " +str(deliverable.Value) + "<br>"
            Trace.Write("DP2 " +str(Labor_Message))

        FO_Eng_1_val = row.GetColumnByName('FO Eng 1').DisplayValue
        FO1_Eng = getfloat(row.GetColumnByName('FO Eng 1 % Split').Value)

        FO_Eng_2_val = row.GetColumnByName('FO Eng 2').DisplayValue
        FO2_Eng = getfloat(row.GetColumnByName('FO Eng 2 % Split').Value)

        #if ((FO_Eng_2_val == '' or FO_Eng_2_val == 'None') and FO2_Eng > 0 ) or ((FO_Eng_1_val == '' or FO_Eng_1_val == 'None') and FO1_Eng > 0):
        if ((FO_Eng_2_val == '' or FO_Eng_2_val == 'None') and FO2_Eng > 0 and FO2_Eng <= 100) or ((FO_Eng_1_val == '' or FO_Eng_1_val == 'None') and FO1_Eng_New > 0):
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
    if Labor_Message != '':
        Product.Attr('ErrorMessage5').AssignValue(Labor_Message)
        Trace.Write("DP#"+str(Labor_Message))