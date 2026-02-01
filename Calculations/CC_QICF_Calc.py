def update_description(parent_item, item,tas_desc):
	#Log.Write("isnnd--update_description")
	if str(parent_item) and str(item.ParentRolledUpQuoteItem).startswith(str(parent_item)):
		part_number = item.PartNumber
		if part_number in tas_desc:
			#Trace.Write("desc--"+str(tas_desc[part_number]["Description"])+"-qty---"+str(tas_desc[part_number]["Qty"]))
			item.QI_ExtendedDescription.Value = tas_desc[part_number]["Description"]
			item.Quantity= float(tas_desc[part_number]["Qty"])

if Quote.GetGlobal('PerformanceUpload') != 'Yes':
	# Header Data
	BookingLOB=Quote.GetCustomField("Booking LOB").Content
	pole=Quote.GetCustomField("Pole").Content
	QuoteType=Quote.GetCustomField("Quote Type").Content
	salesarea = Quote.GetCustomField("Sales Area").Content
	excahnge_rate = float(Quote.GetCustomField("SC_CF_EXCHANGE_RATE").Content) if Quote.GetCustomField("SC_CF_EXCHANGE_RATE").Content else 1
	SC_Currency = Quote.GetCustomField("SC_CF_CURRENCY").Content
	Price_toggle = Quote.GetCustomField("SC_CF_PRICE_TOGGLE").Content
	custreqdat = Quote.GetCustomField('Customer Requested Date').Content
	r2q_prjt_catg = Quote.GetCustomField('R2Q_Category_PRJT').Content
	factdict={}
	plant_detail=SqlHelper.GetList("select Product_line,Pole,Factory_Name FROM CT_MANUFACTURING_PLANT WHERE Pole='{0}' AND Default_Flag='Y'".format(pole))
	for data in plant_detail:
		factdict[data.Product_line]=data.Factory_Name

	# Build Product List
	productSet = set()
	for item in Quote.Items:
		if 1==1: #item.Initialized.Value != 1: we may need this at some point
			productSet.add(item.PartNumber)
	productWhere = "WHERE PartNumber IN ('{0}')".format("', '".join(productSet))

	# Query Data
	Productdetails = SqlHelper.GetList("select h.PartNumber,h.CrossDistributionStatus,h.MindeliveryQuantity,h.MinOrderQuantity,h.ProductLine,h.ProductLineDesc,h.SalesText,h.PLSGDesc,h.PLSG,sp.LOB from HPS_PRODUCTS_MASTER h JOIN SAP_PLSG_LOB_Mapping sp ON h.PLSG = sp.SAP_PL_PLSG {0}".format(productWhere))
	segmentation = SqlHelper.GetList("select PartNumber, A_B_SEGMENTATION from CT_PRODUCT_SALES {0} and SALESORG = '{1}'".format(productWhere,salesarea))
	cartData = SqlHelper.GetList("select UnitOfMeasure, catalogcode from cart_item where userid = {0} and cart_id = {1}".format(Quote.UserId,Quote.QuoteId))
	#Lob = SqlHelper.GetFirst("SELECT LOB FROM SAP_PLSG_LOB_Mapping WHERE SAP_PL_PLSG = '{}'".format(Item.QI_PLSG.Value))

	# Item Loop
	tas_attr = ['TAS_MODULE_PARTS_SUMMARY']
	tas_prd = ['Digital Video Manager', 'Industrial Security (Access Control)', 'Fire Detection & Alarm Engineering', 'Tank Gauging Engineering', 'Small Volume Prover', 'Skid and Instruments', 'Operator Training']
	parent_item = ''
	tas_desc = {}

	for item in Quote.MainItems:
		qty = float(item.Quantity)
		listprc = float(item.ListPrice)
		extn_amt = float(item.ExtendedAmount)
		extnWTWcost = float(item.QI_ExtendedWTWCost.Value)
		extn_listprc = float(item.ExtendedListPrice)
		item_sc_cost = float(item.QI_SC_Cost.Value)
		configuration = ""
		UoM = ""
		attrList = ["QI_Area","Extended Description","PRD_PartNumber","PricingNeeded","Product Line","Product Line Description","PLSG description","Product line sub group","Configuration","SC_ItemEditFlag","Writein_Category"]
		productLine = ""
		productLineDesc = ""
		if (QuoteType not in ("Contract New", "Contract Renewal") and (item.Cost == 0 or item.ProductName == 'WriteIn')) or (QuoteType in ("Contract New", "Contract Renewal")) or item.PartNumber in ['Write-In Entitlement-Hardening Services','Write-In Entitlement-Hardening Cyber Care','Write-In Entitlement-Cyber App Control Care','Write-In Entitlement-Cyber App Control']:# == True:
			attributeData = {attr.Name: attr.Values[0].Display for attr in item.SelectedAttributes if attr.Name in attrList}
			item.QI_Area.Value = attributeData.get("QI_Area",item.QI_Area.Value)
			item.QI_ExtendedDescription.Value = attributeData.get("Extended Description",item.QI_ExtendedDescription.Value) if r2q_prjt_catg == 'TA System' else attributeData.get("Extended Description","")
			item.QI_PartNumber.Value = attributeData.get("PRD_PartNumber")
			item.QI_PricingNeeded.Value = attributeData.get("PricingNeeded")
			productLine = attributeData.get("Product Line","")
			productLineDesc = attributeData.get("Product Line Description","")
			configuration = attributeData.get("Configuration","")
			UoM = attributeData.get("Unit of Measure","")
			PLSG=attributeData.get("Product line sub group","")
			plsgDesc=attributeData.get("PLSG description","")
			SC_ItemEditFlag=attributeData.get("SC_ItemEditFlag","")
			item.QI_PLLOB.Value = "AS" if attributeData.get("Writein_Category","") in ['HCI','HCP'] else attributeData.get("Writein_Category","")
			if (item.PartNumber !='Write-In Standard Warranty' and item.ProductName == 'WriteIn' and item.CategoryName != 'HCI Software/Hardware') or item.PartNumber in ['Write-In Entitlement-Hardening Services','Write-In Entitlement-Hardening Cyber Care','Write-In Entitlement-Cyber App Control Care','Write-In Entitlement-Cyber App Control']:
				if Quote.GetCustomField("R2QFlag").Content=="Yes" and item.ProductName == 'WriteIn':
					WPLSGquery = SqlHelper.GetFirst("SELECT ProductLine,ProductLineDescription,Description,ProductLineSubGroup,UnitofMeasure FROM WriteInProducts WHERE Product= '{}'".format(item.PartNumber))
					if WPLSGquery:
						productLine = WPLSGquery.ProductLine
						productLineDesc = WPLSGquery.ProductLineDescription
						plsgDesc = WPLSGquery.Description
						PLSG = WPLSGquery.ProductLineSubGroup
						UoM = WPLSGquery.UnitofMeasure
				item.QI_ProductLine.Value = productLine
				item.QI_ProductLineDesc.Value = productLineDesc
				item.QI_PLSGDesc.Value  = plsgDesc
				item.QI_PLSG.Value  = PLSG
				item.QI_UoM.Value = UoM
			# Trace.Write(item.PartNumber + "----" + str(item.IsMainItem) + "-----" + str(attributeData))

			
		if QuoteType in ("Contract New", "Contract Renewal"):
			if SC_ItemEditFlag=="Hidden":
				item.QI_SC_ItemFlag.Value="Hidden"
			elif item.PartNumber=="Service Contract":
				item.QI_SC_ItemFlag.Value="0"+SC_ItemEditFlag
			elif SC_ItemEditFlag.startswith("1"): 
				item.QI_SC_ItemFlag.Value="1"+SC_ItemEditFlag

		#disabled for now
		#item.QI_debug.Value = item.RolledUpExtendedAmount  + item.QuoteItemGuid  + item.BaseItemGuid
		item.QI_ExtendedListPrice.Value = listprc * qty
		item.QI_ExtendedWTWCost.Value = qty * float(item.QI_UnitWTWCost.Value)
		item.QI_LineTotal.Value = extn_amt + float(item.QI_Expedite_Fees.Value)

		if segmentation:
			for segment in segmentation:
				if segment.PartNumber == item.PartNumber:
					item.QI_prod_segment.Value = segment.A_B_SEGMENTATION

		if custreqdat:
			item.QI_Customer_Requested_Date.Value = UserPersonalizationHelper.CovertToDate(custreqdat)

		if Productdetails:
			# Is this correct? product line and product line desc are only populated if there are product details even if it is coming from the attribute
			for productDetail in Productdetails:
				if productDetail.PartNumber == item.PartNumber:
					item.QI_CrossDistributionStatus.Value = productDetail.CrossDistributionStatus
					item.QI_MinDeliveryQty.Value = float(productDetail.MindeliveryQuantity) if productDetail.MindeliveryQuantity else 0
					item.QI_MinOrderQty.Value = float(productDetail.MinOrderQuantity) if productDetail.MinOrderQuantity else 0
					item.QI_ProductLine.Value = productLine if productLine != "" else productDetail.ProductLine
					item.QI_ProductLineDesc.Value = productLineDesc if productLineDesc != "" else productDetail.ProductLineDesc
					item.QI_SalesText.Value = productDetail.SalesText
					item.QI_PLSGDesc.Value  = productDetail.PLSGDesc if productDetail.PLSGDesc != "" else plsgDesc
					item.QI_PLSG.Value  = productDetail.PLSG if productDetail.PLSG != "" else PLSG
					item.QI_PLLOB.Value = productDetail.LOB
					if item.QI_PLSG.Value in factdict and BookingLOB!="PMC" and item.QI_ManufacturingPlant.Value=="":
						item.QI_ManufacturingPlant.Value=factdict[item.QI_PLSG.Value]

		#if Lob:
			#Item.QI_PLLOB.Value = Lob.LOB

		#item.QI_ProductPrice.Value = float(TagParserQuote.ParseString("<*CTX( Quote.CurrentItem.TotalPriceWithLineItems.DefaultDecimal )*>") or '0')
		item.QI_ProductPrice.Value = item.AsMainItem.RolledUpListPrice
		item.QI_ProjectType.Value = item.ProductTypeName if item.ProductName != 'TPC_Product' else item.QI_ProjectType.Value
		item.QI_REGIONAL_ETO_COST.Value = float(item.QI_ETO_COST.Value) * qty
		item.QI_SVP_Configuration_Value.Value = configuration

		item.QI_Target_Sell_Price.Value = extn_listprc - float(item.QI_MPA_Discount_Amount.Value)

		item.QI_TOTAL_COST.Value = float(item.QI_ETO_COST.Value) + float(item.Cost)

		item.QI_TOTAL_EXTENDED_COST.Value = float(item.QI_TOTAL_COST.Value) * qty

		item.QI_UnitSellPrice.Value = listprc-(listprc* float(item.DiscountPercent))
		for cartItem in cartData:
			if cartItem.catalogcode == item.PartNumber:
				if cartItem.UnitOfMeasure == "":
					item.QI_UoM.Value = UoM
				else:
					item.QI_UoM.Value = cartItem.UnitOfMeasure



		item.QI_WTWMargin.Value = extn_amt - extnWTWcost
		if extn_amt > 0 :
			item.QI_WTWMarginPercent.Value = float(item.QI_WTWMargin.Value) / extn_amt * 100
			item.QI_SC_True_Honeywell_Discount.Value = (1- (float(item.QI_SC_Honeywell_List_Price.Value)/ extn_amt)) *100

		else:
			#Commented below line as WTW Margin % should not calculate if Sell Price is 0
			#item.QI_WTWMarginPercent.Value = float(item.QI_WTWMargin.Value) * 100
			item.QI_SC_True_Honeywell_Discount.Value = (1- float(item.QI_SC_Honeywell_List_Price.Value)) *100
			
		if item.ProductName in tas_prd:
			#Log.Info("insii--tas--")
			parent_item = item.ParentRolledUpQuoteItem
			attributeData = {attr.Name: attr.Values[0].Display  for attr in item.SelectedAttributes if attr.Name in tas_attr}
			if attributeData:
				rows_data = item.SelectedAttributes.GetContainerByName('TAS_MODULE_PARTS_SUMMARY').Rows
				for val in rows_data:
					part_number = val['Part_Number']
					if part_number:
						tas_desc[part_number] = {"Description": val['Description'],"Qty": val['Quantity']}
		if tas_desc:
			#Log.Info("parent_item---"+str(parent_item))
			update_description(parent_item, item, tas_desc)

		'''if SC_Currency != 'USD':
			if Price_toggle == '':
				item.QI_SC_WTWCost.Value = "USD" +str(round((extnWTWcost / excahnge_rate),2))+(SC_Currency+str(round(extnWTWcost,2)))
				item.QI_SC_ListPrice.Value = "USD" +str(round((extn_listprc / excahnge_rate),2))+(SC_Currency+str(round(extn_listprc,2)))
				item.QI_SC_CostPrice.Value = "USD" +str(round((item_sc_cost / excahnge_rate),2))+(SC_Currency+str(round(item_sc_cost,2)))
				item.QI_SC_SellPrice.Value = "USD" +str(round((extn_amt / excahnge_rate),2))+(SC_Currency+str(round(extn_amt,2)))
			else:
				if Price_toggle == 'USD':
					item.QI_SC_WTWCost.Value  = "USD"+ str(round((extnWTWcost / excahnge_rate),2))
					item.QI_SC_ListPrice.Value  = "USD" + str(round((extn_listprc / excahnge_rate),2))
					item.QI_SC_CostPrice.Value  = "USD" + str(round((item_sc_cost / excahnge_rate),2))
					item.QI_SC_SellPrice.Value  = "USD" + str(round((extn_amt / excahnge_rate),2))
				else:
					item.QI_SC_WTWCost.Value = SC_Currency+str(round(extnWTWcost,2))
					item.QI_SC_ListPrice.Value = SC_Currency+str(round(extn_listprc,2))
					item.QI_SC_CostPrice.Value = SC_Currency+str(round(item_sc_cost,2))
					item.QI_SC_SellPrice.Value = SC_Currency+str(round(extn_amt,2))
		else:
			item.QI_SC_WTWCost.Value = SC_Currency+str(round(extnWTWcost,2))
			item.QI_SC_ListPrice.Value = SC_Currency+str(round(extn_listprc,2))
			item.QI_SC_CostPrice.Value = SC_Currency+str(round(item_sc_cost,2))
			item.QI_SC_SellPrice.Value = SC_Currency+str(round(extn_amt,2))'''
