#IO calculation
total_sum = 0
rem_grp = Product.GetContainerByName('UOC_RemoteGroup_Cont').Rows
for row in rem_grp:
	if row.Product.Attr("UOC_I/O_IsModified").GetValue() == "True":
		rg_cont1 = row.Product.GetContainerByName("UOC_RG_UIO_Cont")
		for rg_row1 in rg_cont1.Rows[0].Columns:
			total_sum += int(rg_row1.Value or 0)
		rg_cont2 = row.Product.GetContainerByName("UOC_RG_Other_IO_Cont")
		for rg_row2 in rg_cont2.Rows[0].Columns:
			total_sum += int(rg_row2.Value or 0)
Product.Attr('R2Q_UOC_IO_Total').AssignValue(str(total_sum))