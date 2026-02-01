#---------------------------------------------------------------------------------------------------------
#					Change History Log
#---------------------------------------------------------------------------------------------------------
# Description : CPQ should send Quote Line items to SFDC
# JIRA Ref.   : CXCPQ-65799,CXCPQ-73354,CXCPQ-65618,
# Author      : H542824
# CreatedDate : 17-01-2024
#----------------------------------------------------------------------------------------------------------
# Date 			Name					    Version     Comment
# 17-01-2024	Pratik Sanghani    			16 	        Initial Version
#----------------------------------------------------------------------------------------------------------

import GS_APIGEE_Integration_Util

###############################################################################################
# Function to filter back office sync
###############################################################################################
def back_office_sync_filter(quoteItems):
    parts = []
    for i in quoteItems:
        parts.append(i['PartNumber'])
    parts = list(set(parts))
    sap_parts = SqlHelper.GetList("select p.PRODUCT_CATALOG_CODE,p.IsSyncedFromBackOffice from Products p join product_versions pv on p.Product_ID = pv.Product_ID where PRODUCT_CATALOG_CODE in ({partnumbers}) and pv.Is_Active = 1 and p.IsSyncedFromBackOffice=1".format(partnumbers=str(parts)[1:-1]))
    quoteItems_filtered = [i for i in quoteItems if i["PartNumber"] in [j.PRODUCT_CATALOG_CODE for j in sap_parts]]
    return quoteItems_filtered


###############################################################################################
# Function to replace special characters in string (Used in SOQL API calls)
###############################################################################################
def replace_special_char(text):
    special_chars = [{"symbol": "&", "code": "%26"}, {"symbol": "#", "code": "%23"}]
    for special_char in special_chars:
        text = text.replace(special_char["symbol"], special_char["code"])

    return text

	
	
###############################################################################################
# Function to get Salesforce QuoteID
###############################################################################################
def get_sf_quote_id(cartId,ownerId):
    QuoteID = None

    url = GS_APIGEE_Integration_Util.GetAPIGEEBaseURL()
    headers = GS_APIGEE_Integration_Util.GetAPIGEEAuthHeader()

    APIGEEQueryURL="{APIGEEURL}/hps/cpq/line-items/v1/get-line-item?q=select+Id,Pricebook2Id+from+Quote+where+Quote_ID__c={cartId}+and+Owner_ID__c={ownerId}".format(APIGEEURL = str(url),cartId = str(cartId),ownerId = str(ownerId))
    APIGEEQueryURL = replace_special_char(APIGEEQueryURL)
    
    Response=call_rest_api(APIGEEQueryURL, headers, None, "GET", "Get_Salesforce_QuoteID")
   
    if Response["totalSize"] > 0:
        QuoteID = Response["records"][0]["Id"]
    
    return QuoteID

###############################################################################################
# Function to get PriceBookIDs
###############################################################################################	
def get_sf_pricebook_ids():
	pricebooks = SqlHelper.GetList("select PARAM_NAME,STRING_VALUE from CT_CUSTOM_PARAMETER where PARAM_NAME in ('SFDC_Standard_Price_Book','SFDC_PMC_Price_Book')")
	for id in pricebooks:
		if id.PARAM_NAME == "SFDC_Standard_Price_Book":
			SFDC_STANDARD_PRICE_BOOK_ID = id.STRING_VALUE
		else:
			PMC_PRICE_BOOK_ID = id.STRING_VALUE
	return SFDC_STANDARD_PRICE_BOOK_ID,PMC_PRICE_BOOK_ID


###############################################################################################
# Function to get SFDC_SAP_Product_RecordTypeId
###############################################################################################	
def get_SFDC_SAP_Product_RecordTypeId():
    RecordTypeId = SqlHelper.GetFirst("select STRING_VALUE from CT_CUSTOM_PARAMETER where PARAM_NAME in ('SFDC_SAP_Product_RecordTypeId')").STRING_VALUE
    return RecordTypeId

