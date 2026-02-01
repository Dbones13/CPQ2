if Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content.lower() =='true' and (Quote.GetCustomField('EGAP_Contract_Start_Date').Content=='')  and (Quote.GetCustomField('EGAP_Contract_End_Date').Content==''):
    Product.Attr('SC_Contract_StartDate').AssignValue(Quote.GetCustomField('SC_CF_CURANNDELSTDT').Content)
    Product.Attr('SC_Contract_EndDate').AssignValue(Quote.GetCustomField('SC_CF_CURANNDELENDT').Content)
else:
    Product.Attr('SC_Contract_StartDate').AssignValue(Quote.GetCustomField('EGAP_Contract_Start_Date').Content)
    Product.Attr('SC_Contract_EndDate').AssignValue(Quote.GetCustomField('EGAP_Contract_End_Date').Content)
Product.Attr('SC_ItemEditFlag').AssignValue('000')
Quote.CustomFields.AssignValue('SC_CF_RENEWAL_FLAG',"0")