from CPQ_SF_FunctionModules import strip_html_tags
from CPQ_SF_CpqHelper import CL_CpqHelper

###############################################################################################
# Class CL_OpportunityLineItemMapping:
#       Class to store Opportunity Line Item Mappings
###############################################################################################
class CL_OpportunityLineItemMapping(CL_CpqHelper):
    ###############################################################################################
    # Function for Oppportunity Line Item Mapping
    ###############################################################################################
    def opplineitem_integration_mapping(self, Quote, TagParserQuote, cpqItem):
        salesforceLineItem = dict()

        salesforceLineItem["Description"] = cpqItem.Description
        salesforceLineItem["Quantity"] = cpqItem.Quantity
        salesforceLineItem["UnitPrice"] = cpqItem.ListPriceInMarket

        return salesforceLineItem

    ###############################################################################################
    # Function for Product Master Mapping
    ###############################################################################################
    def product_integration_mapping(self, Quote, TagParserQuote, cpqItem):
        salesforceLineItem = dict()

        salesforceLineItem["Name"] = cpqItem.PartNumber
        salesforceLineItem["Description"] = cpqItem.ProductName
        #salesforceLineItem["CurrencyIsoCode"] = TagParserQuote.ParseString("<*CTX( Market.CurrencyCode )*>")

        return salesforceLineItem

    ###############################################################################################
    # Function for Product lookup Salesforce
    ###############################################################################################
    def get_product_lookups(self, Quote, TagParserQuote, cpqItem):
        productlookUps = list()

        lookUp = dict()
        lookUp["SalesforceField"] = "Name"
        lookUp["CpqLookUpValue"] = cpqItem.PartNumber
        lookUp["FieldType"] = self.TYPE_STRING
        productlookUps.append(lookUp)

        return productlookUps