###############################################################################################
# Function for Product lookup Salesforce
###############################################################################################
def get_product_lookups(cpqItem):
    productlookUps = list()

    lookUp = dict()
    lookUp["SalesforceField"] = "ProductCode"
    lookUp["CpqLookUpValue"] = cpqItem.PartNumber
    lookUp["FieldType"] = "String"
    productlookUps.append(lookUp)

    return productlookUps
	
###############################################################################################
# Function to get Salesforce Internal Product Ids
###############################################################################################
def get_sf_internal_product_ids(listOfLookUps):

    url = GS_APIGEE_Integration_Util.GetAPIGEEBaseURL()
    headers = GS_APIGEE_Integration_Util.GetAPIGEEAuthHeader()

    responses = list()
    if listOfLookUps:
        # Remove Duplicates
        revListOfLookUps = []
        for lookUpList in listOfLookUps:
            if lookUpList not in revListOfLookUps:
                revListOfLookUps.append(lookUpList)
        # Get Salesforce LookUp Fields
        lookUpFields = str([key["SalesforceField"] for key in listOfLookUps[0]])[1:-1].replace("'", "").replace(" ", "")
        # Get ids in batches of API_LIMIT.GET_INTERNAL_PRODUCT_SOQL_LIMIT (Currently 7000 different items)
        for batch in range(0, len(revListOfLookUps), 7000):
            batchListOfLookUps = (revListOfLookUps[batch:batch+7000])
            # Build Condition
            condition = str()
            for mainIndx, lookUpList in enumerate(batchListOfLookUps):
                condition += "("
                for indx, lookUp in enumerate(lookUpList):
                    lookUpValue = str()
                    if lookUp["FieldType"] == 'String':
                        lookUpValue = "'{lookUpValue}'".format(lookUpValue=str(lookUp["CpqLookUpValue"]))
                    condition += "{lookUpField}={lookUpValue}".format(lookUpField=str(lookUp["SalesforceField"]), lookUpValue=str(lookUpValue))
                    if indx+1 != len(lookUpList):
                        condition += " AND "
                condition += ")"
                if mainIndx+1 != len(batchListOfLookUps):
                    condition += " OR "
            # Build soql to find Salesforce Internal Product Ids
            APIGEEQueryURL="{APIGEEURL}/hps/cpq/line-items/v1/get-line-item?q=select+Id,+ProductCode+from+Product2+where+{condition}".format(APIGEEURL = str(url),condition = str(condition))
            APIGEEQueryURL = replace_special_char(APIGEEQueryURL)
            # Call API
            response=call_rest_api(APIGEEQueryURL, headers, None, "GET", "Get_Salesforce_Internal_Product_Ids")
            responses.append(response)
    return responses
	
###############################################################################################
# Function to collect internal Salesforce product ids in quoteItems list
###############################################################################################
def collect_sf_internal_product_ids(quoteItems, response):
    if response["totalSize"] > 0:
        for item in quoteItems:
            condition = str()
            for indx, lookUp in enumerate(item["lookUps"]):
                lookUpValue = str()
                if lookUp["FieldType"] == "String":
                    lookUpValue = "'{lookUpValue}'".format(lookUpValue=str(lookUp["CpqLookUpValue"]))
                condition += "record['{lookUpField}'] == {lookUpValue}".format(lookUpField=str(lookUp["SalesforceField"]), lookUpValue=str(lookUpValue))
                if indx+1 != len(item["lookUps"]):
                    condition += " and "
            if condition:
                sfId = next((str(record["Id"]) for record in response["records"] if eval(condition)), None)
                
                if sfId:
                    item["sfId"] = sfId
    return quoteItems
	
###############################################################################################
# Function for Product Master Mapping
###############################################################################################
def product_integration_mapping(cpqItem):
    salesforceLineItem = dict()

    salesforceLineItem["Name"] = cpqItem.PartNumber
    salesforceLineItem["Description"] = cpqItem.ProductName

    return salesforceLineItem
	
###############################################################################################
# Function to add sObject collection payload header (url, method, header) for Composite Requests
###############################################################################################
def get_cr_sobjectcollection_payload_header( method, referenceId, records):
    payload = dict()
    if method == "DELETE":
        payload["url"] = build_delete_sobj_collection_url(records)
    else:
        payload["url"] = "/services/data/v55.0/composite/sobjects"
    payload["method"] = method
    payload["referenceId"] = referenceId
    return payload
	
