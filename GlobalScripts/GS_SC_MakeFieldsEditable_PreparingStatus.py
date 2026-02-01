Contract = ['Contract New','Contract Renewal']
if Quote.GetCustomField('Quote Type').Content in Contract:
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
    #Quote.GetCustomField("SC_CF_CURRENCY").Editable = True
    #Quote.GetCustomField("SC_CF_EXCHANGE_RATE").Editable = True