from CPQ_SF_FunctionModules import strip_html_tags
from GS_CommonConfig import CL_CommonSettings as CS


###############################################################################################
# OUTBOUND (CPQ -> Salesforce)
###############################################################################################
###############################################################################################
# Function for Opportunity integration mapping
###############################################################################################
def on_opp_create_outbound_opportunity_integration_mapping(Quote, TagParserQuote):
    opportunity = dict()

    #opportunity["CloseDate"] = Quote.EffectiveDate.ToString("yyyy-MM-dd")

    return opportunity


###############################################################################################
# Function for Opportunity integration mapping
###############################################################################################
def on_opp_update_outbound_opportunity_integration_mapping(Quote, TagParserQuote):
    opportunity = dict()
    OrderId = Quote.GetCustomField("CF_SalesOrderId").Content if Quote.GetCustomField("CF_Manual_Booking").Content == 'True' else Quote.OrderId
    opportunity["Booking_Number__c"] = OrderId
    booking_date = Quote.GetCustomField("Booking Date").Content
    if booking_date != "":
        opportunity["Actual_Book_Date__c"] = UserPersonalizationHelper.CovertToDate(booking_date).ToString ("yyyy-MM-dd")
    if Quote.GetCustomField("Quote Type").Content == "Projects" and Quote.GetCustomField("CF_ProjectId").Content !='' and OrderId !='' :
        opportunity["Sales_Stage__c"] = "9 - Booked / Won"
        opportunity["Win_Loss_Abandon_Comments__c"] = "Booked from CPQ"


    return opportunity


###############################################################################################
# Function for Opportunity integration mapping
###############################################################################################
def on_opp_createupdate_outbound_opportunity_integration_mapping(Quote, TagParserQuote):
    opportunity = dict()

    #opportunity["Name"] = Quote.GetCustomField("CPQ_SF_OPPORTUNITY_NAME").Content

    return opportunity


###############################################################################################
# INBOUND (Salesforce -> CPQ)
###############################################################################################
###############################################################################################
# Function for Opportunity integration mapping
###############################################################################################
def on_quote_create_inbound_opportunity_integration_mapping(Quote, opportunity):
    Quote.GetCustomField("Currency").Content = str(opportunity["CurrencyIsoCode"])
    Quote.GetCustomField("WinProbability").Content = str(opportunity["Win_Probability__c"])



###############################################################################################
# Function for Opportunity integration mapping
###############################################################################################
def on_quote_update_inbound_opportunity_integration_mapping(Quote, opportunity):
    if Quote.OrderStatus.Name=='Preparing':
        Quote.GetCustomField("Sales ORG").Content = str(opportunity["Sales_ORG__c"])
