if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
    import datetime
    from GS_GetOpportunityDetails import GetOpportunityDetails
    current_year = datetime.datetime.now().year
    Product.Attr('Project_Execution_Year').SelectDisplayValue(str(current_year))
    langremovelist = ["German"]
    Product.Attr('Sell Price Strategy').SelectDisplayValue('Market Price')
    Product.Attr('Sell Price Strategy').SelectValue('Market Price')
    lang = Quote.GetCustomField("R2Q_PRJT_Proposal Language").Content
    Product.Attributes.GetByName('R2Q_PRJT_Proposal Language').AssignValue('English')
    Product.Attr('R2Q_PRJT_Proposal Language').SelectDisplayValue('English')
    Product.DisallowAttrValues('R2Q_PRJT_Proposal Language', *langremovelist)
    Log.Info("Migration lang = "+ str(lang))
    if lang != '' and lang != Product.Attr('R2Q_PRJT_Proposal Language').GetValue():
        Product.Attributes.GetByName('R2Q_PRJT_Proposal Language').AssignValue(lang)
        Product.Attr('R2Q_PRJT_Proposal Language').SelectDisplayValue(lang)
    GetOpportunityDetails(Quote,TagParserQuote,Session)
    #Product.Attr('R2QRequest').AssignValue('Yes')
    #Product.Attr('R2Q_QuoteNumber').AssignValue(str(Quote.CompositeNumber))