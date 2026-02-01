if True:
    from GS_SC_CBM_PRICING_CALCULATIONS import reset_values,pricing_calc
    productFamily = Product.Attr("CBM_PRODUCT_FAMILY").GetValue()
    assetType = Product.Attr("CBM_ASSET_TYPE").GetValue()
    level = Product.Attr("CBM_Level").GetValue()
    count = Product.Attr("CBM_COUNT").GetValue()
    cycles = Product.Attr("CBM_PM/CBM_Cycles").GetValue()
    if productFamily is not None and productFamily != "" and assetType is not None and assetType != "":
        #CXCPQ-86942: Added new columns
        getPricingDetails = SqlHelper.GetFirst("select STD_Hours_LT,Remote_TT_NC,Remote_TT_C,Total_Tasks,Remote_T_NC,Remote_T_C,STD_Hours_LT_Quarterly,Remote_TT_NC_Quarterly,Remote_TT_C_Quarterly from SC_CT_CBM_Pricing where Product_Family = '"+str(productFamily)+"' and Asset_Type = '"+str(assetType)+"'")
    if assetType is None or assetType == "":
        reset_values(Product)
    else:
        lpmTask = ""
        if int(level) == 1:
            lpmTask = SqlHelper.GetFirst("select L_PMT_R_NLP from SC_CT_CBM_Pricing where Product_Family = '"+str(productFamily)+"' and Asset_Type = '"+str(assetType)+"'").L_PMT_R_NLP
        elif int(level) == 2:
            lpmTask = SqlHelper.GetFirst("select L_PMT_NR_NLP from SC_CT_CBM_Pricing where Product_Family = '"+str(productFamily)+"' and Asset_Type = '"+str(assetType)+"'").L_PMT_NR_NLP
        else:
            lpmTask = SqlHelper.GetFirst("select Local_TL3 from SC_CT_CBM_Pricing where Product_Family = '"+str(productFamily)+"' and Asset_Type = '"+str(assetType)+"'").Local_TL3
        resultCalc = pricing_calc(level,getPricingDetails,count,cycles,Quote,TagParserQuote,Session)
        Product.Attr("CBM_REMOTE_TIME").AssignValue(resultCalc["RemoteTime"])
        Product.Attr("CBM_LOCAL_TIME").AssignValue(resultCalc["LocalTime"])
        Product.Attr("CBM_TASK_PERCENTAGE").AssignValue(resultCalc["Tasks"])
        Product.Attr("CBM_PER_TIME").AssignValue(resultCalc["PerTime"])
        Product.Attr("CBM_REMOTE_TASKS").AssignValue(resultCalc["RemoteTask"])
        Product.Attr("CBM_LOCAL_TASKS").AssignValue(resultCalc["LocalTask"])
        Product.Attr("CBM_LIST_PRICE_PER_CYCLE").AssignValue(resultCalc["ListPricePerCycle"])
        Product.Attr("CBM_ANNUAL_PRICE").AssignValue(resultCalc["AnnualPrice"])
        Product.Attr('CBM_LPM_TASK').AssignValue(str(lpmTask))
        Trace.Write("SAnnualPrice = " + str(resultCalc))