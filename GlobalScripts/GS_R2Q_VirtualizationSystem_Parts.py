import GS_APIGEE_Integration_Util

excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
VSAttrDict = {}
getselectAttributedict = {}
VSAttrList = ('VS_24Port_Rack_Required', 'VS_48Port_Rack_Required', 'VS_Platform_Options', 'VS_Use_Own_OS_License', 'VS_Distribute_Multi_Clusters', 'VS_Essential_Host_Type', 'Virtualization_Acceptance_Test_requested', 'Virtualization_Will_Honeywell_perform_equipment', 'Virtualization_Does_the_customer_want_Honeywell', 'Virtualization DDS', 'Virtualization FDS', 'Virtualization_EBR_DDS', 'Virtualization_AV_DDS', 'Virtualization_Update existing drawing package', 'Virtualization_Will Honeywell provide the HW/SW?', 'Virtualization_New_drawing_package', 'Virtualization_OnSite_Activities_hours', 'R2Q_QuoteNumber')

def getSFQuoteID():
	from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
	class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
	class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
	bearerToken = class_sf_integration_modules.get_auth2_token()
	headers = class_sf_integration_modules.get_authorization_header(bearerToken)
	query = "?q="+"select+Id+from+Quote+where+Quote_ID__c={cartId}+and+Owner_ID__c={ownerId}".format(cartId = str(Quote.QuoteId),ownerId = str(Quote.UserId))
	quoteID = class_sf_integration_modules.call_soql_api(headers, query)
	if len(quoteID.records) != 0:
			for q in quoteID.records:
				SFQuoteID = str(q.Id)
			return SFQuoteID

def extractProductContainer(attrName, product,getselectAttributedict):
	containerList = []
	containerRows = product.GetContainerByName(attrName).Rows
	if containerRows.Count > 0:
		for contanierRow in containerRows:
			contanierRowDict = {}
			for col in contanierRow.Columns:
				contanierRowDict[col.Name] = contanierRow[col.Name]
			containerList.append(contanierRowDict)
	return containerList

def extractProductAttributes(attributedict, product,getselectAttributedict):
	for attr in product.Attributes:
		if attr.DisplayType == 'Container' and attr.Name not in attributedict:
			attributedict[attr.Name] = extractProductContainer(attr.Name, product,getselectAttributedict)
		else:
			if product.Attr(attr.Name).GetValue() != '' and attr.Name in VSAttrList:
				attributedict[attr.Name] = product.Attr(attr.Name).GetValue()
				getselectAttributedict[attr.Name] = product.Attr(attr.Name).GetValue()

