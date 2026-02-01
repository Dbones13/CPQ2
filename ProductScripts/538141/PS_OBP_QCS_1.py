if arg.NameOfCurrentTab == 'Scope Selection':
    Vcont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont')
    cont = Product.GetContainerByName('QCS_OPB_Editable_Storage_Cont')
    hcont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont_Hidden')
    for row in hcont.Rows:
        if cont.Rows.Count:
            for srow in cont.Rows:
                if srow['Service_Product'] == row['Service Product']:
                    srow['PY_Quantity'] = row['PY_Quantity']
                    srow['PY_UnitPrice'] = row['PY_UnitPrice']
        else:
            for row in hcont.Rows:
                row1 = cont.AddNewRow()
                row1['Service_Product'] = row['Service Product']
                row1['PY_Quantity'] = row['PY_Quantity']
                row1['PY_UnitPrice'] = row['PY_UnitPrice']