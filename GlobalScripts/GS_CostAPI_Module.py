# from System.Net.Http import HttpClient
from GS_Validate_Product_Type import IsVCitem
from CF_UTILS import CF_CONSTANTS, get_custom_field_value, split_after_comma
from SQL_UTILS import get_all_records

def getHost():
	hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
	return hostquery.HostName


#This function gets the variant details 
def getVaraintsData(Product):
	VariantSysList=[]
	VariantList = []
	return_dict={}
	lv_seq=1

	for attr in Product.Attributes:
		for value in attr.SelectedValues:
			if value.SystemId not in VariantSysList:
				Variant_details_dic={}
				valueCode = attr.GetValue() if attr.DisplayType == "FreeInputNoMatching" else attr.SelectedValue.ValueCode
				#valueSystemId = attr.SelectedValue.SystemId if attr.SelectedValue else ""
				AttrSystemId = attr.SystemId if attr.SystemId else ""
				VariantSysList.append(value.SystemId)
				Variant_details_dic["instanceId"]="00000001"#str(p_guid)
				Variant_details_dic["sequenceNo"]=str(lv_seq)
				Variant_details_dic["characteristic"]=str(AttrSystemId)
				Variant_details_dic["value"]=str(valueCode)
				VariantList.append(Variant_details_dic)
			lv_seq=lv_seq+1
	return_dict["item"]=VariantList
	return return_dict


def getVariantsDataETL(Product):
	#type: (Product) -> dict
	"""Gets the variant details for ETL products"""
	variant_sys_ids = set()
	variant_list = []
	seq = 1

	for attr in Product.Attributes:
		for value in attr.SelectedValues:
			if value.SystemId not in variant_sys_ids:
				variant_sys_ids.add(value.SystemId)
				value_code = attr.GetValue() if attr.DisplayType == "FreeInputNoMatching" else attr.SelectedValue.ValueCode
				attr_system_id = attr.SystemId or ""

				# Zero-padded 3 digits
				seq_str = "%03d" % seq

				# build variant details dictionary
				variant_details = {
					"SEQUENCE": seq_str,
					"INST_ID": "00000001",
					"CHARACTERISTIC": str(attr_system_id),
					"CHARACTER_VALUE": str(value_code)
				}
				variant_list.append(variant_details)
			seq += 1

	return variant_list


#Gets accesstoken
def getAccessToken(host):
	url = "https://{}/v2/oauth/accesstoken".format(host)
	Trace.Write('URL:'+url)
	# with HttpClient() as api:
	headers={'ContentType':'application/x-www-form-urlencoded'}
	#SAP_COSTAPI_CRED: user credentials have been defined under credential management
	response=AuthorizedRestClient.GetClientCredentialsGrantOAuthToken('SAP_COSTAPI_CRED',url)
	Trace.Write('token_type in module:'+ str(response["token_type"]))
	Trace.Write('token_type in module:'+ str(response["access_token"]))
	return "{} {}".format(response["token_type"] , response["access_token"])


#Generate plant based on Sales org
def get_Plant(Quote,p_plant_name):
	marketCode = Quote.SelectedMarket.MarketCode
	salesOrg = marketCode.partition('_')[0]
	lv_plant=''
	#Get the plantcode based on Plant name selected at itemlevel #CXCPQ-57020
	qplant = SqlHelper.GetFirst("select PLANT_CODE from COUNTRY_SORG_PLANT_MAPPING CSPM where PLANT_NAME='{}'".format(p_plant_name))
	if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
		lv_plant = p_plant_name if p_plant_name else "7610"
	elif Quote.GetCustomField('Quote Tab Booking LOB').Content == 'LSS':
		qplant_lss = SqlHelper.GetFirst("select PLANT_CODE from COUNTRY_SORG_PLANT_MAPPING CSPM where PRODUCT_NAME='TRACE'")
		lv_plant = qplant_lss.PLANT_CODE # Softco Plant is only used for LSS
	elif qplant is not None:
		lv_plant=qplant.PLANT_CODE
	else:
		#Get the plantcode based on quote header plant field. #CXCPQ-57020
		custom_field_name = CF_CONSTANTS.get("QUOTE_LEVEL_PLANT_FIELD")
		full_plant_value = get_custom_field_value(Quote, custom_field_name)
		plant_code,plant_value = split_after_comma(full_plant_value)
		if plant_code is not None:
			lv_plant=plant_code
	return lv_plant


