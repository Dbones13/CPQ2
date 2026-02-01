import datetime
from CPQ_SF_SC_Modules import CL_SC_Modules
from GS_SC_GetQuoteData import CL_QuoteHandler
from GS_Curr_ExchRate_Mod import fn_get_curr_exchrate
from GS_EGAPCalculateProjectDuration_Module import CalculateProjectDuration

class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None,Session)
is_extension = Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content
Opp_ID = Quote.GetCustomField("Opportunity Number").Content
#is_extension = 'False'
WhereCond = "Opportunity_No__c" if is_extension == 'True' else "Opportunity_No_renewal__c"
resp = class_contact_modules.get_ContractRenewalQuote_Data(Opp_ID,WhereCond)
recordList = resp["records"]
systemID = "Service_Contract_Products_cpq"

serviceContractFlag = True
for item in Quote.MainItems:
    if item.ProductName == "Service Contract Products":
        serviceContractFlag = False
        break

local_ref = Quote.GetCustomField("SC_CF_LOCAL_REF").Content
erp_no = Quote.GetCustomField("SC_CF_ERPREFNO").Content
contract_name = Quote.GetCustomField("SC_CF_CONTRACT_NAME").Content
agreement_type = Quote.GetCustomField("SC_CF_AGREEMENT_TYPE").Content
curr_stdt = Quote.GetCustomField("SC_CF_CURANNDELSTDT").Content
curr_eddt = Quote.GetCustomField("SC_CF_CURANNDELENDT").Content
multi_stdt = Quote.GetCustomField("EGAP_Contract_Start_Date").Content
multi_eddt = Quote.GetCustomField("EGAP_Contract_End_Date").Content
start_date = ''
end_date = ''
Quote_Currency = Quote.GetCustomField("SC_CF_CURRENCY").Content