def BuildJSON(ChildProduct):
	Log.Info('inside = BuildJSON')
	extractProductAttributes(VSAttrDict,ChildProduct,getselectAttributedict)
	SFQuoteId = getSFQuoteID()
	Port24 = VSAttrDict.get('VS_24Port_Rack_Required', '0')
	platform = VSAttrDict.get('VS_Platform_Options', '')
	NewDraw = VSAttrDict.get('Virtualization_New_drawing_package', '')
	OSLicense = VSAttrDict.get('VS_Use_Own_OS_License', '')
	Port48 = VSAttrDict.get('VS_48Port_Rack_Required', '0')
	MultiClus = VSAttrDict.get('VS_Distribute_Multi_Clusters', '')
	VS_DDS = VSAttrDict.get('Virtualization DDS', '')
	Switches = VSAttrDict.get('Virtualization_Does_the_customer_want_Honeywell', '')
	OnSiteHrs = VSAttrDict.get('Virtualization_OnSite_Activities_hours', '')
	AcceptanceReq = VSAttrDict.get('Virtualization_Acceptance_Test_requested', '')
	DoesCusWant = VSAttrDict.get('Virtualization_Does_the_customer_want_Honeywell', '')
	HostType = VSAttrDict.get('VS_Essential_Host_Type', '')
	ExistingDraw = VSAttrDict.get('Virtualization_Update existing drawing package', '')
	PerfEquip = VSAttrDict.get('Virtualization_Will_Honeywell_perform_equipment', '')
	VS_FDS = VSAttrDict.get('Virtualization FDS', '')
	VS_AV_DDS = VSAttrDict.get('Virtualization_AV_DDS', '')
	ProvideHW_SW = VSAttrDict.get('Virtualization_Will Honeywell provide the HW/SW?', '')
	VS_EBR_DDS = VSAttrDict.get('Virtualization_EBR_DDS', '')
	QuoteId = VSAttrDict.get('R2Q_QuoteNumber','')
	WorkLoadDetails = VSAttrDict.get('Virtualization_System_WorkLoad_Cont','')
	for wrkld in WorkLoadDetails:
		wrkld['Workload_Name'] = wrkld.pop('Work_Load_Name')
		wrkld['Workload_Type'] = wrkld.pop('Work_Load_Type')

	if VSAttrDict:
		Fin_JSON_Structure = {"SFQuoteID": SFQuoteId, "CPQQuoteNumber": QuoteId, "Module": "VRT", "Virtualization": {"VRT_Essential_Platform_Options": platform, "VRT_Essential_Host_HW_Type": HostType, "VRT_Use_Own_OS_License": OSLicense, "VRT_Workload_Multiple_Clusters": MultiClus, "VRT_Chasis_level_Protection": "", "VRT_Hardware_Warrenty": "", "VRT_24port_Switch_Number": Port24, "VRT_48port_Switch_Number": Port48, "VRT_DDS": VS_DDS, "VRT_FDS": VS_FDS, "VRT_EBR_DDS": VS_EBR_DDS, "VRT_AV_DDS": VS_AV_DDS, "VRT_ExistingDrawingPackage":  ExistingDraw, "VRT_NewDrawingPackage": NewDraw, "VRT_AcceptanceTest": AcceptanceReq, "VRT_HoneywellHWSW": ProvideHW_SW, "VRT_AdditionalOnsiteActivity":"" , "VRT_OnsiteActivity": OnSiteHrs, "VRT_HoneywellPerformEqipmentInstallation": PerfEquip, "VRT_HoneywellConfigureSwitches": Switches},"Workload_Details": { "Workload_Config" : WorkLoadDetails }}

	Trace.Write('Final_JSON ==> ' + str(JsonHelper.Serialize(Fin_JSON_Structure)))
	return Fin_JSON_Structure

try:
	QuoteNumber = Param.QuoteNumber
	Quote = QuoteHelper.Edit(QuoteNumber)
	for item in Quote.MainItems:
		#Log.Info('inside = MainItems')
		if item.PartNumber == 'Migration':
			Product = item.EditConfiguration()
			migration_new_cont = Product.GetContainerByName('CONT_Migration_MSID_Selection')
			for MigrationNew in migration_new_cont.Rows:
				if 'Virtualization System' in MigrationNew['Selected Products'] or 'Virtualization System Migration' in MigrationNew['Selected Products']:
					#Log.Info('inside = MigrationNew')
					for childproduct in MigrationNew.Product.GetContainerByName('CONT_MSID_SUBPRD').Rows:
						if 'Virtualization System' in childproduct['Selected_Products']:
							#Log.Info('inside = childproduct')
							APIGEE_Credentials = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_Credentials'").Value
							APIGEE_R2Q_URL = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_URL'").Value
							tokenUrl = "{}/v2/oauth/accesstoken".format(APIGEE_R2Q_URL)
							responseToken=AuthorizedRestClient.GetClientCredentialsGrantOAuthToken(APIGEE_Credentials,tokenUrl)
							final_request_body = BuildJSON(childproduct.Product)
							Req_Token = "{} {}".format(responseToken["token_type"], responseToken["access_token"])
							Url="https://it.api-beta.honeywell.com/cpq/r2q/sfdc/v1/cpqtor2q/virtualization"
							header = {"Content-Type" : "application/json","Authorization" : "{}".format(Req_Token),"HON-Org-Id" : "PMT-HPS" }
							res = RestClient.Post(Url,RestClient.SerializeToJson(str(final_request_body)),header)
	Log.Info('GS_R2Q_VirtualizationSystem_Parts Success-->>'+str(final_request_body))
except Exception as ex:
	Log.Info('GS_R2Q_VirtualizationSystem_Parts Error-->>'+str(ex))
	final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'Migration','Action':'Update','Status':'Fail','Action_List':[{'ActionName':str(Param.ActionName),'ScriptName':'GS_R2Q_VirtualizationSystem_Parts','ErrorMessage':str(ex)}]}
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)