scope_summary_hidden = Product.GetContainerByName('SC_WEP_Offering_ServiceProduct_Hidden')
scope_summary = Product.GetContainerByName('SC_WEP_Offering_ServiceProduct')
scope_summary.Rows.Clear()
x = Product.Attr("SC_WEP_RC_Selection").SelectedValues
if scope_summary_hidden.Rows.Count:
	for row in scope_summary_hidden.Rows:
		for i in x:
			if i.Display == row["Comments"]:
				scopeRow = scope_summary.AddNewRow(False)
				scopeRow['Offering_Name'] = row['Offering_Name']
				scopeRow['Model'] = row['Model']
				scopeRow['Description'] = row['Description']
				scopeRow['PY_Quantity'] = row['PY_Quantity']
				scopeRow['CY_Quantity'] = row['CY_Quantity']
				scopeRow['PY_ListPrice'] = row['PY_ListPrice']
				scopeRow['PY_CostPrice'] = row['PY_CostPrice']
				scopeRow['CY_ListPrice'] = row['CY_ListPrice']
				scopeRow['CY_CostPrice'] = row['CY_CostPrice']
				scopeRow['SR_Quantity'] = row['SR_Quantity']
				scopeRow['SA_Quantity'] = row['SA_Quantity']
				scopeRow['Comments'] = row['Comments']