def populateQuoteTableRow(table , dataDict , row = None):
    if not row:
        row = table.AddNewRow()
    for key , value in dataDict.items():
        row[key] = value

def populateProjSynTables(Quote):
    prodline_table = Quote.QuoteTables["Product_Line_Details"]
    fp_prodlinesBase = {}
    fp_prodlinesOpt = {}
    projBase_table = Quote.QuoteTables["PMC_FP_ProjSynopsis"]
    projOpt_table = Quote.QuoteTables["PMC_FP_OptionalProjSynopsis"]
    projBase_row = {"SrNum_PS":"","ProductLineCode_PS":"","ProductLineDesc_PS":"","TotalQuantity_PS":"","TotalPrice_PS":""}
    projOpt_row = {"SrNum_OPS":"","ProductLineCode_OPS":"","ProductLineDesc_OPS":"","TotalQuantity_OPS":"","TotalPrice_OPS":""}
    baseSrNum = 1
    optSrNum = 1

    baseItemTotPrice = 0
    optItemTotPrice = 0


    projBase_table.Rows.Clear()
    projOpt_table.Rows.Clear()

    for qitem in Quote.Items:
        surcharge_price = qitem["QI_Tariff_Amount"].Value if qitem["QI_Tariff_Amount"] else 0.00
        total_sell_price = qitem["QI_Sell_Price_Inc_Tariff"].Value if qitem["QI_Sell_Price_Inc_Tariff"] else 0.00
        fpSparesquery=None
        fpquery=None
        fp_qtyBase = 1
        fp_qtyOpt = 1
        if qitem["QI_SparePartsFlag"].Value == "Spare Part":
            fpSparesquery = SqlHelper.GetFirst("SELECT 1 as flag FROM PMC_FP_Products WHERE PARTNUMBER = '{}'".format(qitem["QI_ParentVcModel"].Value))
        else:
            fpquery = SqlHelper.GetFirst("SELECT 1 as flag FROM PMC_FP_Products WHERE PARTNUMBER = '{}'".format(qitem.PartNumber))

        if fpquery is not None or fpSparesquery is not None:
            prodline_code = qitem["QI_ProductLine"].Value
            if prodline_code is not None:
                #Base
                if qitem.ItemType == 0:
                    if prodline_code not in fp_prodlinesBase.keys():
                        baseItemTotPrice = qitem.ExtendedListPrice
                        fp_prodlinesBase[prodline_code] = [fp_qtyBase, baseItemTotPrice, surcharge_price, total_sell_price]
                        #fp_prodlinesBase[prodline_code] = [fp_qtyBase,baseItemTotPrice]
                        #Trace.Write("fpprodlinesBase: "+str(fp_prodlinesBase))
                    elif prodline_code in fp_prodlinesBase.keys():
                        fp_qtyBase = fp_prodlinesBase[prodline_code][0] + 1
                        baseItemTotPrice = fp_prodlinesBase[prodline_code][1]+ qitem.ExtendedListPrice
                        surcharge_price = fp_prodlinesBase[prodline_code][2] + surcharge_price
                        total_sell_price = fp_prodlinesBase[prodline_code][3] + total_sell_price
                        fp_prodlinesBase[prodline_code] = [fp_qtyBase, baseItemTotPrice, surcharge_price, total_sell_price]
                        #Trace.Write("fpprodlinesBase: "+str(fp_prodlinesBase))
                #Optional
                elif qitem.ItemType == 3:
                    if prodline_code not in fp_prodlinesOpt.keys():
                        optItemTotPrice = qitem.ExtendedListPrice
                        #fp_prodlinesOpt[prodline_code] = [fp_qtyOpt,optItemTotPrice]
                        fp_prodlinesOpt[prodline_code] = [fp_qtyOpt, optItemTotPrice, surcharge_price, total_sell_price]
                    elif prodline_code in fp_prodlinesOpt.keys():
                        fp_qtyOpt = fp_prodlinesOpt[prodline_code][0] + 1
                        optItemTotPrice = fp_prodlinesOpt[prodline_code][1]+ qitem.ExtendedListPrice
                        surcharge_price += fp_prodlinesOpt[prodline_code][2]
                        total_sell_price += fp_prodlinesOpt[prodline_code][3]
                        fp_prodlinesOpt[prodline_code] = [fp_qtyOpt, optItemTotPrice, surcharge_price, total_sell_price]

    #Trace.Write("fpprodlinesBase: "+str(fp_prodlinesBase))
    #Trace.Write("fpprodlinesOpt: "+str(fp_prodlinesOpt))

    #loop over fp_prodlinesBase and populate projBase_table
    '''for pl,qtyLP in fp_prodlinesBase.items():
        for pl_row in prodline_table.Rows:
            if pl == str(pl_row["Product_Line"]):
                #Trace.Write("Prod line row: "+str(pl_row["Product_Line"]))
                projBase_row["SrNum_PS"] = baseSrNum
                projBase_row["ProductLineCode_PS"] = pl
                projBase_row["ProductLineDesc_PS"] = pl_row["Product_Line_PL_Description"]
                projBase_row["TotalQuantity_PS"] = qtyLP[0]
                projBase_row["TotalPrice_PS"] = qtyLP[1]
                populateQuoteTableRow(projBase_table,projBase_row)
                baseSrNum +=1

    #loop over fp_prodlinesOpt and populate projOpt_table
    for opl,oqtyLP in fp_prodlinesOpt.items():
        for pl_row2 in prodline_table.Rows:
            if opl == str(pl_row2["Product_Line"]):
                #Trace.Write("Prod line row: "+str(pl_row2["Product_Line"]))
                projOpt_row["SrNum_OPS"] = optSrNum
                projOpt_row["ProductLineCode_OPS"] = opl
                projOpt_row["ProductLineDesc_OPS"] = pl_row2["Product_Line_PL_Description"]
                projOpt_row["TotalQuantity_OPS"] = oqtyLP[0]
                projOpt_row["TotalPrice_OPS"] = oqtyLP[1]
                populateQuoteTableRow(projOpt_table,projOpt_row)
                optSrNum +=1'''
    
    #loop over fp_prodlinesBase and populate projBase_table
    listt = []
    listt2 = []
    for item in Quote.Items:
        if fp_prodlinesBase.get(item.QI_ProductLine.Value) and item.QI_ProductLine.Value not in listt:
            projBase_row = {}
            projBase_row["SrNum_PS"] = baseSrNum
            projBase_row["ProductLineCode_PS"] = item.QI_ProductLine.Value
            projBase_row["ProductLineDesc_PS"] = item.QI_ProductLineDesc.Value
            projBase_row["TotalQuantity_PS"] = fp_prodlinesBase[item.QI_ProductLine.Value][0]
            projBase_row["TotalPrice_PS"] = fp_prodlinesBase[item.QI_ProductLine.Value][1]
            projBase_row["Surcharge_Price"] = fp_prodlinesBase[item.QI_ProductLine.Value][2]
            projBase_row["Total_Sell_Price"] = fp_prodlinesBase[item.QI_ProductLine.Value][3]
            populateQuoteTableRow(projBase_table,projBase_row)
            baseSrNum +=1
            listt.append(item.QI_ProductLine.Value)
    #loop over fp_prodlinesOpt and populate projOpt_table
        elif fp_prodlinesOpt.get(item.QI_ProductLine.Value) and item.QI_ProductLine.Value not in listt2:
            projOpt_row = {}
            projOpt_row["SrNum_OPS"] = optSrNum
            projOpt_row["ProductLineCode_OPS"] = item.QI_ProductLine.Value
            projOpt_row["ProductLineDesc_OPS"] = item.QI_ProductLineDesc.Value
            projOpt_row["TotalQuantity_OPS"] = fp_prodlinesOpt[item.QI_ProductLine.Value][0]
            projOpt_row["TotalPrice_OPS"] = fp_prodlinesOpt[item.QI_ProductLine.Value][1]
            projOpt_row["Surcharge_Price"] = fp_prodlinesOpt[item.QI_ProductLine.Value][2]
            projOpt_row["Total_Sell_Price"] = fp_prodlinesOpt[item.QI_ProductLine.Value][3]
            populateQuoteTableRow(projOpt_table,projOpt_row)
            optSrNum +=1
            listt2.append(item.QI_ProductLine.Value)
	#populateProjSynTables(Quote)
    projBase_table.Save()
    projOpt_table.Save()