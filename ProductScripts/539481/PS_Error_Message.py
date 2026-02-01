tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
Product.Attr('Error_Message_1').AssignValue('')
if 'Labor Deliverables' in tabs:
    def getFloat(Var):
        if Var:
            return float(Var)
        return 0
    deliverables = Product.GetContainerByName('MIQ Engineering Labor Container').Rows
    count1 = 0
    Labor_Message = Labor_Message1 = ""

    for row in deliverables:
        deliverable = row.GetColumnByName('Deliverable')
        FO_Eng_Split = FO_Eng_Cost = 0
        if row.GetColumnByName('FO Eng % Split').Value not in ('','0'):
            FO_Eng_Split = getFloat(row.GetColumnByName('FO Eng % Split').Value)
        if row.GetColumnByName('FO_Eng_Unit_Regional_Cost').Value not in ('','0'):
            FO_Eng_Cost = float(row.GetColumnByName('FO_Eng_Unit_Regional_Cost').Value)
        Eng_Val = row.GetColumnByName('FO Eng').Value
        finalHrs = row.GetColumnByName('Final Hrs').Value

        if (finalHrs not in ('','0','0.0') and (Eng_Val != '' and Eng_Val != 'None' and FO_Eng_Cost == 0 and FO_Eng_Split > 0)):
            count1 = count1 + 1
            Labor_Message1 = Labor_Message1 + " - " +str(deliverable.Value) + "<br>"

    if count1 > 0:
        Labor_Message1 = "<b>"+'Cost is not available for selected resource in Choose MIQ Engineering Labor Container. Please select different resource or different Execution Country.Deliverables to look into: <br>'+"</b>" + Labor_Message1
    if Labor_Message1 != "":
        Labor_Message += Labor_Message1
    Product.Attr('Error_Message_1').AssignValue(Labor_Message)

    PLC_Error_Message_val = ""
    deliverables = Product.GetContainerByName('MIQ Additional Custom Deliverables')
    count1 = 0
    Labor_Message1 = ''
    for row in deliverables.Rows:
        deliverable = row["Deliverable Name"] if row["Deliverable Name"] else row['Standard Deliverable']
        FO1_Eng = FO1_Eng_Cost = 0
        if row.GetColumnByName('FO Eng % Split').Value not in ('','0'):
            FO1_Eng = getFloat(row.GetColumnByName('FO Eng % Split').Value)
        if row.GetColumnByName('FO_Eng_Unit_Regional_Cost').Value not in ('','0'):
            FO1_Eng_Cost = float(row.GetColumnByName('FO_Eng_Unit_Regional_Cost').Value)
        FO_Eng_1_val = row.GetColumnByName('FO Eng').DisplayValue
        finalHrs = row.GetColumnByName('Final Hrs').Value
        if finalHrs not in ('','0','0.0') and FO1_Eng_Cost == 0 and FO1_Eng > 0:
            count1 = count1 + 1
            Labor_Message1 = Labor_Message1 + " - " +str(deliverable) + "<br>"
    if count1 > 0:
        Labor_Message1 = "<b>"+'Cost is not available for selected resource in Additional Custom Deliverables. Please select different resource or different Execution Country.Deliverables to look into: <br>'+"</b>" + Labor_Message1
    if Labor_Message1 != "":
        Labor_Message += Labor_Message1
    Product.Attr('Error_Message_1').AssignValue(Labor_Message)