SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if SC_Product_Type == 'Renewal':
    tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
    SC_Pricing_Escalation = Product.Attr('SC_Pricing_Escalation').GetValue()
    ComparisonSummary = Product.GetContainerByName("ComparisonSummary")
    if 'Scope Summary' in tabs:
        SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
        Py_List_Price = Product.Attr('HDP_Py_List_Price').GetValue()
        Trace.Write("LP===" + str (Py_List_Price))
        Py_Sell_Price = Product.Attr('HDP_Py_Sell_Price').GetValue()
        if SC_Product_Type == 'Renewal':
            for row in ComparisonSummary.Rows:
                row['Configured_PY_List_Price'] = Py_List_Price
                row['Configured_PY_Sell_Price'] = row['PY_Sell_Price_SFDC']
                if row['Configured_PY_List_Price'] == "0":
                    row['Configured_PY_List_Price'] = row['PY_List_Price_SFDC']
    ComparisonSummary.Calculate()
    #Condition for OPB
    Vcont = Product.GetContainerByName('SC_Honeywell_Scope_Summary_Pricing')
    hcont = Product.GetContainerByName('SC_RC_Honeywell_Scope_Summary_Pricing_Hidden')
    for row in Vcont.Rows:
        if row['PY_ListPrice'] == "":
            row['PY_ListPrice'] = '0'
        if row['R_Quantity'] == "":
            row['R_Quantity'] = '0'
        if row['PY_Quantity'] == "":
            row['PY_Quantity'] = '0'
        if row['HW_ListPrice'] == "":
            row['HW_ListPrice'] = '0'
        if row['PY_ListPrice'] == "":
            row['PY_ListPrice'] = '0'
        if float(row['PY_Quantity']) != 0:
            row['PY_UnitPrice'] = str((float(row['PY_ListPrice']) / float(row['PY_Quantity'])))
        else:
            row['PY_UnitPrice'] = "0"
    for row in hcont.Rows:
        if row['PY_ListPrice'] == "":
            row['PY_ListPrice'] = '0'
        if row['PY_Quantity'] == "":
            row['PY_Quantity'] = '0'
        if float(row['PY_Quantity']) != 0:
            row['PY_UnitPrice'] = str((float(row['PY_ListPrice']) / float(row['PY_Quantity'])))
        else:
            row['PY_UnitPrice'] = "0"
    Vcont = Product.GetContainerByName('SC_Honeywell_Scope_Summary_Pricing')
    for row in Vcont.Rows:
        if int(row['R_Quantity']) > int(row['PY_Quantity']):
            row['SR_Quantity'] = '0'
            row['SA_Quantity'] = str(int(row['R_Quantity'])-int(row['PY_Quantity']))
            row['Comments'] = "Scope Addition"
        elif int(row['R_Quantity']) < int(row['PY_Quantity']):
            row['SR_Quantity'] = str(int(row['R_Quantity'])-int(row['PY_Quantity']))
            row['SA_Quantity'] = '0'
            row['Comments'] = "Scope Reduction"
        else:
            row['SR_Quantity'] = '0'
            row['SA_Quantity'] = '0'
            row['Comments'] = "No Scope Change"
        row['SR_Price'] = str (float(row['SR_Quantity']) * float(row['PY_UnitPrice']))
        row['SA_Price'] = str(float(row['SA_Quantity']) * float(row['HW_ListPrice']))

    hcont = Product.GetContainerByName('SC_RC_Honeywell_Scope_Summary_Pricing_Hidden')
    for row in hcont.Rows:
        if int(row['Quantity']) > int(row['PY_Quantity']):
            row['SR_Quantity'] = '0'
            row['SA_Quantity'] = str(int(row['Quantity'])-int(row['PY_Quantity']))
            row['Comments'] = "Scope Addition"
        elif int(row['Quantity']) < int(row['PY_Quantity']):
            row['SR_Quantity'] = str(int(row['Quantity'])-int(row['PY_Quantity']))
            row['SA_Quantity'] = '0'
            row['Comments'] = "Scope Reduction"
        else:
            row['SR_Quantity'] = '0'
            row['SA_Quantity'] = '0'
            row['Comments'] = "No Scope Change"
        row['SR_Price'] = str (float(row['SR_Quantity']) * float(row['PY_UnitPrice']))
        row['SA_Price'] = str(float(row['SA_Quantity']) * float(row['HW_ListPrice']))
        if SC_Pricing_Escalation == "Yes":
            if row['Comments'] == "Scope Reduction" or row['Comments'] == "No Scope Change":
                row['Escalation_Price'] = str(float(row['Quantity'])*float(row['PY_ListPrice'])/float(row['PY_Quantity'])) if row['PY_Quantity'] not in ('','0') else '0'
                row['Hidden_ListPrice'] = str(float(row['Quantity'])*float(row['PY_ListPrice'])/float(row['PY_Quantity'])) if row['PY_Quantity'] not in ('','0') else '0'
            elif row['Comments'] == "Scope Addition":
                row['Escalation_Price'] = str(float(row['PY_Quantity']) * float(row['PY_ListPrice']))
                row['Hidden_ListPrice'] = str(float(row['PY_ListPrice']) + ((float(row['Quantity']) - float(row['PY_Quantity']))*float(row['HW_ListPrice'])))
        else:
            row['Escalation_Price'] = '0'
            row['Hidden_ListPrice'] = str(float(row['Quantity']) * float(row['HW_ListPrice']))
    for row in ComparisonSummary.Rows:
        if float(row['Configured_PY_List_Price']) == 0.0:
            row['Configured_PY_List_Price'] = row['PY_List_Price_SFDC']
    for row in hcont.Rows:
        if row['Description'] == "Base Package Experion":
            row['PY_Quantity'] = "1"
    for row in Vcont.Rows:
        if row['Description'] == "Base Package Experion":
            row['PY_Quantity'] = "1"
        if row['Description'] == "No of Concurrent Users or Stations":
            if int(row['PY_Quantity']) <0 or int(row['PY_Quantity']) > 99:
                row['PY_Quantity'] = "0"
    Vcont.Calculate()
    hcont.Calculate()