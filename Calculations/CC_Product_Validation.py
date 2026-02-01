if Session["prevent_execution"] != "true" and Quote.GetGlobal('PerformanceUpload') != 'Yes':
	from GS_ItemCalculations import assignLeadTime,calculatePublishedLeadTime,calculateLTDevileryDate,calculateExpediteFee
	if Item.ProductName == 'MSID_New':
		Session["MSID"]=Item.PartNumber
		Session["msid_QInumber"]=Item.RolledUpQuoteItem
	elif Session["MSID"] and Session["msid_QInumber"] and Item.RolledUpQuoteItem.startswith(str(Session["msid_QInumber"])):
		if len(list(Item.AsMainItem.Children))==0:
			Item.QI_Area.Value = Session["MSID"]
	assignLeadTime(Quote,Item)
	calculatePublishedLeadTime(Quote,Item)
	calculateLTDevileryDate(Quote,Item)
	if Quote.GetCustomField('Booking Lob').Content == "LSS" and Quote.GetCustomField('Quote Type').Content == 'Parts and Spot':
		calculateExpediteFee(Quote,Item)
if Quote.GetCustomField('Booking Lob').Content == "PMC" and Quote.OrderStatus.Id == 32:
	from GS_Validate_Product_Type import IsVCitem
	from GS_VcModel_Update import VcModelupdate
	if IsVCitem(Item.PartNumber)==True:
		VcModelupdate(Quote,Item)
	if Item and Item.AsMainItem and Item.AsMainItem.VCItemPricingPayload and Item.AsMainItem.VCItemPricingPayload.Conditions:
		conditions = Item.AsMainItem.VCItemPricingPayload.Conditions
		for cond in conditions:
			if cond.ConditionType == "ZTSC":
				Item['QI_Tariff_PCT'].Value = cond.ConditionRate if cond.ConditionRate else 0.00
if Item.ProductName == 'WriteIn':
    for attr in Item.SelectedAttributes:
        if attr.Name == 'Writein_Category':
            Item.QI_Writein_Category.Value = attr.Values[0].Display
if Quote.GetCustomField('Booking Lob').Content == "LSS" and Quote.OrderStatus.Id == 32:
    account_name=Quote.GetCustomField("Account Name").Content
    if Item and Item.AsMainItem and Item.AsMainItem.VCItemPricingPayload and Item.AsMainItem.VCItemPricingPayload.Conditions :
        conditions = Item.AsMainItem.VCItemPricingPayload.Conditions
        for cond in conditions:
            if cond.ConditionType == "ZTSC":
                Item['QI_Tariff_PCT'].Value = cond.ConditionRate if cond.ConditionRate else 0.00