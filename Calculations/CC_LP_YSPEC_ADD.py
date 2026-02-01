if Quote.GetCustomField('Booking LOB').Content == "PMC" and Quote.GetCustomField('CF_Plant_Prevent_Calc').Content != 'true':
	import GS_Validate_Product_Type
	if GS_Validate_Product_Type.IsVCitem( Item.PartNumber)==True:
		if float(Item.Yspec_Add.Value) > 0.0:
			Item.ListPrice = Item.Yspec_Add.Value
		Trace.Write("item.ListPrice---->"+str(Item.ListPrice))
		if float(Item.QI_GAS_ETO_PRICE_ADD.Value) > 0.0 or float(Item.QI_ETO_PMC_Price_Add.Value) > 0.0:
			pf_res = SqlHelper.GetFirst("select PartNumber,family_code from PMC_GASETO_YSPEC_MARINE_PRODUCTS where PartNumber = '{}'".format(Item.PartNumber))
			if pf_res is not None:
				if (pf_res.family_code=='Gas Products'):#CXCPQ-42168: Gas ETO cannot be discounted. Business asked to update ETO price to the Net price
					Item.QI_NetPrice_With_ETO.Value = Item.ExtendedAmount+(Item.QI_GAS_ETO_PRICE_ADD.Value*Item.Quantity)
				else: #Other ETO products can be discounted.
					Item.ListPrice = Item.QI_ETO_PMC_Price_Add.Value
					Item.QI_NetPrice_With_ETO.Value= Item.NetPrice
		if float(Item.QI_AceQuote_ListPrice.Value) > 0.0:
			Item.ListPrice = Item.QI_AceQuote_ListPrice.Value
		if Item.QI_Parent_Generic_system_GUID.Value!='':
			Item.ListPrice = 0
		Trace.Write("item.ListPrice---->"+str(Item.ListPrice))
		Trace.Write("item.QI_ETO_PMC_Price_Add---->"+str(Item.QI_ETO_PMC_Price_Add))
		Trace.Write("item.QI_AceQuote_ListPrice---->"+str(Item.QI_AceQuote_ListPrice))
		if Quote.GetCustomField('CF_Plant_Prevent_Calc').Content == 'true':
			Quote.GetCustomField('CF_Plant_Prevent_Calc').Content = ''