from CPQ_SF_CpqHelper import CL_CpqHelper
from CPQ_SF_FunctionModules import strip_html_tags


###############################################################################################
# Class CL_CustomObjectMapping:
#       Class to store Custom Object Mappings
###############################################################################################
class CL_CustomObjectMapping(CL_CpqHelper):

    ###############################################################################################
    # Function to to store custom object mappings
    ###############################################################################################
    def custom_object_mappings(self):
        mappings = list()
        # OBJECT DEFINITION FOR OPPORTUNITY ACCOUNT (ACCOUNT)
        mapping = dict()
        mapping["Name"] = "Opportunity_Account"
        mapping["Type"] = "Account"
        mapping["Query"] = self.build_soql_query(selectedFields="AccountId",
                                                 table="Opportunity",
                                                 condition="Id='"+self.Quote.GetCustomField("CPQ_SF_OPPORTUNITY_ID").Content+"'")
        mapping["Linked_To_Quote"] = False
        mapping["Inbound"] = True
        mapping["Outbound"] = True
        mapping["Create"] = False
        mappings.append(mapping)

        # Lead Account Manager
        mapping = dict()
        mapping["Name"] = "Lead_Account_Manager"
        mapping["Type"] = "Honeywell_Sales_Team__c"
        # Query = select Id from Honeywell_Sales_Team__c where Opportunity__c = '<*CTX( SFDC.Opportunity.Id )*>' and Lead_Flag__c = true
        mapping["Query"] = self.build_soql_query(selectedFields="Id",
                                                 table="Honeywell_Sales_Team__c",
                                                 condition="Opportunity__c='"+self.Quote.GetCustomField("CPQ_SF_OPPORTUNITY_ID").Content+"' and Lead_Flag__c = true")
        mapping["Linked_To_Quote"] = False
        mapping["Inbound"] = True
        mapping["Outbound"] = True
        mapping["Create"] = False
        mappings.append(mapping)

        # Sold To Account Xref
        if self.Quote.GetCustomField("SoldToId").Content != "":
            mapping = dict()
            mapping["Name"] = "Sold_To_Account_Xref"
            mapping["Type"] = "Account_Xref__c"
            # Query = SELECT Id FROM Account_Xref__c WHERE Id ='<*CTX( Quote.CustomField(SoldToId) )*>'
            mapping["Query"] = self.build_soql_query(selectedFields="Id",
                                                     table="Account_Xref__c",
                                                     condition="Id='"+self.Quote.GetCustomField("SoldToId").Content+"'")
            mapping["Linked_To_Quote"] = False
            mapping["Inbound"] = True
            mapping["Outbound"] = True
            mapping["Create"] = False
            mappings.append(mapping)

        # Opty
        mapping = dict()
        mapping["Name"] = "Opty"
        mapping["Type"] = "Opportunity"
        # Query = select Id from opportunity where id='<*CTX( SFDC.Opportunity.Id )*>'
        mapping["Query"] = self.build_soql_query(selectedFields="Id",
                                                 table="opportunity",
                                                 condition="Id='"+self.Quote.GetCustomField("CPQ_SF_OPPORTUNITY_ID").Content+"'")
        mapping["Linked_To_Quote"] = False
        mapping["Inbound"] = True
        mapping["Outbound"] = True
        mapping["Create"] = False
        mappings.append(mapping)


        return mappings

    #############################
    # INBOUND Salesforce -> CPQ #
    ###############################################################################################
    # Function for Custom Object mappings on Quote Create (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_create_custom_object_mapping(self, Quote, TagParserQuote, customObject, customObjectName):
        # if customObjectName == "Opportunity_Decision_Maker":
        #     # Set customObject data => Quote
        pass

    ###############################################################################################
    # Function for Custom Object mappings on Quote Update (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_update_custom_object_mapping(self, Quote, TagParserQuote, customObject, customObjectName):
        # if customObjectName == "Opportunity_Decision_Maker":
        #     # Set customObject data => Quote
        #     pass
        pass

    ###############################################################################################
    # Function for Custom Object mappings on Quote Create/Update (Salesforce -> CPQ)
    ###############################################################################################
    def on_quote_createupdate_custom_object_mapping(self, Quote, TagParserQuote, customObject, customObjectName):
        # Opportunity Account
        if customObjectName == "Opportunity_Account":
            #Set customObject data => Quote
            # Account Site
            Quote.GetCustomField("Account Site").Content = str(customObject["Site"])
            # Access To Inventory
            Quote.GetCustomField("Access to Inventory").Content = str(customObject["Access_to_Inventory__c"])	
            # Siebel Row Id
            Quote.GetCustomField("Siebel Row Id").Content =	str(customObject["Siebel_Row_Id__c"])	
            # Minimum Order Fee Waiver
            Quote.GetCustomField("Minimum Order Fee Waiver").Content =	str(customObject["Minimum_Order_Fee_Waiver__c"])	
            # Expedite Fee Waiver
            Quote.GetCustomField("Expedite Fee Waiver").Content = str(customObject["Expedite_Fee_Waiver__c"])
            # Account Type
            Quote.GetCustomField("Account Type").Content = str(customObject["Type"])	
            # Global Account Name
            #Quote.GetCustomField("Global Account Name").Content = str(customObject["Global_Account_Name__c"])	
            # Customer Segmentation
            Quote.GetCustomField("Customer Segmentation").Content = str(customObject["Customer_Segmentation__c"])

        # Sold To Account Xref
        if customObjectName == "Sold_To_Account_Xref":
            #Set customObject data => Quote
            expected_id = str(customObject["System_ID__c"]) if customObject["IsActive__c"] == 'true' else ''
            current_id = Quote.GetCustomField("SoldToCustomerId").Content
            if current_id!='' and current_id != expected_id:
                Quote.GetCustomField("SoldToCustomerIdChange").Content = 'True'
            Quote.GetCustomField("SoldToCustomerId").Content = str(customObject["System_ID__c"])

            Quote.GetCustomField("SoldToAddress1").Content = str(customObject["Address_Line_1__c"])

            Quote.GetCustomField("SoldToAddress2").Content = str(customObject["Address_Line_2__c"])

            Quote.GetCustomField("SoldToCity").Content = str(customObject["City__c"])

            Quote.GetCustomField("SoldToProvince").Content = str(customObject["State__c"])

            Quote.GetCustomField("SoldToZipCode").Content = str(customObject["Postal_Code__c"])

            Quote.GetCustomField("SoldToCountry").Content =	str(customObject["Country__c"])

        pass

    ##############################
    # OUTBOUND CPQ -> Salesforce #
    ###############################################################################################
    # Function for Custom Object mappings on Quote Create (CPQ -> Salesforce)
    ###############################################################################################
    def on_opp_create_custom_object_mapping(self, Quote, TagParserQuote, customObjectName):
        customObject = dict()
        #if customObjectName == "Opportunity_Decision_Maker":
            # Populate customObject data
        return customObject

    ###############################################################################################
    # Function for Custom Object mappings on Quote Update (CPQ -> Salesforce)
    ###############################################################################################
    def on_opp_update_custom_object_mapping(self, Quote, TagParserQuote, customObjectName):
        customObject = dict()
        #if customObjectName == "Opportunity_Decision_Maker":
            # Populate customObject data
        return customObject

    ###############################################################################################
    # Function for Custom Object mappings on Quote Create/Update (CPQ -> Salesforce)
    ###############################################################################################
    def on_opp_createupdate_custom_object_mapping(self, Quote, TagParserQuote, customObjectName):
        customObject = dict()
        #if customObjectName == "Opportunity_Decision_Maker":
            # Populate customObject data
        return customObject