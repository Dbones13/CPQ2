CGCont = Product.GetContainerByName('Series_C_Control_Groups_Cont')
if CGCont.Rows.Count > 0:
	for row in CGCont.Rows:
		if str(row["Series_C_CG_Name"]) != row.Product.Attr('Series_C_CG_Name').GetValue():
			row.Product.Attr('Series_C_CG_Name').AssignValue(str(row["Series_C_CG_Name"]))
		row.ApplyProductChanges()
		row.Calculate()