scopeContHidden = Product.GetContainerByName('SC_GN_AT_Models_Cont_Hidden')
scopeCont = Product.GetContainerByName('SC_GN_AT_Models_Cont')
scopeCont.Rows.Clear()
x = Product.Attr("SC_GN_AT_RC_Selection").SelectedValues
if scopeContHidden.Rows.Count:
    for row in scopeContHidden.Rows:
        for i in x:
            if i.Display == row["Comments"]:
                scopeContRow = scopeCont.AddNewRow(False)
                scopeContRow['Service_Product'] = row['Service_Product']
                scopeContRow['Asset'] = row['Asset']
                scopeContRow['Model'] = row['Model']
                scopeContRow['Description'] = row['Description']
                scopeContRow['PY_Quantity'] = row['PY_Quantity']
                scopeContRow['Renewal_Quantity'] = row['Renewal_Quantity']
                scopeContRow['PY_ListPrice'] = row['PY_ListPrice']
                scopeContRow['HW_UnitPrice'] = row['HW_UnitPrice']
                scopeContRow['PY_CostPrice'] = row['PY_CostPrice']
                scopeContRow['CY_CostPrice'] = row['CY_CostPrice']
                scopeContRow['SR_Quantity'] = row['SR_Quantity']
                scopeContRow['SA_Quantity'] = row['SA_Quantity']
                scopeContRow['Comments'] = row['Comments']