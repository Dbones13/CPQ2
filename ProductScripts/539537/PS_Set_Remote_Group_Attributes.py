RGCont = Product.GetContainerByName('Series_C_Remote_Groups_Cont')
if Quote.GetCustomField('R2QFlag').Content == 'Yes':
	upc_io_count = Quote.GetGlobal('UPC_Universal_IO_Count')
	if RGCont.Rows.Count > 0:
		exist_upc_io_cnt = Product.GetContainerByName('Series_C_Remote_Groups_Cont').Rows[0].Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
		if exist_upc_io_cnt == '0' and upc_io_count != exist_upc_io_cnt:
			Product.GetContainerByName('Series_C_Remote_Groups_Cont').Rows[0].Product.Attr('C300_RG_UPC_Universal_IO_Count').SelectDisplayValue(str(upc_io_count))
if RGCont.Rows.Count > 0:
    for row in RGCont.Rows:
        Sys_Group_Name = row.Product.Attr('Series_C_RG_Name').GetValue()
        if str(row["Series_C_RG_Name"]) != Sys_Group_Name:
            row.Product.Attr('Series_C_RG_Name').AssignValue(str(row["Series_C_RG_Name"]))
        row.ApplyProductChanges()
        row.Calculate()