#Generate Payload from Quote Items
def gen_QuoteItems_PayLoad(Quote):
	domainquery = SqlHelper.GetFirst("Select domain from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
	lv_Source=''
	if domainquery is not None:
		lv_Source = domainquery.domain
	etl_query = "select BRP_PART from CT_ETL_PRODUCTS"
	etl_result = get_all_records(SqlHelper, etl_query, page_size=1000)
	etl_partnumbers = [record.BRP_PART for record in etl_result]
	vcMaterialCost_dic={}
	#Header Dictionary
	header_dic={"sourceSystem": lv_Source,"interfaceName": "HPSCPQ_SAP_COST_API","objectRowId": "1"}
	itemDetails_dic={}
	itemsList=[]
	lv_salesOrg_dic={}
	lv_salesOrg_dic["salesOrg"]=""#Quote.GetCustomField("Sales Area").Content
	lv_salesOrg_dic["distChnl"]=""
	lv_salesOrg_dic["soldTo"]=""
	lv_salesOrg_dic["shipTo"]=""
	lv_insitem_dic={}
	lv_insitem_dic["instanceId"]=""
	lv_insitem_dic["parentId"]=""
	lv_insitem_dic["partOfNo"]=""
	lv_insitem_dic["objKey"]=""
	lv_insitem_empty={}
	lv_ins_list=[]
	lv_ins_list.append(lv_insitem_dic)
	lv_insitem_empty["item"]=lv_ins_list
	ConfigIDSeq=1
	lv_Q_Type=Quote.GetCustomField("Quote Type").Content
	if lv_Q_Type == "Parts and Spot":
		for i in Quote.MainItems:
			getprdid = SqlHelper.GetFirst("SELECT UnitOfMeasure,IsSyncedFromBackOffice from products where product_catalog_code= '{}' and IsSyncedFromBackOffice = 'True' and PRODUCT_ACTIVE = 1 ".format(str(i.PartNumber))) #IsSyncedFromBackOffice= True--> SAP product
			if getprdid:
				item_dic={}
				item_dic["itemNo"]=i.QuoteItemGuid #Sending Guid as ItemNo
				full_plant_value = i.QI_Plant.Value
				plant_code,plant_name = split_after_comma(full_plant_value)
				lv_plant=get_Plant(Quote,plant_name)
				item_dic["plant"]= str(lv_plant)
				item_dic["saldet"]= lv_salesOrg_dic
				item_dic["material"]= i.PartNumber
				item_dic["quantity"]= str(1)# Get the cost for one unit quantity
				item_dic["uom"]=getprdid.UnitOfMeasure
				if i.PartNumber not in etl_partnumbers: item_dic["modelNo"] = i.QI_FME.Value
				item_dic["configId"]= str('{:0>6}'.format(ConfigIDSeq)) #Config ID is 6 digit. Padding the number with 0
				if IsVCitem(i.PartNumber)==True and i.QI_FME.Value=='':
					lvproduct = i.EditConfiguration()
					if i.PartNumber in etl_partnumbers:
						# build variant details for ETL products
						resp=getVariantsDataETL(lvproduct)
					else:
						resp=getVaraintsData(lvproduct)
					item_dic["variantConditions"]=resp
					lvproduct.UpdateQuote()
				else:
					item_dic["variantConditions"]=""
					
				item_dic["inst"]=lv_insitem_empty if i.PartNumber not in etl_partnumbers else ""
				itemsList.append(item_dic)
				ConfigIDSeq+=1

	req_payload={}
	if itemsList:
		itemDetails_dic["item"]=itemsList
		vcMaterialCost_dic["headerRequest"]=header_dic
		vcMaterialCost_dic["itemDetails"]=itemDetails_dic
		req_payload["vcMaterialCost"]=vcMaterialCost_dic

	return req_payload


#Generate Payload for single VC model/Part Number
def gen_Item_PayLoad(Quote,p_Material,p_fme,p_plant=''):
	domainquery = SqlHelper.GetFirst("Select domain from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
	lv_Source=''
	if domainquery is not None:
		lv_Source = domainquery.domain
	vcMaterialCost_dic={}
	#Header Dictionary
	header_dic={"sourceSystem": lv_Source,"interfaceName": "HPSCPQ_SAP_COST_API","objectRowId": "1"}
	itemDetails_dic={}
	itemsList=[]
	lv_salesOrg_dic={}
	lv_salesOrg_dic["salesOrg"]=""#Quote.GetCustomField("Sales Area").Content
	lv_salesOrg_dic["distChnl"]=""
	lv_salesOrg_dic["soldTo"]=""
	lv_salesOrg_dic["shipTo"]=""
	item_dic={}
	getprdid = SqlHelper.GetFirst("SELECT UnitOfMeasure,IsSyncedFromBackOffice from products where product_catalog_code= '{}' and IsSyncedFromBackOffice = 'True' and PRODUCT_ACTIVE = 1 ".format(str(p_Material))) #IsSyncedFromBackOffice= True--> SAP product
	if getprdid is not None:
		lv_plant=get_Plant(Quote,p_plant)
		item_dic["itemNo"]="000001"
		item_dic["plant"]= str(lv_plant)
		item_dic["saldet"]= lv_salesOrg_dic
		item_dic["material"]= str(p_Material)
		item_dic["quantity"]= str(1)
		item_dic["uom"]=getprdid.UnitOfMeasure
		item_dic["modelNo"]= str(p_fme)
		item_dic["configId"]= "000001" #Config ID is 6 digit. Padding the number with 0
		item_dic["variantConditions"]=""
		item_dic["inst"]=""
	itemsList.append(item_dic)
	req_payload={}
	if itemsList:
		itemDetails_dic["item"]=itemsList
		vcMaterialCost_dic["headerRequest"]=header_dic
		vcMaterialCost_dic["itemDetails"]=itemDetails_dic
		req_payload["vcMaterialCost"]=vcMaterialCost_dic
	return req_payload


#Calls the API and gets the cost
def getCost(host,accessTkn, payload):
	hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
	host = hostquery.HostName
	headers = {"HON-Org-Id":"PMT-HPS", "Authorization":accessTkn}
	Url = "https://{0}/sap/product/v1/product-cost".format(host)
	Trace.Write('URL:'+str(Url))
	Trace.Write('accessTkn:'+str(accessTkn))
	Trace.Write('payload:'+str(payload))
	return RestClient.Post(Url, payload, headers)
