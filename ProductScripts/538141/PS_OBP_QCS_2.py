if arg.NameOfCurrentTab == 'Scope Summary':
    Vcont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont')
    cont = Product.GetContainerByName('QCS_OPB_Editable_Storage_Cont')
    hcont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont_Hidden')
    for row in cont.Rows:
        for ro in Vcont.Rows:
            if ro['Service Product'] == row['Service_Product']:
                ro['PY_Quantity'] = row['PY_Quantity']
                ro['PY_UnitPrice'] = row['PY_UnitPrice']
        for row1 in hcont.Rows:
            if row1['Service Product'] == row['Service_Product']:
                row1['PY_Quantity'] = row['PY_Quantity']
                row1['PY_UnitPrice'] = row['PY_UnitPrice']
    #cont.Rows.Clear()
Vcont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont')
for row in Vcont.Rows:
    row['Renewal_Quantity'] = row['Renewal_Quantity'] if row['Renewal_Quantity']!= "" else "0"
    row['PY_Quantity'] = row['PY_Quantity'] if row['PY_Quantity']!= "" else "0"
    row['PY_UnitPrice'] = row['PY_UnitPrice'] if row['PY_UnitPrice']!= "" else "0"
    if int(row['Renewal_Quantity']) > int(row['PY_Quantity']):
        row['SR_Quantity'] = '0'
        row['SA_Quantity'] = str(int(row['Renewal_Quantity'])-int(row['PY_Quantity']))
        row['Comments'] = "Scope Addition"
    elif int(row['Renewal_Quantity']) < int(row['PY_Quantity']):
        row['SR_Quantity'] = str(int(row['Renewal_Quantity'])-int(row['PY_Quantity']))
        row['SA_Quantity'] = '0'
        row['Comments'] = "Scope Reduction"
    else:
        row['SR_Quantity'] = '0'
        row['SA_Quantity'] = '0'
        row['Comments'] = "No Scope Change"
    row['PY_ListPrice'] = str((float(row['PY_Quantity']) * float(row['PY_UnitPrice'])))
hcont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont_Hidden')
for row in hcont.Rows:
    row['Renewal_Quantity'] = row['Renewal_Quantity'] if row['Renewal_Quantity']!= "" else "0"
    row['PY_Quantity'] = row['PY_Quantity'] if row['PY_Quantity']!= "" else "0"
    row['PY_UnitPrice'] = row['PY_UnitPrice'] if row['PY_UnitPrice']!= "" else "0"
    if int(row['Renewal_Quantity']) > int(row['PY_Quantity']):
        row['SR_Quantity'] = '0'
        row['SA_Quantity'] = str(int(row['Renewal_Quantity'])-int(row['PY_Quantity']))
        row['Comments'] = "Scope Addition"
    elif int(row['Renewal_Quantity']) < int(row['PY_Quantity']):
        row['SR_Quantity'] = str(int(row['Renewal_Quantity'])-int(row['PY_Quantity']))
        row['SA_Quantity'] = '0'
        row['Comments'] = "Scope Reduction"
    else:
        row['SR_Quantity'] = '0'
        row['SA_Quantity'] = '0'
        row['Comments'] = "No Scope Change"
    row['PY_ListPrice'] = str((float(row['PY_Quantity']) * float(row['PY_UnitPrice'])))
Vcont.Calculate()
hcont.Calculate()
Vcont.Calculate()