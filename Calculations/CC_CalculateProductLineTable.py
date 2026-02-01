if Quote.GetGlobal('PerformanceUpload') != 'Yes' and Quote.GetCustomField('Booking LOB').Content == "PMC" and Quote.GetCustomField('CF_Plant_Prevent_Calc').Content == 'true':
    Quote.GetCustomField('CF_Plant_Prevent_Calc').Content = ''
if Quote.GetGlobal('PerformanceUpload') != 'Yes' and Session["prevent_execution"] != "XXX" and (Quote.GetCustomField('CF_Plant_Prevent_Calc').Content != 'true' or Quote.GetCustomField('Booking LOB').Content != 'PMC'):
    from GS_CommonConfig import CL_CommonSettings as CS
    from GS_CalculateTotals import calculateProductLines
    from GS_GetData_LOBContent import getLOB_Content
    Quote.Save(False) # This save is required becoz we use cartitem table in GS_CalculateTotals.

    def deleteRows(table , ids):
        for id in ids:
            table.DeleteRow(id)

    def populateProductTypeTable(table , productTypeDict):
        toBeDeleted = []
        for row in table.Rows:
            totalLineDict = productTypeDict.get(row['Product_Type'])
            if totalLineDict:
                row['List_Price']                   = totalLineDict.get("totalListPrice",0)
                row['Regional_Cost']                = totalLineDict.get("totalCost",0)
                # row['India_Discounted_TP']          = totalLineDict.get("indiaDiscountedTP",0)  #CXCPQ-101295
                row['WTW_Cost']                     = totalLineDict.get("totalWTWCost",0)
                row['MPA_Discount_Amount']          = totalLineDict.get("mpaDiscountAmount",0)
                row['Sell_Price_Discount_Amount']   = totalLineDict.get("additionalDiscountAmount",0)
                row['Max_Discount_Amount']          = totalLineDict.get("maxDiscountLimit" , 0)
                #CXCPQ-42168:06/13/2023:Start
                #row['Sell_Price']                   = totalLineDict.get("totalExtendedAmount" , 0)
                row['Sell_Price']				    = totalLineDict.get("totalExtendedAmount" , 0)+totalLineDict.get("totalETOPrice" , 0)           
                #row['Target_Sell_Price']			= totalLineDict.get('totalListPrice' , 0) - totalLineDict.get('mpaDiscountAmount' , 0)
                row['Target_Sell_Price']			= totalLineDict.get('totalListPrice' , 0) + totalLineDict.get("totalETOPrice" , 0) - totalLineDict.get('mpaDiscountAmount' , 0)
                row['GAS_ETO_Price']                = totalLineDict.get("totalETOPrice" , 0)#Added
                #CXCPQ-42168:06/13/2023:End
                row['PROS_Guidance_Recommended_Price']			= totalLineDict.get("PROSRecommendedPrice" , 0)
                # Trace.Write("lp:" + str(row['List_Price']))
                # Trace.Write("mda:" + str(row['MPA_Discount_Amount']))
                if totalLineDict.get("totalListPrice",0):
                    row['MPA_Discount_Percent']         = (totalLineDict.get("mpaDiscountAmount",0) * 100) / totalLineDict.get("totalListPrice",0)
                    # Trace.Write("aaa" + str(row['MPA_Discount_Percent']))
                    row['Sell_Price_Discount_Percent']  = (totalLineDict.get("additionalDiscountAmount",0) * 100) / (totalLineDict.get("totalListPrice",0) - totalLineDict.get('mpaDiscountAmount' , 0))
                productTypeDict.pop(row['Product_Type'])
            else:
                toBeDeleted.append(row.Id)

        for key , totalLineDict in productTypeDict.items():
            row = table.AddNewRow()
            row['Product_Type']                 = key
            row['List_Price']                   = totalLineDict.get("totalListPrice",0)
            row['Regional_Cost']                = totalLineDict.get("totalCost",0)
            # row['India_Discounted_TP']          = totalLineDict.get("indiaDiscountedTP",0)  #CXCPQ-101295
            row['WTW_Cost']                     = totalLineDict.get("totalWTWCost",0)
            row['MPA_Discount_Amount']          = totalLineDict.get("mpaDiscountAmount",0)
            row['Sell_Price_Discount_Amount']   = totalLineDict.get("additionalDiscountAmount",0)
            row['Max_Discount_Amount']          = totalLineDict.get("maxDiscountLimit" , 0)
            #CXCPQ-42168:06/13/2023:Start
            #row['Sell_Price']                   = totalLineDict.get("totalExtendedAmount" , 0)
            row['Sell_Price']                   = totalLineDict.get("totalExtendedAmount" , 0)+totalLineDict.get("totalETOPrice" , 0)
            #row['Target_Sell_Price']			= totalLineDict.get('totalListPrice' , 0) - totalLineDict.get('mpaDiscountAmount' , 0)
            row['Target_Sell_Price']			= totalLineDict.get('totalListPrice' , 0) + totalLineDict.get("totalETOPrice" , 0)- totalLineDict.get('mpaDiscountAmount' , 0)
            row['GAS_ETO_Price']                = totalLineDict.get("totalETOPrice" , 0) #Added
            #CXCPQ-42168:06/13/2023:End
            row['PROS_Guidance_Recommended_Price']			= totalLineDict.get("PROSRecommendedPrice" , 0)
            if totalLineDict.get("totalListPrice",0):
                row['MPA_Discount_Percent']         = (totalLineDict.get("mpaDiscountAmount",0) * 100) / totalLineDict.get("totalListPrice",0)
                # Trace.Write("bbb" + str(row['MPA_Discount_Percent']))
                row['Sell_Price_Discount_Percent']  = (totalLineDict.get("additionalDiscountAmount",0) * 100) / (totalLineDict.get("totalListPrice",0) - totalLineDict.get('mpaDiscountAmount' , 0))

        deleteRows(table , toBeDeleted)
        table.Save()

    totalDict , totalDictPLSG , totalProductType , quoteTotalDict = calculateProductLines(Quote)
    if Quote.GetCustomField('Quote Type').Content in ['Contract New','Contract Renewal']:
        quoteTotalDict['totalWTWCost']= Quote.MainItems[0].QI_ExtendedWTWCost.Value if Quote.Items.Count > 0 else 0
        quoteTotalDict['totalCost']= Quote.MainItems[0].QI_SC_Cost.Value if Quote.Items.Count > 0 else 0
        quoteTotalDict['totalRegionalMargin'] = quoteTotalDict.get('totalExtendedAmount',0) - quoteTotalDict.get('totalCost' , 0)


    populateProductTypeTable(Quote.QuoteTables["Product_Type_Details"] , totalProductType)

    quoteTotalTable = Quote.QuoteTables["Product_Line_Details"]

    toBeDeleted = []

    rows = quoteTotalTable.Rows
    for row in rows:
        totalLineDict = totalDict.get(row['Product_Line'])
        if totalLineDict:
            row['Product_Line_PL_Description'] 	= totalLineDict.get("desc",'')
            row['PL_List_Price'] 				= totalLineDict.get("totalListPrice",0)
            row['PL_Regional_Cost'] 			= totalLineDict.get("totalCost",0)
            row['PL_WTW_Cost'] 					= totalLineDict.get("totalWTWCost",0)
            row['MPA_Discount_Amount'] 			= totalLineDict.get("mpaDiscountAmount",0)
            row['Sell_Price_Discount_Amount']	= totalLineDict.get("additionalDiscountAmount",0)
            row['PL_Max_Discount_Amount']       = totalLineDict.get("maxDiscountLimit" , 0)
            #CXCPQ-42168:06/13/2023:start
            #row['PL_Sell_Price']				= totalLineDict.get("totalExtendedAmount" , 0)
            row['PL_Sell_Price']				= totalLineDict.get("totalExtendedAmount" , 0)+totalLineDict.get("totalETOPrice" , 0)
            #row['PL_Target_Sell_Price']			= totalLineDict.get('totalListPrice' , 0) - totalLineDict.get('mpaDiscountAmount' , 0)
            row['PL_Target_Sell_Price']			= totalLineDict.get('totalListPrice' , 0) + totalLineDict.get("totalETOPrice" , 0)- totalLineDict.get('mpaDiscountAmount' , 0)
            #row['PL_Regional_Margin']           = totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalCost",0)
            row['PL_Regional_Margin']           = totalLineDict.get("totalExtendedAmount" , 0)+totalLineDict.get("totalETOPrice" , 0) - totalLineDict.get("totalCost",0)
            row['PL_WTW_Margin_Amount']			= totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalWTWCost",0) #CXCPQ-109165
            row['PL_GAS_ETO_Price']				= totalLineDict.get("totalETOPrice" , 0)#CXCPQ-42168:06/13/2023:Added PL_GAS_ETO_Price Key
            #CXCPQ-42168:06/13/2023:End
            if totalLineDict.get("totalExtendedAmount" , 0):
                row['PL_Regional_margin_Percentage'] = ((totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalCost",0))/ totalLineDict.get("totalExtendedAmount" , 0)) * 100
                row['PL_WTW_Margin_Percentage'] = ((totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalWTWCost",0))/ totalLineDict.get("totalExtendedAmount" , 0)) * 100 #CXCPQ-109165
            row['PROS_Guidance_Recommended_Price']			= totalLineDict.get("PROSRecommendedPrice" , 0)
            if totalLineDict.get("totalListPrice",0):
                row['MPA_Discount_Percent'] 			= (totalLineDict.get("mpaDiscountAmount",0) * 100) / totalLineDict.get("totalListPrice",0)
                Trace.Write("ccc" + str(row['MPA_Discount_Percent']))
                row['Sell_Price_Discount_Percent'] 	= (totalLineDict.get("additionalDiscountAmount",0) * 100) / (totalLineDict.get("totalListPrice",0) - totalLineDict.get('mpaDiscountAmount' , 0))
            totalDict.pop(row['Product_Line'])
            if Quote.GetCustomField('Booking LOB').Content == 'CCC':
                row['CCC_Regional_Cost'] = totalLineDict.get("totalCCCRegionalCost",0)
        else:
            toBeDeleted.append(row.Id)

    for key , totalLineDict in totalDict.items():
        newRow = quoteTotalTable.AddNewRow()
        newRow['Product_Line_PL_Description'] 	= totalLineDict.get("desc",'')
        newRow['Product_Line'] 					= key
        newRow['PL_List_Price'] 				= totalLineDict.get("totalListPrice",0)
        newRow['PL_Regional_Cost'] 				= totalLineDict.get("totalCost",0)
        newRow['PL_WTW_Cost'] 					= totalLineDict.get("totalWTWCost",0)
        newRow['MPA_Discount_Amount'] 			= totalLineDict.get("mpaDiscountAmount",0)
        newRow['Sell_Price_Discount_Amount']	= totalLineDict.get("additionalDiscountAmount",0)
        newRow['PL_Max_Discount_Amount']       	= totalLineDict.get("maxDiscountLimit" , 0)
        #CXCPQ-42168:06/13/2023:start
        #newRow['PL_Sell_Price']					= totalLineDict.get("totalExtendedAmount" , 0)
        newRow['PL_Sell_Price']					= totalLineDict.get("totalExtendedAmount" , 0) + totalLineDict.get("totalETOPrice" , 0)
        #newRow['PL_Target_Sell_Price']			= totalLineDict.get('totalListPrice' , 0) - totalLineDict.get('mpaDiscountAmount' , 0)   
        newRow['PL_Target_Sell_Price']			= totalLineDict.get('totalListPrice' , 0) + totalLineDict.get("totalETOPrice" , 0) - totalLineDict.get('mpaDiscountAmount' , 0)
        #newRow['PL_Regional_Margin']            = totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalCost",0)
        newRow['PL_Regional_Margin']            = totalLineDict.get("totalExtendedAmount" , 0)+totalLineDict.get("totalETOPrice" , 0) - totalLineDict.get("totalCost",0)
        newRow['PL_WTW_Margin_Amount']			= totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalWTWCost",0) #CXCPQ-109165
        newRow['PL_GAS_ETO_Price']				= totalLineDict.get("totalETOPrice" , 0)#CXCPQ-42168:06/13/2023:Added PL_GAS_ETO_Price Key
        #CXCPQ-42168:06/13/2023:end
        if totalLineDict.get("totalExtendedAmount" , 0):
            newRow['PL_Regional_margin_Percentage'] = ((totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalCost",0))/ totalLineDict.get("totalExtendedAmount" , 0)) * 100
            newRow['PL_WTW_Margin_Percentage'] = ((totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalWTWCost",0))/ totalLineDict.get("totalExtendedAmount" , 0)) * 100 #CXCPQ-109165
        newRow['PROS_Guidance_Recommended_Price']			= totalLineDict.get("PROSRecommendedPrice" , 0)
        if totalLineDict.get("totalListPrice",0):
            newRow['MPA_Discount_Percent'] 			= (totalLineDict.get("mpaDiscountAmount",0) * 100) / totalLineDict.get("totalListPrice",0)
            newRow['Sell_Price_Discount_Percent'] 	= (totalLineDict.get("additionalDiscountAmount",0) * 100) / (totalLineDict.get("totalListPrice",0) - totalLineDict.get('mpaDiscountAmount' , 0))
        if Quote.GetCustomField('Booking LOB').Content == 'CCC':
            newRow['CCC_Regional_Cost'] = totalLineDict.get("totalCCCRegionalCost",0)
    
    for id in toBeDeleted:
        quoteTotalTable.DeleteRow(id)
    quoteTotalTable.Save()
    plsg_query = SqlHelper.GetList("SELECT SAP_PL_PLSG,Cost_Category,B.Third_Party_Category,B.LOB FROM QT__Product_Line_Sub_Group_Details A JOIN SAP_PLSG_LOB_Mapping B ON A.Product_Line_Sub_Group = B.SAP_PL_PLSG WHERE A.cartid = {} AND A.ownerId ={}".format(Quote.QuoteId,Quote.UserId))
    Trace.Write("query 333-->SELECT SAP_PL_PLSG,Cost_Category,B.Third_Party_Category,B.LOB FROM QT__Product_Line_Sub_Group_Details A JOIN SAP_PLSG_LOB_Mapping B ON A.Product_Line_Sub_Group = B.SAP_PL_PLSG WHERE A.cartid = {} AND A.ownerId ={}".format(Quote.QuoteId,Quote.UserId))
    plsg_dic = {row.SAP_PL_PLSG: [row.Cost_Category, row.Third_Party_Category, row.LOB] for row in plsg_query}
    quoteTotalTable = Quote.QuoteTables["Product_Line_Sub_Group_Details"]
    toBeDeleted = []
    rows = quoteTotalTable.Rows
    for row in rows:
        totalLineDict = totalDictPLSG.get(row['Product_Line_Sub_Group'])
        if totalLineDict:
            row['PLSG_Description'] 			= totalLineDict.get("desc",'')
            row['Cost_categary']						= plsg_dic.get(row['Product_Line_Sub_Group'], ['','',''])[0]
            row['Third_Party_Category']   = plsg_dic.get(row['Product_Line_Sub_Group'], ['','',''])[1]
            row['LOB']   									= plsg_dic.get(row['Product_Line_Sub_Group'], ['','',''])[2]
            row['PLSG_List_Price'] 				= totalLineDict.get("totalListPrice",0)
            row['PLSG_Regional_Cost'] 			= totalLineDict.get("totalCost",0)
            row['PLSG_WTW_Cost'] 				= totalLineDict.get("totalWTWCost",0)
            row['MPA_Discount_Amount'] 			= totalLineDict.get("mpaDiscountAmount",0)
            row['Sell_Price_Discount_Amount']	= totalLineDict.get("additionalDiscountAmount",0)
            row['PLSG_Max_Discount_Amount']     = totalLineDict.get("maxDiscountLimit" , 0)
            #CXCPQ-42168:06/13/2023:start
            #row['PLSG_Sell_Price']				= totalLineDict.get("totalExtendedAmount" , 0)
            row['PLSG_Sell_Price']				= totalLineDict.get("totalExtendedAmount" , 0) + totalLineDict.get("totalETOPrice" , 0)
            #row['PLSG_Target_Sell_Price']		= totalLineDict.get('totalListPrice' , 0) - totalLineDict.get('mpaDiscountAmount' , 0)
            row['PLSG_Target_Sell_Price']		= totalLineDict.get('totalListPrice' , 0) + totalLineDict.get("totalETOPrice" , 0) - totalLineDict.get('mpaDiscountAmount' , 0)
            row['PLSG_GAS_ETO_Price']           = totalLineDict.get("totalETOPrice" , 0)#Added
            #CXCPQ-42168:06/13/2023:end
            row['PROS_Guidance_Recommended_Price']			= totalLineDict.get("PROSRecommendedPrice",0)
            #CXCPQ-109165: Start
            row['PLSG_Regional_Margin_Amount']  = totalLineDict.get("totalExtendedAmount" , 0) + totalLineDict.get("totalETOPrice" , 0) - totalLineDict.get("totalCost",0)
            row['PLSG_WTW_Margin_Amount']		= totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalWTWCost",0)
            if totalLineDict.get("totalExtendedAmount" , 0):
                row['PLSG_Regional_Margin_Percentage'] = ((totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalCost",0))/ totalLineDict.get("totalExtendedAmount" , 0)) * 100
                row['PLSG_WTW_Margin_Percentage'] = ((totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalWTWCost",0))/ totalLineDict.get("totalExtendedAmount" , 0)) * 100
            #CXCPQ-109165: End
            if totalLineDict.get("totalListPrice",0):
                row['MPA_Discount_Percent'] 			= (totalLineDict.get("mpaDiscountAmount",0) * 100) / totalLineDict.get("totalListPrice",0)
                # Trace.Write("fff:" + str(row['MPA_Discount_Percent']))
                row['Sell_Price_Discount_Percent'] 	= (totalLineDict.get("additionalDiscountAmount",0) * 100) / (totalLineDict.get("totalListPrice",0) - totalLineDict.get('mpaDiscountAmount' , 0))
            totalDictPLSG.pop(row['Product_Line_Sub_Group'])
        else:
            toBeDeleted.append(row.Id)


    for key , totalLineDict in totalDictPLSG.items():
        newRow = quoteTotalTable.AddNewRow()
        newRow['PLSG_Description'] 				= totalLineDict.get("desc",'')
        newRow['Product_Line_Sub_Group'] 		= key
        newRow['PLSG_List_Price'] 				= totalLineDict.get("totalListPrice",0)
        newRow['PLSG_Regional_Cost'] 			= totalLineDict.get("totalCost",0)
        newRow['PLSG_WTW_Cost'] 				= totalLineDict.get("totalWTWCost",0)
        newRow['MPA_Discount_Amount'] 			= totalLineDict.get("mpaDiscountAmount",0)
        newRow['Sell_Price_Discount_Amount']	= totalLineDict.get("additionalDiscountAmount",0)
        newRow['PLSG_Max_Discount_Amount']      = totalLineDict.get("maxDiscountLimit" , 0)
        #CXCPQ-42168:06/13/2023:start
        #newRow['PLSG_Sell_Price']				= totalLineDict.get("totalExtendedAmount" , 0)
        newRow['PLSG_Sell_Price']				= totalLineDict.get("totalExtendedAmount" , 0) + totalLineDict.get("totalETOPrice" , 0)
        #newRow['PLSG_Target_Sell_Price']		= totalLineDict.get('totalListPrice' , 0) - totalLineDict.get('mpaDiscountAmount' , 0)
        newRow['PLSG_Target_Sell_Price']		= totalLineDict.get('totalListPrice' , 0) + totalLineDict.get("totalETOPrice" , 0) - totalLineDict.get('mpaDiscountAmount' , 0)
        newRow['PLSG_GAS_ETO_Price']            = totalLineDict.get("totalETOPrice" , 0)#Added
        #CXCPQ-42168:06/13/2023:end
        newRow['PROS_Guidance_Recommended_Price']			= totalLineDict.get("PROSRecommendedPrice",0)
        #CXCPQ-109165: Start
        newRow['PLSG_Regional_Margin_Amount']  = totalLineDict.get("totalExtendedAmount" , 0) + totalLineDict.get("totalETOPrice" , 0) - totalLineDict.get("totalCost",0)
        newRow['PLSG_WTW_Margin_Amount']		= totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalWTWCost",0)
        if totalLineDict.get("totalExtendedAmount" , 0):
            newRow['PLSG_Regional_Margin_Percentage'] = ((totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalCost",0))/ totalLineDict.get("totalExtendedAmount" , 0)) * 100
            newRow['PLSG_WTW_Margin_Percentage'] = ((totalLineDict.get("totalExtendedAmount" , 0) - totalLineDict.get("totalWTWCost",0))/ totalLineDict.get("totalExtendedAmount" , 0)) * 100
        #CXCPQ-109165: End
        if totalLineDict.get("totalListPrice",0):
            newRow['MPA_Discount_Percent'] 			= (totalLineDict.get("mpaDiscountAmount",0) * 100) / totalLineDict.get("totalListPrice",0)
            #Trace.Write("ggg:" + str(row['MPA_Discount_Percent']))
            newRow['Sell_Price_Discount_Percent'] 	= (totalLineDict.get("additionalDiscountAmount",0) * 100) / (totalLineDict.get("totalListPrice",0) - totalLineDict.get('mpaDiscountAmount' , 0))

    for id in toBeDeleted:
        quoteTotalTable.DeleteRow(id)
    quoteTotalTable.Save()

    quoteTotalTable = Quote.QuoteTables["Quote_Details"]

    minOrderFee = UserPersonalizationHelper.ConvertToNumber(Quote.GetCustomField('Minimum Order Fee').Content) if Quote.GetCustomField('Minimum Order Fee').Content.strip() else 0.0
    totalExpediteFee = 0.0

    if quoteTotalTable.Rows.Count == 0:
        row = quoteTotalTable.AddNewRow()
    else:
        row = quoteTotalTable.Rows[0]
    #Log.Info("totallistprice cc calculation"+str(quoteTotalDict.get('totalListPrice' , 0)))
    row['Quote_List_Price'] 			= quoteTotalDict.get('totalListPrice' , 0)
    row['Quote_Regional_Cost'] 			= quoteTotalDict.get('totalCost' , 0)
    # row['India_Discounted_TP']          = quoteTotalDict.get("indiaDiscountedTP",0)  #CXCPQ-101295
    row['Quote_WTW_Cost'] 				= quoteTotalDict.get('totalWTWCost',0)
    #CXCPQ-42168:06/13/2023:start
    #row['Quote_Sell_Price']				= quoteTotalDict.get('totalExtendedAmount',0)
    row['Quote_Sell_Price']				= quoteTotalDict.get('totalExtendedAmount',0) + quoteTotalDict.get("totalETOPrice" , 0)
    row['Total_Tariff_Amount']				= quoteTotalDict.get('totalTariffAmount',0) 
    row['Quote_Sell_Price_Incl_Tariff']		= row['Quote_Sell_Price'] if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal') else quoteTotalDict.get('quoteSellPriceInclTariff',0)
    #CXCPQ-42168:06/13/2023:End
    row['MPA_Discount_Amount'] 			= quoteTotalDict.get('mpaDiscountAmount' , 0)
    row['Quote_Discount_Amount'] 		= quoteTotalDict.get('additionalDiscountAmount' , 0)
    row['Quote_Regional_Margin_Amount'] = quoteTotalDict.get('totalRegionalMargin' , 0)
    # Log.Info('maxDiscountLimit---'+str(quoteTotalDict.get('maxDiscountLimit' , 0)))
    row['Max_Quote_Discount_Amount']    = quoteTotalDict.get('maxDiscountLimit' , 0)

    row['Quote_WTW_Margin_Amount']      = quoteTotalDict.get('totalExtendedAmount',0) - quoteTotalDict.get('totalWTWCost' , 0)
    #CXCPQ-42168:06/13/2023:start
    #row['Target_Sell_Price']			= quoteTotalDict.get('totalListPrice' , 0) - quoteTotalDict.get('mpaDiscountAmount' , 0)
    row['Target_Sell_Price']			= quoteTotalDict.get('totalListPrice' , 0) + quoteTotalDict.get("totalETOPrice" , 0) - quoteTotalDict.get('mpaDiscountAmount' , 0)
    row['GAS_ETO_Price']                = quoteTotalDict.get("totalETOPrice" , 0)#Added
    #CXCPQ-42168:06/13/2023:End
    row['PROS_Guidance_Recommended_Price']			= quoteTotalDict.get("PROSRecommendedPrice",0)
    row['CCC_Regional_Cost']			= quoteTotalDict.get("totalCCCRegionalCost",0)
    # Trace.Write("MPA Exists ====== "+str(Quote.GetCustomField('MPA').Content))
    if str(Quote.GetCustomField('MPA').Content) !='':
        # Log.Info('VJ List PRice log === '+str(quoteTotalDict.get('totalListPrice' , 0)))
        # Log.Info('VJ Discount log === '+str(quoteTotalDict.get('mpaDiscountAmount' , 0)))
        row['Recommended_Target_Price']		= quoteTotalDict.get('totalListPrice' , 0) - quoteTotalDict.get('mpaDiscountAmount' , 0)
        # Trace.Write("Recommended_Target_Priceifif "+str(row['Recommended_Target_Price']))
        # Log.Info('VJ Rec Target PRice'+str(row['Recommended_Target_Price']))
    else:
        row['Recommended_Target_Price']		= quoteTotalDict.get('totalListPrice' , 0) - quoteTotalDict.get('recommendedMpaDiscountAmount' , 0)

    if quoteTotalDict.get('totalListPrice' , 0):
        row['MPA_Discount_percent'] = (quoteTotalDict.get('mpaDiscountAmount' , 0) * 100) / quoteTotalDict.get('totalListPrice' , 0)
        Trace.Write("hhh111updated:" + str(row['MPA_Discount_Percent']))
    if Quote.GetCustomField('Booking LOB').Content == "PMC" and Quote.GetCustomField('Quote Type').Content == "Parts and Spot":
        row['Quote_Discount_Percent'] = ((row['Quote_List_Price']-(row['Quote_Sell_Price']-row['GAS_ETO_Price']))*100)/row['Quote_List_Price'] if row['Quote_List_Price'] else 0.0
    elif row['Target_Sell_Price']:
        #CXCPQ-42168:06/13/2023:start
        # Trace.Write("AdditionalDIS=====>"+str(quoteTotalDict.get('additionalDiscountAmount'))+"tsp"+str(row['Target_Sell_Price'])+"eto"+str(row['GAS_ETO_Price']))
        #row['Quote_Discount_Percent'] = (quoteTotalDict.get('additionalDiscountAmount' , 0) * 100) / row['Target_Sell_Price']
        if quoteTotalDict.get('additionalDiscountAmount'):
            row['Quote_Discount_Percent'] = (quoteTotalDict.get('additionalDiscountAmount') * 100) / (row['Target_Sell_Price']-row['GAS_ETO_Price'] )
        elif quoteTotalDict.get('additionalDiscountAmount') == 0:
            row['Quote_Discount_Percent'] = 0
        #CXCPQ-42168:06/13/2023:End
    if quoteTotalDict.get('totalExtendedAmount' , 0):
        #row['Quote_Regional_Margin_Percent'] = (quoteTotalDict.get('totalRegionalMargin' , 0) * 100) / quoteTotalDict.get('totalExtendedAmount' , 0)
        # Trace.Write("===totalCost===="+str(quoteTotalDict.get('totalCost' , 0))+"====totalExtendedAmount===="+str(quoteTotalDict.get('totalExtendedAmount' , 0)))
        # Trace.Write("===totalRegionalMargin===="+str(quoteTotalDict.get('totalRegionalMargin' , 0)))
        row['Quote_Regional_Margin_Percent'] =((quoteTotalDict.get('totalExtendedAmount',0) - quoteTotalDict.get('totalCost' , 0)) * 100) / quoteTotalDict.get('totalExtendedAmount' , 0)
        row['Quote_WTW_Margin_Percent'] = ((quoteTotalDict.get('totalExtendedAmount',0) - quoteTotalDict.get('totalWTWCost' , 0)) * 100) / quoteTotalDict.get('totalExtendedAmount' , 0)

    # for item in Quote.Items:
        # if item['QI_Expedite_Fees'].Value:
            # totalExpediteFee = totalExpediteFee + UserPersonalizationHelper.ConvertToNumber(str(item['QI_Expedite_Fees'].Value))

    # row['Total_Sell_Price_incl_appl_Fees_'] = row['Quote_Sell_Price'] + minOrderFee + totalExpediteFee
    row['Total_Sell_Price_incl_appl_Fees_'] = row['Quote_Sell_Price'] + minOrderFee + float(CS.setdefaultvalue["QI_Expedite_Fees"])
    
    '''Updating the Walk away Sales Price '''
    row['Walk_away_Sales_Price'] = row['Quote_Sell_Price'] - row['Negotiation_Limit']
    '''Updating the milestonePrice'''
    cf_milestonePrice = Quote.GetCustomField('EGAP_Milestone_Price')
    nonMilestoneBillingTotal = 0
    cf_nonMilestoneBillingTotal = Quote.GetCustomField('EGAP_Non_Milestone_Billing_Total_Sell_Price')
    if cf_nonMilestoneBillingTotal.Content:
        nonMilestoneBillingTotal = cf_nonMilestoneBillingTotal.Content
    milestonePrice = float(row['Walk_away_Sales_Price']) - float(nonMilestoneBillingTotal)
    cf_milestonePrice.Content = str(milestonePrice)

    quoteTotalTable.Save()
    #Assign Values to Total fields
    Quote.GetCustomField('Total_Sell_Price_Updated').Content=UserPersonalizationHelper.ToUserFormat(row['Total_Sell_Price_incl_appl_Fees_'])
    Quote.GetCustomField('Total Sell Price').Content=UserPersonalizationHelper.ToUserFormat(row['Quote_Sell_Price'])
    Quote.GetCustomField('Total_Tariff_Amount').Content=UserPersonalizationHelper.ToUserFormat(row['Total_Tariff_Amount'])
    Quote.GetCustomField('Total_Sell_Price_Incl_Tariff').Content=UserPersonalizationHelper.ToUserFormat(row['Quote_Sell_Price_Incl_Tariff'])
    Quote.GetCustomField('Total Discount Percent').Content=str(row['Quote_Discount_Percent'])
    #Trace.Write("----aditional_%--"+str(item['QI_Additional_Discount_Percent'].Value))
    Quote.GetCustomField('Total Regional Margin Percent').Content=str(row['Quote_Regional_Margin_Percent'])
    Quote.GetCustomField('TotalwtwMarginPercent').Content=str(row['Quote_WTW_Margin_Percent'])
    #Trace.Write("TotalwtwMarginPercent "+str(Quote.GetCustomField('TotalwtwMarginPercent').Content))
    # if Quote.GetCustomField("Booking Country").Content.lower() == 'india' and Quote.GetCustomField("Booking LOB").Content in ('PAS','LSS') and Quote.GetCustomField("Quote Type").Content == 'Projects':
        # Quote.GetCustomField('India Discounted TP Margins').Content = str(round(((row['Quote_Sell_Price'] - quoteTotalDict.get('indiaDiscountedTP' , 0))/row['Quote_Sell_Price'])*100.0,2)) if row['Quote_Sell_Price'] != 0 else '0.00'
    getLOB_Content(Quote)
    # Log.Info('check wtw margin for R2Q == '+str(row['Quote_Sell_Price'])+'====wtw== '+str(row['Quote_WTW_Margin_Percent']))
    #Quote.Save(False)