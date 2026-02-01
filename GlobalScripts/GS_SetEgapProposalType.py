# Get Authorization Token
from System import Array
#import clr
#clr.AddReference("System.Xml")
#from System.Xml import XmlElement, XmlNode
#import sys
import GS_CommonModule as CM
from CPQ_SF_FunctionModules import get_quote_opportunity_id
from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules

def getProposalType(headers):
    quoteId = Quote.QuoteId
    userId = Quote.UserId
    query = "?q="+"SELECT+Proposal_Type__c+FROM+Quote+WHERE+Quote_ID__c+=+{}+and+Owner_ID__c+=+{}".format(quoteId,userId)
    propType = class_sf_integration_modules.call_soql_api(headers, query)
    #QuoteInfo = SalesforceProxy.Binding.query("SELECT Primary_Quote__c,ContactId FROM Quote WHERE Quote_ID__c = {} and Owner_ID__c = {}".format(quoteId,userId))
    return propType.records
CF_PropType = str(CM.getCFValue(Quote , "EGAP_Proposal_Type"))
quoteType = Quote.GetCustomField('Quote Type').Content
if CF_PropType == '' and quoteType not in ['Contract New','Contract Renewal']:
    class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
    bearerToken = class_sf_integration_modules.get_auth2_token()
    headers = class_sf_integration_modules.get_authorization_header(bearerToken)
    propType = getProposalType(headers)
    Egap_PT = ''
    for item in propType:
        Egap_PT = item["Proposal_Type__c"]
        Trace.Write("ProposalType --------------> {}".format(Egap_PT))
    Quote.GetCustomField("EGAP_Proposal_Type").Content = str(Egap_PT)