###############################################################################################
# Function to get the final body of a Composite Request
###############################################################################################
def build_composite_body(compositePayload):
    body = dict()
    body["compositeRequest"] = compositePayload
    return body
	
	
###############################################################################################
# General Function to call APIs
###############################################################################################
def call_rest_api( url, headers, body, method, integrationReference):
    response = None
    try:
        if method == "GET":
            response = RestClient.Get(url, headers)
            
        elif method == "POST":
            response = RestClient.Post(url, body, headers)
            Log.Info("PMC QLI Sync: Request ({integrationReference})".format(integrationReference=str(integrationReference)), unicode(body))
        elif method == "DELETE":
            response = RestClient.Delete(url, headers)
        if len(unicode(response)) > 10000:
            Log.Info("PMC QLI Sync: Response ({integrationReference})".format(integrationReference=str(integrationReference)), unicode(response)[:10000])
            Log.Info("PMC QLI Sync: Response ({integrationReference})".format(integrationReference=str(integrationReference)), unicode(response)[10000:])
        else:
            Log.Info("PMC QLI Sync: Response ({integrationReference})".format(integrationReference=str(integrationReference)), unicode(response))
    except SystemError as e:
        response = None
        msg = """Integration Error - {integrationReference}: {error}""".format(integrationReference=str(integrationReference), error=str(e))
        Log.Error("PMC QLI Sync: Integration Error", str(e))
        Log.Error("PMC QLI Sync: Integration Error"+ str(msg))
    return response

###############################################################################################
# Function to call POST Composite API
###############################################################################################
def post_composite_request(compositePayload, integrationReference):
    # API path
    url = GS_APIGEE_Integration_Util.GetAPIGEEBaseURL()
    headers = GS_APIGEE_Integration_Util.GetAPIGEEAuthHeader()
    APIGEEQueryURL="{APIGEEURL}/hps/cpq/composite/v1/create-records".format(APIGEEURL = str(url))
    body = build_composite_body(compositePayload)
    response = call_rest_api(APIGEEQueryURL, headers, body, "POST", integrationReference)
    return response

###############################################################################################
# Function to create Salesforce product master
###############################################################################################
def create_sf_product_master(quoteItems):
	
    response = None
    compositePayload = list()
    # Collect line items without corresponding Salesforce products
    productsToCreate = filter(lambda x: x["sfId"] == "", quoteItems)

    # POST: Create new product records
    if productsToCreate:
        records = list()
        #PARAM Table SOQL
        for item in productsToCreate:
            record = product_integration_mapping(item["item"])
            # Fill Look Up Fields
            for lookUp in item["lookUps"]:
                record[lookUp["SalesforceField"]] = lookUp["CpqLookUpValue"]
            record["IsActive"] = True
            record["attributes"] = {"type": "Product2"}
            record["RecordTypeId"] = get_SFDC_SAP_Product_RecordTypeId()
            records.append(record)
        compositeRequest = get_cr_sobjectcollection_payload_header("POST", "Create_Products", None)
        compositeRequest["body"] = {"records": records}
        compositePayload.append(compositeRequest)

    if compositePayload:
        # Call REST API
        response = post_composite_request(compositePayload, "Create Product Master")
    return response

