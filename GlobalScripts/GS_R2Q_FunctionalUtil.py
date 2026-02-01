#---------------------------------------------------------------------------------------------------------
#					Change History Log
#---------------------------------------------------------------------------------------------------------
# Description: Main script for R2Q Parts and Spot Quote product addition
#----------------------------------------------------------------------------------------------------------
# Date 			Name					    Version   Comment
# 05-12-2023	Sourav Kumar Samal			113		  Applied fix for CXCPQ-73085

import GS_APIGEE_Integration_Util
from Scripting import GenDocFormat
from System import Convert
from GS_R2Q_Integration_Messages import CL_R2Q_Integration_ErrorMessages as Error, CL_R2Q_Integration_SuccessMessages as Success
import GS_CalculateTotals
from System.Net import HttpWebRequest
from System.Text import Encoding

def getItem(R2Q_ID):
    #Initiate Data Dictionary
    productData = dict()
    url = GS_APIGEE_Integration_Util.GetAPIGEEBaseURL()
    headers = GS_APIGEE_Integration_Util.GetAPIGEEAuthHeader()
    query_url="{url}/hps/cpq/line-items/{ver}/get-line-item?q=Select+Id,Product2.ProductCode,Quantity,Discount,Requested_Unit_Sell_Price__c+from+QuoteLineItem+where+Quote.QuoteNumber='{R2QID}'".format(url = str(url), ver = "v1",R2QID = str(R2Q_ID))

	#call API
    while True:
        response = RestClient.Get(query_url, headers)
        for i in response["records"]:
            if str(i['Discount']) == "":
                discount=0
            else:
                discount = float(i['Discount'])

            if str(i['Quantity']) == "":
                quantity=0
            else:
                quantity = int(i['Quantity'])

            if str(i['Requested_Unit_Sell_Price__c']) == "":
                targetSellPrice=0
            else:
                targetSellPrice = float(i['Requested_Unit_Sell_Price__c'])

            DiscountAsked = 1 if discount != 0 or targetSellPrice != 0 else 0
            
            key = str(i["Id"])
            productData[key] = {
                "PartNumber": str(i["Product2"]["ProductCode"]),
                "Quantity": quantity,
                "DiscountPercentage": discount,
                "TargetSellPrice": targetSellPrice,
                "DiscountAsked": DiscountAsked
            }
        if response.done == True:
            break
        query_url = response.next_url
    return productData

def AddProducts(Quote, TagParserQuote, products):
    try:
        Messagetext = ""

        # Creating a list of all partnumbers from the products
        sfPartNumbersList = []
        for i in products.values():
            sfPartNumbersList.append(i["PartNumber"])
        format_partNumberFilters = "(" + "'{}', " * (len(sfPartNumbersList) - 1) + "'{}')"
        partNumberFilters = format_partNumberFilters.format(*sfPartNumbersList)

        # Fetching the product details from database
        sqlQuery = "Select SYSTEM_ID, PRODUCT_CATALOG_CODE from products where PRODUCT_CATALOG_CODE in " + partNumberFilters + " and PRODUCT_ACTIVE = 'True'"
        ProductData = SqlHelper.GetList(sqlQuery)

        # Validating if the number of products received from database matches with the products received from SFDC
        if len(list(set(sfPartNumbersList))) != ProductData.Count:
            Messagetext = "One or more error(s) occured while processing:
"
            cpqProductsList = []
            for i in ProductData:
                cpqProductsList.append(i.PRODUCT_CATALOG_CODE) 
            for i in sfPartNumbersList:
                if i not in cpqProductsList:
                    Messagetext += "Product with part number '{0}' was not found in SAP CPQ.
".format(i)
            # Log the error and retun false
            UpdateStatusMessage(Quote, "Error", "Notification", Messagetext)
            return False

        # Adding the products to the Quote
        cpqProductDict = {}
        for item in ProductData:
            cpqProductDict[item.PRODUCT_CATALOG_CODE] = item.SYSTEM_ID
        successCount = 0
        for item_v in products.values():
            # Check if quantity is less than or equals to 0
            if item_v["Quantity"] <= 0:
                Messagetext += "Product with part number '{0}' has incorrect quantity provided.
".format(item_v["PartNumber"])
                continue
            # Check if discount percentage is in range of 0-100
            elif item_v["DiscountPercentage"] < 0 or item_v["DiscountPercentage"] > 100:
                Messagetext += "Product with part number '{0}' has incorrect discounts provided.
".format(item_v["PartNumber"])
                continue
            # Check id target sell price is not -ve
            elif item_v["TargetSellPrice"] < 0:
                Messagetext += "Product with part number '{0}' has target sell price is less than 0.
