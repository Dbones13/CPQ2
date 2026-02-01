if Quote:
    Product.Attr('PreviousQuoteCStartDate_EnabledServices').AssignValue(Quote.GetCustomField('EGAP_Contract_Start_Date').Content)
    Product.Attr('PreviousQuoteCEndDate_EnabledServices').AssignValue(Quote.GetCustomField('EGAP_Contract_End_Date').Content)
    Product.Attr('ContractStartDate_EnabledService').AssignValue(Quote.GetCustomField('EGAP_Contract_Start_Date').Content)
    Product.Attr('ContractEndDate_EnabledService').AssignValue(Quote.GetCustomField('EGAP_Contract_End_Date').Content)