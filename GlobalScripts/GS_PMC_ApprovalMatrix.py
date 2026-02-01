from GS_PMCMatrixNameUtil import PMC_MatrixName,PMC_MaxApprovalLogic

def PMC_Approval(Quote, UserPersonalizationHelper, TagParserQuote):
    LOB = "PMC"
    LimitType = "Discount"
    BookingCountry = ""
    TSP = UserPersonalizationHelper.ConvertToNumber(Quote.GetCustomField("Total Sell Price").Content)
    #TDP = UserPersonalizationHelper.ConvertToNumber(Quote.GetCustomField("Total Discount Percent").Content)
    
    # CXCPQ-80277 --- Start
    ListPrice_Discount_check = False
    for item in Quote.Items:
        if item['QI_Additional_Discount_Percent'].Value > 0:
            ListPrice_Discount_check = True
            break

    QLP = float(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_List_Price) *>"))
    QSP = float(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_Sell_Price) *>"))
    QSP = QSP - float(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, GAS_ETO_Price) *>"))
    if QLP > 0 and ListPrice_Discount_check :
        TDP = UserPersonalizationHelper.ConvertToNumber(str(((QLP - QSP) / QLP) * 100))
    else:
        TDP = 0
    # CXCPQ-80277 --- END

    exchangeRate = Quote.GetCustomField("Exchange Rate").Content
    TSP_USD = TSP / float(exchangeRate)

    MatrixName = PMC_MatrixName(Quote)

# Adding logic to update the EGAP Highest Approval Level for the Quote ----> H541049 (start)
    if MatrixName:
        PMCApprovalMatrixName = MatrixName.PMCMatrixName
        MatrixApprovalLevel = ''
        if TDP > 0.01:
            if (Quote.GetCustomField("Booking Country").Content).lower() == "india":
                BookingCountry = 'india'
                SqlQuery2 = "SELECT ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LOB = '{0}' AND LimitType = '{1}' AND BookingCountry = '{2}' AND PMCMatrixName = '{3}' AND CAST(MinimumSellPrice as int) <= {4} AND CAST(MaximumSellPrice as int) > {4} AND CAST(MinimumLimit as float) < {5} AND CAST(MaximumLimit as float) >= {5}".format(LOB,LimitType,BookingCountry,PMCApprovalMatrixName,TSP_USD,TDP)
            else:
                BookingCountry = ''
                SqlQuery2 = "SELECT ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LOB = '{0}' AND LimitType = '{1}' AND (BookingCountry = '{2}' OR BookingCountry Is null) AND PMCMatrixName = '{3}' AND CAST(MinimumSellPrice as int) <= {4} AND CAST(MaximumSellPrice as int) > {4} AND CAST(MinimumLimit as float) < {5} AND CAST(MaximumLimit as float) >= {5}".format(LOB,LimitType,BookingCountry,PMCApprovalMatrixName,TSP_USD,TDP)
        else:
            if (Quote.GetCustomField("Booking Country").Content).lower() == "india":
                BookingCountry = 'india'
                SqlQuery2 = "SELECT ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LOB = '{0}' AND LimitType = '{1}' AND BookingCountry = '{2}' AND PMCMatrixName = '{3}' AND CAST(MinimumSellPrice as int) <= {4} AND CAST(MaximumSellPrice as int) > {4} AND CAST(MinimumLimit as float) = {5}".format(LOB,LimitType,BookingCountry,PMCApprovalMatrixName,TSP_USD,TDP)
            else:
                BookingCountry = ''
                SqlQuery2 = "SELECT ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LOB = '{0}' AND LimitType = '{1}' AND (BookingCountry = '{2}' OR BookingCountry Is null) AND PMCMatrixName = '{3}' AND CAST(MinimumSellPrice as int) <= {4} AND CAST(MaximumSellPrice as int) > {4} AND CAST(MinimumLimit as float) = {5}".format(LOB,LimitType,BookingCountry,PMCApprovalMatrixName,TSP_USD,TDP)

        MatrixApprovalLevel_query = SqlHelper.GetFirst(SqlQuery2)
        if MatrixApprovalLevel_query:
            MatrixApprovalLevel = MatrixApprovalLevel_query.ApprovalLevel

        QuoteApprovalLevel = '0'

        Quote.GetCustomField("CF_MaxApprovalLevel").Content = ''
        Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content = ''
        Quote.GetCustomField("IsApprovalNotRequired").Content = '0'
        if MatrixApprovalLevel == '':
            Quote.GetCustomField("CF_MaxApprovalLevel").Content = ''
            Quote.GetCustomField("IsApprovalNotRequired").Content = '1'
        elif MatrixApprovalLevel != "NA":
            QuoteApprovalLevel = PMC_MaxApprovalLogic(Quote,TSP_USD,MatrixApprovalLevel,QuoteApprovalLevel)
            Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content = str(QuoteApprovalLevel)
            Quote.GetCustomField("CF_MaxApprovalLevel").Content = str(QuoteApprovalLevel)
        else:
            Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content = 'NA'
            Quote.GetCustomField("CF_MaxApprovalLevel").Content = 'NA'
            Quote.GetCustomField("IsApprovalNotRequired").Content = '1' #----> H541049 (end)