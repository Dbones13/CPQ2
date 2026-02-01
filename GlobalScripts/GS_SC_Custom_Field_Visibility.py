'''
Nilesh - removed Opportunity info and commercial tab event - also removed local refer CF change event - 01102024

'''
def GS_SC_Custom_Field_Visibility(Quote,User):
    Country = Quote.GetCustomField('Opportunity Tab Booking Country').Content
    quoteCurrency = Quote.SelectedMarket.CurrencyCode
    currency_query = SqlHelper.GetFirst("select Currency from CT_SC_LABOR_RESOURCETYPE where Country = '{}' ".format(Country))
    currency = currency_query.Currency
    quote=Quote
    def getCF(quote , cfName):
        Trace.Write(cfName)
        return quote.GetCustomField(cfName)

    def getCFValue(quote , cfName):
        return getCF(quote,cfName).Content

    def hideCF(customField):
        customField.Visible = False

    def showCF(customField):
        customField.Visible = True

    def setCFReadonly(customField):
        customField.Editable = False

    Quote_Type = getCFValue(Quote,'Quote Type')
    #--------------------------------------------------------------------------------
    attValues = Quote.GetCustomField('SC_CF_FIN_APPROVAL_METHOD').AttributeValues
    if Quote_Type == "Contract New":
        hideCF(getCF(Quote,'SC_CF_PRVYR_EXCH_RATE'))
        for value in attValues:
            if value.DisplayValue == "SEA":
                value.Allowed = False
    #-------------------------------------------------------------------------
    attrValues = Quote.GetCustomField('Proposal Validity').AttributeValues
    if Quote_Type != "Contract Renewal":
        for value in attrValues:
            if value.DisplayValue == "None":
                value.Allowed = False

    #-------------------------------------------------------------------------------
    Contracts = ['Contract New','Contract Renewal']
    payment_values = Quote.GetCustomField('Payment Terms').AttributeValues
    payment_terms_Values = ['30','45','60','90','0','15','75','120','150','COD']

    if Quote_Type in Contracts and getCFValue(Quote , "Booking LOB") == "LSS":
        
        getCF(Quote , "ProfitCentre").Rank = 10
        getCF(Quote , "Account Contact Name").Rank = 28
        getCF(Quote , "Account Contact Email").Rank = 25
        getCF(Quote , "Partner Account Contact Email").Rank = 27
        getCF(Quote , "Partner Account Contact Name").Rank = 30
        getCF(Quote , "Pole").Rank = 13
        getCF(Quote , "EGAP_Contract_Start_Date").Rank = 40
        getCF(Quote , "EGAP_Contract_End_Date").Rank = 41
        getCF(Quote , "EGAP_Project_Duration_Months").Rank = 51
        getCF(Quote , "Language").Rank = 35
        getCF(Quote , "EGAP_Proposal_Type").Rank = 10
        
        R= 0
        Opp_fields = ['Opportunity Number','CPQ_SF_OPPORTUNITY_NAME','EstimatedSellPrice','Opportunity Type','Sales Stage','Opportunity Category','Booking LOB','Sub LOB','Opp Prod Desc','Close Date','Business Model','CompetitorCount','Primary_Competitor']
        for f in Opp_fields:
            R+=10
            Quote.GetCustomField(f).Rank = R

        getCF(Quote , "EGAP_Contract_Start_Date").Label = "Multi Year Start Date"
        getCF(Quote,"EGAP_Contract_Start_Date").Label = "Multi Year Start Date"
        getCF(Quote,"EGAP_Contract_End_Date").Label = "Multi Year End Date"
        getCF(Quote,"EGAP_Project_Duration_Months").Label = "Contract Duration(Months) #N# Multi Year End Date -Multi Year Start date (In Months)"

        Aggrement_Type = 'MPA' if getCFValue(Quote,'SC_CF_AGREEMENT_TYPE') == 'None' else getCFValue(Quote,'SC_CF_AGREEMENT_TYPE')
        getCF(Quote,"MPA Commercial").Label = Aggrement_Type
        getCF(Quote,"MPA Price Plan").Label = Aggrement_Type + " Price Plan"
        getCF(Quote,"MPA Customer Reference No").Label = Aggrement_Type + " Customer Reference No"
        getCF(Quote,"MPA Honeywell Ref").Label = Aggrement_Type + " Honeywell Ref"

        if getCFValue(Quote , "Change Proposal Type") != '1':
            hideCF(getCF(Quote,"Revised proposal type"))
        else:
            showCF(getCF(Quote,"Revised proposal type"))

        for pv in  payment_values:
            pv.Allowed = True
            if pv.DisplayValue not in payment_terms_Values:
                pv.Allowed = False

        if getCFValue(Quote , "Change Proposal Type") != '1':
            hideCF(getCF(Quote,"Revised proposal type"))

        getCF(Quote,'EstimatedSellPrice').Label = 'EstSellPrice' +' '+ getCFValue(Quote,'SC_CF_CURRENCY')
        table_exchage_rate = SqlHelper.GetFirst("SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = 'USD' AND To_Currency = '"+str(Quote.GetCustomField('SC_CF_CURRENCY').Content)+"'").Exchange_Rate
        if User.BelongsToPermissionGroup('ExchangeRate_PermissionGroup') and Quote.OrderStatus.Name== "Preparing":
            Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Editable=True
            Quote.GetCustomField('SC_CF_EXCHANGE_RATE_Editable_Value').Content = Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content
        elif User.BelongsToPermissionGroup('ExchangeRate_PermissionGroup') and Quote.OrderStatus.Name != "Preparing":
            Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content = Quote.GetCustomField('SC_CF_EXCHANGE_RATE_Editable_Value').Content
        elif Quote.OrderStatus.Name== "Preparing" and (Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content == table_exchage_rate or not(Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content)):
            Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content = table_exchage_rate
        
        #Nilesh added code to set value to Exchange rate as it is failing Cash flow
        Quote.GetCustomField('Exchange Rate').Content = Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content
        if Quote.OrderStatus.Name== "Preparing":
            Quote.GetCustomField('EGAP_Contract_Start_Date').Editable = True
            Quote.GetCustomField('EGAP_Contract_End_Date').Editable = True
            Quote.GetCustomField('EGAP_Proposal_Type').Editable = True
            Quote.GetCustomField("SC_CF_LOCAL_REF").Editable = True
            Quote.GetCustomField("Language").Editable = True
            Quote.GetCustomField('SC_CF_CONTRACT_NAME').Editable = True
            Quote.GetCustomField('SC_CF_AGREEMENT_TYPE').Editable = True
            Quote.GetCustomField('Quote Comment').Editable = True
            Quote.GetCustomField("SC_CF_CURANNDELSTDT").Editable = True
            Quote.GetCustomField("SC_CF_CURANNDELENDT").Editable = True
    #---------------------------------------------------------- ---------------------
    if Quote_Type == "Contract Renewal":
        hideCF(getCF(Quote,'Customer Requested Date'))
        if Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content.lower() == 'true':
            Quote.GetCustomField("EGAP_Contract_Start_Date").Editable = False
            Quote.GetCustomField("EGAP_Contract_End_Date").Editable = False
        if getCFValue(Quote,"SC_CF_FIN_APPROVAL_METHOD") == '':
            Quote.GetCustomField('SC_CF_FIN_APPROVAL_METHOD').Content = 'SEA'