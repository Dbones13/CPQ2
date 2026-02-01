Quote_Type = Quote.GetCustomField('Quote Type').Content
if Quote_Type in ('Contract New','Contract Renewal'):
	import GS_PMC_QLI_Sync_Functional_Util as QLI_Helper
	from CPQ_SF_PriceBookMapping import CL_PriceBookMapping
	from CPQ_SF_Configuration import CL_SalesforceSettings
	from GS_SC_QuoteLinesHelper import CL_SC_QuoteLinesHelper
	qLineHelper = CL_SC_QuoteLinesHelper(Quote, TagParserQuote, None, Session)
	SF_QUOTE_LINE_ITEM_OBJECT = "QuoteLineItem"
	SF_QUOTE_ID_FIELD = "Quote.Name"
	SF_PSC_QUOTE_ID_FIELD = "QuoteLineItemId__r.Quote.Name"
	SF_PRODUCT_OBJECT = "Product2"
	SF_PSC_LINE_ITEM_OBJECT = "PSC_Scope__c"
	SF_INVOICING_SCHEDULE_OBJECT = "Invoicing_Schedule__c"
	SF_INVOICING_SCHEDULE_QUOTE_ID_FIELD = "SC_Quote_Id__r.ID"
	SF_PSC_SCOPE_QUOTE_ID_FIELD = "QuoteLineItemId__r.QuoteId"
	SF_TEAMROLE_OBJECT = "Service_Contract_Team__c"
	SALESFORCE_URL = CL_SalesforceSettings.SALESFORCE_URL
	SALESFORCE_VERSION = "55.0"
	GET_SOQL_API = "{sfUrl}/services/data/v{version}/query/{soql}"
	GET = "GET"
	POST = "POST"
	PATCH = "PATCH"
	DELETE = "DELETE"
	GET_DESCRIBE_API = "{sfUrl}/services/data/v{version}/sobjects".format(sfUrl=str(SALESFORCE_URL), version=str(SALESFORCE_VERSION))
	REF_GET_DESCRIBE = "Get Describe information on all SObjects"
	AUTH_API = "/services/oauth2/token"
	SALESFORCE_PWD= "CPQ_SFDC_PWD"
	SALESFORCE_SECRET = "CPQ_SFDC_SECRET"
	REF_GET_QUOTE_LINE_ITEMS = "Quote Line Items"
	REF_GET_PSC_LINE_ITEMS = "PSC Line Items"
	REF_DEL_QUOTE_LINE_ITEMS = "Delete Quote Line Items"
	REF_DEL_PSC_LINE_ITEMS = "Delete PSC Line Items"
	REF_DEL_INVOICING_SCHEDULE_ITEMS = "Delete Invoicing Schedule Items"
	REF_CREATE_QUOTE_LINE_ITEMS = "Create Quote Line Items"
	REF_CREATE_PSC_LINE_ITEMS = "Create PSC Line Items"
	REF_GET_PRICE_BOOK = "Get Price Book Entries"
	DELETE_API_RECORD_LIMIT = CREATE_API_RECORD_LIMIT = 200
	GET_INTERNAL_PRODUCT_SOQL_LIMIT = 7000
	GET_PRICEBOOK_ENTRIES_SOQL_LIMIT = 5000
	CR_DELETE_SOBJECT_COLLECTION_API = "/services/data/v{version}/composite/sobjects?ids={records}"
	CR_SOBJECT_COLLECTION_API = "/services/data/v{version}/sobjects/Quote/{recordid}"
	TYPE_STRING = "String"
	TYPE_FLOAT = "Float"
	TYPE_BOOL = "Boolean"

	SERVICE_PRICE_BOOK_ID = CL_PriceBookMapping.SERVICE_PRICE_BOOK_ID
	# Salesforce Multi-Currency Everywhere
	SF_MCE = True
	SOBJECT_COLLECTION_API = "{sfUrl}/services/data/v{version}/composite/sobjects".format(sfUrl=str(SALESFORCE_URL), version=str(SALESFORCE_VERSION))
	genric_prd =  SqlHelper.GetList("SELECT distinct Product_Type FROM CT_SC_Entitlements_Data WHERE Status='Active' and Module_Name ='Generic Module'")
	gen_product = [prd.Product_Type for prd in genric_prd]

	def build_permission_checklist( sObject, createable = False, updateable = False, deletable = False, queryable = False):
		permission = dict()
		permission["SObject"] = sObject
		permission["createable"] = createable
		permission["updateable"] = updateable
		permission["deletable"] = deletable
		permission["queryable"] = queryable
		return permission

	def replace_special_char(text):
		special_chars = [{"symbol": "&", "code": "%26"}, {"symbol": "#", "code": "%23"}]
		for special_char in special_chars:
			text = text.replace(special_char["symbol"], special_char["code"])
		return text

	def build_soql_query(selectedFields, table, condition):
		soql = None
		if selectedFields != "" and table != "":
			if condition == "":
				soql = "?q=SELECT {selectedFields} FROM {table}".format(selectedFields=str(selectedFields), table=str(table))
			else:
				condition = replace_special_char(str(condition))
				soql = "?q=SELECT {selectedFields} FROM {table} WHERE {condition}".format(selectedFields=str(selectedFields), table=str(table), condition=str(condition))
		if soql is not None: soql = soql.replace(" ", "+")
		return soql

	def get_authorization_header(bearerToken):
		headers = dict()
		headers["Authorization"] = "Bearer " + bearerToken
		return headers

	def get_describe_all(bearerToken):
		response = None
		if not Session["Describe"]:
			url = GET_DESCRIBE_API
			headers = get_authorization_header(bearerToken)
			response = call_rest_api(url, headers, None, GET, REF_GET_DESCRIBE)
			if response: Session["Describe"] = response
		else: response = Session["Describe"]
		return response

	def get_auth2_token():
		accessToken = str()
		if not Session["apiSessionID"]: accessToken = get_admin_auth2_token()
		else: accessToken = Session["apiSessionID"]
		return accessToken

	def get_user_auth2_token():
		accessToken = str()
		if Session["apiSessionID"]: accessToken = Session["apiSessionID"]
		return accessToken

	def get_admin_auth2_token():
		accessToken = str()
		if Session["adminApiSessionID"]:
			url = SALESFORCE_URL + AUTH_API
			response = AuthorizedRestClient.GetPasswordGrantOAuthToken(SALESFORCE_PWD, SALESFORCE_SECRET, url)
			if response["access_token"] != "" and response["access_token"] is not None:
				Session["adminApiSessionID"] = accessToken = str(response.access_token)
			else:
				Trace.Write("CPQ-SFDC: Integration Authentication Error : {}".format(str(response)))
		else:
			accessToken = Session["adminApiSessionID"]
		return accessToken

	def check_api_permissions(permissionList):
		# Permission
		allowed = True
		# Stop permission check flag
		checkFinished = False
		# Get Describe
		describe = get_describe_all(get_auth2_token())
		# Check Permissions
		for permission in permissionList:
			# Get permissions for SObject
			sObjectPermission = next((desc for desc in describe.sobjects if desc["name"]==permission["SObject"]), None)
			if sObjectPermission:
				for action in ["createable", "updateable", "deletable", "queryable"]:
					if permission[action]:
						if sObjectPermission[action] == False:
							allowed = False
							checkFinished = True
							break
			else:
				allowed = False
				checkFinished = True

			if checkFinished:
				break
		return allowed

	def call_rest_api( url, headers, body, method, integrationReference, permissionList = None):
		response = None
		#class_msg_handler = CL_MessageHandler(self.Quote, self.TagParserQuote, None, None)
		# Check permissions
		if permissionList:
			allowed = check_api_permissions(permissionList)
			if allowed is False:
				# Set header auth to admin
				adminToken = get_admin_auth2_token()
				headers["Authorization"] = "Bearer "+ adminToken
		try:
			if method == GET:
				response = RestClient.Get(url, headers)
			elif method == POST:
				response = RestClient.Post(url, body, headers)
				Log.Info("CPQ-SFDC: Request ({integrationReference})".format(integrationReference=str(integrationReference)), unicode(body))
			elif method == PATCH:
				response = RestClient.Patch(url, body, headers)
			elif method == DELETE:
				response = RestClient.Delete(url, headers)
		except SystemError as e:
			response = None
			msg = """Integration Error - {integrationReference}: {error}""".format(integrationReference=str(integrationReference), error=str(e))
		return response

	def get_sf_quote_id(bearerToken, quoteId, integrationReference):
		SFDC_QuoteID = None
		condition = """{sfQuoteIdField}='{quoteId}'""".format(sfQuoteIdField="Name" ,quoteId=str(Quote.CompositeNumber))
		soql = build_soql_query(selectedFields="Id",
										table="Quote",
										condition=condition)
		if soql:
			headers = get_authorization_header(bearerToken)
			response = call_soql_api(headers, soql, integrationReference)
			#Trace.Write(response)
			if response["totalSize"] > 0:
				SFDC_QuoteID = response["records"][0]["Id"]
				#Trace.Write(SFDC_QuoteID)
		return SFDC_QuoteID


	def set_sf_PMC_pricebook(quoteID, bearerToken, body, integrationReference, permissionList = None):
		# API path
		headers = get_authorization_header(bearerToken)
		url = SALESFORCE_URL + CR_SOBJECT_COLLECTION_API.format( version=str(SALESFORCE_VERSION), recordid=str(quoteID))
		response = call_rest_api(url, headers, body, PATCH, integrationReference, permissionList)
		return response

	def call_soql_api(headers, soql, integrationReference=None):
		# API path
		url = GET_SOQL_API.format(sfUrl=str(SALESFORCE_URL), version=str(SALESFORCE_VERSION), soql=str(soql))
		response = call_rest_api(url, headers, None, GET, integrationReference)
		return response

	# Function to get Salesforce Line item records from OpportunityLineItem object
	def get_sf_quote_line_items(bearerToken, quoteId, integrationReference):
		response = None
		condition = """{sfQuoteIdField}='{quoteId}'""".format(sfQuoteIdField=str(SF_QUOTE_ID_FIELD) ,quoteId=str(quoteId))
		soql = build_soql_query(selectedFields="Id,Product2Id,Product2.ProductCode,PricebookEntryId,QuoteId",
										table=SF_QUOTE_LINE_ITEM_OBJECT,
										condition=condition)
		if soql:
			headers = get_authorization_header(bearerToken)
			response = call_soql_api(headers, soql, integrationReference)
		return response

	def get_sf_psc_scope_items(bearerToken, quoteId, integrationReference):
		response = None
		condition = """{sfQuoteIdField}='{quoteId}'""".format(sfQuoteIdField=str(SF_PSC_SCOPE_QUOTE_ID_FIELD) ,quoteId=str(quoteId))
		soql = build_soql_query(selectedFields="Id",
										table=SF_PSC_LINE_ITEM_OBJECT,
										condition=condition)
		if soql:
			headers = get_authorization_header(bearerToken)
			response = call_soql_api(headers, soql, integrationReference)
		return response

	# Function to build delete SObject collection url
	def build_delete_sobj_collection_url(records):
		url = None
		records = str(records)[1:-1].replace("'", "").replace(" ", "")
		# API path
		url = CR_DELETE_SOBJECT_COLLECTION_API.format(version=str(SALESFORCE_VERSION), records=str(records))
		return url
	
	def call_sobject_delete_api( bearerToken, url, integrationReference, permissionList = None):
		headers = get_authorization_header(bearerToken)
		response = call_rest_api(url, headers, None, DELETE, integrationReference, permissionList)
		return response
	
	def delete_PSC_scope_items(bearerToken, quoteId):
		responses = list()
		permissionList = [build_permission_checklist(SF_PSC_LINE_ITEM_OBJECT, False, False, True, False)]
		# Get all QuoteLineItem records to delete
		lineItems = get_sf_psc_scope_items(bearerToken, quoteId, REF_GET_PSC_LINE_ITEMS)
		if lineItems and lineItems["totalSize"] > 0:
			lineItemrecords = [str(record["Id"]) for record in lineItems["records"]]
			# Delete in batches of API_LIMIT.DELETE_API_RECORD_LIMIT (Currently 200)
			for batch in range(0, len(lineItemrecords), DELETE_API_RECORD_LIMIT):
				url = SALESFORCE_URL + build_delete_sobj_collection_url(lineItemrecords[batch:batch+DELETE_API_RECORD_LIMIT])
				response = call_sobject_delete_api(bearerToken, url, REF_DEL_PSC_LINE_ITEMS, permissionList)
				responses.append(response)
		return responses

	def get_product_lookups(Quote, TagParserQuote, cpqItem):
		productlookUps = list()
		lookUp = dict()
		lookUp["SalesforceField"] = "ProductCode"
		lookUp["CpqLookUpValue"] = cpqItem.QI_PartNumber.Value.strip().split(';')[0] #"MC-TAMR06" #cpqItem.QI_PartNumber.Value
		lookUp["FieldType"] = TYPE_STRING
		productlookUps.append(lookUp)
		return productlookUps

	def get_sf_internal_product_ids(bearerToken, listOfLookUps):
		responses = list()
		if listOfLookUps:
			headers = get_authorization_header(bearerToken)
			revListOfLookUps = []
			for lookUpList in listOfLookUps:
				if lookUpList not in revListOfLookUps:
					revListOfLookUps.append(lookUpList)
			lookUpFields = str([key["SalesforceField"] for key in listOfLookUps[0]])[1:-1].replace("'", "").replace(" ", "")
			for batch in range(0, len(revListOfLookUps), GET_INTERNAL_PRODUCT_SOQL_LIMIT):
				batchListOfLookUps = (revListOfLookUps[batch:batch+GET_INTERNAL_PRODUCT_SOQL_LIMIT])
				# Build Condition
				condition = str()
				for mainIndx, lookUpList in enumerate(batchListOfLookUps):
					condition += "("
					for indx, lookUp in enumerate(lookUpList):
						lookUpValue = str()
						if lookUp["FieldType"] == TYPE_STRING:
							lookUpValue = "'{lookUpValue}'".format(lookUpValue=str(lookUp["CpqLookUpValue"]))
						elif lookUp["FieldType"] == TYPE_FLOAT or lookUp["FieldType"] == TYPE_BOOL:
							lookUpValue = "{lookUpValue}".format(lookUpValue=str(lookUp["CpqLookUpValue"]))
						condition += "{lookUpField}={lookUpValue}".format(lookUpField=str(lookUp["SalesforceField"]), lookUpValue=str(lookUpValue))
						if indx+1 != len(lookUpList):
							condition += " AND "
					condition += ")"
					if mainIndx+1 != len(batchListOfLookUps):
						condition += " OR "
				soql = build_soql_query(selectedFields="Id,"+lookUpFields,
												table=SF_PRODUCT_OBJECT,
												condition=condition)
				# Call API
				response = call_soql_api(headers, soql, REF_GET_QUOTE_LINE_ITEMS)
				responses.append(response)
		return responses

	def get_sf_internal_product_ids_byName(bearerToken, listOfLookUps):
		response = None
		if listOfLookUps:
			headers = get_authorization_header(bearerToken)
			condition = ' Name in {} and Product_Level__c <> null'.format(str(tuple(listOfLookUps)).replace(',)',')'))
			lookUpFields = 'Name,ProductCode,Product_Level__c'
			soql = build_soql_query(selectedFields="Id,"+lookUpFields,
												table=SF_PRODUCT_OBJECT,
												condition=condition)
			response = call_soql_api(headers, soql, REF_GET_QUOTE_LINE_ITEMS)
		return response

	def collect_sf_internal_product_ids(quoteItems, response):
		if response["totalSize"] > 0:
			for item in quoteItems:
				condition = str()
				for indx, lookUp in enumerate(item["lookUps"]):
					lookUpValue = str()
					if lookUp["FieldType"] == TYPE_STRING:
						lookUpValue = "'{lookUpValue}'".format(lookUpValue=str(lookUp["CpqLookUpValue"]))
					elif lookUp["FieldType"] == TYPE_FLOAT or lookUp["FieldType"] == TYPE_BOOL:
						lookUpValue = "{lookUpValue}".format(lookUpValue=str(lookUp["CpqLookUpValue"]))
					condition += "record['{lookUpField}'] == {lookUpValue}".format(lookUpField=str(lookUp["SalesforceField"]), lookUpValue=str(lookUpValue))
					if indx+1 != len(item["lookUps"]):
						condition += " and "
				if condition:
					sfId = next((str(record["Id"]) for record in response["records"] 
									if eval(condition)), None)
					if sfId:
						item["sfId"] = sfId
		return quoteItems
	def get_existing_price_book_entries(bearerToken, quoteItems, sfServicePriceBookId):
		responses = list()
		currencyCode = Quote.SelectedMarket.CurrencyCode
		sfProductIds = [item["sfId"] for item in quoteItems if item["sfId"] != ""]
		if sfProductIds:
			# Remove Duplicates
			sfProductIds = list(set(sfProductIds))
			headers = get_authorization_header(bearerToken)
			for batch in range(0, len(sfProductIds), GET_PRICEBOOK_ENTRIES_SOQL_LIMIT):
				sfProductIds = sfProductIds[batch:batch+GET_PRICEBOOK_ENTRIES_SOQL_LIMIT]
				soql = """?q=SELECT+Id,+Name,+Pricebook2Id,+Product2Id,+UnitPrice,+CurrencyIsoCode+FROM+PricebookEntry+WHERE+Pricebook2Id+IN+('{sfServicePriceBookId}')+AND+Product2Id+IN+({sfProductIds})+AND+CurrencyIsoCode+=+'{currencyCode}'+AND+IsActive+=True""".format(sfServicePriceBookId=str(sfServicePriceBookId), sfProductIds=str(sfProductIds)[1:-1], currencyCode=str(currencyCode))
				priceBookEntries = call_soql_api(headers, soql, REF_GET_PRICE_BOOK)
				responses.append(priceBookEntries)
		return responses

	def get_product_price_book_entries(bearerToken, sfProductIds, sfServicePriceBookId):
		responses = list()
		currencyCode = Quote.SelectedMarket.CurrencyCode
		if sfProductIds:
			sfProductIds = list(set(sfProductIds))
			headers = get_authorization_header(bearerToken)
			for batch in range(0, len(sfProductIds), GET_PRICEBOOK_ENTRIES_SOQL_LIMIT):
				sfProductIds = sfProductIds[batch:batch+GET_PRICEBOOK_ENTRIES_SOQL_LIMIT]
				soql = """?q=SELECT+Id,+Name,+Pricebook2Id,+Product2Id,+UnitPrice,+CurrencyIsoCode+FROM+PricebookEntry+WHERE+Pricebook2Id+IN+('{sfServicePriceBookId}')+AND+Product2Id+IN+({sfProductIds})+AND+CurrencyIsoCode+=+'{currencyCode}'+AND+IsActive+=True""".format(sfServicePriceBookId=str(sfServicePriceBookId), sfProductIds=str(sfProductIds)[1:-1], currencyCode=str(currencyCode))
				priceBookEntries = call_soql_api(headers, soql, REF_GET_PRICE_BOOK)
				responses.append(priceBookEntries)
		return responses

	def collect_sf_pricebook_ids(quoteItems, response, sfServicePriceBookId):
		if response["totalSize"] > 0:
			for item in filter(lambda x: x["sfId"] != "", quoteItems):
				for entry in filter(lambda x: str(x["Product2Id"]) == item["sfId"], response["records"]):
					if str(entry["Pricebook2Id"]) == sfServicePriceBookId:
						item["sfStandardPriceBookEntryId"] = str(entry["Id"])
					else:
						item["sfCustomPriceBookEntryId"] = str(entry["Id"])
		return quoteItems

	def process_collection_pricebook_ids( bearerToken, quoteItems,  sfServicePriceBookId):
		# Call API to get existing Price Book Entries
		responses = get_existing_price_book_entries(bearerToken, quoteItems,  sfServicePriceBookId)
		for response in responses:
			quoteItems = collect_sf_pricebook_ids(quoteItems, response, sfServicePriceBookId)
		return quoteItems

	def quotelineitem_integration_mapping(Quote, TagParserQuote, cpqItem, flexiHourDist):
		salesforceLineItem = dict()
		flexHourData = flexiHourDist.get(cpqItem["Description"],{})
		salesforceLineItem["Description"] = flexHourData.get("Description",cpqItem["Description"])
		if cpqItem["Quantity"] == 0:
			salesforceLineItem["Scope_removal__c"] = 'true'
			salesforceLineItem["Scope_Impact__c"] = cpqItem["Scope_Change__c"]
		else:
			if Quote_Type == 'Contract Renewal':
				salesforceLineItem["Scope_Impact__c"] = cpqItem["Scope_Change__c"]
				salesforceLineItem["Is_Extension__c"] = str(Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content.lower())
			else:
				salesforceLineItem["Scope_Impact__c"] = cpqItem["Scope_Change__c"]
		salesforceLineItem["Quantity"] = 1 if cpqItem["Quantity"] == 0 else cpqItem["Quantity"]
		salesforceLineItem["UnitPrice"] = cpqItem["UnitPrice"]
		salesforceLineItem['CPQ_Unti_List_Price__c'] = cpqItem['CPQ_Unti_List_Price__c']
		salesforceLineItem['MPA__c'] = cpqItem['MPA__c']
		salesforceLineItem['Other_Discount__c'] = cpqItem['Other_Discount__c']
		salesforceLineItem["Requested_Unit_Sell_Price__c"] = cpqItem["Requested_Unit_Sell_Price__c"]
		salesforceLineItem["Sell_price__c"] = cpqItem["Requested_Unit_Sell_Price__c"]
		salesforceLineItem["Target_Price__c"] = cpqItem["Target_Price__c"]
		salesforceLineItem["SC_Price_Impact__c"] = cpqItem["SC_Price_Impact__c"]
		salesforceLineItem["Booked_Margin__c"] = cpqItem["Booked_Margin__c"]
		salesforceLineItem["Gross_Margin__c"] = cpqItem["Gross_Margin__c"]
		salesforceLineItem['Previous_Year_List_Price__c'] = cpqItem["Previous_Year_List_Price__c"]
		salesforceLineItem['SC_Previous_Year_Sell_Price__c'] = cpqItem["SC_Previous_Year_Sell_Price__c"]
		salesforceLineItem["Scope_Change__c"] = cpqItem["Scope_Change__c"]
		salesforceLineItem["Start_Date__c"] = cpqItem["Start_Date__c"]
		salesforceLineItem["End_Date__c"] = cpqItem["End_Date__c"]
		salesforceLineItem["Variable_Invoice_Amount__c"] = cpqItem["Variable_Invoice_Amount__c"]
		salesforceLineItem["Recurring_Invoice_Amount__c"] = cpqItem["Recurring_Invoice_Amount__c"]
		salesforceLineItem["Product2Id"] = cpqItem["Product2Id"]
		salesforceLineItem["PriceBookEntryId"] = cpqItem["PriceBookEntryId"]
		salesforceLineItem["Royalty_Excluded_Amount__c"] = cpqItem["Royalty_Excluded_Amount__c"]
		salesforceLineItem["SC_ModuleName__c"] = cpqItem["SC_ModuleName"]
		salesforceLineItem["SC_DiscountAmout__c"] = cpqItem["SC_DiscountAmout"]
		salesforceLineItem["SC_EscalationAmount__c"] = cpqItem["SC_EscalationAmount"]
		salesforceLineItem["SC_EscalationValue__c"] = cpqItem["SC_EscalationValue"]
		salesforceLineItem["Flexible_Hours__c"] = flexHourData.get("Flexible_Hours__c",0)
		salesforceLineItem["January__c"] = flexHourData.get("January__c",0)
		salesforceLineItem["February__c"] = flexHourData.get("February__c",0)
		salesforceLineItem["March__c"] = flexHourData.get("March__c",0)
		salesforceLineItem["April__c"] = flexHourData.get("April__c",0)
		salesforceLineItem["May__c"] = flexHourData.get("May__c",0)
		salesforceLineItem["June__c"] = flexHourData.get("June__c",0)
		salesforceLineItem["July__c"] = flexHourData.get("July__c",0)
		salesforceLineItem["August__c"] = flexHourData.get("August__c",0)
		salesforceLineItem["September__c"] = flexHourData.get("September__c",0)
		salesforceLineItem["October__c"] = flexHourData.get("October__c",0)
		salesforceLineItem["November__c"] = flexHourData.get("November__c",0)
		salesforceLineItem["December__c"] = flexHourData.get("December__c",0)
		return salesforceLineItem

	def post_sobjectcollection_request( headers, body, integrationReference, permissionList = None):
		# API path
		url = SOBJECT_COLLECTION_API
		response = call_rest_api(url, headers, body, POST, integrationReference, permissionList)
		return response


	def create_line_items( bearerToken, quoteId, quoteItems, flexiHourDist):
		responses = list()
		# Permission List
		permissionList = [build_permission_checklist(SF_QUOTE_LINE_ITEM_OBJECT, True, True)]
		quoteLineItemsToCreate = filter(lambda item: item["Product2Id"] != "" and item["PriceBookEntryId"] != "", quoteItems)
		if quoteLineItemsToCreate:
			# Create in batches of API_LIMIT.CREATE_API_RECORD_LIMIT (Currently 200)
			for batch in range(0, len(quoteLineItemsToCreate), CREATE_API_RECORD_LIMIT):
				records = list()
				for item in quoteLineItemsToCreate[batch:batch+CREATE_API_RECORD_LIMIT]:
					record = quotelineitem_integration_mapping(Quote, TagParserQuote, item, flexiHourDist)
					record["QuoteId"] = quoteId
					record["attributes"] = {"type": SF_QUOTE_LINE_ITEM_OBJECT}
					records.append(record)
				if records:
					body = dict()
					body["records"] = records
					headers = get_authorization_header(bearerToken)
					response = post_sobjectcollection_request(headers, body, REF_CREATE_QUOTE_LINE_ITEMS, permissionList)
					#Trace.Write(response)
					responses.append(response)
		return responses, quoteLineItemsToCreate


	def get_sf_ServiceProduct_id(bearerToken, ProdCodeList, integrationReference):
		SFDC_ProdList = None
		condition = """{sfProductCode} IN {pCodeList}""".format(sfProductCode="ProductCode" ,pCodeList= str(tuple(ProdCodeList)).replace(',)',')').replace(' ', '+') if ProdCodeList else "")
		soql = build_soql_query(selectedFields="id, name, ProductCode, Product_Level__c",
										table="Product2",
										condition=condition)
		if soql:
			headers = get_authorization_header(bearerToken)
			response = call_soql_api(headers, soql, integrationReference)
			#Trace.Write(response)
			if response["totalSize"] > 0:
				SFDC_ProdList = response["records"]
				#Trace.Write(SFDC_ProdList)
		return SFDC_ProdList


	def create_PSC_items( bearerToken, pscItems):
		responses = list()
		# Permission List
		permissionList = [build_permission_checklist(SF_PRODUCT_OBJECT, True, True)]
		if pscItems:
			PSCitemSubList = [pscItems[i:i+CREATE_API_RECORD_LIMIT] for i in range(0, len(pscItems), CREATE_API_RECORD_LIMIT)]
			for psitem in PSCitemSubList:
				body = dict()
				body["records"] = psitem
				headers = get_authorization_header(bearerToken)
				response = post_sobjectcollection_request(headers, body, REF_CREATE_PSC_LINE_ITEMS, permissionList)
				#Trace.Write(response)
				responses.append(response)
		return responses

	def getEntitlementServiceHours(EntitlementList):
		sHourList = SqlHelper.GetList("SELECT Entitlement, Service_Hours FROM CT_SC_Entitlements_Data WHERE Entitlement IN {eList}".format(eList = str(tuple(EntitlementList)).replace(',)',')')))
		serviceHourDist = {}
		for row in sHourList:
			serviceHourDist[row.Entitlement] = row.Service_Hours
		return serviceHourDist

	def UpdateMileStoneData(SFDC_QuoteID):
		MileStoneData = []
		currencyCode = Quote.SelectedMarket.CurrencyCode
		InvoiceType = 'Variable' if Quote.GetCustomField('SC_CF_INVTYPE').Content == 'Milestone' else 'Recurring'
		for row in Quote.QuoteTables['SC_Milestone_Table'].Rows:
			MileStoneData.append({"Period_Start_Date__c": row['Start_Date'].ToString('yyyy-MM-dd'),
					"Period_End_Date__c": row['End_Date'].ToString('yyyy-MM-dd'),
					"Bill_Amount__c": row['Value'],
					"Status__c": "Pending",
					"CurrencyIsoCode": currencyCode,
					"SC_Quote_Id__c" : SFDC_QuoteID,
					"Invoice_Type__c": InvoiceType,
					"attributes": {"type": SF_INVOICING_SCHEDULE_OBJECT}})
		responses = list()
		# Permission List
		permissionList = [build_permission_checklist(SF_INVOICING_SCHEDULE_OBJECT, True, True)]
		if MileStoneData:
			body = dict()
			body["records"] = MileStoneData
			headers = get_authorization_header(bearerToken)
			response = post_sobjectcollection_request(headers, body, SF_INVOICING_SCHEDULE_OBJECT, permissionList)
			responses.append(response)
		return responses

	def UpdateTeamRolesData(SFDC_QuoteID):
		TeamData = []
		for row in Quote.QuoteTables['SC_SFDC_Data_QuoteTable'].Rows:
			if row['Role']:
				TeamData.append({"User__c": row['SFDC_ID'],
							"Team_role__c": row['Role'],
							"Quote__c": SFDC_QuoteID,
							"attributes": {"type": SF_TEAMROLE_OBJECT}})
		responses = list()
		# Permission List
		permissionList = [build_permission_checklist(SF_TEAMROLE_OBJECT, True, True)]
		if TeamData:
			body = dict()
			body["records"] = TeamData
			headers = get_authorization_header(bearerToken)
			response = post_sobjectcollection_request(headers, body, SF_TEAMROLE_OBJECT, permissionList)
			responses.append(response)
		return responses


	def get_sf_quote_object_items(bearerToken, quoteId, integrationReference):
		response = None
		condition = """{sfQuoteIdField}='{quoteId}'""".format(sfQuoteIdField=str(SF_INVOICING_SCHEDULE_QUOTE_ID_FIELD) ,quoteId=str(quoteId))
		soql = build_soql_query(selectedFields="Id",
										table=SF_INVOICING_SCHEDULE_OBJECT,
										condition=condition)
		if soql:
			headers = get_authorization_header(bearerToken)
			response = call_soql_api(headers, soql, integrationReference)
		return response

	def delete_SFDC_Object_items(bearerToken, quoteId, integrationReference, referneceActivity):
		responses = list()
		permissionList = [build_permission_checklist(integrationReference, False, False, True, False)]
		objItems = get_sf_quote_object_items(bearerToken, quoteId, integrationReference)
		if objItems["totalSize"] > 0:
			itemrecords = [str(record["Id"]) for record in objItems["records"]]
			for batch in range(0, len(itemrecords), DELETE_API_RECORD_LIMIT):
				url = SALESFORCE_URL + build_delete_sobj_collection_url(itemrecords[batch:batch+DELETE_API_RECORD_LIMIT])
				response = call_sobject_delete_api(bearerToken, url, referneceActivity, permissionList)
				responses.append(response)
		return responses

	bearerToken = get_auth2_token()
	SFDC_QUOTEID = QLI_Helper.get_sf_quote_id(Quote.QuoteId, Quote.UserId)
	presponses = ''

	if str(SFDC_QUOTEID) != None:
		delete_PSC_scope_items(bearerToken, str(SFDC_QUOTEID))
		QLI_Helper.delete_quote_line_items(str(SFDC_QUOTEID))
		delete_SFDC_Object_items(bearerToken, str(SFDC_QUOTEID), SF_INVOICING_SCHEDULE_OBJECT, REF_DEL_INVOICING_SCHEDULE_ITEMS)
		UniqueIDList = []
		UniqueIDItems = {}
		QuoteLines = []
		LaborProductDetails = []
		FlexiHourDist = {}
		FlexiHourEntitlementDist = {}
		if Quote_Type == 'Contract New':
			Quote_Table = Quote.QuoteTables["QT_SC_FlexibleHours"]
			Module_Name = 'Module_Name'
		elif Quote_Type == 'Contract Renewal':
			Quote_Table = Quote.QuoteTables["QT_SC_PSC_Labor_Details"]
			Module_Name = 'Service_Product'
		for row in Quote_Table.Rows:
			module_value = row[Module_Name]
			if module_value not in FlexiHourDist:
				FlexiHourDist[module_value] = {field: 0 for field in [
			'Description', 'Flexible_Hours__c', 'January__c', 'February__c', 'March__c', 'April__c', 
			'May__c', 'June__c', 'July__c', 'August__c', 'September__c', 'October__c', 'November__c', 
			'December__c', 'Totals__c']}
				FlexiHourDist[module_value]['Description'] = row["Description"]
			for month in ['Flexible_Hours', 'January', 'February', 'March', 'April', 'May', 'June', 
						'July', 'August', 'September', 'October', 'November', 'December', 'Totals']:
				month_field = '{}__c'.format(month)
				FlexiHourDist[module_value][month_field] += row[month]
				FlexiHourEntitlementDist[module_value + "__" + row["Entitlement"] +"__" + row["Resource_Type"] +"__" + month] = row[month]
		QuoteLines, UniqueIDList, UniqueIDItems = qLineHelper.generateSFDCQuoteLines()
		pp=str(QuoteLines)
		rr=str(UniqueIDList)
		rrr=str(UniqueIDItems)
		ServiceProductList = []
		for qItem in UniqueIDItems:
			if  UniqueIDItems[qItem]['PartNumber'] == 'SESP':
				pscList = UniqueIDItems[qItem]['pscList']
				sesp_ES_Desc = UniqueIDItems[qItem]['Desc'].split('-EnabledService-')
				strPair = sesp_ES_Desc[0].split('-----')
				if len(strPair)>1:
					ServiceProductList.append(strPair[0])
					MSIDList = strPair[2].split(';')
					for scEnt in strPair[1].split(';'):
						Ent = scEnt.split('|')
						ServiceProductList.append(Ent[0])
						if Ent[-1] == 'False':
							pscList.append({'UniqueID': qItem, 'Product': 'SESP', 'ServiceProduct': strPair[0], 'Entitlement': Ent[0], 'Asset': '', 'Qty': '0' })
						else:
							for MSID in MSIDList:
								pscList.append({'UniqueID': qItem, 'Product': 'SESP', 'ServiceProduct': strPair[0], 'Entitlement': Ent[0], 'Asset': MSID, 'Qty': '1' })
				if len(sesp_ES_Desc)>1 and len(sesp_ES_Desc[1].strip()):
					Ent = sesp_ES_Desc[1].split('|')
					ServiceProductList.append(Ent[0])
					ServiceProductList.append(Ent[1])
					pscList.append({'UniqueID': qItem, 'Product': 'Enabled Services', 'ServiceProduct': Ent[0], 'Entitlement': Ent[1], 'Asset': '', 'Qty': '0' })
				UniqueIDItems[qItem]['pscList'] = pscList
			elif UniqueIDItems[qItem]['PartNumber'] == 'Parts Management':
				strPair = UniqueIDItems[qItem]['Desc'].split('-----')
				if len(strPair)>1:
					scProd = {}
					scprd = []
					for scpair in strPair[0].split(';'):
						scprd = scpair.split('|')
						if len(scprd)>1:
							scProd[scprd[0]] = scprd[1]
							ServiceProductList.append(scprd[0])
					pscList = UniqueIDItems[qItem]['pscList']
					if strPair[1].strip():
						partrsDict = {}
						for scEnt in strPair[1].split(';'):
							Ent = scEnt.split('|')
							ServiceProductList.append(scProd[Ent[0]])
							partrsDict.setdefault(Ent[0], []).append({"ProductCode":Ent[1],"Quantity":int(Ent[2]) if Ent[2]!= '' else 0})
						for entitleItem in partrsDict:
							pscList.append({'UniqueID': qItem, 'Product': 'Parts Management', 'ServiceProduct': entitleItem, 'Entitlement': scProd[entitleItem], 'Asset': {"items" : partrsDict[entitleItem]}, 'Qty': '1' })
					else:
						if len(scprd)>1:
							pscList.append({'UniqueID': qItem, 'Product': 'Parts Management', 'ServiceProduct': scprd[0], 'Entitlement': scprd[1], 'Asset': '', 'Qty': '0' })
					UniqueIDItems[qItem]['pscList'] = pscList
			elif UniqueIDItems[qItem]['PartNumber'] in ['Third Party Services', 'Honeywell Digital Prime', 'Condition Based Maintenance', 'Experion Extended Support - RQUP ONLY', 'MES Performix', 'Hardware Warranty', 'Hardware Refresh','Local Support Standby']:
				pscList = UniqueIDItems[qItem]['pscList']
				strPair = UniqueIDItems[qItem]['Desc'].split('-----')
				if len(strPair)>1:
					ServiceProductList.append(strPair[0])
					for scpair in strPair[1].split(';'):
						ServiceProductList.append(scpair)
						pscList.append({'UniqueID': qItem, 'Product': UniqueIDItems[qItem]['PartNumber'], 'ServiceProduct': strPair[0], 'Entitlement': scpair, 'Asset': '', 'Qty': '0' })
					UniqueIDItems[qItem]['pscList'] = pscList

			elif (UniqueIDItems[qItem]['PartNumber'] in ['QCS 4.0', 'BGP inc Matrikon', 'Cyber', 'Workforce Excellence Program', 'Enabled Services', 'Trace']) or (UniqueIDItems[qItem]['PartNumber'] in gen_product):
				pscList = UniqueIDItems[qItem]['pscList']
				strPair = UniqueIDItems[qItem]['Desc'].split(';')
				for scEnt in strPair:
					Ent = scEnt.split('|')
					ServiceProductList.append(Ent[0])
					ServiceProductList.append(Ent[1])
					pscList.append({'UniqueID': qItem, 'Product': UniqueIDItems[qItem]['PartNumber'], 'ServiceProduct': Ent[0], 'Entitlement': Ent[1], 'Asset': '', 'Qty': '0' })
				UniqueIDItems[qItem]['pscList'] = pscList
			elif UniqueIDItems[qItem]['PartNumber'] == 'Labor':
				strPair = UniqueIDItems[qItem]['Desc'].split(';')
				pscList = UniqueIDItems[qItem]['pscList']
				for scEnt in strPair:
					Ent = scEnt.split('|')
					LaborProductDetails.append({'Product' : Ent[0], 'ServiceProduct' : Ent[1], 'Entitlement' : Ent[2], 'Qty' : Ent[3] })
					ServiceProductList.append(Ent[1])
					ServiceProductList.append(Ent[2])
					pscList.append({'UniqueID': qItem, 'Product': UniqueIDItems[qItem]['PartNumber'], 'ServiceProduct': Ent[1], 'Entitlement': Ent[2], 'Asset': '', 'Qty': Ent[3] })
				UniqueIDItems[qItem]['pscList'] = pscList
		fr=str(UniqueIDItems)
		re=str(LaborProductDetails)
		slist=str(tuple(ServiceProductList))
		SFproductList = get_sf_internal_product_ids_byName(bearerToken,ServiceProductList)
		EntitlementProducts = {}
		ServiceContractProducts = {}
		ServiceContractProductsIds = []
		if SFproductList is not None:
			for pitem in SFproductList.records:
				if str(pitem.Product_Level__c) == 'Entitlement':
					EntitlementProducts[str(pitem.Name)] = {'Id': str(pitem.Id), 'Name': str(pitem.Name), 'Code': str(pitem.ProductCode), 'Level': str(pitem.Product_Level__c) }
				else:
					ServiceContractProducts[str(pitem.Name)] = {'Id': str(pitem.Id), 'Name': str(pitem.Name), 'Code': str(pitem.ProductCode), 'Level': str(pitem.Product_Level__c) }
					ServiceContractProductsIds.append(str(pitem.Id))
		ts=str(ServiceContractProducts)
		tss=str(EntitlementProducts)
		SFprodPriceList = get_product_price_book_entries(bearerToken, ServiceContractProductsIds, SERVICE_PRICE_BOOK_ID)
		for precords in SFprodPriceList:
			for precord in precords.records:
				ServiceContractProducts[str(precord.Name)]['PriceEntryId'] = str(precord.Id)
		rssd=str(ServiceContractProducts)

		for qitem in QuoteLines:
			if qitem['Description'] in ServiceContractProducts:
				qitem['Product2Id'] = ServiceContractProducts[qitem['Description']]['Id']
				qitem['PriceBookEntryId'] = ServiceContractProducts[qitem['Description']]['PriceEntryId']
				qitem['PSCLines'] = []
				PSCItems = UniqueIDItems[qitem['ParentUniqueID']]['pscList']
				for pitem in PSCItems:
					if pitem['ServiceProduct'] == qitem['Description']:
						pitem['Id'] = EntitlementProducts[pitem['Entitlement']]['Id'] if pitem['Entitlement'] in EntitlementProducts else ''
						qitem['PSCLines'].append(pitem)

		ghj=str(QuoteLines)
		wer=str(UniqueIDItems)
		index = {}
		if QuoteLines:
			Log.Write("QuoteLines Request " + str(QuoteLines))
			qResponse, mQuoteLines = create_line_items(bearerToken, str(SFDC_QUOTEID), QuoteLines, FlexiHourDist)
			qRespIndex = -1
			for jResp in qResponse:
				for iResp in jResp:
					qRespIndex+=1
					Log.Write("QuoteLines Response " + str(iResp))
					mQuoteLines[qRespIndex]['SFDCLineID'] = str(iResp.id)
			PSCitems = []
			hhpu=str(mQuoteLines)
			for sfItem in mQuoteLines:
				for pscline in sfItem['PSCLines']:
					if pscline.get('Id', '') == '':
						continue
					composite_key = sfItem['ParentUniqueID'] + sfItem['Start_Date__c']
					resource_data = sfItem.get('Contract_ResourceType__c', {}).get(composite_key, [])
					# Extract values safely
					key = pscline['Entitlement'] + str(sfItem['Start_Date__c'])
					if key not in index:
							index[key] = 0
					else:
							index[key] += 1
					indx = index[pscline['Entitlement']+str(sfItem['Start_Date__c'])]
					contract_resource_type = resource_data[pscline['Entitlement']][indx][0] if len(resource_data) > 0 and resource_data[pscline['Entitlement']][indx]  else 'N/A'
					list_price = resource_data[pscline['Entitlement']][indx][1] if len(resource_data) > 0 and resource_data[pscline['Entitlement']][indx] else '0.00'
					sales_price = resource_data[pscline['Entitlement']][indx][2] if len(resource_data) > 0 and resource_data[pscline['Entitlement']][indx] else '0.00'
					PSCitems.append({"Name": pscline['Entitlement'],
									"CurrencyIsoCode" : Quote.GetCustomField('Currency').Content,
									"Contract_ResourceType__c": str(contract_resource_type) if contract_resource_type != '' else 'N/A',
									"List_Price__c": str(list_price) if list_price != '' else '0.00',
									"Sales_Price__c": str(sales_price) if sales_price != '' else '0.00',
									"Account__c": Quote.GetCustomField('AccountId').Content,
									"Asset__c": pscline['Asset'] if pscline['Product'] == 'SESP' else '',
									"Start_Date__c": sfItem['Start_Date__c'],
									"End_Date__c": sfItem['End_Date__c'],
									"Service_Detail__c": pscline['Id'],
									"QuoteLineItemId__c": sfItem['SFDCLineID'],
									"Model_Name__c": pscline['Product'],
									"P1P2Parts_List__c": str(pscline['Asset']).replace("'", '"') if pscline['Product'] == 'Parts Management' else "",
									"Budgeted_Quota__c": sfItem['TrainingMatch_SellPrice'] if pscline['Entitlement'] == 'Training Match' else 0,
									"Flexible_Hours__c" : FlexiHourEntitlementDist.get(sfItem['Description'] + "__" + pscline['Entitlement'] + "__" + contract_resource_type + "__Flexible_Hours", 0),
									"Jan_Planned_Hours__c" : FlexiHourEntitlementDist.get(sfItem['Description'] + "__" + pscline['Entitlement'] + "__" + contract_resource_type + "__January", 0),
									"Feb_Planned_Hours__c" : FlexiHourEntitlementDist.get(sfItem['Description'] + "__" + pscline['Entitlement'] + "__" + contract_resource_type + "__February", 0),
									"Mar_Planned_Hours__c" : FlexiHourEntitlementDist.get(sfItem['Description'] + "__" + pscline['Entitlement'] + "__" + contract_resource_type + "__March", 0),
									"Apr_Planned_Hours__c" : FlexiHourEntitlementDist.get(sfItem['Description'] + "__" + pscline['Entitlement'] + "__" + contract_resource_type + "__April", 0),
									"May_Planned_Hours__c" : FlexiHourEntitlementDist.get(sfItem['Description'] + "__" + pscline['Entitlement'] + "__" + contract_resource_type + "__May", 0),
									"Jun_Planned_Hours__c" : FlexiHourEntitlementDist.get(sfItem['Description'] + "__" + pscline['Entitlement'] + "__" + contract_resource_type + "__June", 0),
									"Jul_Planned_Hours__c" : FlexiHourEntitlementDist.get(sfItem['Description'] + "__" + pscline['Entitlement'] + "__" + contract_resource_type + "__July", 0),
									"Aug_Planned_Hours__c" : FlexiHourEntitlementDist.get(sfItem['Description'] + "__" + pscline['Entitlement'] + "__" + contract_resource_type + "__August", 0),
									"Sep_Planned_Hours__c" : FlexiHourEntitlementDist.get(sfItem['Description'] + "__" + pscline['Entitlement'] + "__" + contract_resource_type + "__September", 0),
									"Oct_Planned_Hours__c" : FlexiHourEntitlementDist.get(sfItem['Description'] + "__" + pscline['Entitlement'] + "__" + contract_resource_type + "__October", 0),
									"Nov_Planned_Hours__c" : FlexiHourEntitlementDist.get(sfItem['Description'] + "__" + pscline['Entitlement'] + "__" + contract_resource_type + "__November", 0),
									"Dec_Planned_Hours__c" : FlexiHourEntitlementDist.get(sfItem['Description'] + "__" + pscline['Entitlement'] + "__" + contract_resource_type + "__December", 0),
									"attributes": {"type": SF_PSC_LINE_ITEM_OBJECT}})
			kbk = str(PSCitems)
			if PSCitems:
				presponses = create_PSC_items(bearerToken, PSCitems)
			mresponses = UpdateMileStoneData(str(SFDC_QUOTEID))
			UpdateTeamRolesData(str(SFDC_QUOTEID))