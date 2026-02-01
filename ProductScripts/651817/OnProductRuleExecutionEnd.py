UOC_Common_Questions_Cont = Product.GetContainerByName('UOC_Common_Questions_Cont')
if UOC_Common_Questions_Cont.Rows.Count == 1:
	Cabinet_Required_Racks_Mounting = UOC_Common_Questions_Cont.Rows[0].GetColumnByName('UOC_Cabinet_Required_Racks_Mounting').Value
	Product.Attr('Cabinet_Required_Racks_Mounting').AssignValue(Cabinet_Required_Racks_Mounting)

PLC_ControlGroup_Cont = Product.GetContainerByName('UOC_ControlGroup_Cont')
if PLC_ControlGroup_Cont.Rows.Count > 0:
	for row in PLC_ControlGroup_Cont.Rows:
		PLC_CG_Name = row.Product.Attr('UOC_CG_Name').GetValue()
		if str(row["Control Group Name"]) != PLC_CG_Name:
			row.Product.Attr('UOC_CG_Name').AssignValue(str(row["Control Group Name"]))
			row.ApplyProductChanges()
			row.Calculate()