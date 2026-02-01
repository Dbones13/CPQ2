#---------------------------------------------------------------------------------------------------------
#					Change History Log
#---------------------------------------------------------------------------------------------------------
# Description : CPQ should send Quote Line items to SFDC
# JIRA Ref.   : CXCPQ-65799
# Author      : H542824
# CreatedDate : 17-01-2024
#----------------------------------------------------------------------------------------------------------
# Date 			Name					    Version     Comment
# 17-01-2024	Pratik Sanghani    			7 	        Initial Version
#----------------------------------------------------------------------------------------------------------

import GS_PMC_QLI_Sync_Functional_Util as QLI_Helper

CREATE_API_RECORD_LIMIT = 200
SFDC_QUOTEID = QLI_Helper.get_sf_quote_id(Quote.QuoteId, Quote.UserId)
SFDC_STANDARD_PRICE_BOOK_ID, PMC_PRICE_BOOK_ID = QLI_Helper.get_sf_pricebook_ids()

quoteItems = [{"PartNumber":item.PartNumber, "item": item, "lookUps": list(), "sfId": "", "sfStandardPriceBookEntryId": "", "sfCustomPriceBookEntryId": ""} for item in Quote.Items]
#quoteItems = QLI_Helper.back_office_sync_filter(quoteItems)
#for item in Quote.Items:
#    if item.ProductName == "WriteIn":
#        quoteItems.append({"PartNumber":item.PartNumber+'_'+item.Description, "item": item, "lookUps": list(), "sfId": "", "sfStandardPriceBookEntryId": "", "sfCustomPriceBookEntryId": ""})
if quoteItems:
    # Get product lookup value for each item
    for item in quoteItems:
        item["lookUps"] = QLI_Helper.get_product_lookups(item["item"])
        
    listOfLookUps = [item["lookUps"] for item in quoteItems if item["lookUps"]]
    if listOfLookUps:
        responses = QLI_Helper.get_sf_internal_product_ids(listOfLookUps)

        if responses:
            for response in responses:
                quoteItems = QLI_Helper.collect_sf_internal_product_ids(quoteItems, response)

        responses = list()
        # Collect line items without corresponding Salesforce products            
        productsToCreate = filter(lambda x:x["sfId"]=="", quoteItems)
        # Remove Duplicates by lookups
        uniqueProductsToCreate = list()
        for item in productsToCreate:
            if item["lookUps"] not in [i["lookUps"] for i in uniqueProductsToCreate]:
                uniqueProductsToCreate.append(item)
        for batch in range(0, len(uniqueProductsToCreate), CREATE_API_RECORD_LIMIT):
            response = QLI_Helper.create_sf_product_master(uniqueProductsToCreate[batch:batch+CREATE_API_RECORD_LIMIT])
            responses.append(response)
        # Collect sfIds of created products
        if responses:
            createdProductIds = list()
            for response in responses:
                if response["compositeResponse"]:
                    createdProductsResp = next((resp for resp in response["compositeResponse"] if resp["referenceId"]=="Create_Products"), None)
                    if createdProductsResp:
                        createdProducts = [str(prod["id"]) for prod in createdProductsResp["body"]]
                        if createdProducts: 
                            createdProductIds += createdProducts
            if createdProductIds:
                responses = QLI_Helper.get_sf_product_by_ids(createdProductIds, listOfLookUps)
                if responses:
                    for response in responses:
                        quoteItems = QLI_Helper.collect_sf_internal_product_ids(quoteItems, response)
                
        sfPMCPriceBookId = PMC_PRICE_BOOK_ID
        # Call API to get existing Price Book Entries
        quoteItems = QLI_Helper.process_collection_pricebook_ids(Quote, quoteItems, sfPMCPriceBookId, SFDC_STANDARD_PRICE_BOOK_ID)

        done = set()
        quoteItemsToProcess = list()
        for item in quoteItems:
            if item["sfId"] not in done:
                done.add(item["sfId"])
                quoteItemsToProcess.append(item)
        # Create/Update Price Book Entries in batches of API_LIMIT.CREATE_API_RECORD_LIMIT (Currently 200)
        for batch in range(0, len(quoteItemsToProcess), 200):
            QLI_Helper.create_price_book_entries(Quote,quoteItemsToProcess[batch:batch+200], sfPMCPriceBookId,SFDC_STANDARD_PRICE_BOOK_ID)

        # Call API to retreive existing/created/updated Price Book Entries
        quoteItems = QLI_Helper.process_collection_pricebook_ids(Quote,quoteItems, sfPMCPriceBookId, SFDC_STANDARD_PRICE_BOOK_ID)


        #body = {"Pricebook2ID": "01s020000003ib1AAA"}
        if SFDC_QUOTEID != None:
            QLI_Helper.delete_quote_line_items(str(SFDC_QUOTEID))
            #set_sf_PMC_pricebook(SFDC_QUOTEID, bearerToken, body, "integrationReference")
            QLI_Helper.create_line_items(str(SFDC_QUOTEID), quoteItems)