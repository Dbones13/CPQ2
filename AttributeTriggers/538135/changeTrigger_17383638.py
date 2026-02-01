Trace.Write("$$$$$$$$$$$$$$$$$$$$$$$$$$$ level $$$$$$$$$$$$$$$$$$$$$$$$$$$")
from GS_SC_CBM_PRICING_CALCULATIONS import reset_values,pricing_calc
level = Product.Attr("CBM_Level").GetValue()
cycles = Product.Attr("CBM_PM/CBM_Cycles").GetValue()
for row in Product.GetContainerByName('CBM_Pricing_Container').Rows:
    productFamily = row["Product Family"]
    assetType = row["Asset Type"]
    if productFamily is not None and productFamily != "" and assetType is not None and assetType != "":
        getPricingDetails = SqlHelper.GetFirst("select Remote_T_C,Remote_T_NC,Total_Tasks,Remote_TT_C,Remote_TT_NC,STD_Hours_LT,L_PMT_R_NLP,L_PMT_NR_NLP,Local_TL3 from SC_CT_CBM_PRICING where Product_Family = '"+str(productFamily)+"' and Asset_Type = '"+str(assetType)+"'")
        count = row["Count"]
        lpmTask = ""
        if int(level) == 1:
            lpmTask = getPricingDetails.L_PMT_R_NLP
        elif int(level) == 2:
            lpmTask = getPricingDetails.L_PMT_NR_NLP
        else:
            lpmTask = getPricingDetails.Local_TL3
        resultCalc = pricing_calc(level,getPricingDetails,count,cycles,Quote,TagParserQuote,Session)
        row.Product.Attr("CBM_REMOTE_TIME").AssignValue(resultCalc["RemoteTime"])
        row.Product.Attr("CBM_LOCAL_TIME").AssignValue(resultCalc["LocalTime"])
        row.Product.Attr("CBM_TASK_PERCENTAGE").AssignValue(resultCalc["Tasks"])
        row.Product.Attr("CBM_PER_TIME").AssignValue(resultCalc["PerTime"])
        row.Product.Attr("CBM_REMOTE_TASKS").AssignValue(resultCalc["RemoteTask"])
        row.Product.Attr("CBM_LOCAL_TASKS").AssignValue(resultCalc["LocalTask"])
        row.Product.Attr("CBM_LIST_PRICE_PER_CYCLE").AssignValue(resultCalc["ListPricePerCycle"])
        row.Product.Attr("CBM_ANNUAL_PRICE").AssignValue(resultCalc["AnnualPrice"])
        row.Product.Attr('CBM_LPM_TASK').AssignValue(str(lpmTask))
        row.Calculate()
        row.ApplyProductChanges()
Product.GetContainerByName('CBM_Pricing_Container').Calculate()