###############################################################################################
# Function for Opportunity integration mapping
###############################################################################################
def on_quote_createupdate_inbound_opportunity_integration_mapping(Quote, opportunity):
    if Quote.OrderStatus.Name=='Preparing':
        Quote.GetCustomField("Booking LOB").Content                         = str(opportunity["Line_of_Business__c"])
        Quote.GetCustomField("Sales ORG").Content                           = str(opportunity["Sales_ORG__c"])
        Quote.GetCustomField("Parts Price List").Content                    = str(opportunity["Parts_Price_List__c"])
        Quote.GetCustomField("Systems Price List").Content                  = str(opportunity["Systems_Price_List__c"])
        Quote.GetCustomField("Sub LOB").Content                             = str(opportunity["Sub_Line_of_Business__c"])
        if Quote.GetCustomField("Opportunity Type").Content =='':#added to fix CXCPQ-112289
            Quote.GetCustomField("Opportunity Type").Content                    = str(opportunity["Type"])
        Quote.GetCustomField("Sales Area").Content                          = str(opportunity["Sales_Area__c"])
        Quote.GetCustomField("Opportunity Tab Booking Country").Content     = str(opportunity["Booking_Country_Name__c"])
        Opportunity=Quote.GetCustomField("Opportunity Type").Content
        Quote.GetCustomField("SFDC_Quote_Type").Content = str(Opportunity)#str(opportunity["Type"]) added to fix CXCPQ-112289
        if str(Opportunity)=='Contract New' and str(opportunity["Line_of_Business__c"])=='HCP':
            Quote.GetCustomField("Quote Type").Content ="Projects"
            Quote.GetCustomField("Opportunity Type").Content="Project"
            Quote.GetCustomField("CF_Manual_Booking").Content ="True"
            Log.Info("CPQ_SF_OpportunityMapping CPQ_SF_OpportunityMapping CPQ_SF_OpportunityMapping ")
            Log.Info("CPQ_SF_OpportunityMapping111 " +str(Quote.GetCustomField("Quote Type").Content))
            #Quote.Save()
        else:
            Quote.GetCustomField("Quote Type").Content = CS.getQuoteType[str(Opportunity)]#CS.getQuoteType[str(opportunity["Type"])] added to fix CXCPQ-112289
            Log.Info("CPQ_SF_OpportunityMapping222 CPQ_SF_OpportunityMapping CPQ_SF_OpportunityMapping2222 ")
    Quote.GetCustomField("Sales Stage").Content                         = str(opportunity["Sales_Stage__c"])
    if Quote.GetCustomField("Opportunity Category").Content =='':#added to fix CXCPQ-112289
        Quote.GetCustomField("Opportunity Category").Content                = str(opportunity["Category__c"])
    #Quote.GetCustomField("CPQ_SF_OPPORTUNITY_ID").Content               = str(opportunity["Opportunity_Number__c"])
    Quote.GetCustomField("CPQ_SF_OPPORTUNITY_NAME").Content             = str(opportunity["Name"])
    Quote.GetCustomField("Business Model").Content                      = str(opportunity["Business_Model__c"])
    Quote.GetCustomField("Market Segment").Content                      = str(opportunity["Market_Segment__c"])
    Quote.GetCustomField("Sub Market Segment").Content                  = str(opportunity["Sub_Market_Segment__c"])
    Quote.GetCustomField("Global Major Project").Content                = str(opportunity["Global_Mega_Project__c"])
    Quote.GetCustomField("Opp Prod Desc").Content                       = str(opportunity["Opp_Prod_Desc__c"])
    Quote.GetCustomField("Forecast Status").Content                     = str(opportunity["Forecast_Type__c"])
    if str(opportunity["CloseDate"]):
        CloseDate = UserPersonalizationHelper.ToUserFormat(DateTime.Parse(str(opportunity["CloseDate"])))
        Quote.GetCustomField("Close Date").Content                      = CloseDate
    Quote.GetCustomField("Legacy CRM ID").Content                       = str(opportunity["Siebel_Opportunity_Id__c"])
    Quote.GetCustomField("PONumber").Content                            = str(opportunity["Customer_PO_Number__c"])
    if str(opportunity["PO_Date__c"]):
        PO_date = UserPersonalizationHelper.ToUserFormat(DateTime.Parse(str(opportunity["PO_Date__c"])))
        Quote.GetCustomField("PurchaseOrderDate").Content               = PO_date
    Quote.GetCustomField("CF_NewCurrency").Content                      = str(opportunity["CurrencyIsoCode"])
    Quote.GetCustomField("Commercial Tab Booking LOB").Content          = str(opportunity["Line_of_Business__c"])
    Quote.GetCustomField("CompetitorCount").Content                     = str(opportunity["Count_Competitor__c"])
    Quote.GetCustomField("EstimatedSellPrice").Content                  = str(opportunity["Estimated_Sell_Price__c"])
    Quote.GetCustomField("Commercial Tab Opportunity Category").Content = str(opportunity["Category__c"])
    Quote.GetCustomField("Pole").Content                                = str(opportunity["FC_Pole__c"])
    Quote.GetCustomField("Destination Region").Content                  = str(opportunity["FC_Region__c"])
    Quote.GetCustomField("ProjectGo").Content                           = str(opportunity["Project_Go__c"])
    Quote.GetCustomField("PartnerAccountID").Content                    = str(opportunity["Sales_Stage__c"])
    Quote.GetCustomField("Account Siebel Id").Content                   = str(opportunity["Account_Siebel_Row_Id__c"])
    Quote.GetCustomField("Booking Country").Content                     = str(opportunity["Booking_Country_Name__c"])
    Quote.GetCustomField("Legacy CRM ID_Booking Info Tab").Content      = str(opportunity["LEGACYSYSID_C__c"])
    Quote.GetCustomField("Opportunity Siebel Id").Content               = str(opportunity["Siebel_Opportunity_Id__c"])
    Quote.GetCustomField("Destination Country").Content               	= str(opportunity["Destination_Country_Name__c"])
    Quote.GetCustomField("Opportunity Number").Content               	= str(opportunity["Opportunity_Number__c"])
    Quote.GetCustomField("SC_CF_STATUS").Content                        = str(opportunity["Account_Status__c"])
    Quote.GetCustomField("SC_CF_Currency").Content = str(opportunity["CurrencyIsoCode"])
    Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content         = str(opportunity["isExtension__c"])
    #Quote.GetCustomField("Currency").Content 							= str(opportunity["CurrencyIsoCode"])
    Quote.GetCustomField("Customer Segmentation").Content               = str(opportunity["Customer_Segmentation__c"])
    #Quote.GetCustomField("Language").Visible = False if str(opportunity["Booking_Country_Name__c"]) == '' else True
    if str(opportunity["Booking_Country_Name__c"]) == '':
        Quote.GetCustomField("Language").Visible = False
    else:
        Quote.GetCustomField("Language").Visible = True
        if Quote.GetCustomField("Language").Content == '': #GS_SetDefaultLanguage 
            query = SqlHelper.GetFirst("select Default_Language from COUNTRY_LANGUAGE_MAPPING(nolock) where country='{}'".format(str(opportunity["Booking_Country_Name__c"])))
            Quote.GetCustomField("Language").Content = query.Default_Language if query else ''
    Opportunity=Quote.GetCustomField("Opportunity Type").Content
    if Quote.GetCustomField("Booking LOB").Content in ('PMC','LSS') and Quote.OrderStatus.Name == 'Preparing' and str(opportunity["Type"]) not in ("Contract New", "Contract Renewal","Project"):
        Quote.GetCustomField("SoldToId").Content = str(opportunity["Sold_To__c"]) if str(opportunity["Sold_To__c"]) not in ('None') else ''
    #if Quote.GetCustomField("Booking LOB").Content == 'PMC' or (Quote.GetCustomField("Booking LOB").Content=='LSS' and Quote.GetCustomField("Quote Type").Content=='Parts and Spot'):
    #	Quote.GetCustomField("SoldToId").Content = str(opportunity["Sold_To__c"])
    #Log.Info("=SoldTo=111=>"+str(opportunity["Sold_To__c"]))
    if Quote.OrderStatus.Name == 'Preparing': #GS_ResetPrimaryFlag
        Quote.GetCustomField('IsPrimary').Content = '' 
    if str(opportunity["Type"]) in ("Contract New", "Contract Renewal") and Quote.OrderStatus.Name == 'Preparing':
        ScriptExecutor.ExecuteGlobal('GS_SC_SFDC_RoleDetails')
        if str(opportunity["Type"]) in ("Contract Renewal"):
            ScriptExecutor.ExecuteGlobal('GS_SC_Contract_Renewal_FieldsMapping')
    Log.Info("CPQ_SF_OpportunityMapping222 " +str(Quote.GetCustomField("Quote Type").Content))