###############################################################################################
# Function to get Salesforce Products by their IDs. To retrieve LookupValues.
###############################################################################################
def get_sf_product_by_ids( sfIds, listOfLookUps):
    responses = list()
    url = GS_APIGEE_Integration_Util.GetAPIGEEBaseURL()
    headers = GS_APIGEE_Integration_Util.GetAPIGEEAuthHeader()
    # Remove Duplicates
    sfIds = list(set(sfIds))
    if sfIds:
        # Get Salesforce LookUp Fields
        lookUpFields = str([key["SalesforceField"] for key in listOfLookUps[0]])[1:-1].replace("'", "").replace(" ", "")
        # Get ids in batches of API_LIMIT.GET_INTERNAL_PRODUCT_SOQL_LIMIT (Currently 7000 different items)
        for batch in range(0, len(sfIds), 7000):
            sfIds = str((sfIds[batch:batch+7000]))[1:-1]
            # Call API
            APIGEEQueryURL="{APIGEEURL}/hps/cpq/line-items/v1/get-line-item?q=Select+id+,+{lookUpField}+FROM+Product2+WHERE+id+IN+({sfIds})".format(APIGEEURL = str(url),lookUpField=str(lookUpFields), sfIds=str(sfIds))
            APIGEEQueryURL = replace_special_char(APIGEEQueryURL)
            response=call_rest_api(APIGEEQueryURL, headers, None, "GET", "Get_Salesforce_Products_By_Their_IDs.To_retrieve_LookupValues")
            responses.append(response)
    return responses

###############################################################################################
# Function to get existing Salesforce Price Book entries
###############################################################################################
def get_existing_price_book_entries(Quote, quoteItems, sfPMCPriceBookId, SFDC_STANDARD_PRICE_BOOK_ID):
    responses = list()
    currencyCode = Quote.GetCustomField('Currency').Content
    url = GS_APIGEE_Integration_Util.GetAPIGEEBaseURL()
    headers = GS_APIGEE_Integration_Util.GetAPIGEEAuthHeader()
    sfProductIds = [item["sfId"] for item in quoteItems if item["sfId"] != ""]
    if sfProductIds:
        # Remove Duplicates
        sfProductIds = list(set(sfProductIds))
        # Get ids in batches of API_LIMIT.GET_PRICEBOOK_ENTRIES_SOQL_LIMIT (Currently 5000 different items)
        for batch in range(0, len(sfProductIds), 5000):
            sfProductIds = sfProductIds[batch:batch+5000]
            # Call API to get existing Price Book Entries
            APIGEEQueryURL="{APIGEEURL}/hps/cpq/line-items/v1/get-line-item?q=SELECT+Id,+Pricebook2Id,+Product2Id,+UnitPrice,+CurrencyIsoCode+FROM+PricebookEntry+WHERE+Pricebook2Id+IN+('{sfStandardPriceBookId}','{sfPriceBookId}')+AND+Product2Id+IN+({sfProductIds})+AND+CurrencyIsoCode+=+'{currencyCode}'+AND+IsActive+=True".format(APIGEEURL = str(url),sfStandardPriceBookId=str(SFDC_STANDARD_PRICE_BOOK_ID), sfPriceBookId = str(sfPMCPriceBookId),sfProductIds=str(sfProductIds)[1:-1], currencyCode=str(currencyCode))
            APIGEEQueryURL = replace_special_char(APIGEEQueryURL)
            priceBookEntries=call_rest_api(APIGEEQueryURL, headers, None, "GET", "Get_Existing_Salesforce_PriceBook_Entries")
            responses.append(priceBookEntries)
    return responses

###############################################################################################
# Function to collect pricebook entries in quoteItems list
###############################################################################################
def collect_sf_pricebook_ids(quoteItems, response, sfPMCPriceBookId):
    if response["totalSize"] > 0:
        for item in filter(lambda x: x["sfId"] != "", quoteItems):
            for entry in filter(lambda x: str(x["Product2Id"]) == item["sfId"], response["records"]):
                if str(entry["Pricebook2Id"]) == sfPMCPriceBookId:
                    item["sfCustomPriceBookEntryId"] = str(entry["Id"])
                else:
                     item["sfStandardPriceBookEntryId"] = str(entry["Id"])
    return quoteItems

###############################################################################################
# Function to collect pricebook entries
###############################################################################################
def process_collection_pricebook_ids( Quote,quoteItems,  sfPMCPriceBookId, SFDC_STANDARD_PRICE_BOOK_ID):
    # Call API to get existing Price Book Entries
    responses = get_existing_price_book_entries( Quote,quoteItems,  sfPMCPriceBookId, SFDC_STANDARD_PRICE_BOOK_ID)
    for response in responses:
        quoteItems = collect_sf_pricebook_ids(quoteItems, response, sfPMCPriceBookId)
    return quoteItems


