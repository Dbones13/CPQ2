SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if SC_Product_Type == 'Renewal':
    hcont = Product.GetContainerByName("SC_RC_Honeywell_Scope_Summary_Pricing_Hidden")
    Vcont = Product.GetContainerByName("SC_Honeywell_Scope_Summary_Pricing")
    comparision_cont = Product.GetContainerByName("ComparisonSummary")
    SC_Pricing_Escalation = Product.Attr('SC_Pricing_Escalation').GetValue()
    for row in comparision_cont.Rows:
        if row.IsSelected:
            for row2 in Vcont.Rows:
                row2['R_Quantity'] = '0'
            for row3 in hcont.Rows:
                row3['Quantity'] = '0'
                row3['List Price'] = '0'
    for row in hcont.Rows:
        if row['Quantity'] == "":
            row['Quantity'] = "0"
        if row['PY_Quantity'] == "":
            row['PY_Quantity'] = "0"
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
        row['List Price'] = str(float(row['Quantity']) * float(row['HW_ListPrice']))
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
        for row2 in Vcont.Rows:
            if row['Description'] == row2['Description']:
                row2['Honeywell_List_Price'] = row['List Price']
                row2['SR_Quantity'] = row['SR_Quantity']
                row2['SA_Quantity'] = row['SA_Quantity']
                row2['Comments'] = row['Comments']
    discount = 0
    for row in comparision_cont.Rows:
        if float(row['PY_List_Price_SFDC']) != '':
            discount = (float(row['PY_List_Price_SFDC']) - float(row['PY_Sell_Price_SFDC']))/float(row['PY_List_Price_SFDC'])
        else:
            discount = 0
    for row in hcont.Rows:
        if row['PY_ListPrice'] == "":
            row['PY_ListPrice'] = "0"
        row['LY_Discount'] = str(discount * 100.0)
        row['PY_SellPrice'] = str(float(row['PY_ListPrice']) - (float(row['PY_ListPrice']) * discount))
    hcont.Calculate()
    Vcont.Calculate()