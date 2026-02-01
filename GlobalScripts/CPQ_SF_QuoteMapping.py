from CPQ_SF_FunctionModules import strip_html_tags
from CPQ_SF_PriceBookMapping import CL_PriceBookMapping
from GS_SC_GetQuoteData import CL_QuoteHandler
from CF_UTILS import CF_CONSTANTS, get_custom_field_value, split_after_comma
###############################################################################################
# Function for Quote integration mapping
###############################################################################################
def quote_integration_mapping(Quote, TagParserQuote, visitor):

    salesforceQuote = dict()

    # Approval Request (to clarify)
    EGAP_Proposal_Type = TagParserQuote.ParseString("[EQ](<*CTX( Quote.CustomField(EGAP_Proposal_Type) )*>,Booking)")
    quoteType=TagParserQuote.ParseString("<*CTX( Quote.CustomField(Quote Type) )*>")
    BookingLOB=TagParserQuote.ParseString("<*CTX( Quote.CustomField(Booking LOB) )*>")
    if BookingLOB =='HCP' and quoteType =='Parts and Spot':
        salesforceQuote["Approval_Req_from_Booking_Gatekeeper__c"] = False
    else:
        if EGAP_Proposal_Type == "0":
            salesforceQuote["Approval_Req_from_Booking_Gatekeeper__c"] = False
        elif EGAP_Proposal_Type == "1":
            salesforceQuote["Approval_Req_from_Booking_Gatekeeper__c"] = True
    # Booking Revision
    salesforceQuote["Booking_Revision__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Booking Revision) )*>")
    # Cash Flow Quality
    salesforceQuote["Cash_Flow_Quality__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Cash_Flow_Quality) )*>")
    # Contact Id
    salesforceQuote["ContactId"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(ContactId) )*>")
    # Contingency Cost
    #salesforceQuote["Contingency_Costs__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Contigency_Costs_USD) )*>")
    contigency_costs = Quote.GetCustomField("EGAP_Contigency_Costs_USD").Content
    if contigency_costs != "":
        salesforceQuote["Contingency_Costs__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Contigency_Costs_USD) )*>")
    # Contact End Date
    Contract_End_date = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Contract_End_Date).Format(yyyy-MM-dd) )*>")
    #if Contract_End_date != "":
        #salesforceQuote["Contract_End_Date__c"] = Contract_End_date
    # Contact Start Date
    Contract_Start_Date = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Contract_Start_Date).Format(yyyy-MM-dd) )*>")
    if Contract_Start_Date != "":
        salesforceQuote["Contract_Start_Date__c"] = Contract_Start_Date
    # Exchange Rate
    salesforceQuote["CPQ_Exchange_Rate__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Exchange Rate) )*>")
    # Quote Currency
    salesforceQuote["CPQ_Quote_Currency__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Currency) )*>")
    # Quote Id
    salesforceQuote["CPQ_Quote_Id__c"] = TagParserQuote.ParseString("<*CTX( Quote.OwnerId )*><*CTX( Quote.CartId )*><*CTX( Quote.Revision.Name )*>")
    #salesforceQuote["CPQ_Quote_Id__c"] = TagParserQuote.ParseString("<*CTX( Quote.CartCompositeNumber )*><*CTX( Quote.Revision.Name )*>")
    # Table Api
    CPQ_Table_Api = TagParserQuote.ParseString("[IF]([NEQ](<*CTX( Quote.CustomField(Quote Type) )*>,Parts and Spot)){true}{false}[ENDIF]")
    if Quote.GetCustomField('Quote Type').Content == 'Parts and Spot' and (Quote.GetCustomField("Booking LOB").Content == 'CCC' or Quote.GetCustomField("Booking LOB").Content == 'HCP'):
        CPQ_Table_Api="true"

    if CPQ_Table_Api == "true":
        salesforceQuote["CPQ_Table_Api__c"] = True
    else:
        salesforceQuote["CPQ_Table_Api__c"] = False
    # CurrencyIsoCode
    salesforceQuote["CurrencyIsoCode"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Currency) )*>")
    # Discount Percent (# no such column on salesforce)
    #salesforceQuote["Discount_Percent__c"] = TagParserQuote.ParseString("<*CTX( Quote.Total.AverageProductDiscountPercent.DefaultDecimal )*>")
    # Discount Request Reason
    salesforceQuote["Discount_Request_Reason__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Discount Request Reason) )*>")
    # CXCPQ-73619 - Start
    if TagParserQuote.ParseString("<*CTX( Quote.CustomField(Booking LOB) )*>") == 'PMC':
        QLP = float(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_List_Price) *>"))
        QSP = float(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_Sell_Price) *>"))
        if QLP == 0:
            salesforceQuote["Discount_Requested__c"] = str(0.00)
        else:
            salesforceQuote["Discount_Requested__c"] = str(round((((QLP - QSP) / QLP) * 100), 2)) # CXCPQ-73619 - end
    else:
        salesforceQuote["Discount_Requested__c"] = TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_Discount_Percent) *>")
    # Expiration Date
    salesforceQuote["ExpirationDate"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Quote Expiration Date).Format(yyyy-MM-dd) )*>")
    # Highest Approval Level
    salesforceQuote["Highest_Approval_Level__c"] = TagParserQuote.ParseString("[IF]([NEQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects)){<*CTX( Quote.CustomField(CF_MaxApprovalLevel) )*>}{<*CTX( Quote.CustomField(EGAP_Highest_Approval_Level_for_the_Quote) )*>}[ENDIF]")
    # Is Active
    Is_Active = TagParserQuote.ParseString("[IF](<*CTX( Quote.ActiveRevision )*>){true}{false}[ENDIF]")
    if Is_Active == "true":
        salesforceQuote["Is_Active__c"] = True
    else:
        salesforceQuote["Is_Active__c"] = False
    # Is Currency Changed
    is_cur_changed = TagParserQuote.ParseString("[NEQ](<*CTX( Quote.CustomField(Currency) )*>,<*CTX( Quote.CustomField(CF_NewCurrency) )*>)")
    if is_cur_changed == "0":
        salesforceQuote["Is_Currency_Changed__c"] = False
    else:
        salesforceQuote["Is_Currency_Changed__c"] = True
    # Is Approved required
    IsApprovalNotRequired = TagParserQuote.ParseString("<*CTX( Quote.CustomField(IsApprovalNotRequired) )*>")
    if IsApprovalNotRequired == "0":
        salesforceQuote["IsApprovalNotRequired__c"] = False
    else:
        salesforceQuote["IsApprovalNotRequired__c"] = True
    # Last Modified By User
    if visitor == True:
        salesforceQuote["Last_Modified_By_User__c"] = TagParserQuote.ParseString("<*CTX( Quote.Owner.Name )*>")
    else:
        salesforceQuote["Last_Modified_By_User__c"] = TagParserQuote.ParseString("<*CTX( Visitor.Name )*>")
    # List Price
    salesforceQuote["List_Price__c"] = TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_List_Price) *>")

    # List Price USD
    salesforceQuote["List_Price_USD__c"] = TagParserQuote.ParseString("<*Eval(<* GetFirstFromQuoteTable( Quote_Details, Quote_List_Price) *>/<*CTX( Quote.CustomField(Exchange Rate) )*>))*>")
    # Lowest Cum CF in any single month
    salesforceQuote["Lowest_Cum_CF_in_any_Single_Month_USD__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Lowest_Cum_CF_in_any_Single_Month_USD) )*>")
    # Max Consecutive Months Negative Cumulative Cash Flows
    salesforceQuote["Max_Consec_Months_Neg_Cum_Cash_Flows__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Max_Consec_Months_Neg_Cum_Cash_Flows) )*>")
    # Months Negative Cumulative Cash Flows
    salesforceQuote["Months_Negative_Cumulative_Cash_Flows__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Months_Negative_Cumulative_Cash_Flows) )*>")
    # MPA Name
    salesforceQuote["MPA_Name__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(MPA) )*>")
    # MPA Pricing Plan Name
    salesforceQuote["MPA_Pricing_Plan_Name__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(MPA Price Plan) )*>")
    # Quote Number
    salesforceQuote["Name"] = TagParserQuote.ParseString("<*CTX( Quote.CartCompositeNumber )*>[IF]([EQ](<*CTX( Quote.Revision.RevisionNumber)*>,0)){}{-<*CTX( Quote.Revision.RevisionNumber)*>}[ENDIF]")
    # Opportunity Id
    OpportunityId = Quote.GetCustomField("CPQ_SF_OPPORTUNITY_ID").Content
    if OpportunityId != "":
        salesforceQuote["OpportunityId"] = OpportunityId
    # Order Type
    salesforceQuote["Order_Type__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Order_Type) )*>")
    # Parent_Firm_Revision__c
    salesforceQuote["Parent_Firm_Revision__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Parent Firm Revision) )*>")
    salesforceQuote["Parent_Quote_number__c"] = TagParserQuote.ParseString("<*CTX( Quote.QuoteNumber )*>") # CXCPQ-111161 New Revision to synced the values.
    #salesforceQuote["Booking_Region__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Booking Country) )*>") # CXCPQ-111161 New Revision to synced the values.
    #salesforceQuote["Booking_Revision__c"] = TagParserQuote.ParseString("<*CTX( Quote.RevisionNumber )*>")
    # Payment Milestones
    #salesforceQuote["Payment_Milestones__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SFDCMAP_Payment_Milstones) )*>")
    # Payment Milestones Category
    # salesforceQuote["Payment_Milestones_Category__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Payment Milestones Category) )*>")
    # Payment Terms
    salesforceQuote["Payment_Terms__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Payment Terms) )*>")
    # Primary Quote (to clarify)
    Primary_Quote = TagParserQuote.ParseString("<*CTX( Quote.CustomField(IsPrimary) )*>")
    salesforceQuote["Primary_Quote__c"] = False
    if Primary_Quote and Quote.OrderStatus.Name != 'Preparing':
        if Primary_Quote == "1":
            salesforceQuote["Primary_Quote__c"] = True
    '''Primary_Quote = TagParserQuote.ParseString("<*CTX( Quote.CustomField(IsPrimary) )*>")
    if Primary_Quote != "":
        if Primary_Quote == "0":
            salesforceQuote["Primary_Quote__c"] = False
        elif Primary_Quote == "1":
            salesforceQuote["Primary_Quote__c"] = True'''
    # Project Duration in Months
    salesforceQuote["Project_Duration_in_Months__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Project_Duration_Months) )*>")
    # Primary Quote
    salesforceQuote["Proposal_Type__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Proposal_Type) )*>")
    # Primary Quote
    #salesforceQuote["Quote_Cart_Comment__c"] = TagParserQuote.ParseString("<*CTX( Quote.Total.CartComment )*>")
    # Quote Comments
    salesforceQuote["Quote_comments__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Quote Comment) )*>")
    # Quote Revision
    salesforceQuote["Quote_Revision__c"] = TagParserQuote.ParseString("<*CTX( Quote.Revision.Name )*>")

    # Record Type Id (to clarify)


    salesforceQuote["RecordTypeId"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Quote Record Type) )*>")
    # Revision number
    #salesforceQuote["Revision_Number__c"] = TagParserQuote.ParseString("<*CTX( Quote.Revision.Name )*>")
    # Risk Analysis Required (to clarify)
    Risk_Analysis_Required = TagParserQuote.ParseString("<*CTX( Quote.CustomField(IS_RandO_AssesmentRequired) )*>")
    if Risk_Analysis_Required != "":
        if Risk_Analysis_Required == "0":
            salesforceQuote["Risk_Analysis_Required__c"] = False
        elif Risk_Analysis_Required == "1":
            salesforceQuote["Risk_Analysis_Required__c"] = True
    # RQUP Number
    salesforceQuote["RQUP_Number__c"] = TagParserQuote.ParseString("<*CTX(Quote.CustomField(EGAP_RAFR1_RQUP_Number))*>")
    # ETR Number
    EGAP_CFR4_Ques = Quote.GetCustomField("EGAP_CFR4_Ques").Content
    if Quote.GetCustomField("Quote Type").Content == 'Projects':
        salesforceQuote["ETR_Number__c"] = TagParserQuote.ParseString("<*CTX(Quote.CustomField(EGAP_ETR_Number))*>") if EGAP_CFR4_Ques == 'Yes' else ''
    # Profit Center
    if Quote.OrderStatus.Name in ('Accepted by Customer' , 'Pending Project Creation' , 'Project Created' , 'Pending Order Confirmation' ,'Booked') and Quote.GetCustomField("Quote Type").Content in ('Projects' , 'Parts and Spot'):
        salesforceQuote["Profit_Center__c"] = Quote.GetCustomField('ProfitCentre').Content.Split(',')[0] #TagParserQuote.ParseString("<*CTX(Quote.CustomField(ProfitCentre))*>")
    if Quote.OrderStatus.Name == 'Booked' and Quote.GetCustomField("Quote Type").Content == 'Projects' and Quote.GetCustomField("EGAP_Proposal_Type").Content == 'Booking':
        salesforceQuote["Manually_Booked__c"] = True if Quote.GetCustomField("CF_Manual_Booking").Content == 'True' else False
        salesforceQuote["SAP_Project_Id__c"] = TagParserQuote.ParseString("<*CTX(Quote.CustomField(CF_ProjectId))*>")
    # Sell Price--- Updated the condition for R2Q
    salesforceQuote["Sell_Price__c"] = TagParserQuote.ParseString("[IF]([NEQ](<*CTX( Quote.CustomField(Booking LOB) )*>,LSS)){<* GetFirstFromQuoteTable( Quote_Details, Quote_Sell_Price) *>}{<* GetFirstFromQuoteTable( Quote_Details, Total_Sell_Price_incl_appl_Fees_) *>}[ENDIF]")
    #salesforceQuote["Sell_Price__c"] = TagParserQuote.ParseString("[IF]([EQ]([IF]([NEQ](<*CTX( Quote.CustomField(Booking LOB) )*>,LSS)){<* GetFirstFromQuoteTable( Quote_Details, Quote_Sell_Price) *>}{<* GetFirstFromQuoteTable( Quote_Details, Total_Sell_Price_incl_appl_Fees_) *>}[ENDIF],0)){<*CTX( Quote.CustomField(Total_Sell_Price_Updated) )*>}{[IF]([NEQ](<*CTX( Quote.CustomField(Booking LOB) )*>,LSS)){<* GetFirstFromQuoteTable( Quote_Details, Quote_Sell_Price) *>}{<* GetFirstFromQuoteTable( Quote_Details, Total_Sell_Price_incl_appl_Fees_) *>}[ENDIF]}[ENDIF]")
    # Sell Price USD
    salesforceQuote["Sell_Price_USD__c"] = TagParserQuote.ParseString("<*Eval([IF]([NEQ](<*CTX( Quote.CustomField(Booking LOB) )*>,LSS)){<* GetFirstFromQuoteTable( Quote_Details, Quote_Sell_Price) *>}{<* GetFirstFromQuoteTable( Quote_Details, Total_Sell_Price_incl_appl_Fees_) *>}[ENDIF]/ <*CTX( Quote.CustomField(Exchange Rate) )*>)*>")
    exchangeRate = Quote.GetCustomField('Exchange Rate').Content if Quote.GetCustomField('Exchange Rate').Content.strip() !='' else 1.0
    quoteDetails = Quote.QuoteTables["Quote_Details"]
    if Quote.GetCustomField('isR2QRequest').Content == 'Yes' and quoteDetails.Rows.Count:
        row = quoteDetails.Rows[0]
        sellPrice1 = row["Quote_Sell_Price"] if Quote.GetCustomField("Booking LOB").Content != 'LSS' else row["Total_Sell_Price_incl_appl_Fees_"]
        sellPrice2 = row["Walk_away_Sales_Price"] / float(exchangeRate)
        salesforceQuote["Sell_Price__c"] = sellPrice1
        salesforceQuote["Sell_Price_USD__c"] = sellPrice1 / float(exchangeRate)
        if TagParserQuote.ParseString('<*CTX( Visitor.UserType.Name )*>') != "Estimator NCM":
            salesforceQuote["Regional_Margin__c"] = row["Quote_Regional_Margin_Percent"]
    # Status
    salesforceQuote["Status"] = TagParserQuote.ParseString("<*CTX( Quote.Status.NameDefaultLanguage )*>")
    # Target Price
    salesforceQuote["Target_Price__c"] = TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Target_Sell_Price) *>")
    # Target Price USD
    salesforceQuote["Target_Price_USD__c"] = TagParserQuote.ParseString("<*Eval(<* GetFirstFromQuoteTable( Quote_Details, Target_Sell_Price) *>/<*CTX( Quote.CustomField(Exchange Rate) )*>))*>")
    # CF_R2Q_QuoteRef (Temp Comment : Don't move to production untill below custom field of SFDc & CPQ are created in Prod)
    salesforceQuote["R2Q_Quote_Request_Number__c"] = TagParserQuote.ParseString("<*CTX(Quote.CustomField(CF_R2Q_QuoteRef))*>")
    # CF_Quote_Creation_Process ---Added for R2Q
    salesforceQuote["Quote_Creation_Process__c"] = TagParserQuote.ParseString("[IF]([NEQ](<*CTX( Quote.CustomField(CF_Quote_Creation_Process) )*>,)){<*CTX( Quote.CustomField(CF_Quote_Creation_Process) )*>}{Manually Created}[ENDIF]")
    if TagParserQuote.ParseString("<*CTX( Quote.CustomField(isR2QRequest) )*>") == 'Yes':
        salesforceQuote["IsR2QRequest__c"] =TagParserQuote.ParseString("<*CTX( Quote.CustomField(isR2QRequest) )*>")
        # salesforceQuote["Customer_Budget__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(CustomerBudget) )*>")
        #salesforceQuote["Sell_Price_Strategy__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SellPricestrategy) )*>")
        #salesforceQuote["Project_Type__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(ProductType) )*>")
    # PMC Approval Logic to send 10% Advance Payment message to SFDC Field
    if TagParserQuote.ParseString("<*CTX( Quote.CustomField(Booking LOB) )*>") == 'PMC':
        # PMC Approval Quote Creation Process #----> CXCPQ-69808 H541049 (start)
        salesforceQuote["PMC_Quote_Type__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(PMC Type) )*>")
        salesforceQuote["PMC_Product_Line__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(PMC Product Line) )*>")
        salesforceQuote["PMC_Product_Family__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(PMC Product Family) )*>")
        # salesforceQuote["PMC_Total_Costs__c"] = TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_WTW_Cost) *>")   # CXCPQ-68835
        if Quote.OrderStatus.Name == 'Preparing':
            salesforceQuote["Sold_To__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SoldToId) )*>")
        from GS_PMCMatrixNameUtil import PMC_MilestoneMessage
        salesforceQuote["PMC_10Percent_Advance_Payment__c"] = PMC_MilestoneMessage(Quote,UserPersonalizationHelper) #----> H541049 (end)
    if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
        salesforceQuote["Contract_Name__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_CONTRACT_NAME) )*>")
        salesforceQuote["Description"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Description) )*>")
        salesforceQuote["Do_not_send_survey__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Do_not_send_Survey) )*>").lower()
        if TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Do_not_send_Survey) )*>").lower() == 'false':
            salesforceQuote["X1st_Survey_Month__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_1st_Survey_Month) )*>")
            salesforceQuote["X2nd_Survey_Month__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_2nd_Survey_Month) )*>")
        else:
            salesforceQuote["X1st_Survey_Month__c"] = ''
            salesforceQuote["X2nd_Survey_Month__c"] = ''
        salesforceQuote["Velocity_Renewal__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Velocity_Renewal) )*>").lower()
        salesforceQuote["Special_Terms__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Special_Terms) )*>")
        salesforceQuote["Local_Ref__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_LOCAL_REF) )*>")
        salesforceQuote["Service_Contract_Tier__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Service_Contract_Tier) )*>")
        salesforceQuote["Service_Contract_Type__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Service_Contract_Type) )*>")
        salesforceQuote["Callout_Response__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Callout_Response) )*>")
        salesforceQuote["Call_out_Response_Comments__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Callout_Response_Comments) )*>")
        salesforceQuote["Tax_Exemption_Certificate__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_TAX_EXMPT_CERTIFICATE) )*>")
        salesforceQuote["Invoice_Email_Address__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_INVOICE_EMAIL_ADDRESS) )*>")
        salesforceQuote["Invoice_Portal_URL__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Invoice_Portal_URL) )*>")
        salesforceQuote["Financial_Approval_Method__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_FIN_APPROVAL_METHOD) )*>")
        if Contract_Start_Date != "" or Contract_End_date!= "":
            salesforceQuote["Multi_Year_Start_Date__c"] = Contract_Start_Date 
            salesforceQuote["Multi_Year_End_Date__c"] = Contract_End_date
        salesforceQuote["Invoice_Type__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_INVTYPE) )*>")
        salesforceQuote["Invoicing_Frequency__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_INV_FREQUENCY) )*>")
        salesforceQuote["Invoicing_in_Advance__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_INV_IN_ADVANCE) )*>")
        salesforceQuote["Invoicing_Day__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_INV_DAY) )*>")
        salesforceQuote["Invoice_Text__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_invoice_Text) )*>")
        salesforceQuote["Invoicing_Comments__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_INVOICING_COMMENTS) )*>")
        salesforceQuote["Profit_Center__c"] = Quote.GetCustomField('ProfitCentre').Content.Split(',')[0] #TagParserQuote.ParseString("<*CTX( Quote.CustomField(ProfitCentre) )*>")
        salesforceQuote["Purchase_Order_No__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(PONumber) )*>")
        salesforceQuote["Sales_Org__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Sales Area) )*>")
        salesforceQuote["Single_line_invoice__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_SINGLE_LINE_INV) )*>")
        salesforceQuote["Threshold__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Threshold) )*>")
        #salesforceQuote["Ship_To__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(ShipToId) )*>")
        #salesforceQuote["Bill_To__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(BillToId) )*>")
        #salesforceQuote["Sold_To__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SoldToId) )*>")
        salesforceQuote["Contract_Start_Date__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_CURANNDELSTDT).Format(yyyy-MM-dd) )*>")
        salesforceQuote["Contract_End_Date__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_CURANNDELENDT).Format(yyyy-MM-dd) )*>")
        salesforceQuote["Proposal_Type__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Proposal_Type) )*>")
        salesforceQuote["Pricing_Agreement_Type__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_AGREEMENT_TYPE) )*>")
        salesforceQuote["Quote_Comments__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Quote Comment) )*>")
        #salesforceQuote["Quote_Revision__c"] = Quote.RevisionNumber
        salesforceQuote["Contract_Manager__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_CONTRACT_MANAGER) )*>")
        salesforceQuote["Auto_Escalate__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Auto_Escalate) )*>").lower()
        salesforceQuote["Auto_Renewal__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Auto_Renewal) )*>").lower()
        salesforceQuote["Order_Reason__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_ORDER_REASON) )*>")
        salesforceQuote["Invoice_block_needed__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_INVOICE_BLOCK_NEEDED) )*>")
        salesforceQuote["Current_Annual_Deliverable_Start_Date__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_CURANNDELSTDT).Format(yyyy-MM-dd) )*>")
        salesforceQuote["Current_Annual_Deliverable_End_Date__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_CURANNDELENDT).Format(yyyy-MM-dd) )*>")
        salesforceQuote["Contract_Duration__c"] = Quote.GetCustomField('SC_CF_CONTRACTDURYR').Content.Replace(' years', '')
        salesforceQuote["Entity__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Honeywell Entity Name) )*>")
        salesforceQuote["Language__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Language) )*>")
        salesforceQuote["Sub_LOB__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Sub LOB) )*>")
        salesforceQuote["Proposal_Validity__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Proposal Validity) )*>")
        salesforceQuote["Highest_Approval_Level__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Highest_Approval_Level_for_the_Quote) )*>")
        #salesforceQuote["Regional_Margin__c"] = TagParserQuote.ParseString("<*CTX( Quote.CurrentItem.CustomField(QI_SC_Margin_Percent) )*>").replace(",", "")
        salesforceQuote["Service_Contract_content__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_Service_Contract_Content) )*>")
        salesforceQuote["Prior_Year_Exchange__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_PRVYR_EXCH_RATE) )*>")
        salesforceQuote["Sell_Price__c"] = '{0:.2f}'.format(round(UserPersonalizationHelper.ConvertToNumber(TagParserQuote.ParseString("[IF]([NEQ](<*CTX( Quote.CustomField(Booking LOB) )*>,LSS)){<* GetFirstFromQuoteTable( Quote_Details, Quote_Sell_Price) *>}{<* GetFirstFromQuoteTable( Quote_Details, Total_Sell_Price_incl_appl_Fees_) *>}[ENDIF]")),2)).replace(",", "")

        salesforceQuote["Sell_Price_USD__c"] = '{0:.2f}'.format(round(UserPersonalizationHelper.ConvertToNumber(TagParserQuote.ParseString("<*Eval([IF]([NEQ](<*CTX( Quote.CustomField(Booking LOB) )*>,LSS)){<* GetFirstFromQuoteTable( Quote_Details, Quote_Sell_Price) *>}{<* GetFirstFromQuoteTable( Quote_Details, Total_Sell_Price_incl_appl_Fees_) *>}[ENDIF]/ <*CTX( Quote.CustomField(SC_CF_EXCHANGE_RATE) )*>)*>")),2)).replace(",", "")
        salesforceQuote["Target_Price__c"] = '{0:.2f}'.format(round(UserPersonalizationHelper.ConvertToNumber(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Target_Sell_Price) *>")),2)).replace(",", "")
        salesforceQuote["Target_Price_USD__c"] = '{0:.2f}'.format(round(UserPersonalizationHelper.ConvertToNumber(TagParserQuote.ParseString("<*Eval(<* GetFirstFromQuoteTable( Quote_Details, Target_Sell_Price) *>/<*CTX( Quote.CustomField(SC_CF_EXCHANGE_RATE) )*>))*>")),2)).replace(",", "")
        salesforceQuote["List_Price__c"] = '{0:.2f}'.format(round(UserPersonalizationHelper.ConvertToNumber(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_List_Price) *>")),2)).replace(",", "")

        salesforceQuote["List_Price_USD__c"] = '{0:.2f}'.format(round(UserPersonalizationHelper.ConvertToNumber(TagParserQuote.ParseString("<*Eval(<* GetFirstFromQuoteTable( Quote_Details, Quote_List_Price) *>/<*CTX( Quote.CustomField(SC_CF_EXCHANGE_RATE) )*>))*>")),2)).replace(",", "")
        salesforceQuote["Pricebook2Id"] = CL_PriceBookMapping.SERVICE_PRICE_BOOK_ID if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal') else CL_PriceBookMapping.STANDARD_PRICE_BOOK_ID
        salesforceQuote["USD_Exchange_Rate__c"] = float(Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content) if Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content else 1
        salesforceQuote["Discount_Requested__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(Total Discount Percent(CW)) )*>")
        if Quote.OrderStatus.Name == "Accepted by Customer" and Quote.GetCustomField("Sales Area").Content == "736P" and str(Quote.GetCustomField("Booking Country").Content).upper() == "INDIA":
			custom_field_name = CF_CONSTANTS.get("QUOTE_LEVEL_PLANT_FIELD")
			full_plant_value = get_custom_field_value(Quote, custom_field_name)
			plant_code,plant_name = split_after_comma(full_plant_value)
			if plant_code is not None:
				salesforceQuote["SC_Plant__c"] = str(plant_code)
				salesforceQuote["SC_Plant_Name__c"] = str(plant_name)
        if Quote.GetCustomField('Quote Type').Content == 'Contract Renewal':
            salesforceQuote["ERP_Reference__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_ERPREFNO) )*>")
            salesforceQuote["Is_Extension__c"] = TagParserQuote.ParseString("<*CTX( Quote.CustomField(SC_CF_IS_CONTRACT_EXTENSION) )*>").lower()
        quoteNumber = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
        if quoteNumber != '' and Quote.GetCustomField('Quote Type').Content == 'Contract Renewal':
            QuoteHandler = CL_QuoteHandler(quoteNumber)
            PreQuoteInfo = QuoteHandler.GetFieldValues(['EGAP_Cross_Margin','Honeywell List Price','Honeywell List Price(USD)','Total Sell Price(CW)','Total Sell Price(USD)',])
            for x in PreQuoteInfo:
                if x.Name == 'EGAP_Cross_Margin':
                    salesforceQuote["Previous_Year_Margin__c"] = round(float(x.Value)*100,2)
                elif x.Name == 'Honeywell List Price':
                    salesforceQuote["Previous_Year_List_Price__c"] = x.Value.replace(",", "")[4:]
                elif x.Name == 'Honeywell List Price(USD)':
                    salesforceQuote["Previous_Year_List_Price_USD__c"] = x.Value.replace(",", "").replace("USD", "")
                elif x.Name == 'Total Sell Price(CW)':
                    salesforceQuote["Previous_year_Sell_Price__c"] = x.Value.replace(",", "")[4:]
                else:
                    salesforceQuote["Previous_Year_Sell_Price_USD__c"] = x.Value.replace(",", "").replace("USD", "")

    return salesforceQuote