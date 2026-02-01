RGCont = Product.GetContainerByName('Series_C_Remote_Groups_Cont')
if RGCont.Rows.Count > 0:
	for row in RGCont.Rows:
		if str(row["Series_C_RG_Name"]) != row.Product.Attr('Series_C_RG_Name').GetValue():
			row.Product.Attr('Series_C_RG_Name').AssignValue(str(row["Series_C_RG_Name"]))
		row.ApplyProductChanges()
		row.Calculate()