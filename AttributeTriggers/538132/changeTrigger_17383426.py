scopeContHidden = Product.GetContainerByName('SC_MES_Models_Hidden')
scopeCont = Product.GetContainerByName('SC_MES_Models')
scopeCont.Rows.Clear()
x = Product.Attr("SC_MES_RC_Selection").SelectedValues
if scopeContHidden.Rows.Count:
    for row in scopeContHidden.Rows:
        for i in x:
            if i.Display == row["Comments"]:
                scopeContRow = scopeCont.AddNewRow(False)
                scopeContRow['MES Models'] = row['MES Models']
                scopeContRow['Description'] = row['Description']
                scopeContRow['PY_Quantity'] = row['PY_Quantity']
                scopeContRow['Renewal_Quantity'] = row['Renewal_Quantity']
                scopeContRow['PY_UnitPrice'] = row['PY_UnitPrice']
                scopeContRow['PY_ListPrice'] = row['PY_ListPrice']
                scopeContRow['HW_UnitPrice'] = row['HW_UnitPrice']
                scopeContRow['SR_Quantity'] = row['SR_Quantity']
                scopeContRow['SA_Quantity'] = row['SA_Quantity']
                scopeContRow['Comments'] = row['Comments']