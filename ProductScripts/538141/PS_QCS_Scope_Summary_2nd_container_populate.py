if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
	SC_QCS_Scope_Summary_2nd_Table = Product.GetContainerByName("SC_QCS_Scope_Summary_2nd_Table")
	SC_QCS_Scope_Summary_2nd_Table.Clear()
	attr_selected=Product.Attributes.GetByName('SC_QCS_Support_Center_Select').GetValue()
	Trace.Write("test"+str(attr_selected))
	Subscription_Tier= Product.Attr('SC_QCS_Subscription Tier').GetValue()
	Subscription_Tier_PY = Product.Attr('SC_QCS_Subscription_Tier_PY').GetValue()
	if Subscription_Tier is not None:
		SC_QCS_Scope_Summary_2nd_Table.AddNewRow(True)
		for row in SC_QCS_Scope_Summary_2nd_Table.Rows:
			row['Service_Product'] = "QCS 4.0"
			row['Section'] = "Price Calculator"
			row['Description'] = "Subscription Tier"
			row['Previous_Year_Values'] = Subscription_Tier_PY
			row['Renewal_Year_Values'] = Subscription_Tier