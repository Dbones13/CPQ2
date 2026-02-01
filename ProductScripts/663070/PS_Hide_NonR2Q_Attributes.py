def hideAttr(attrList):
	for attr in attrList:
		Product.Attr(attr).Access = AttributeAccess.Hidden
switch = Product.Attr('L2 Switch Required').GetValue()
isR2Qquote = True if Quote.GetCustomField("R2QFlag").Content else False
if isR2Qquote:
	cont = Product.GetContainerByName('List of Locations/Clusters/Network Groups')
	if Product.Attr('L2 Switch Required').GetValue() == 'No':
		rows_to_delete = [row.RowIndex for row in cont.Rows if row['List of Locations/Clusters/ Network Groups'] == 'Location/Cluster/Network Group1']
		for row_index in sorted(rows_to_delete, reverse=True):
			cont.DeleteRow(row_index)
	else:
		if cont.Rows.Count == 0:
			cont.AddNewRow(False)

R2QAttr = ["Header_50_open","ESD_FGS_Aux_PanelsConsoles","Header_50_close","ATTCON_30_close","ATTCON_30_open","Station Furniture (0-200)","Server Furniture (0-50)","Header_32_open","Header_32_close","ATTCON_26_open","ATTCON_26_close","Network_Firewall_Required","Network Cabinet Required (0-50)","L2 Switch Required","L3 Switch Required (0-10)","PDB Cabinet (0-50)","GPS NTP Server System (0-1)","Laptop (0-50)","Colour A4 printer","B_W_A3_printer","Colour_A3_printer"]
hideAttr(R2QAttr)

if Quote.GetCustomField("R2QFlag").Content == 'Yes':
	if Product.Attr("CMS Flex Station Hardware Selection").GetValue()=="STN_PER_DELL_Rack_RAID1" and Product.Attr("CMS Remote Peripheral Solution Type RPS").GetValue()!="Pepperl+Fuchs BTC22":
		Product.AllowAttr("Remote Peripheral validation message")
	else:
		Product.DisallowAttr("Remote Peripheral validation message")

	if Product.Attr("DMS Flex Station Hardware Selection").GetValue()=="STN_PER_DELL_Rack_RAID1" and Product.Attr("DMS Remote Peripheral Solution Type RPS").GetValue()!="Pepperl+Fuchs BTC12":
		Product.AllowAttr("DMS Message 1")
	else:
		Product.DisallowAttr("DMS Message 1")