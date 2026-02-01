from System import Array
import GS_CommonModule as CM
from CPQ_SF_FunctionModules import get_quote_opportunity_id
from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
def getOpportunityRecordType(headers,OppId):
    quoteId = Quote.QuoteId
    userId = Quote.UserId
    query = "?q="+"SELECT+T_Opportunity_Record_Type__c+FROM+Opportunity+WHERE+Id+=+'"+str(OppId)+"'"
    opprectype = class_sf_integration_modules.call_soql_api(headers, query)
    #QuoteInfo = SalesforceProxy.Binding.query("SELECT Primary_Quote__c,ContactId FROM Quote WHERE Quote_ID__c = {} and Owner_ID__c = {}".format(quoteId,userId))
    return opprectype.records
CF_OppRecType = str(CM.getCFValue(Quote , "Opportunity Record Type"))
quoteType = Quote.GetCustomField('Quote Type').Content
Trace.Write("GS_OPP_REC_TYPE  " +str(Quote.GetCustomField("Quote Type").Content))
if quoteType not in ['Contract New','Contract Renewal']:
    OppId = get_quote_opportunity_id(Quote)
    class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
    bearerToken = class_sf_integration_modules.get_auth2_token()
    headers = class_sf_integration_modules.get_authorization_header(bearerToken)
    opprectype = getOpportunityRecordType(headers,OppId)
    Trace.Write("opprectype--- "+str(opprectype))
    Opp_RT = ''
    for item in opprectype:
        Opp_RT = item["T_Opportunity_Record_Type__c"]
        Trace.Write(str(Opp_RT))
	Quote.GetCustomField("Opportunity Record Type").Content = str(Opp_RT)