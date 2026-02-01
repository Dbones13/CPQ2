scopeContHidden = Product.GetContainerByName('SC_Experion_Models_Hidden')
summaryCont = Product.GetContainerByName('SC_Experion_Models_Summary')
summaryCont.Rows.Clear()
x = Product.Attr("SC_Experion_RC_Selection").SelectedValues
if scopeContHidden.Rows.Count:
    for row in scopeContHidden.Rows:
        for i in x:
            if i.Display == row["Comment"]:
                summaryContRow = summaryCont.AddNewRow(False)
                summaryContRow['MSIDs'] = row['MSIDs']
                summaryContRow['Description'] = row['Description']
                summaryContRow['PY_Quantity'] = row['PY_Quantity']
                summaryContRow['Renewal_Quantity'] = row['Renewal_Quantity']
                summaryContRow['PY_ListPrice'] = row['PY_ListPrice']
                summaryContRow['PY_CostPrice'] = row['PY_CostPrice']
                summaryContRow['HW_ListPrice'] = row['HW_ListPrice']
                summaryContRow['Cost_Price'] = row['Cost_Price']
                summaryContRow['SR_Price'] = row['SR_Price']
                summaryContRow['SA_Price'] = row['SA_Price']
                summaryContRow['Comment'] = row['Comment']