cont = Product.GetContainerByName('Firewall_Thirdpartycont').Rows
cont_count = cont.Count
if cont_count > 0 :
	ps_cont = Product.GetContainerByName('EPKS_Part_Summary_Cont_3rd_Party')
	ps_cont.Rows.Clear()
	for data in cont:
		ps_cont_newRow = ps_cont.AddNewRow()
		ps_cont_newRow['PartNumber'] = data['Part']
		ps_cont_newRow['Part_Description'] = data['Description']
		ps_cont_newRow['Part_Qty'] = data['Qty']