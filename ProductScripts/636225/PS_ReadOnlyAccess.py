if Product.Name != "Service Contract Products":
	SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
	Product.Attr('SC_Hosted_by_Honeywell').Access = AttributeAccess.ReadOnly
	Product.Attr('SC_Honeywell_Digital_Prime').Access = AttributeAccess.ReadOnly
	if SC_Product_Type == 'New':
		Product.Attr('SC_Contract_Duration').Access = AttributeAccess.ReadOnly
	elif SC_Product_Type == "Renewal":
		Product.Attr('SC_Select_subscription_type').Access = AttributeAccess.ReadOnly
		Product.Attr('SC_Experion_System').Access = AttributeAccess.ReadOnly
		Product.Attr('SC_Num_of_MSID').Access = AttributeAccess.ReadOnly