from CF_UTILS import CF_CONSTANTS, get_custom_field_value, split_after_comma

if Session["prevent_execution"] != "true" and Quote.GetGlobal('PerformanceUpload') != 'Yes' and (Quote.GetCustomField('CF_Plant_Prevent_Calc').Content != 'true' or Quote.GetCustomField('Booking LOB').Content != 'PMC'):
	#Get cost from SAP
	#import sys # Commented due to th error "Import of iron python built-in modules: "sys" on the line 2 is not allowed."
	import GS_Curr_ExchRate_Mod
	import re

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
		hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME(NOLOCK) where Domain in (select tenant_name from tenant_environments(NOLOCK) where is_current_environment = 1)")
		if hostquery is not None:
			return hostquery.HostName
		return ''

	#Call API to fetch cost and assign to Quote Item fields
	def fn_getCost(host,p_Material,p_fme,p_plant):
		import GS_CostAPI_Module

		try:
			req_payload=GS_CostAPI_Module.gen_Item_PayLoad(Quote,p_Material,p_fme,p_plant)
			accessTkn = GS_CostAPI_Module.getAccessToken(host)
			CostAPIResp_Json = GS_CostAPI_Module.getCost(host, accessTkn,req_payload)
			lv_res=CostAPIResp_Json['vcMaterialCostResponse']['vcCostResponse']['item']

			for atnm in list(lv_res):
				if str(atnm["status"])!='E' and getFloat(atnm["totalCost"])>0:
					#CXCPQ-59003 Added conversion logic when CPQ quote currency is different from the SAP Plant Currency code. 07/19/2023
					if Quote.GetCustomField("Currency").Content==str(atnm["currency"]):
						Item.Cost=getFloat(atnm["totalCost"])
						Item.QI_SAP_UnitCost.Value=getFloat(atnm["totalCost"])
						Item.QI_prev_plant_value.Value=Item.QI_Plant.Value

					else:
						lv_exrate=GS_Curr_ExchRate_Mod.fn_get_curr_exchrate(str(atnm["currency"]),Quote.GetCustomField("Currency").Content)
						if lv_exrate!=0:
							Item.Cost=getFloat(atnm["totalCost"]) * getFloat(lv_exrate)
							Item.QI_SAP_UnitCost.Value=getFloat(atnm["totalCost"]) * getFloat(lv_exrate)
							Item.QI_prev_plant_value.Value=Item.QI_Plant.Value

						else:
							Item.Cost=0
							Item.QI_SAP_UnitCost.Value=0
							# Quote.Messages.Clear()
							removeQuoteMessages(Quote) # CXCPQ-78401: Added on 28/02/2024
							Quote.Messages.Add("Quote Currency " + Quote.GetCustomField("Currency").Content +" and SAP Plant "+str(Item.QI_Plant.Value)+ " Cost Currency "+ str(atnm["currency"]) + " is different. Exchange Rate is missing in the Currency_ExchangeRate_Mapping table.")

				else:
					Item.Cost=0
					Item.QI_SAP_UnitCost.Value=0
					# Quote.Messages.Clear()
					removeQuoteMessages(Quote) # CXCPQ-78401: Added on 28/02/2024
					Quote.Messages.Add("Cost for the "+ p_Material + ' is either Zero or not defined in SAP (Plant :'+str(Item.QI_Plant.Value)+')')

		except Exception as e:
			Item.Cost=0
			Item.QI_SAP_UnitCost.Value=0
			# Quote.Messages.Clear()
			removeQuoteMessages(Quote) # CXCPQ-78401: Added on 28/02/2024
			Quote.Messages.Add("Error while Fetching the Cost from SAP for the material"+ p_Material)


			#Below logic runs only for PMC Parts & Spot Quote       
	if Quote.GetCustomField("CF_Plant").Content!='' and ((Quote.GetCustomField("Quote Type").Content == 'Parts and Spot' and Quote.GetCustomField('Booking LOB').Content == "PMC")):


		#Observed PMC writeIn products are created in SAP. Hence, adding extra condition to not to override writeIn cost via API
		writein_data = SqlHelper.GetFirst("SELECT Product FROM WRITEINPRODUCTS(NOLOCK) WHERE Product= '{}'".format(str(Item.PartNumber)))
		getprdid = SqlHelper.GetFirst("SELECT IsSyncedFromBackOffice from products(NOLOCK) where product_catalog_code= '{}' and IsSyncedFromBackOffice = 'True' and PRODUCT_ACTIVE = 1 ".format(str(Item.PartNumber)))
		if getprdid is not None and writein_data is None:
			if Item.QI_Plant.Value == '' or Item.QI_prev_plant_value.Value!=Item.QI_Plant.Value or Item.QI_SAP_UnitCost.Value>=0:
				#call cost API only when there is plant change at Item level or when cost is zero.
				host=getHost()
				if Item.QI_Plant.Value=='':#Set only when Quote Item Plant is blank
					custom_field_name = CF_CONSTANTS.get("QUOTE_LEVEL_PLANT_FIELD")
					full_plant_value = get_custom_field_value(Quote, custom_field_name)
					plant_code,plant_name = split_after_comma(full_plant_value)
					Item.QI_Plant.Value = plant_name
				if host!='':
					full_plant_value = Item.QI_Plant.Value
					plant_code,plant_name = split_after_comma(full_plant_value)
					fn_getCost(host,Item.PartNumber,Item.QI_FME.Value,plant_name)
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


	#Get VC cost from SAP for Project Type Quote CXCPQ-59003 & CXCPQ-66622
	if Quote.GetCustomField('Booking LOB').Content != 'HCP' and Quote.GetCustomField("Quote Type").Content == 'Projects' and SqlHelper.GetFirst("select 1 from Products where IsSyncedFromBackOffice = 'True' and IsSimple = 'False' and product_catalog_code = '{}'".format(Item.PartNumber)):
		qplant=None
		if Item.ProductName=='Generic System Child Product' and Item.QI_FME.Value!='': # For Generic system
			qplant = SqlHelper.GetFirst("select PLANT_CODE,PLANT_NAME from COUNTRY_SORG_PLANT_MAPPING(NOLOCK)  where PRODUCT_NAME='{}'".format(Item.ProductName))
		else:
			qVFD = SqlHelper.GetFirst("select VFD_VC_Model from VFD_VC_MODELS(NOLOCK)  where VFD_VC_Model='{}'".format(Item.PartNumber))
			if qVFD is not None: #VFD Materials
				qplant = SqlHelper.GetFirst("select PLANT_CODE,PLANT_NAME from COUNTRY_SORG_PLANT_MAPPING(NOLOCK)  where PART_NUMBER='{}'".format(Item.PartNumber))
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

		else:
			Trace.Write('Plant is not defined for the VC Material:'+str(Item.PartNumber))