if Quote.GetCustomField("Quote Type").Content == 'Contract Renewal':
    for record in recordList:
        #Quote.GetCustomField("SC_CF_Opportunity_ID").Content = str(record["Id"]) if str(record["Id"]) != '' else ''
        #Quote.GetCustomField("Opportunity Number").Content = str(record["Opportunity_No_renewal__c"]) if str(record["Opportunity_No_renewal__c"]) != '' else ''

        Local_Reference = str(record["Local_Ref__c"]) if str(record["Local_Ref__c"]) !='' else ''
        Quote.GetCustomField("SC_CF_LOCAL_REF").Content = Local_Reference if not local_ref else local_ref

        ERP_Contract_Reference = str(record["ERP_Contract_Reference__c"]) if str(record["ERP_Contract_Reference__c"]) !='' else ''
        Quote.GetCustomField("SC_CF_ERPREFNO").Content = ERP_Contract_Reference if not erp_no else erp_no

        Contract_Name = 'Q-'+str(record["Name"]) if str(record["Name"]) !='' else '' #Added Q- as prefix:CXCPQ-92749
        Quote.GetCustomField("SC_CF_CONTRACT_NAME").Content = Contract_Name if not contract_name else contract_name

        Purchasing_Agreement_Type = str(record["Purchasing_Agreement_Type__c"]) if str(record["Purchasing_Agreement_Type__c"]) !='' else ''
        Quote.GetCustomField("SC_CF_AGREEMENT_TYPE").Content = Purchasing_Agreement_Type if not agreement_type or agreement_type==None  else agreement_type 

        #Service Contract Currency(Prior Currency)
        Prior_Currency = str(record["CurrencyIsoCode"])
        Quote.GetCustomField("SC_CF_Prior_Year_Currency").Content = Prior_Currency if Prior_Currency != '' else ''

        #Parent Quote Number and Link
        QuoteNo = str(record["Renewal_Opportunity__r"]["Previous_Year_CPQ_Quote__c"])
        Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content = QuoteNo if QuoteNo != '' else ''

        #Parent Contract Number and Link
        ContractNumber = str(record["ContractNumber"])
        Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content =  ContractNumber if ContractNumber != '' else ''

        if str(record["EndDate"]) !='':
            d = DateTime.Parse(str(record["EndDate"]))
            start_date = d.AddDays(1)
            if start_date.Year%4 == 0 and start_date.Month in [1,2]:
                if start_date <= DateTime.Parse(str(datetime.date(start_date.Year, 2, 29))):
                    end_date = start_date.AddYears(1) if is_extension == 'False' else start_date.AddMonths(3)
                else:
                    end_date = start_date.AddYears(1) if is_extension == 'False' else start_date.AddMonths(3)
            else:
                end_date = start_date.AddYears(1).AddDays(-1) if is_extension == 'False' else start_date.AddMonths(3).AddDays(-1)

        CURR_ANNDEL_Start_Date = UserPersonalizationHelper.ToUserFormat(start_date) if start_date !='' else ''
        Quote.GetCustomField("SC_CF_CURANNDELSTDT").Content = CURR_ANNDEL_Start_Date if not curr_stdt else curr_stdt

        CURR_ANNDEL_End_Date = UserPersonalizationHelper.ToUserFormat(end_date) if end_date !='' else ''
        Quote.GetCustomField("SC_CF_CURANNDELENDT").Content = CURR_ANNDEL_End_Date if not curr_eddt else curr_eddt

        Multi_Year_Start_Date = UserPersonalizationHelper.ToUserFormat(DateTime.Parse(str(record["Multi_Year_Start_Date__c"]))) if str(record["Multi_Year_Start_Date__c"]) !='' else ''
        Multi_Year_End_Date = UserPersonalizationHelper.ToUserFormat(DateTime.Parse(str(record["Multi_Year_End_Date__c"]))) if str(record["Multi_Year_End_Date__c"]) !='' else ''
        SC_CF_ContractEndDate = DateTime.Parse(str(record["Multi_Year_End_Date__c"])) if str(record["Multi_Year_End_Date__c"]) !='' else None
        Quote.SetGlobal('SC_CF_ContractEndDate', str(record["Multi_Year_End_Date__c"]))

        if is_extension == 'True' and ((CURR_ANNDEL_End_Date and SC_CF_ContractEndDate and UserPersonalizationHelper.CovertToDate(CURR_ANNDEL_End_Date) > SC_CF_ContractEndDate) or SC_CF_ContractEndDate==None):
        	Quote.GetCustomField("EGAP_Contract_Start_Date").Content = ''
        	Quote.GetCustomField("EGAP_Contract_End_Date").Content = ''
        else:
        	Quote.GetCustomField("EGAP_Contract_Start_Date").Content = Multi_Year_Start_Date if not multi_stdt else multi_stdt
        	Quote.GetCustomField("EGAP_Contract_End_Date").Content = Multi_Year_End_Date if not multi_stdt else multi_eddt
		'''
        if is_extension == 'True':
            Quote.GetCustomField("EGAP_Contract_Start_Date").Editable = False
            Quote.GetCustomField("EGAP_Contract_End_Date").Editable = False
        '''

        Exchange_Rate = fn_get_curr_exchrate(Prior_Currency,Quote_Currency) if Prior_Currency != Quote_Currency else 1
        Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content = str(Exchange_Rate)
        #nilesh-added code -to execute duration calculation in case of contract renewal
        CalculateProjectDuration(TagParserQuote,Quote)
        #CXCPQ-69761 - update renewal quote info from contract new quote
        if Quote.GetCustomField('SC_CF_Invoice_Portal_URL').Content == '':
            if QuoteNo != '':
                QuoteHandler = CL_QuoteHandler(QuoteNo)
                PreQuoteInfo = QuoteHandler.GetFieldValues(['SC_CF_EXCHANGE_RATE', 'SC_CF_Invoice_Portal_URL', 'SC_CF_INVOICE_EMAIL_ADDRESS','EndUse','Incoterms on Sales Order','ProfitCentre','Profit Centre Description','SC_CF_Threshold','SC_CF_Special_Terms','SC_CF_Service_Contract_Tier','SC_CF_Service_Contract_Type','SC_CF_Service_Contract_Content','SC_CF_INVOICING_COMMENTS','SC_CF_invoice_Text','SC_CF_INV_FREQUENCY','SC_CF_INVTYPE','SC_CF_INV_DAY','SC_CF_INV_IN_ADVANCE','SC_CF_HONEYWELL_AFF_ADR','SC_CF_SINGLE_LINE_INV','SC_CF_PRICING_PER_VERSION','SC_CF_PRICING_HEADER_ID','Honeywell Entity Name','Delivery Terms- Additional Info','Proposal Validity','Payment Terms'])
                for x in PreQuoteInfo:
                    CFName = x.Name if x.Name != 'SC_CF_EXCHANGE_RATE' else 'SC_CF_PRVYR_EXCHANGE_RATE'
                    if x.Value:
                        Quote.GetCustomField(CFName).Content = x.Value

    if serviceContractFlag:
        serviceContractProduct = ProductHelper.CreateProduct(systemID)
        serviceContractProduct.AddToQuote()