"""if Product.Name == 'Hardware Warranty' or Product.Name == 'Hardware Refresh':
	if Product.IsComplete == True:
		Product.Messages.Clear()
	elif Product.IsComplete == False:
		if Product.Messages.Contains('Please enter all the mandatory fields with required values in Model Scope section'):
			pass
		else:
			Product.Messages.Add('Please enter all the mandatory fields with required values in Model Scope section')"""
if Product.Attr('SC_Product_Type').GetValue() is not None and Product.Attr('SC_Product_Type').GetValue() != 'Renewal':
	if Product.GetContainerByName('HWOS_Model Scope_3party').Rows.Count < 1:
		Product.Attr('SC_InComplete_Product_Validation').Required = True
		Product.Attr('SC_InComplete_Product_Validation').AssignValue('True')
	else:
		Product.Attr('SC_InComplete_Product_Validation').Required = False
		Product.Attr('SC_InComplete_Product_Validation').AssignValue('False')
	for row in Product.GetContainerByName('HWOS_Model Scope_3party').Rows:
		if float(row['Quantity']) > 0 and round(float(row['Unit List Price']),2) > 0 and round(float(row['Unit Cost']),2) > 0 and row["Description"] != "" and row["3rd Party Model"] != "":
			Product.Attr('SC_InComplete_Product_Validation').Required = False
			Product.Attr('SC_InComplete_Product_Validation').AssignValue('False')
		else:
			Product.Attr('SC_InComplete_Product_Validation').Required = True
			Product.Attr('SC_InComplete_Product_Validation').AssignValue('True')
			break
else:
	Product.Attr('SC_InComplete_Product_Validation').Required = False
	Product.Attr('SC_InComplete_Product_Validation').AssignValue('False')