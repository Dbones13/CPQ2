total_sum,total_Count = 0,0
con_grp = Product.GetContainerByName('UOC_ControlGroup_Cont').Rows
for row in con_grp:
	if row.Product.Attr("UOC_I/O_IsModified").GetValue() == "True":
		cg_cont1 = row.Product.GetContainerByName("UOC_CG_UIO_Cont")
		for cg_row1 in cg_cont1.Rows[0].Columns:
			total_sum += int(cg_row1.Value or 0)
		cg_cont2 = row.Product.GetContainerByName("UOC_CG_Other_IO_Cont")
		for cg_row2 in cg_cont2.Rows[0].Columns:
			total_sum += int(cg_row2.Value or 0)
	total_Count = int(row.Product.Attr('R2Q_UOC_IO_Total').GetValue() or 0)+int(total_sum)
labour_rows = Product.GetContainerByName('UOC_Labor_Details').Rows
if labour_rows.Count > 0:
	labour_cont = labour_rows[0]
	labour_cont.GetColumnByName("UOC_Enter_Total_Count_Labour").Value = "0" if total_Count <= 2000 else "15"