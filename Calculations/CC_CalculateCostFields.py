#CXCPQ-65110: Added condition to improve the performance. calculateCosts not required to run for PMC Parts and Spot Quote and for VC products defined in FME_PARTS table.
if Session["prevent_execution"] != "true" and Quote.GetGlobal('PerformanceUpload') != 'Yes' and (Quote.GetCustomField('CF_Plant_Prevent_Calc').Content != 'true' or Quote.GetCustomField('Booking LOB').Content != 'PMC'):
	BookingLob = Quote.GetCustomField("Booking LOB").Content
	Quotetype = Quote.GetCustomField("Quote Type").Content
	import GS_ItemCalculations
	import GS_Validate_Product_Type
	from GS_CommonConfig import CL_CommonSettings as CS
	from GS_ITEMCREATE_UPDATE_Functions import loadwtwfactor
	import GS_HCP_Set_Cost
	wtwcostfactor_dict,nonpricecont = loadwtwfactor(Quote)
	#Log.Info("WTWFac=>"+str(wtwcostfactor_dict))
	for Item in Quote.Items:
		if Item.ProductName == 'TPC_Product':
			continue
		if Item.ProductName in ['HCI Labor Upload', 'HCI Labor Config','PHD Labor','Uniformance Insight Labor','AFM Labor']:
			CS.setdefaultvalue["LaborParentGuid"]=Item.QuoteItemGuid
		if Item.ProductName in  ['HCI Labor Config']:
			CS.setdefaultvalue["LaborConfigParentGuid"]=Item.RolledUpQuoteItem + '.'
		if Item.ProductName == "Cyber" and Item.ProductTypeName != "Service Contract" and '.' not in Item.RolledUpQuoteItem:
			CS.setdefaultvalue["rolled_up"]=Item.RolledUpQuoteItem + '.'

		if (BookingLob != "PMC" or Quotetype != "Parts and Spot") and Quotetype not in ('Contract New','Contract Renewal') and CS.setdefaultvalue.get("LaborParentGuid",'0')!= Item.ParentItemGuid:
			# Log.Info(Item.PartNumber+"-CC_CalculateCostFields  ----- tvs --"+str(Item.QI_Additional_Discount_Percent.Value))
			if Item.ProductName!='Productized Skid Quote Item': #For productized skid Items cost is fetched from SAP
				qry = SqlHelper.GetFirst("SELECT 1 as flag from FME_PARTS WHERE PARTNUMBER = '{}'".format(str(Item.PartNumber)))

				if qry is None: #	CXCPQ-69436: Added Qry condition to avoid conflict with  K&E VC materials
					GS_ItemCalculations.calculateCosts(Quote , BookingLob, Quotetype, Item,wtwcostfactor_dict,nonpricecont,TagParserQuote)

		#CXCPQ-80164 : [PMC] Unit WTW cost should be equal to Unit Regional Cost at Quote Line items
		elif (BookingLob == "PMC" and Quotetype == "Parts and Spot" and Item.QuoteItemGuid in Session["ItemGUID"]) or (BookingLob == "HCP" and CS.setdefaultvalue.get("LaborParentGuid",'')!= Item.ParentItemGuid  and Quotetype == "Parts and Spot"):
			Trace.Write(str(Item.Cost)+"-------rechecking---222--->"+str(Item.MrcCost))
			Trace.Write(str(Item.QuoteItemGuid)+"-------rechecking---333--->"+str(Session["ItemGUID"]))
			GS_ItemCalculations.calculateCosts(Quote , BookingLob, Quotetype, Item,wtwcostfactor_dict,nonpricecont,TagParserQuote)
		if BookingLob in ('HCP','LSS','PAS') and GS_Validate_Product_Type.IsVCitem(Item.PartNumber):
			GS_HCP_Set_Cost.setCost(Item,wtwcostfactor_dict)
		'''if Item.QI_PLSG.Value not in ('7061-Y963', '7061-Y964','7061-Y992'):
			Item.ExtendedCost = Item.Quantity * Item.Cost
			#CXCPQ-94438 : Reprice should update warranty line item
			Item["QI_RegionalMargin"].Value = Item.ExtendedAmount - Item.ExtendedCost
			Item["QI_WTWMargin"].Value = Item.ExtendedAmount - Item["QI_ExtendedWTWCost"].Value
			if Item.ExtendedAmount != 0.00:
				if Item.ExtendedAmount < Item.ExtendedCost:
					Item["QI_RegionalMarginPercent"].Value = (Item["QI_RegionalMargin"].Value / Item.ExtendedAmount) * 100
					#Item["QI_RegionalMarginPercent"].Value = 0.0
					Item["QI_WTWMarginPercent"].Value = (Item["QI_WTWMargin"].Value / Item.ExtendedAmount) * 100
					#Item["QI_WTWMarginPercent"].Value = 0.0
				else:
					Item["QI_RegionalMarginPercent"].Value = (Item["QI_RegionalMargin"].Value / Item.ExtendedAmount) * 100
					Item["QI_WTWMarginPercent"].Value = (Item["QI_WTWMargin"].Value / Item.ExtendedAmount) * 100'''

		#CXCPQ-101295
		if Quote.GetCustomField("Booking Country").Content.lower() == 'india' and Quote.GetCustomField("Booking LOB").Content in ('PAS','LSS') and Quote.GetCustomField("Quote Type").Content == 'Projects':
			indiaDiscountTP = Item.Quantity * Item.Cost
			if Item['QI_PLSG'].Value != '':
				sqlre = SqlHelper.GetFirst("""SELECT Discount_Percent FROM BOOKINGREPORT_INDIA WHERE SG = '{}'""".format(Item['QI_PLSG'].Value))
				if sqlre:
					indiaDiscountTP = indiaDiscountTP * (1 - (float(sqlre.Discount_Percent)/100.0))
			Item['QI_India_discounted_TP'].Value = indiaDiscountTP