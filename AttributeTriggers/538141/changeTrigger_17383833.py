scopeContHidden = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont_Hidden')
scopeCont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont')
scopeCont.Rows.Clear()
x = Product.Attr("SC_QCS_Scope_Button").SelectedValues
if scopeContHidden.Rows.Count:
    for row in scopeContHidden.Rows:
        for i in x:
            if i.Display == row["Comments"]:
                scopeContRow = scopeCont.AddNewRow(False)
                scopeContRow['Service Product'] = row['Service Product']
                scopeContRow['Description'] = row['Description']
                scopeContRow['Section'] = row['Section']
                scopeContRow['PY_Quantity'] = row['PY_Quantity']
                scopeContRow['Renewal_Quantity'] = row['Renewal_Quantity']
                scopeContRow['PY_UnitPrice'] = row['PY_UnitPrice']
                scopeContRow['PY_ListPrice'] = row['PY_ListPrice']
                scopeContRow['HW_UnitPrice'] = row['HW_UnitPrice']
                scopeContRow['HW_ListPrice'] = row['HW_ListPrice']
                scopeContRow['SR_Quantity'] = row['SR_Quantity']
                scopeContRow['SA_Quantity'] = row['SA_Quantity']
                scopeContRow['Comments'] = row['Comments']