###############################################################################################
# Function to create Salesforce Price Book entries
###############################################################################################
def create_price_book_entries(Quote,quoteItems, sfPMCPriceBookId, sfStandardPriceBookId):
    response = None
    compositePayload = list()
    currencyCode = Quote.GetCustomField('Currency').Content
    
    # Create Price Book Entries (Standard & Custom)
    quoteItemsPriceToCreate = filter(lambda item: item["sfId"] != "" and (item["sfCustomPriceBookEntryId"] == ""), quoteItems)
    if quoteItemsPriceToCreate:
        records = list()
        for item in quoteItemsPriceToCreate:
            if item["sfStandardPriceBookEntryId"] == "":
                record = dict()
                record["Pricebook2Id"] = sfStandardPriceBookId
                record["Product2Id"] = item["sfId"]
                record["UnitPrice"] = float(item["item"].ListPriceInMarket)
                record["CurrencyIsoCode"] = currencyCode
                record["attributes"] = {"type": "PricebookEntry"}
                record["IsActive"] = True
                records.append(record)
            if item["sfCustomPriceBookEntryId"] == "":
                record = dict()
                record["Pricebook2Id"] = sfPMCPriceBookId
                record["Product2Id"] = item["sfId"]
                record["UnitPrice"] = float(item["item"].ListPriceInMarket)
                record["CurrencyIsoCode"] = currencyCode
                record["attributes"] = {"type": "PricebookEntry"}
                record["IsActive"] = True
                records.append(record)
        if records:
            compositeRequest = get_cr_sobjectcollection_payload_header("POST", "Create_PriceBookEntries", None)
            compositeRequest["body"] = {"records": records}
            compositePayload.append(compositeRequest)

    if compositePayload:
        # Call REST API
        response = post_composite_request( compositePayload, 'Create_PriceBookEntries')
    return response


###############################################################################################
# Function to get Salesforce Line item records from Quote LineItem object
###############################################################################################
def get_sf_quote_line_items(quoteId):

    url = GS_APIGEE_Integration_Util.GetAPIGEEBaseURL()
    headers = GS_APIGEE_Integration_Util.GetAPIGEEAuthHeader()

    APIGEEQueryURL="{APIGEEURL}/hps/cpq/line-items/v1/get-line-item?q=select+Id+from+QuoteLineItem+where+QuoteId='{quoteId}'".format(APIGEEURL = str(url),quoteId = str(quoteId))
    APIGEEQueryURL = replace_special_char(APIGEEQueryURL)
    Response=call_rest_api(APIGEEQueryURL, headers, None, "GET", "Get_Salesforce_Line_Item")
        
    return Response

###############################################################################################
# Function to build delete SObject collection url
###############################################################################################
def build_delete_sobj_collection_url(records):
    url = None
    records = str(records)[1:-1].replace("'", "").replace(" ", "")
    # API path
    url = "/hps/cpq/line-items/v1/delete-line-item?ids={records}".format(records=str(records))
    return url


###############################################################################################
# Function to delete Quote Line Items
###############################################################################################
def delete_quote_line_items(quoteId):
    responses = list()

    # Get all QuoteLineItem records to delete
    lineItems = get_sf_quote_line_items(quoteId)
    if lineItems["totalSize"] > 0:
        lineItemrecords = [str(record["Id"]) for record in lineItems["records"]]
        # Delete in batches of API_LIMIT.DELETE_API_RECORD_LIMIT (Currently 200)
        for batch in range(0, len(lineItemrecords), 200):
            APIGEEurl = GS_APIGEE_Integration_Util.GetAPIGEEBaseURL()
            headers = GS_APIGEE_Integration_Util.GetAPIGEEAuthHeader()

            url = APIGEEurl + build_delete_sobj_collection_url(lineItemrecords[batch:batch+200])

            response = call_rest_api(url, headers, None, "DELETE", "Delete Quote Line Items")
            responses.append(response)
    return responses