else:
	TPCPLSGs = str(Quote.GetGlobal('TPCPLSGs')).replace("[","").replace("]","").replace("'","").replace(" ","") if Quote.GetGlobal('TPCPLSGs') else ''
	TPCPLSGsList = TPCPLSGs.split(",") if TPCPLSGs else []
	#Trace.Write(str(TPCPLSGsList))
	for item in Quote.MainItems:
		if item.ProductName == 'TPC_Product' and item.QuoteItemGuid in TPCPLSGsList:
			attrList = ["PRD_Cost","PRD_Year","PRD_WTWCost","PRD_SellPrice","PRD_SellDiscount","PRD_MPADiscount","PRD_SellDiscountPercentage","PRD_MPADiscountPercentage","PRD_No_Discount_Allowed","PRD_ProductLine","PRD_ProductLineDesc","PRD_Description","PRD_Name","PRD_CrossDistributionStatus","PRD_TariffAmount","PRD_TariffCost", "PRD_ProductCostCategory"]
			attributeData = {attr.Name: attr.Values[0].Display for attr in item.SelectedAttributes if attr.Name in attrList}
			item.QI_Year.Value = attributeData.get("PRD_Year","") if attributeData.get("PRD_Year","") != "None" else ""
			item.Cost = float(attributeData.get("PRD_Cost",0))
			item.ExtendedCost = float(attributeData.get("PRD_Cost",0))
			item.QI_UnitWTWCost.Value = float(attributeData.get("PRD_WTWCost",0))
			item.QI_ExtendedWTWCost.Value = float(attributeData.get("PRD_WTWCost",0))
			item.QI_MPA_Discount_Percent.Value = float(attributeData.get("PRD_MPADiscountPercentage",0))
			item.QI_MPA_Discount_Amount.Value = float(attributeData.get("PRD_MPADiscount",0))
			item.QI_Additional_Discount_Percent.Value = float(attributeData.get("PRD_SellDiscountPercentage",0))
			item.QI_Additional_Discount_Amount.Value = float(attributeData.get("PRD_SellDiscount",0))
			item.QI_UnitSellPrice.Value = float(attributeData.get("PRD_SellPrice",0))
			item.ExtendedAmount = float(attributeData.get("PRD_SellPrice",0))
			item.QI_Tariff_Amount.Value = float(attributeData.get("PRD_TariffAmount",0))
			item.QI_Cost_Tariff_Amount.Value = float(attributeData.get("PRD_TariffCost",0))

			item.QI_ProductLine.Value = attributeData.get("PRD_ProductLine","")
			item.QI_ProductLineDesc.Value = attributeData.get("PRD_ProductLineDesc","")
			item.QI_SalesText.Value = attributeData.get("PRD_SalesText","")
			item.QI_PLSGDesc.Value = attributeData.get("PRD_Description","")
			item.QI_PLSG.Value  = attributeData.get("PRD_Name","")
			item.QI_No_Discount_Allowed.Value  = attributeData.get("PRD_No_Discount_Allowed","")
			item.QI_CrossDistributionStatus.Value  = attributeData.get("PRD_CrossDistributionStatus","")
			item.QI_ProductCostCategory.Value  = attributeData.get("PRD_ProductCostCategory","")
			item.QI_ProjectType.Value  = attributeData.get("PRD_ProductCostCategory","")
			Trace.Write('QICF -- Executed')
	Quote.SetGlobal('TPCPLSGs','')