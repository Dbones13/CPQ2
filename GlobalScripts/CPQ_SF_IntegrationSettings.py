###############################################################################################
# Class CL_GeneralIntegrationSettings:
#       Class to store feature enablement properties
###############################################################################################
class CL_GeneralIntegrationSettings:
    # Update existing products in Salesforce when sending data from CPQ items
    UPDATE_EXISTING_PRODUCTS_IN_SALESFORCE = False
    # Attach quote to opportunity immediately upon quote is created
    ATTACH_TO_OPP_IMMEDIATELY_ON_QUOTE_CREATED = True
    # Product types that will not be included in CRM opportunity
    PRODUCT_TYPE_EXCLUSION = ['5002-5566','A01','ABC','Accessories','ACF','AHT','BAPZ','BBH','BBT','C17','C2A','C2B','C2Y','C4Y','C5V','C5Y','C6C','C6P','CLS','CLS','CLV','CST','DAP','DRI','E1Y','E2D','E2K','E2Y','E3C','E3Y','E4B','E4K','E4M','E4P','E4S','E4Y','E5B','E5F','E5R','E5Y','E6B','E6D','E6L','E6O','E6P','E6S','E6T','E6Y','E74','E7A','E7B','E7C','E7D','E7H','E7J','E7M','E7N','E7P','E7Q','E7R','E7U','E7V','E7Y','E8R','E8S','E8Y','E9A','E9E','E9F','E9K','E9M','E9P','E9Q','E9R','E9T','E9Y','E9Z','ECC','ECK','ECM','ECY','EHA','EHC','EHF','EHH','EHJ','EHW','EHY','EMA','EMB','EMD','EME','EMM','EMP','EMT','EMY','EOB','EOC','EOF','EOH','EOT','EOY','F2A','F2C','F3B','F6D','F6Y','F7C','F8F','F8G','F8H','F8N','F8T','Hardware','Honeywell products','INPZ','IT Projects','KNE','KNEA','LDC','LNRZ','M1C','M1M','M1X','M1Y','M2H','M2M','M2Y','M3B','M3D','M3F','M3P','M3R','M3S','M3U','M3Y','M4B','M4L','M4V','M4Y','M6P','M6Y','MOB','MOT','N12Y','N137','N143','N230','N3W1','N423','N42Y','N441','N44D','N4B1','N4F2','N4GY','N4H9','N4HD','N4HF','N53Y','N554','N561','N565','N56Y','N6E2','N980','P118','P120','P123','P125','P153','P15Y','P1Y0','P411','P41A','P41L','P423','P424','P42D','P42E','P42F','P42G','P42H','P42I','P430','P440','P444','PRE-SALES','S1T','S2S','S3F','S3S','S4C','S4M','S4S','S4Y','S5A','S5C','S5S','S5Y','S6M','S6S','S6Y','STANDARD WARRANTY','THIRD-PARTY LABOR','TRP','TST','X1F','X1Y','X2A','X2B','X2C','X2D','X2E','X2F','X2G','X2R','X2Y','X3A','X3B','X3D','X3E','X3F','X3K','X3N','X3P','X3T','X3V','X3Y','X4A','X4B','X4C','X4D','X4F','X4G','X4H','X4M','X4N','X4P','X4Q','X4R','X4S','X4T','X4U','X4Y','X5P','X5T','YX2','YX4','YX6','YX8','YX9','YXL','YXP']
    # Only one quote can be linked to SF opportunity
    ONLY_ONE_QUOTE_LINKED_TO_OPPORTUNITY = False
    # Quote object in CRM is NOT deleted every time action 'Create/Update Opportunity' is executed
    DO_NOT_DELETE_CRM_QUOTE_ON_CREATE_UPDATE = True
    # All revisions from the quote will be attached to the same opportunity
    ALL_REV_ATTACHED_TO_SAME_OPPORTUNITY = False
    # Salesforce Multi-Currency Everywhere
    SF_MCE = True
    # Debugging parameter to log all API calls in CPQ. This should remain inactive.
    LOG_API_CALLS = True
    # Refresh cache for Salesforce object definitions when using tag scripts (CPQ_SF_***_TAG)
    TAG_CACHING = True

###############################################################################################
# Class CL_CpqIntegrationParams:
#       Class to store CPQ key fields involved in the integration
###############################################################################################
class CL_CpqIntegrationParams:

    OPPORTUNITY_ID_FIELD = "CPQ_SF_OPPORTUNITY_ID"
    OPPORTUNITY_NAME_FIELD = "CPQ_SF_OPPORTUNITY_NAME"