###############################################################################################
# Function to Create Quote Line Items
###############################################################################################
def create_line_items( quoteId, quoteItems):
    responses = list()
    compositePayload = list()
    quoteLineItemsToCreate = filter(lambda item: item["sfId"] != "", quoteItems)
    if quoteLineItemsToCreate:
        # Create in batches of API_LIMIT.CREATE_API_RECORD_LIMIT (Currently 200)
        for batch in range(0, len(quoteLineItemsToCreate), 200):
            records = list()
            for item in quoteLineItemsToCreate[batch:batch+200]:
                record = quotelineitem_integration_mapping( item["item"])
                record["QuoteId"] = quoteId
                record["Product2Id"] = item["sfId"]
                record["PriceBookEntryId"] = item["sfCustomPriceBookEntryId"]
                record["attributes"] = {"type": "QuoteLineItem"}
                records.append(record)
            if records:
                compositeRequest = get_cr_sobjectcollection_payload_header("POST", "Create_Quote_Line_Items", None)
                compositeRequest["body"] = {"records": records}
                compositePayload.append(compositeRequest)

                if compositePayload:
                    response = post_composite_request( compositePayload, 'Create_Quote_Line_Items')
                    responses.append(response)
    return responses

##############################################################################################
# Function for Quote Line Item Mapping
###############################################################################################
def quotelineitem_integration_mapping(cpqItem):
    salesforceLineItem = dict()
    salesforceLineItem["Description"] = cpqItem.Description
    salesforceLineItem["Quantity"] = cpqItem.Quantity
    salesforceLineItem["UnitPrice"] = cpqItem.ListPrice
    salesforceLineItem["CPQ_Item_Number__c"] = cpqItem.RolledUpQuoteItem
    #salesforceLineItem["CPQ_Part_Number__c"] = cpqItem.PartNumber
    salesforceLineItem["CPQ_Part_Name__c"] = cpqItem.ProductName if cpqItem.ProductName != "WriteIn" else cpqItem.Description
    salesforceLineItem["CPQ_Product_Line__c"] = cpqItem['QI_ProductLine'].Value
    salesforceLineItem["CPQ_Plant__c"] = cpqItem['QI_Plant'].Value
    salesforceLineItem["CPQ_Qty__c"] = cpqItem.BaseQuantity
    salesforceLineItem["CPQ_Unti_List_Price__c"] = cpqItem.ListPrice
    salesforceLineItem["CPQ_Extended_List_Price__c"] = cpqItem['QI_ExtendedListPrice'].Value
    salesforceLineItem["PMC_Contract_Discount__c"] = cpqItem['QI_MPA_Discount_Percent'].Value
    salesforceLineItem["PMC_Contract_Sell_Price__c"] = cpqItem['QI_Target_Sell_Price'].Value
    salesforceLineItem["PMC_Additional_Discount__c"] = cpqItem['QI_Additional_Discount_Percent'].Value
    salesforceLineItem["PMC_Requested_Discount__c"] = cpqItem['QI_Additional_Discount_Percent'].Value + cpqItem['QI_MPA_Discount_Percent'].Value
    salesforceLineItem["Requested_Unit_Sell_Price__c"] = cpqItem.NetPrice
    salesforceLineItem["CPQ_Extended_Sell_Price__c"] = cpqItem.ExtendedAmount
    salesforceLineItem["PMC_Unit_Gas_ETO_Price__c"] = cpqItem['QI_GAS_ETO_PRICE_ADD'].Value
    salesforceLineItem["CPQ_Sell_Price_With_Gas_ETO_Price__c"] = cpqItem['QI_NetPrice_With_ETO'].Value
    salesforceLineItem["PMC_Unit_Cost__c"] = cpqItem['QI_UnitWTWCost'].Value or cpqItem.Cost
    salesforceLineItem["PMC_Extended_Cost__c"] = cpqItem['QI_ExtendedWTWCost'].Value or cpqItem.ExtendedCost
    salesforceLineItem["WTW_Margin_at_Requested_Purchase_Price__c"] = cpqItem['QI_WTWMarginPercent'].Value
    salesforceLineItem["CPQ_Item_GUID__c"] = cpqItem.QuoteItemGuid

    return salesforceLineItem