".format(item_v["PartNumber"])
                continue
            else:
                ProductAdded = Quote.AddItem(cpqProductDict[item_v["PartNumber"]], item_v["Quantity"])
                # Once product is added update the discount percentage
                for item_p in ProductAdded:
                    if item_p.QI_No_Discount_Allowed.Value == '0' or (item_p.QI_No_Discount_Allowed.Value == '1' and item_v["DiscountAsked"] == 0):
                        if item_p.ListPrice > 0:
                            if item_v["TargetSellPrice"] != 0:
                                item_p.QI_Additional_Discount_Percent.Value = ( ( item_p.ListPrice - item_v["TargetSellPrice"] ) / item_p.ListPrice ) * 100
                            else:
                                item_p.QI_Additional_Discount_Percent.Value = item_v["DiscountPercentage"]
                            successCount += 1
                        else:
                            Messagetext += "Product with part number '{0}' has no list price available.
".format(item_v["PartNumber"])
                    else:
                        Messagetext += "Product with part number '{0}' is not discountable.
".format(item_v["PartNumber"])
        Quote.Calculate(2)

        # If successful, Repricing and Saving the Quote
        if successCount == len(products):
            for action in Quote.Actions:
                if action.Name == "Reprice":
                    Quote.ExecuteAction(action.Id)
                    break
            QT = Quote.QuoteTables["Quote_Details"]
            sellPrice = 0.00
            for i in QT.Rows:
                sellPrice = round(i.GetColumnValue('Quote_Sell_Price'), 2)
                break
            Quote.GetCustomField("Total Sell Price").Content = str(sellPrice)

        # In case of any error, log the error and retun false
        if Messagetext != "":
            Messagetext = "One or more error(s) occured while processing:
" + Messagetext
            UpdateStatusMessage(Quote, "Error", "Notification", Messagetext)
            return False
        else:
            return True

    except Exception as e:
        # In case of any error, log the error and retun false
        Log.Write("Exception Found as >>> {0}".format(e))
        UpdateStatusMessage(Quote, "Error", "Notification", str(e))
        return False

def getKeyDict():
    query = "select * from HPS_INTEGRATION_PARAMS"
    keyDict = dict()
    for r in SqlHelper.GetList(query):
        keyDict[r.Key] = r.Value
    return keyDict

def getToken(keyDict, StreamReader):

    url = "https://{}/v2/oauth/accesstoken".format(keyDict['SFDC_Host'])

    payload = "grant_type=client_credentials&client_id={}&client_secret={}".format(keyDict['SFDC_Client_Id'] , keyDict['SFDC_Client_Secret'])

    data = Encoding.ASCII.GetBytes(payload)

    webRequest = HttpWebRequest.Create(url)
    webRequest.Method = "POST"
    webRequest.ContentType = "application/x-www-form-urlencoded"
    webRequest.ContentLength = data.Length

    requestStream = webRequest.GetRequestStream()
    requestStream.Write(data , 0 , data.Length)

    response = webRequest.GetResponse()
    responseStream = response.GetResponseStream()

    jsonData = StreamReader(responseStream).ReadToEnd()

    json = RestClient.DeserializeJson(jsonData)

    return "{} {}".format(json.token_type , json.access_token)

def getBody(Quote, TagParserQuote):
    productLines , PLSGroups , productTypes, totalDict = GS_CalculateTotals.calculateProductLines(Quote)
    quoteTotalTable = Quote.QuoteTables["Quote_Details"]

    minOrderFee = UserPersonalizationHelper.ConvertToNumber(Quote.GetCustomField('Minimum Order Fee').Content) if Quote.GetCustomField('Minimum Order Fee').Content else 0.0
    totalExpediteFee = 0.0
    if quoteTotalTable.Rows.Count > 0:#--Added due to exception on SaveQuote
        row = quoteTotalTable.Rows[0]

        for item in Quote.Items:
            if item['QI_Expedite_Fees'].Value:
                totalExpediteFee = totalExpediteFee + UserPersonalizationHelper.ConvertToNumber(str(item['QI_Expedite_Fees'].Value))

        row['Total_Sell_Price_incl_appl_Fees_'] = row['Quote_Sell_Price'] + minOrderFee + totalExpediteFee
        quoteTotalTable.Save()
        Quote.GetCustomField('Total_Sell_Price_Updated').Content = UserPersonalizationHelper.ToUserFormat(row['Total_Sell_Price_incl_appl_Fees_'])
        SellPriceQuote = str(row['Total_Sell_Price_incl_appl_Fees_'] )
        SellPriceUSDQuote = float(SellPriceQuote) / float(Quote.GetCustomField('Exchange Rate').Content) if Quote.GetCustomField('Exchange Rate').Content else 1
    
    listPrice = totalDict.get('totalListPrice' , 0)
    listPriceUSD = float(listPrice) / float(TagParserQuote.ParseString('<*CTX( Quote.CustomField(Exchange Rate) )*>')) if TagParserQuote.ParseString('<*CTX( Quote.CustomField(Exchange Rate) )*>') else 1
    discountRequested = (totalDict.get('additionalDiscountAmount' , 0) * 100) / (totalDict.get('totalListPrice' , 0) - totalDict.get('mpaDiscountAmount' , 0))
    transferPrice = totalDict.get('totalCost' , 0)
    transferPriceInUsd = None
    if transferPrice:
        transferPriceInUsd = float(transferPrice) / float(TagParserQuote.ParseString('<*CTX( Quote.CustomField(Exchange Rate) )*>')) if TagParserQuote.ParseString('<*CTX( Quote.CustomField(Exchange Rate) )*>') else 1
    margin = round(float((totalDict.get('totalRegionalMargin' , 0) * 100) / totalDict.get('totalExtendedAmount' , 0)), 2)

    return {"Discount_Requested__c" : str(discountRequested), "List_Price__c" : str(listPrice), "List_Price_USD__c" : str(listPriceUSD), "Sell_Price__c" : str(SellPriceQuote), "Sell_Price_USD__c" : str(SellPriceUSDQuote), "Transfer_Price__c" : str(transferPrice), "Transfer_Price_USD__c" : str(transferPriceInUsd) if transferPriceInUsd else transferPrice, "Regional_Margin__c" : str(margin)}

