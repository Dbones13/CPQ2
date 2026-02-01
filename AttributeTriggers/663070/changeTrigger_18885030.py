attr_val = Product.Attr('Firewall Required').GetValue()
if attr_val == 'No':
	Product.GetContainerByName('Firewall_Thirdpartycont').Rows.Clear()
	Product.GetContainerByName('EPKS_Part_Summary_Cont_3rd_Party').Rows.Clear()