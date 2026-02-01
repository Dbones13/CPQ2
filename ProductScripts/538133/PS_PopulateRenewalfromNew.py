if Product.Attr('SC_Product_Type').GetValue() == "Renewal":

    ####Parts Management Logic####
    import GS_GetPriceFromCPS
    Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
    Invalid_cont = Product.GetContainerByName("SC_P1P2_Invalid_Parts")
    if Invalid_cont.Rows.Count:
        for row in Invalid_cont.Rows:
            row['PY_Quantity'] = row['Hidden_Quantity']
        Invalid_cont.Calculate()

	holdPercentDict	= {}
	summaryCont = Product.GetContainerByName("SC_P1P2_Parts_List_Summary")
	if summaryCont.Rows.Count:
	    for row in summaryCont.Rows:
		    holdPercentDict[row["Service_Product"]] = row["Holding_Percentage"]

    Model_cont = Product.GetContainerByName("SC_P1P2_Parts_Details")
    partsList = []
    if Model_cont.Rows.Count:
        for row in Model_cont.Rows:
            row['PY_Quantity'] = row['Hidden_Quantity']
            row['PY_UnitPrice'] = str(float(row['Unit_Price']) * Exchange_Rate) if row['Unit_Price'] else '0'
            row['PY_ExtPrice'] = str(float(row['Hidden_ListPrice']) * Exchange_Rate) if row['Hidden_ListPrice'] else '0'
            row['CY_Quantity'] = row['Hidden_Quantity']
            row['BackupRenewalQuantity'] = row['Hidden_Quantity']
            row['Comments'] = "No Scope Change"
            row['Product_Type'] = "Renewal"
            row['PY_HoldingPercentage'] = str(float(holdPercentDict.get(row["Service_Product"],"0"))*0.01)
            row['PY_HoldingFeeListPrice'] = str(float(row['PY_ExtPrice'])*float(row['PY_HoldingPercentage']))
            row.Calculate()
            partsList.append(row['Part_Number'])
        priceDict = GS_GetPriceFromCPS.getPrice(Quote,{},partsList,TagParserQuote,Session)
        for row in Model_cont.Rows:
            row["Unit_Price"] = priceDict[row['Part_Number']] if priceDict.get(row['Part_Number']) else '0'
        Model_cont.Calculate()

    ####Parts Replacement Logic####
    pyListPrice = 0
    pySellPrice = 0
    Trace.Write("PartsUsage-----"+str(Product.Attr('SC_P1P2_PartsUsageMethod').GetValue()))
    if Product.Attr('SC_P1P2_PartsUsageMethod').GetValue() == "1 Year Pricing":
        pyExtPrice = float(Product.Attr('SC_P1P2_Parts_Ext_Price').GetValue()) if Product.Attr('SC_P1P2_Parts_Ext_Price').GetValue() else 0
        Product.Attr('SC_P1P2_PY_Parts_Ext_Price').AssignValue(str(pyExtPrice*Exchange_Rate))
        Product.Attr('SC_P1P2_Parts_Ext_Price').AssignValue('0')
        pyListPrice = float(Product.Attr('SC_P1P2_ListPrice').GetValue()) if Product.Attr('SC_P1P2_ListPrice').GetValue() else 0
        Product.Attr('SC_P1P2_PY_ListPrice').AssignValue(str(pyListPrice*Exchange_Rate))
        Product.Attr('SC_P1P2_ListPrice').AssignValue('0')
        Product.Attr('SC_P1P2_LPDA_PY_ListPrice').AssignValue('0')
        Product.Attr('SC_P1P2_LPDA_PY_SellPrice').AssignValue('0')
        Product.Attr('SC_P1P2_LTYA_PY_ListPrice').AssignValue('0')
    else:
        reference_number = Quote.GetCustomField("SC_CF_PREVIOUS_QUOTE_NO").Content
        query = SqlHelper.GetFirst("Select Product, QuoteDetails from CT_SC_RENEWAL_QUOTE_TABLE where QuoteID = '{}' and Product = '{}'".format(reference_number,"Parts Management"))
        if query is not None:
            quotedetail = eval(query.QuoteDetails)
            if "Year-1|Parts Management|Parts Replacement|Parts Replacement" in quotedetail.keys():
                pyListPrice = quotedetail["Year-1|Parts Management|Parts Replacement|Parts Replacement"]["ListPrice"]
                pySellPrice = quotedetail["Year-1|Parts Management|Parts Replacement|Parts Replacement"]["SellPrice"]
        if Product.Attr('SC_P1P2_PartsUsageMethod').GetValue() == "List Price with Discount Applied":
            Product.Attr('SC_P1P2_LPDA_PY_ListPrice').AssignValue(str(float(pyListPrice)*Exchange_Rate))
            Product.Attr('SC_P1P2_LPDA_PY_SellPrice').AssignValue(str(float(pySellPrice)*Exchange_Rate))
            Product.Attr('SC_P1P2_LPDA_CY_ListPrice').AssignValue('0')
            Product.Attr('SC_P1P2_LPDA_CY_DiscountPrice').AssignValue('0')
            Product.Attr('SC_P1P2_LPDA_CY_FinalListPrice').AssignValue('0')
            Product.Attr('SC_P1P2_LPDA_ScopeChange').AssignValue('0')
            Product.Attr('SC_P1P2_PY_Parts_Ext_Price').AssignValue('0')
            Product.Attr('SC_P1P2_PY_ListPrice').AssignValue('0')
        elif Product.Attr('SC_P1P2_PartsUsageMethod').GetValue() == "Last 3 Year Average":
            Product.Attr('SC_P1P2_LTYA_PY_ListPrice').AssignValue(str(float(pyListPrice)*Exchange_Rate))
            Product.Attr('SC_P1P2_LTYA_PY1_ListPrice').AssignValue('0')
            Product.Attr('SC_P1P2_LTYA_PY2_ListPrice').AssignValue('0')
            Product.Attr('SC_P1P2_LTYA_CY_FinalListPrice').AssignValue('0')
            Product.Attr('SC_P1P2_LTYA_ScopeChange').AssignValue('0')
            Product.Attr('SC_P1P2_PY_Parts_Ext_Price').AssignValue('0')
            Product.Attr('SC_P1P2_PY_ListPrice').AssignValue('0')

    #####Contigency Container#####
    contigency_hidden_cont = Product.GetContainerByName("SC_P1P2_Contigency_Cost_Hidden")
    for row in contigency_hidden_cont.Rows:
        row["PY_Cost"] = str(float(row['CY_Cost']) * Exchange_Rate) if row['CY_Cost'] else '0'
        row["CY_Cost"] = "0"
        row.Calculate()
    contigency_hidden_cont.Calculate()

    Product.Attr('SC_Renewal_check').AssignValue('1')