def calculateQuoteDetails(Quote, TagParserQuote, StreamReader):
    try:
        keyDict =  getKeyDict()
        header = {"Authorization" : getToken(keyDict, StreamReader) , "HON-Org-Id" : "PMT-HPS"}

        url = "https://{}/sfdc/sales/profiles/access/v1/cpqQuoteId/{}".format(keyDict['SFDC_Host'] , TagParserQuote.ParseString('<*CTX( Quote.OwnerId )*><*CTX( Quote.CartId )*><*CTX( Quote.Revision.Name )*>'))

        body = getBody(Quote, TagParserQuote)
        res = RestClient.Patch(url , body , header)

    except Exception as e:
        # In case of any error, log the error and retun false
        Log.Write("Exception Found as >>> {0}".format(e))
        UpdateStatusMessage(Quote, "Error", "Notification", str(e))
        return False
def getSFQuoteID(QuoteContext):
    APIGEEURL=GS_APIGEE_Integration_Util.GetAPIGEEBaseURL()
    APIGEEHeader=GS_APIGEE_Integration_Util.GetAPIGEEAuthHeader()
    #Fetch QuoteID from APIGEE
    cartId = QuoteContext.QuoteId
    ownerId = QuoteContext.UserId
    APIGEEQuoteURL="{APIGEEURL}/hps/cpq/line-items/{ver}/get-line-item?q=select+Id+from+Quote+where+Quote_ID__c={cartId}+and+Owner_ID__c={ownerId}".format(APIGEEURL = str(APIGEEURL), ver = "v1",cartId = str(cartId),ownerId = str(ownerId))
    quoteID=RestClient.Get(APIGEEQuoteURL,APIGEEHeader)
    #Check whether QuoteId is received from the APIGEE
    if len(quoteID.records) != 0:
        for q in quoteID.records:
            SFQuoteID = str(q.Id)
        return SFQuoteID

