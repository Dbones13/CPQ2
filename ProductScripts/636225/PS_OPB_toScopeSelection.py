if arg.NameOfCurrentTab == 'Scope Selection':
    Vcont = Product.GetContainerByName('SC_Honeywell_Scope_Summary_Pricing')
    cont = Product.GetContainerByName('HDP_OPB_Editable_Storage_Cont')
    hcont = Product.GetContainerByName('SC_RC_Honeywell_Scope_Summary_Pricing_Hidden')
    cont.Rows.Clear()
    for row in hcont.Rows:
        row1 = cont.AddNewRow()
        row1['Description'] = row['Description']
        row1['PY_Quantity'] = row['PY_Quantity']
        row1['PY_ListPrice'] = row['PY_ListPrice'] 
    '''for row2 in hcont.Rows:
        for ro in cont.Rows:
            if ro['Description'] == row2['Description']:
                row2['PY_Quantity'] = ro['PY_Quantity']
                row2['PY_ListPrice'] = ro['PY_ListPrice']'''
    Vcont.Calculate()
    hcont.Calculate()
    cont.Calculate()