###############################################################################################
# Class CL_SalesforceQuoteParams:
#       Class to store key Salesforce Quote key Objects/fields
###############################################################################################
class CL_SalesforceQuoteParams:
    # CRM Quote Object Name
    SF_QUOTE_OBJECT = "Quote"
    # CRM Field For Persisting Quote Id
    SF_QUOTE_ID_FIELD = "Quote_ID__c"
    # CRM Field For Persisting Quote Owner Id
    SF_OWNER_ID_FIELD = "Owner_ID__c"
    # CRM Field For Persisting Information About Primary Quote
    SF_PRIMARY_QUOTE_FIELD = "Primary__c"
    # CRM Field For Persisting Information About Quote Currency
    SF_QUOTE_CURRENCY_FIELD = ""
    # Salesforce Opportunity Field on Quote Object
    SF_QUOTE_OPPORTUNITY_FIELD = "OpportunityId"

    # Salesforce Quote Number field (Should remain set as --> Name)
    SF_QUOTE_NUMBER_FIELD = "Name"
    # Salesforce relationship between Opportunity and Quote
    SF_OPP_QUOTE_REL = "Quotes"


###############################################################################################
# Class CL_SalesforceAccountObjects:
#       Class to store standard Salesforce Account objects used in Account Mapping
###############################################################################################
class CL_SalesforceAccountObjects:

    SF_OPPORTUNITY_ACC = "OpportunityAccount"
    SF_OPPORTUNITY_PARTNER_ACC_BILL_TO = "OpportunityPartnerRoleAccountBillTo"
    SF_OPPORTUNITY_PARTNER_ACC_SHIP_TO = "OpportunityPartnerRoleAccountShipTo"
    SF_OPPORTUNITY_PARTNER_ACC_END_USER = "OpportunityPartnerRoleAccountEndUser"
    SF_OPPORTUNITY_PARTNER_ROLE_ACC = "OpportunityPartnerRoleAccount"
    SF_OPPORTUNITY_ACC_PARTNER_ROLE_ACC = "OpportunityAccountPartnerRoleAccount"
    SF_OPP_PARTNERS = (SF_OPPORTUNITY_PARTNER_ACC_BILL_TO, SF_OPPORTUNITY_PARTNER_ACC_SHIP_TO,
                       SF_OPPORTUNITY_PARTNER_ACC_END_USER, SF_OPPORTUNITY_PARTNER_ROLE_ACC)


###############################################################################################
# Class CL_SalesforceContactObjects:
#       Class to store standard Salesforce Contact objects used in Contact Mapping
###############################################################################################
class CL_SalesforceContactObjects:

    SF_OPPORTUNITY_ACC_FIRST_CONTACT = "OpportunityAccountFirstContact"
    SF_OPPORTUNIY_ACC_BILL_TO_ROLE = "OpportunityAccountBillToRole"
    SF_OPPORTUNITY_ACC_SHIP_TO_ROLE = "OpportunityAccountShipToRole"
    SF_OPPORTUNIY_ACC_PRIMARY_CONTACT = "OpportunityAccountPrimaryContact"
    SF_OPPORTUNITY_BILL_TO_ROLE = "OpportunityBillToRole"
    SF_OPPORTUNITY_SHIP_TO_ROLE = "OpportunityShipToRole"
    SF_OPPORTUNITY_FIRST_ROLE = "OpportunityFirstRole"
    SF_OPPORTUNITY_PRIMARY_ROLE = "OpportunityPrimaryRole"
    SF_OPPORTUNITY_PARTNER_ACC_FIRST_CONTACT = "OpportunityPartnerAccountFirstContact"
    SF_OPPORTUNITY_PARTNER_ROLE_ACC_PRIMARY_CONTACT = "OpportunityPartnerRoleAccountPrimaryContact"


###############################################################################################
# Class CL_SalesforceIntegrationParams:
#       Class to store key Salesforce Object Identifiers
###############################################################################################
class CL_SalesforceIntegrationParams:
    # Standard Opportunity Objects
    SF_OPPORTUNITY_OBJECT = "Opportunity"
    SF_OPPORTUNITY_LINE_ITEM_OBJECT = "OpportunityLineItem"
    SF_OPPORTUNITY_ID_FIELD = "OpportunityId"
    SF_PRODUCT_OBJECT = "Product2"
    SF_PRICEBOOK_OBJECT = "Pricebook2"
    SF_PRICEBOOK_ENTRY_OBJECT = "PricebookEntry"

    # Standard Objects
    SF_ACCOUNT_OBJECT = "Account"
    SF_CONTACT_OBJECT = "Contact"
    SF_OPPORTUNITY_PARTNER_OBJECT = "OpportunityPartner"
    SF_OPPORTUNITY_CONTACT_OBJECT = "OpportunityContactRole"
    SF_ACCOUNT_CONTACT_ROLE = "AccountContactRole"
    SF_PARTNER = "Partner"
    SF_CONTENT_VERSION = "ContentVersion"
    SF_CONTENT_DOC_LINK = "ContentDocumentLink"