msid_scope = Product.Attr('MIgration_Scope_Choices').GetValue()
contObj = Product.GetContainerByName('CONT_MSID_SUBPRD')
if contObj.Rows.Count > 0:
	for row in contObj.Rows:
		row.Product.Attr('Scope').AssignValue(msid_scope)
		row.Product.Attr('MIgration_Scope_Choices').AssignValue(msid_scope)
		