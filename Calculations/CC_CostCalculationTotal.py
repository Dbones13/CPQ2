if Session["prevent_execution"] != "true":
	#Get cost from SAP
	import GS_Curr_ExchRate_Mod
	import GS_Validate_Product_Type
	import re
	import GS_CostAPI_Module
	import GS_ItemCalculations
	import GS_CalculateTotals as tcUtil

	def removeQuoteMessages(Quote):
		pattern = r'^Cost for [\w\W]*? is either Zero or not defined in SAP[\w\W]*?Plant[^>]*?$|^Quote Currency [\w\W]*? and SAP Plant [\w\W]*? Cost Currency [\w\W]*? is different. Exchange Rate is missing in the Currency_ExchangeRate_Mapping table.$|^Error while Fetching the Cost from SAP for the material[\w\W]*?$'
		for i in list(Quote.Messages):
			if re.match(pattern, i):
				Quote.Messages.Remove(i)

	def getFloat(Var):
		if Var:
			return float(Var)
		return 0

	#Get host name from environment
	def getHost():
		hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
		if hostquery is not None:
			return hostquery.HostName
		return ''

	#Call API to fetch cost and assign to Quote Item fields
	def fn_getCost(host,p_Material,p_fme,p_plant):
		Trace.Write('In CC_GetCost_Plant_Change fn_getCost')
		try:
			req_payload=GS_CostAPI_Module.gen_Item_PayLoad(Quote,p_Material,p_fme,p_plant)
			accessTkn = GS_CostAPI_Module.getAccessToken(host)
			CostAPIResp_Json = GS_CostAPI_Module.getCost(host, accessTkn,req_payload)
			lv_res=CostAPIResp_Json['vcMaterialCostResponse']['vcCostResponse']['item']
			Trace.Write('API response:'+str(lv_res))
			for atnm in list(lv_res):
				if str(atnm["status"])!='E' and getFloat(atnm["totalCost"])>0:
					#CXCPQ-59003 Added conversion logic when CPQ quote currency is different from the SAP Plant Currency code. 07/19/2023
					if Quote.GetCustomField("Currency").Content==str(atnm["currency"]):
						Item.Cost=getFloat(atnm["totalCost"])
						Item.QI_SAP_UnitCost.Value=getFloat(atnm["totalCost"])
						Item.QI_prev_plant_value.Value=Item.QI_Plant.Value
						Trace.Write('Material Cost from SAP:'+ str(getFloat(atnm["totalCost"])))
					else:
						lv_exrate=GS_Curr_ExchRate_Mod.fn_get_curr_exchrate(str(atnm["currency"]),Quote.GetCustomField("Currency").Content)
						if lv_exrate!=0:
							Item.Cost=getFloat(atnm["totalCost"]) * getFloat(lv_exrate)
							Item.QI_SAP_UnitCost.Value=getFloat(atnm["totalCost"]) * getFloat(lv_exrate)
							Item.QI_prev_plant_value.Value=Item.QI_Plant.Value
							Trace.Write('Material Cost from SAP:'+ str(getFloat(atnm["totalCost"])))
							Trace.Write('Material Cost after conversion:'+ str(Item.Cost))
						else:
							Item.Cost=0
							Item.QI_SAP_UnitCost.Value=0
							# Quote.Messages.Clear()
							removeQuoteMessages(Quote) # CXCPQ-78401: Added on 28/02/2024
							Quote.Messages.Add("Quote Currency " + Quote.GetCustomField("Currency").Content +" and SAP Plant "+str(Item.QI_Plant.Value)+ " Cost Currency "+ str(atnm["currency"]) + " is different. Exchange Rate is missing in the Currency_ExchangeRate_Mapping table.")
							Trace.Write('Missing Exchange rate:')
				else:
					Item.Cost=0
					Item.QI_SAP_UnitCost.Value=0
					# Quote.Messages.Clear()
					removeQuoteMessages(Quote) # CXCPQ-78401: Added on 28/02/2024
					Quote.Messages.Add("Cost for the "+ p_Material + ' is either Zero or not defined in SAP (Plant :'+str(Item.QI_Plant.Value)+')')
					Trace.Write('Cost for the material is zero or not defined')
		except Exception as e:
			Item.Cost=0
			Item.QI_SAP_UnitCost.Value=0
			# Quote.Messages.Clear()
			removeQuoteMessages(Quote) # CXCPQ-78401: Added on 28/02/2024
			Quote.Messages.Add("Error while Fetching the Cost from SAP for the material"+ p_Material)
			# Trace.Write("Error--->:"+str(sys.exc_info()[1]))

	for Item in Quote.Items:
		#Below logic runs only for PMC Parts & Spot Quote
		if Quote.GetCustomField("CF_Plant").Content!='' and Quote.GetCustomField("Quote Type").Content == 'Parts and Spot' and Quote.GetCustomField('Booking LOB').Content == "PMC":
			Trace.Write('In CC_GetCost_Plant_Change:'+str(Item.PartNumber)+':'+str(Item.QI_Plant.Value)+'::'+str(Item.QI_prev_plant_value.Value)+':::'+str(Item.Cost))

			#Observed PMC writeIn products are created in SAP. Hence, adding extra condition to not to override writeIn cost via API
			writein_data = SqlHelper.GetFirst("SELECT Product FROM WRITEINPRODUCTS WHERE Product= '{}'".format(str(Item.PartNumber)))
			getprdid = SqlHelper.GetFirst("SELECT IsSyncedFromBackOffice from products where product_catalog_code= '{}' and IsSyncedFromBackOffice = 'True' and PRODUCT_ACTIVE = 1 ".format(str(Item.PartNumber)))
			if getprdid is not None and writein_data is None:
				if Item.QI_prev_plant_value.Value!=Item.QI_Plant.Value or Item.QI_SAP_UnitCost.Value==0:
					#call cost API only when there is plant change at Item level or when cost is zero.
					host=getHost()
					if Item.QI_Plant.Value=='':#Set only when Quote Item Plant is blank
						Item.QI_Plant.Value=Quote.GetCustomField("CF_Plant").Content
					if host!='':
						fn_getCost(host,Item.PartNumber,Item.QI_FME.Value,Item.QI_Plant.Value)
				else:
					if Item.QI_prev_plant_value.Value==Item.QI_Plant.Value and Item.QI_SAP_UnitCost.Value!=0:
						#cost already fetched from SAP
						Item.Cost=Item.QI_SAP_UnitCost.Value
					else:
						Item.Cost=0
						Item.QI_SAP_UnitCost.Value=0
						# Quote.Messages.Clear()
						removeQuoteMessages(Quote) # CXCPQ-78401: Added on 28/02/2024
						Quote.Messages.Add('Cost for material '+ p_Material + ' is either Zero or not defined in SAP (Plant :'+str(Item.QI_Plant.Value)+'). Please consider different Plant.')
						Trace.Write('Cost for the material is zero or not defined')

		#Get VC cost from SAP for Project Type Quote CXCPQ-59003 & CXCPQ-66622
		elif Quote.GetCustomField("Quote Type").Content == 'Projects' and GS_Validate_Product_Type.IsVCitem(Item.PartNumber)==True:
			qplant=None
			if Item.ProductName=='Generic System Child Product' and Item.QI_FME.Value!='': # For Generic system
				qplant = SqlHelper.GetFirst("select PLANT_CODE,PLANT_NAME from COUNTRY_SORG_PLANT_MAPPING  where PRODUCT_NAME='{}'".format(Item.ProductName))
			else:
				qVFD = SqlHelper.GetFirst("select VFD_VC_Model from VFD_VC_MODELS  where VFD_VC_Model='{}'".format(Item.PartNumber))
				if qVFD is not None: #VFD Materials
					qplant = SqlHelper.GetFirst("select PLANT_CODE,PLANT_NAME from COUNTRY_SORG_PLANT_MAPPING  where PART_NUMBER='{}'".format(Item.PartNumber))
			if qplant is not None:
				if Item.QI_SAP_UnitCost.Value==0:
					host=getHost()
					if host!='' and qplant.PLANT_NAME!='':
						fn_getCost(host,Item.PartNumber,Item.QI_FME.Value,qplant.PLANT_NAME)
				else:
					if Item.QI_SAP_UnitCost.Value!=0:
						#cost already fetched from SAP
						Item.Cost=Item.QI_SAP_UnitCost.Value
					else:
						Item.Cost=0
						Item.QI_SAP_UnitCost.Value=0
						# Quote.Messages.Clear()
						removeQuoteMessages(Quote) # CXCPQ-78401: Added on 28/02/2024
						Quote.Messages.Add('Cost for material '+ p_Material + ' is either Zero or not defined in SAP (Plant :'+str(Item.QI_Plant.Value)+'). Please consider different Plant.')
						Trace.Write('Cost for the material is zero or not defined')
			else:
				Trace.Write('Plant is not defined for the VC Material:'+str(Item.PartNumber))

		#CXCPQ-65110: Added condition to improve the performance. calculateCosts not required to run for PMC Parts and Spot Quote and for VC products defined in FME_PARTS table.
		elif (Quote.GetCustomField("Booking LOB").Content != "PMC" or Quote.GetCustomField("Quote Type").Content != "Parts and Spot") and Quote.GetCustomField('Quote Type').Content not in ('Contract New','Contract Renewal'):
			if Item.ProductName!='Productized Skid Quote Item': #For productized skid Items cost is fetched from SAP
				qry = SqlHelper.GetFirst("SELECT 1 as flag from FME_PARTS WHERE PARTNUMBER = '{}'".format(str(Item.PartNumber)))
				if qry is None: #	CXCPQ-69436: Added Qry condition to avoid conflict with  K&E VC materials
						GS_ItemCalculations.calculateCosts(Quote , Quote.GetCustomField("Booking LOB").Content,Quote.GetCustomField("Quote Type").Content,Item, TagParserQuote)
		Item.ExtendedCost = Item.Quantity * Item.Cost
		Item["QI_RegionalMargin"].Value = Item.ExtendedAmount - Item.ExtendedCost
		Item["QI_WTWMargin"].Value = Item.ExtendedAmount - Item["QI_ExtendedWTWCost"].Value
		if Item.ExtendedAmount != 0.00:
			if Item.ExtendedAmount < Item.ExtendedCost:
				Item["QI_RegionalMarginPercent"].Value = 0.0
				Item["QI_WTWMarginPercent"].Value = 0.0
			else:
				Item["QI_RegionalMarginPercent"].Value = (Item["QI_RegionalMargin"].Value / Item.ExtendedAmount) * 100
				Item["QI_WTWMarginPercent"].Value = (Item["QI_WTWMargin"].Value / Item.ExtendedAmount) * 100
	tcUtil.calculateParent(Quote)