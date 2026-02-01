from System.Net import HttpWebRequest
from System.Text import Encoding
from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules

class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
bearerToken = class_sf_integration_modules.get_auth2_token()
headers = class_sf_integration_modules.get_authorization_header(bearerToken)
def getQuoteDetails(headers):
    quoteId = Quote.QuoteId
    userId = Quote.UserId
    query = "?q="+"SELECT+Id+FROM+Quote+WHERE+Quote_ID__c+=+{}+and+Owner_ID__c+=+{}".format(quoteId,userId)
    QuoteInfo = class_sf_integration_modules.call_soql_api(headers, query)
    return QuoteInfo.records

def getKeyDict():
    query = "select * from HPS_INTEGRATION_PARAMS"
    keyDict = dict()
    for r in SqlHelper.GetList(query):
        keyDict[r.Key] = r.Value
    return keyDict


def getToken(keyDict):

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

def getBody():
	transferPriceInUsd = None
	exchange_rate = Quote.GetCustomField("Exchange Rate").Content
	if Quote.GetCustomField("Quote Type").Content in ['Contract New','Contract Renewal']:
		transferPrice = '{0:.2f}'.format(round(UserPersonalizationHelper.ConvertToNumber(TagParserQuote.ParseString('<* GetFirstFromQuoteTable( Quote_Details, Quote_Regional_Cost) *>')),2))
		if transferPrice:
			transferPriceInUsd = '{0:.2f}'.format(round(float(transferPrice) / float(TagParserQuote.ParseString(exchange_rate)) if TagParserQuote.ParseString(exchange_rate) else 1 ,2))
	else:
		transferPrice = TagParserQuote.ParseString('<* GetFirstFromQuoteTable( Quote_Details, Quote_Regional_Cost) *>')
		if transferPrice:
			transferPriceInUsd = float(transferPrice) / float(TagParserQuote.ParseString(exchange_rate)) if TagParserQuote.ParseString(exchange_rate) else 1 
	margin = TagParserQuote.ParseString("""[IF]([NEQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects)){<* GetFirstFromQuoteTable( Quote_Details, Quote_Regional_Margin_Percent) *>}{<*Eval(replace("<*GetFirstFromQuoteTable(EGAP_Revenue_Margin,EGAP_Quote_Currency,EGAP_Field_Details='Regional Margin %')*>" , "%" , ""))*>}[ENDIF]""")

	return {"Transfer_Price__c" : str(transferPrice) , "Transfer_Price_USD__c" : str(transferPriceInUsd) if transferPriceInUsd else transferPrice , "Regional_Margin__c" : margin,'CPQ_Table_Api__c': False}

keyDict =  getKeyDict()
header = {"Authorization" : getToken(keyDict) , "HON-Org-Id" : "PMT-HPS"}


sfdcDetails = getQuoteDetails(headers)
if sfdcDetails:
	Session['SFDC_Quote_ID'] = sfdcDetails[0]["Id"]

#url = "https://{}/sfdc/sales/profiles/access/v1/cpqQuoteId/{}".format(keyDict['SFDC_Host'] , TagParserQuote.ParseString('<*CTX( Quote.OwnerId )*><*CTX( Quote.CartId )*><*CTX( Quote.Revision.Name )*>'))
url = "https://{}/sfdc/sales/profiles/access/v1/cpqQuoteId/{}".format(keyDict['SFDC_Host'] , Session['SFDC_Quote_ID'])

body = getBody()
Log.Write(str(url))
Log.Write(str(body))
res = RestClient.Patch(url , body , header)
#ScriptExecutor.ExecuteGlobal('GS_GetQuoteStatus')