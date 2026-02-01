Product.Attr('SC_Service_Product_Model').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Coverage_Model').Access = AttributeAccess.ReadOnly
Product.Attr('CurrentSupportContract_EnabledService').Access = AttributeAccess.ReadOnly
Customer_has_cyber_attr = Product.Attr('Customer_has_cyber_enabledServicesModel')
L3_L4_Mover_Essential_attr = Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel')
for i in Customer_has_cyber_attr.Values:
	if i.IsSelected == True:
		for j in L3_L4_Mover_Essential_attr.Values:
			j.IsSelected = False
		Product.Attr("L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel").Access = AttributeAccess.ReadOnly
	else:
		for j in L3_L4_Mover_Essential_attr.Values:
			j.IsSelected = True
		Product.Attr("L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel").Access = AttributeAccess.Editable