def R2QDocumentGeneration(ctxQuote):
    try:
        #Get APIGEE Header and URL
        APIGEEHeader=GS_APIGEE_Integration_Util.GetAPIGEEAuthHeader()
        APIGEEURL=GS_APIGEE_Integration_Util.GetAPIGEEBaseURL()
        APIGEEDocurl='{APIGEEURL}/hps/cpq/proposal-doc/v1/get-attachment'.format(APIGEEURL = str(APIGEEURL))

        #Get OpportunityType
        OppType=ctxQuote.GetCustomField('Opportunity Type').Content
        isR2QProject = ctxQuote.GetCustomField("IsR2QRequest").Content
        CustomParamDict={}
        SqlQuery="Select STRING_VALUE,PARAM_NAME from CT_CUSTOM_PARAMETER where PARAM_NAME in ('R2Q_OpportunityType','R2Q_TemplateName','R2Q_TemplateName_Common')"
        CustomParamList=SqlHelper.GetList(SqlQuery)
        for i in CustomParamList:
            CustomParamDict[i.PARAM_NAME]=i.STRING_VALUE
        #Assign Template name-If Opportunity type in Quote is "Automation College" then assign template name as "Honeywell Academy Proposal" else assign template name as "LSS Parts and Spot - No Terms and Conditions"
        if OppType==CustomParamDict['R2Q_OpportunityType']:
            templateName=CustomParamDict['R2Q_TemplateName']
        else:
            templateName=CustomParamDict['R2Q_TemplateName_Common']
        if isR2QProject == 'Yes':
            templateName = 'New/Expansion Project (Multilanguage)'

        #Fetch QuoteID from APIGEE
        cartId = ctxQuote.QuoteId
        ownerId = ctxQuote.UserId
        APIGEEQuoteURL="{APIGEEURL}/hps/cpq/line-items/{ver}/get-line-item?q=select+Id+from+Quote+where+Quote_ID__c={cartId}+and+Owner_ID__c={ownerId}".format(APIGEEURL = str(APIGEEURL), ver = "v1",cartId = str(cartId),ownerId = str(ownerId))
        quoteID=RestClient.Get(APIGEEQuoteURL,APIGEEHeader)
        #Check whether QuoteId is received from the APIGEE
        if len(quoteID.records) != 0:
            for q in quoteID.records:
                SFQuoteID = str(q.Id)
        else:
            UpdateStatusMessage(ctxQuote, "Error", "Notification", Error.ProposalDocGenerationError)
            return False

        #Generate Pdf document (except for Project type R2Q quotes)
        if isR2QProject != 'Yes':
            pdf_doc=ctxQuote.GenerateDocument(templateName,GenDocFormat.PDF)

            #Converting pdf to 64bit stream
            pdfName=ctxQuote.GetLatestGeneratedDocumentFileName()
            PdfBytes=ctxQuote.GetLatestGeneratedDocumentInBytes()
            pdf_64bit=Convert.ToBase64String(PdfBytes)

            #Send Generated Pdf to APIGEE
            parampdf={'ParentId' : SFQuoteID ,'Name' : pdfName, 'body' : pdf_64bit,'ContentType': 'application/pdf'}
            pdfPost=RestClient.Post(APIGEEDocurl,parampdf,APIGEEHeader)

        #Generate docx document
        docx_doc=ctxQuote.GenerateDocument(templateName,GenDocFormat.DOCX)

        #Converting DOCX to 64bit stream
        docName=ctxQuote.GetLatestGeneratedDocumentFileName()
        docBytes=ctxQuote.GetLatestGeneratedDocumentInBytes()
        doc_64bit=Convert.ToBase64String(docBytes)

        #Send Generated DOCX to APIGEE
        paramdoc={'ParentId' : SFQuoteID ,'Name' : docName, 'body' : doc_64bit,'ContentType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
        docpost=RestClient.Post(APIGEEDocurl,paramdoc,APIGEEHeader)

        if docpost.success==True and isR2QProject == 'Yes':
            return True
		#Return error message if the post call returns error
        if docpost.success==True and pdfPost.success==True:
            #UpdateStatusMessage(ctxQuote, "GenerateDocument", "Action", Success.ProposalDocGenerated)
            return True
        else:
            UpdateStatusMessage(ctxQuote, "Error", "Notification", Error.ProposalDocGenerationError)
            return False
    except Exception as e:
        # In case of any error, log the error and retun false
        Log.Write("Exception Found as >>> {0}".format(e))
        UpdateStatusMessage(ctxQuote, "Error", "Notification", Error.ProposalDocGenerationError)
        return False

def UpdateStatusMessage(QuoteContext,ProcessStage,Action,Messagetext):
    ApigeeHeader= GS_APIGEE_Integration_Util.GetAPIGEEAuthHeader()	#Get SFDC Header and URL
    ApigeeURL= GS_APIGEE_Integration_Util.GetAPIGEEBaseURL()
    if Action == "Notification":
        QuoteContext.GetCustomField("CF_R2Q_ErrorText").Content = Messagetext[0:4000]
        QuoteContext.Save(False)
    if QuoteContext.GetCustomField("R2QFlag").Content=="Yes":
        SFQuoteID =  getSFQuoteID(QuoteContext)
    else:
        SFQuoteID = QuoteContext.GetCustomField("CF_R2Q_SFDCQuoteId").Content

	#Preparing data for constructing json
    #Change made to JSON Structure on 25-08-2023
    data = {
        "Quote__c" : SFQuoteID,
        "Record_Type__c" : "R2Q Process Event",		#Change made to JSON Structure on 25-08-2023
        "Field_history__c" : ProcessStage,
        "Action_Type__c" : Action,
        "Message__c" : Messagetext
    }
    Log.Write(str(data))
    jsondata = JsonHelper.Serialize(data)	#Serializing the data into JSON format
    compositeURL=ApigeeURL+"/hps/cpq/report-status/v1/quote-table"	#Framing the SFDC endpoint URL by Combining base URL and webservice url
    jsonpost=RestClient.Post(compositeURL,jsondata,ApigeeHeader)	#Making the post call for posting the json data to the webservice