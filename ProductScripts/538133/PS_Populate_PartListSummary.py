tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Scope Summary' in tabs:

    if Product.Attr('SC_Product_Type').GetValue() == "New":
        summaryCont = Product.GetContainerByName('SC_P1P2_Parts_List_Summary')
        if summaryCont.Rows.Count:
            summaryCont.Rows.Clear()
        partDetCont = Product.GetContainerByName('SC_P1P2_Parts_Details')
        BookingCountry = ""
        if Quote:
            BookingCountry = Quote.GetCustomField("Booking Country").Content

        p1Qty = 0
        p1hotQty = 0
        p2Qty = 0
        p1Ext = 0
        p1hotExt = 0
        p2Ext = 0
        p1hp = 0
        p1hothp = 0
        p2hp = 0

        Trace.Write(BookingCountry)
        hpQuery = SqlHelper.GetFirst("select Parts_Holding_P1, Parts_Holding_P1_Hot, Parts_Holding_P2 from P1P2_HOLDING_PERCENTAGE where Country = '{}'".format(BookingCountry))
        prodTable = SqlHelper.GetList("select distinct ServiceProduct, ProductCode from CT_SC_ENTITLEMENTS_DATA where Product_Type = 'Parts Management'")
        prodDist = {}
        for row in prodTable:
            prodDist[row.ServiceProduct] = row.ProductCode
        if hpQuery is not None:
            p1hp = int(hpQuery.Parts_Holding_P1)
            p1hothp = int(hpQuery.Parts_Holding_P1_Hot)
            p2hp = int(hpQuery.Parts_Holding_P2)

        for row in partDetCont.Rows:
            if row['Qty'] not in ("","0") and row['Ext_Price'] not in ("","0","0.00"):
                if row['Service_Product'] == 'Parts Holding P1':
                    p1Qty += int(float(row['Qty']))
                    p1Ext += float(str(row['Ext_Price']))
                elif row['Service_Product'] == 'Parts Holding P1 Hot':
                    p1hotQty += int(float(row['Qty']))
                    p1hotExt += float(str(row['Ext_Price']))
                elif row['Service_Product'] == 'Parts Holding P2':
                    p2Qty += int(float(row['Qty']))
                    p2Ext += float(str(row['Ext_Price']))

        if p1Qty != 0:
            p1row = summaryCont.AddNewRow(False)
            p1row['Service_Product'] = 'Parts Holding P1'
            p1row['Holding_Percentage'] = str(p1hp)
            p1row['Qty'] = str(p1Qty)
            p1row['Ext_Price'] = str(p1Ext)
            p1row['Ext_Holding_Price'] = str(p1hp*p1Ext/100)
            costFactor = SqlHelper.GetFirst("select Value from SC_HARDCODE_VALUES where Name = 'Parts Holding P1'")
            if costFactor is not None:
                p1row['CY_TotalCost'] = str((eval(p1row['Ext_Price'])*eval(costFactor.Value))/100)
            p1row['ProductCode'] = prodDist[p1row['Service_Product']]

        if p1hotQty != 0:
            p1hotrow = summaryCont.AddNewRow(False)
            p1hotrow['Service_Product'] = 'Parts Holding P1 Hot'
            p1hotrow['Holding_Percentage'] = str(p1hothp)
            p1hotrow['Qty'] = str(p1hotQty)
            p1hotrow['Ext_Price'] = str(p1hotExt)
            p1hotrow['Ext_Holding_Price'] = str(p1hothp*p1hotExt/100)
            costFactor = SqlHelper.GetFirst("select Value from SC_HARDCODE_VALUES where Name = 'Parts Holding P1 Hot'")
            if costFactor is not None:
                p1hotrow['CY_TotalCost'] = str((eval(p1hotrow['Ext_Price'])*eval(costFactor.Value))/100)
            p1hotrow['ProductCode'] = prodDist[p1hotrow['Service_Product']]

        if p2Qty != 0:
            p2row = summaryCont.AddNewRow(False)
            p2row['Service_Product'] = 'Parts Holding P2'
            p2row['Holding_Percentage'] = str(p2hp)
            p2row['Qty'] = str(p2Qty)
            p2row['Ext_Price'] = str(p2Ext)
            p2row['Ext_Holding_Price'] = str(p2hp*p2Ext/100)
            p2row['ProductCode'] = prodDist[p2row['Service_Product']]
            costFactor = SqlHelper.GetFirst("select Value from SC_HARDCODE_VALUES where Name = 'Parts Holding P2'")
            if costFactor is not None:
                p2row['CY_TotalCost'] = str((eval(p2row['Ext_Price'])*eval(costFactor.Value))/100)
        summaryCont.Calculate()

        if summaryCont.Rows.Count > 0 and Product.Attr("SC_P1P2_AutoUpdate_Editable_Ext").GetValue() == "&nbsp":
            x = TagParserProduct.ParseString('<*CTX ( Container(SC_P1P2_Parts_List_Summary).Sum(Ext_Price) )*>')
            Product.Attr("SC_P1P2_Parts_Ext_Price").AssignValue(x)
            fee_percent = float(Product.Attr("SC_P1P2_Fee_Percentage").GetValue())
            Product.Attr("SC_P1P2_ListPrice").AssignValue(str((fee_percent/100)*float(x)))
        elif Product.Attr("SC_P1P2_AutoUpdate_Editable_Ext").GetValue() != "&nbsp":
            if Product.Attr("SC_P1P2_Fee_Percentage").GetValue() != "" and Product.Attr("SC_P1P2_Parts_Ext_Price").GetValue() != "":
                fee_percent = float(Product.Attr("SC_P1P2_Fee_Percentage").GetValue())
                parts_ext = float(Product.Attr("SC_P1P2_Parts_Ext_Price").GetValue())
                Product.Attr("SC_P1P2_ListPrice").AssignValue(str((fee_percent/100)*parts_ext))


        replacementCont = Product.GetContainerByName('SC_P1P2_Parts_Replacement_Summary')
        replacementCont.Rows.Clear()
        if Product.Attr("SC_P1P2_AutoUpdate_Editable_Ext").GetValue() == "&nbsp" or (Product.Attr("SC_P1P2_AutoUpdate_Editable_Ext").GetValue() != "&nbsp" and Product.Attr('SC_P1P2_Parts_Ext_Price').GetValue() != "0"):
            row = replacementCont.AddNewRow(False)
            row['Service_Product'] = "Parts Replacement"
            row["Pricing_Method"] = "1 Year Pricing"
            row['Fee_Percentage'] = Product.Attr('SC_P1P2_Fee_Percentage').GetValue()
            row['Parts_Ext_Price'] = Product.Attr('SC_P1P2_Parts_Ext_Price').GetValue()
            row['List_Price'] = Product.Attr('SC_P1P2_ListPrice').GetValue()
            row['ProductCode'] = prodDist[row['Service_Product']]
        replacementCont.Calculate()

    elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
        prev_quote = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
        active_contract = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
        summaryCont = Product.GetContainerByName('SC_P1P2_Parts_List_Summary')
        summaryCont.Rows.Clear()
        partDetCont = Product.GetContainerByName('SC_P1P2_Parts_Details')
        contigencyhidden_cont = Product.GetContainerByName('SC_P1P2_Contigency_Cost_Hidden')
        contigency_cont = Product.GetContainerByName('SC_P1P2_Contigency_Cost')
        BookingCountry = ""
        if Quote:
            BookingCountry = Quote.GetCustomField("Booking Country").Content

        p1Qty = 0
        p1hotQty = 0
        p2Qty = 0
        p1Ext = 0
        p1hotExt = 0
        p2Ext = 0
        p1hp = 0
        p1hothp = 0
        p2hp = 0
        py_p1Qty = 0
        py_p1hotQty = 0
        py_p2Qty = 0
        py_p1Ext = 0
        py_p1hotExt = 0
        py_p2Ext = 0
        py_p1Cost = 0
        py_p1hotCost = 0
        py_p2Cost = 0
        p1Cost = 0
        p1hotCost = 0
        p2Cost = 0
        py_p1SellPrice = 0
        py_p1hotSellPrice = 0
        py_p2SellPrice = 0
        py_p1HoldPrice = 0
        py_p1hotHoldPrice = 0
        py_p2HoldPrice = 0

        Trace.Write(BookingCountry)
        hpQuery = SqlHelper.GetFirst("select Parts_Holding_P1, Parts_Holding_P1_Hot, Parts_Holding_P2 from P1P2_HOLDING_PERCENTAGE where Country = '{}'".format(BookingCountry))
        prodTable = SqlHelper.GetList("select distinct ServiceProduct, ProductCode from CT_SC_ENTITLEMENTS_DATA where Product_Type = 'Parts Management'")
        prodDist = {}
        for row in prodTable:
            prodDist[row.ServiceProduct] = row.ProductCode
        if hpQuery is not None:
            p1hp = int(hpQuery.Parts_Holding_P1)
            p1hothp = int(hpQuery.Parts_Holding_P1_Hot)
            p2hp = int(hpQuery.Parts_Holding_P2)

        for row in contigency_cont.Rows:
            if row["Service_Product"] == "Parts Holding P1":
                p1Cost = float(str(row["CY_Cost"])) if row["CY_Cost"] else 0
            elif row["Service_Product"] == "Parts Holding P1 Hot":
                p1hotCost = float(str(row["CY_Cost"])) if row["CY_Cost"] else 0
            elif row["Service_Product"] == "Parts Holding P2":
                p2Cost = float(str(row["CY_Cost"])) if row["CY_Cost"] else 0

        for row in contigencyhidden_cont.Rows:
            if row["Service_Product"] == "Parts Holding P1":
                py_p1Cost = float(str(row["PY_Cost"])) if row["PY_Cost"] else 0
            elif row["Service_Product"] == "Parts Holding P1 Hot":
                py_p1hotCost = float(str(row["PY_Cost"])) if row["PY_Cost"] else 0
            elif row["Service_Product"] == "Parts Holding P2":
                py_p2Cost = float(str(row["PY_Cost"])) if row["PY_Cost"] else 0

        compdict = {}
        compdictwithdiscount = {}
        ComparisonCont = Product.GetContainerByName('ComparisonSummary')
        if ComparisonCont.Rows.Count:
            for compRow in ComparisonCont.Rows:
                cost = str(round((1-float(compRow['Booked_Margin'])/100) *float(compRow["PY_Sell_Price_SFDC"]),2)) if compRow["PY_Sell_Price_SFDC"] else "0"
                compdict[compRow["Service_Product"]] = cost
                compdictwithdiscount[compRow["Service_Product"]] = compRow["PY_Discount_SFDC"] if compRow["PY_Discount_SFDC"] else '0'

        for row in partDetCont.Rows:
            if (row['PY_Quantity'] not in ("","0") or row['CY_Quantity'] not in ("","0")) and (row['PY_ExtPrice'] not in ("","0","0.00") or row['CY_ExtPrice'] not in ("","0","0.00")):
                if row['Service_Product'] == 'Parts Holding P1':
                    p1Qty += int(float(row['CY_Quantity'])) if row['CY_Quantity'] else 0
                    p1Ext += float(str(row['CY_ExtPrice'])) if row['CY_ExtPrice'] else 0
                    py_p1Qty += int(float(row['PY_Quantity'])) if row['PY_Quantity'] else 0
                    py_p1Ext += float(str(row['PY_ExtPrice'])) if row['PY_ExtPrice'] else 0
                    py_p1SellPrice += float(str(row['PY_HoldingFeeSellPrice'])) if row['PY_HoldingFeeSellPrice'] else 0
                    py_p1HoldPrice += float(str(row['PY_HoldingFeeListPrice'])) if row['PY_HoldingFeeListPrice'] else 0
                elif row['Service_Product'] == 'Parts Holding P1 Hot':
                    p1hotQty += int(float(row['CY_Quantity'])) if row['CY_Quantity'] else 0
                    p1hotExt += float(str(row['CY_ExtPrice'])) if row['CY_ExtPrice'] else 0
                    py_p1hotQty += int(float(row['PY_Quantity'])) if row['PY_Quantity'] else 0
                    py_p1hotExt += float(str(row['Py_ExtPrice'])) if row['Py_ExtPrice'] else 0
                    py_p1hotSellPrice += float(str(row['PY_HoldingFeeSellPrice'])) if row['PY_HoldingFeeSellPrice'] else 0
                    py_p1hotHoldPrice += float(str(row['PY_HoldingFeeListPrice'])) if row['PY_HoldingFeeListPrice'] else 0
                elif row['Service_Product'] == 'Parts Holding P2':
                    p2Qty += int(float(row['CY_Quantity'])) if row['CY_Quantity'] else 0
                    p2Ext += float(str(row['CY_ExtPrice'])) if row['CY_ExtPrice'] else 0
                    py_p2Qty += int(float(row['PY_Quantity'])) if row['PY_Quantity'] else 0
                    py_p2Ext += float(str(row['PY_ExtPrice'])) if row['PY_ExtPrice'] else 0
                    py_p2SellPrice += float(str(row['PY_HoldingFeeSellPrice'])) if row['PY_HoldingFeeSellPrice'] else 0
                    py_p2HoldPrice += float(str(row['PY_HoldingFeeListPrice'])) if row['PY_HoldingFeeListPrice'] else 0

        if p1Qty != 0 or py_p1Qty != 0:
            p1row = summaryCont.AddNewRow(False)
            p1row['Service_Product'] = 'Parts Holding P1'
            p1row['Holding_Percentage'] = str(p1hp)
            p1row['PY_Quantity'] = str(py_p1Qty)
            p1row['CY_Quantity'] = str(p1Qty)
            p1row['PY_ExtPrice'] = str(py_p1Ext)
            p1row['CY_ExtPrice'] = str(p1Ext)
            p1row['PY_ExtHoldingPrice'] = str(py_p1HoldPrice)
            p1row['CY_ExtHoldingPrice'] = str(p1hp*p1Ext/100)
            p1row['PY_ContigencyCost'] = str(py_p1Cost)
            p1row['CY_ContigencyCost'] = str(p1Cost) if p1Qty > 0 else '0'
            py_p1unitprice = py_p1HoldPrice/py_p1Qty if py_p1Qty != 0 else 0
            cy_p1unitprice = (p1hp*p1Ext/100)/p1Qty if p1Qty != 0 else 0
            py_discount = float(compdictwithdiscount.get(p1row["Service_Product"],0))
            p1row['PY_Discount'] = str(py_discount * 100)
            if active_contract and prev_quote in ("None",""):
                p1row['PY_SellPrice'] = str(py_p1SellPrice)
            else:
                p1row["PY_SellPrice"] = str(float(p1row['PY_ExtHoldingPrice']) - (float(p1row['PY_ExtHoldingPrice']) * py_discount))
            costFactor = SqlHelper.GetFirst("select Value from SC_HARDCODE_VALUES where Name = 'Parts Holding P1'")
            if costFactor is not None:
                p1row['PY_TotalCost'] = str(float(compdict.get("Parts Holding P1","0")) + eval(p1row['PY_ContigencyCost']))
                p1row['CY_TotalCost'] = str((eval(p1row['CY_ExtPrice'])*eval(costFactor.Value))/100 + eval(p1row['CY_ContigencyCost'])) if p1Qty > 0 else '0'
            if p1Qty > py_p1Qty:
                p1row['SA_Quantity'] = str(p1Qty-py_p1Qty)
                p1row['SR_Quantity'] = "0"
                p1row['Escalation_Price'] = str(py_p1Qty*(eval(p1row['PY_ExtHoldingPrice'])/py_p1Qty)) if py_p1Qty != 0 else "0"
                p1row['Comments'] ="Scope Addition"
            elif p1Qty < py_p1Qty:
                p1row['SA_Quantity'] = "0"
                p1row['SR_Quantity'] = str(p1Qty-py_p1Qty)
                p1row['Escalation_Price'] = str(p1Qty*(eval(p1row['PY_ExtHoldingPrice'])/py_p1Qty)) if py_p1Qty != 0 else "0"
                p1row['Comments'] ="Scope Reduction"
            else:
                p1row['SA_Quantity'] = "0"
                p1row['SR_Quantity'] = "0"
                p1row['Escalation_Price'] = str(py_p1Qty*(eval(p1row['PY_ExtHoldingPrice'])/py_p1Qty)) if py_p1Qty != 0 else "0"
                p1row['Comments'] ="No Scope Change"
            if Product.Attr('SC_Pricing_Escalation').GetValue() == "Yes":
                if int(p1row['CY_Quantity']) > int(p1row['PY_Quantity']):
                    p1row['Ext_Holding_Price'] = str((float(p1row['PY_Quantity'])*py_p1unitprice) + ((int(p1row['CY_Quantity']) - int(p1row['PY_Quantity']))*cy_p1unitprice))
                else:
                    p1row['Ext_Holding_Price'] = str(float(p1row['CY_Quantity'])*py_p1unitprice)
            else:
                p1row['Escalation_Price'] = '0'
                p1row['Ext_Holding_Price'] = p1row['CY_ExtHoldingPrice']
            p1row['SR_Price'] = str((eval(p1row['PY_ExtHoldingPrice'])/py_p1Qty)*eval(p1row['SR_Quantity'])) if py_p1Qty != 0 else "0"
            p1row['SA_Price'] = str((eval(p1row['CY_ExtHoldingPrice'])/p1Qty)*eval(p1row['SA_Quantity'])) if p1Qty != 0 else "0"
            p1row['ProductCode'] = prodDist[p1row['Service_Product']]
            p1row.Calculate()

        if p1hotQty != 0 or py_p1hotQty != 0:
            p1hotrow = summaryCont.AddNewRow(False)
            p1hotrow['Service_Product'] = 'Parts Holding P1 Hot'
            p1hotrow['Holding_Percentage'] = str(p1hothp)
            p1hotrow['PY_Quantity'] = str(py_p1hotQty)
            p1hotrow['CY_Quantity'] = str(p1hotQty)
            p1hotrow['PY_ExtPrice'] = str(py_p1hotExt)
            p1hotrow['CY_ExtPrice'] = str(p1hotExt)
            p1hotrow['PY_ExtHoldingPrice'] = str(py_p1hotHoldPrice)
            p1hotrow['CY_ExtHoldingPrice'] = str(p1hothp*p1hotExt/100)
            p1hotrow['PY_ContigencyCost'] = str(py_p1hotCost)
            p1hotrow['CY_ContigencyCost'] = str(p1hotCost) if p1hotQty > 0 else '0'
            py_p1hotunitprice = py_p1hotHoldPrice/py_p1hotQty if py_p1hotQty != 0 else 0
            cy_p1hotunitprice = (p1hothp*p1hotExt/100)/p1hotQty if p1hotQty != 0 else 0
            py_discount = float(compdictwithdiscount.get(p1hotrow["Service_Product"],0))
            p1hotrow['PY_Discount'] = str(py_discount * 100)
            if active_contract and prev_quote in ("None",""):
                p1hotrow['PY_SellPrice'] = str(py_p1hotSellPrice)
            else:
                p1hotrow["PY_SellPrice"] = str(float(p1hotrow['PY_ExtHoldingPrice']) - (float(p1hotrow['PY_ExtHoldingPrice']) * py_discount))
            costFactor = SqlHelper.GetFirst("select Value from SC_HARDCODE_VALUES where Name = 'Parts Holding P1 Hot'")
            if costFactor is not None:
                p1hotrow['PY_TotalCost'] = str(float(compdict.get("Parts Holding P1 Hot","0")) + eval(p1hotrow['PY_ContigencyCost']))
                p1hotrow['CY_TotalCost'] = str((eval(p1hotrow['CY_ExtPrice'])*eval(costFactor.Value))/100 + eval(p1hotrow['CY_ContigencyCost'])) if p1hotQty > 0 else '0'
            if p1hotQty > py_p1hotQty:
                p1hotrow['SA_Quantity'] = str(p1hotQty-py_p1hotQty)
                p1hotrow['SR_Quantity'] = "0"
                p1hotrow['Escalation_Price'] = str(py_p1hotQty*(eval(p1hotrow['PY_ExtHoldingPrice'])/py_p1hotQty)) if py_p1hotQty != 0 else "0"
                p1hotrow['Comments'] ="Scope Addition"
            elif p1hotQty < py_p1hotQty:
                p1hotrow['SA_Quantity'] = "0"
                p1hotrow['SR_Quantity'] = str(p1hotQty-py_p1hotQty)
                p1hotrow['Escalation_Price'] = str(p1hotQty*(eval(p1hotrow['PY_ExtHoldingPrice'])/py_p1hotQty)) if py_p1hotQty != 0 else "0"
                p1hotrow['Comments'] ="Scope Reduction"
            else:
                p1hotrow['SA_Quantity'] = "0"
                p1hotrow['SR_Quantity'] = "0"
                p1hotrow['Escalation_Price'] = str(py_p1hotQty*(eval(p1hotrow['PY_ExtHoldingPrice'])/p1hotQty)) if py_p1hotQty != 0 else "0"
                p1hotrow['Comments'] ="No Scope Change"
            if Product.Attr('SC_Pricing_Escalation').GetValue() == "Yes":
                if int(p1hotrow['CY_Quantity']) > int(p1hotrow['PY_Quantity']):
                    p1hotrow['Ext_Holding_Price'] = str((float(p1hotrow['PY_Quantity'])*py_p1hotunitprice) + ((int(p1hotrow['CY_Quantity']) - int(p1hotrow['PY_Quantity']))*cy_p1hotunitprice))
                else:
                    p1hotrow['Ext_Holding_Price'] = str(float(p1hotrow['CY_Quantity'])*py_p1hotunitprice)
            else:
                p1hotrow['Escalation_Price'] = '0'
                p1hotrow['Ext_Holding_Price'] = p1hotrow['CY_ExtHoldingPrice']
            p1hotrow['SR_Price'] = str((eval(p1hotrow['PY_ExtHoldingPrice'])/py_p1hotQty)*eval(p1hotrow['SR_Quantity'])) if py_p1hotQty != 0 else "0"
            p1hotrow['SA_Price'] = str((eval(p1hotrow['CY_ExtHoldingPrice'])/p1hotQty)*eval(p1hotrow['SA_Quantity'])) if p1hotQty != 0 else "0"
            p1hotrow['ProductCode'] = prodDist[p1hotrow['Service_Product']]
            p1hotrow.Calculate()

        if p2Qty != 0 or py_p2Qty != 0:
            p2row = summaryCont.AddNewRow(False)
            p2row['Service_Product'] = 'Parts Holding P2'
            p2row['Holding_Percentage'] = str(p2hp)
            p2row['PY_Quantity'] = str(py_p2Qty)
            p2row['CY_Quantity'] = str(p2Qty)
            p2row['PY_ExtPrice'] = str(py_p2Ext)
            p2row['CY_ExtPrice'] = str(p2Ext)
            p2row['PY_ExtHoldingPrice'] = str(py_p2HoldPrice)
            p2row['CY_ExtHoldingPrice'] = str(p2hp*p2Ext/100)
            p2row['PY_ContigencyCost'] = str(py_p2Cost)
            p2row['CY_ContigencyCost'] = str(p2Cost) if p2Qty > 0 else '0'
            py_discount = float(compdictwithdiscount.get(p2row["Service_Product"],0))
            p2row['PY_Discount'] = str(py_discount * 100)
            py_p2unitprice = py_p2HoldPrice/py_p2Qty if py_p2Qty != 0 else 0
            cy_p2unitprice = (p2hp*p2Ext/100)/p2Qty if p2Qty != 0 else 0
            if active_contract and prev_quote in ("None",""):
                p2row['PY_SellPrice'] = str(py_p2SellPrice)
            else:
                p2row["PY_SellPrice"] = str(float(p2row['PY_ExtHoldingPrice']) - (float(p2row['PY_ExtHoldingPrice']) * py_discount))
            costFactor = SqlHelper.GetFirst("select Value from SC_HARDCODE_VALUES where Name = 'Parts Holding P2'")
            if costFactor is not None:
                p2row['PY_TotalCost'] = str(float(compdict.get("Parts Holding P2","0")) + eval(p2row['PY_ContigencyCost']))
                p2row['CY_TotalCost'] = str((eval(p2row['CY_ExtPrice'])*eval(costFactor.Value))/100 + eval(p2row['CY_ContigencyCost'])) if p2Qty > 0 else '0'
            if p2Qty > py_p2Qty:
                p2row['SA_Quantity'] = str(p2Qty-py_p2Qty)
                p2row['SR_Quantity'] = "0"
                p2row['Escalation_Price'] = str(py_p2Qty*(eval(p2row['PY_ExtHoldingPrice'])/py_p2Qty)) if py_p2Qty != 0 else "0"
                p2row['Comments'] ="Scope Addition"
            elif p2Qty < py_p2Qty:
                p2row['SA_Quantity'] = "0"
                p2row['SR_Quantity'] = str(p2Qty-py_p2Qty)
                p2row['Escalation_Price'] = str(p2Qty*(eval(p2row['PY_ExtHoldingPrice'])/py_p2Qty)) if py_p2Qty != 0 else "0"
                p2row['Comments'] ="Scope Reduction"
            else:
                p2row['SA_Quantity'] = "0"
                p2row['SR_Quantity'] = "0"
                p2row['Escalation_Price'] = str(py_p2Qty*(eval(p2row['PY_ExtHoldingPrice'])/py_p2Qty)) if py_p2Qty != 0 else "0"
                p2row['Comments'] ="No Scope Change"
            if Product.Attr('SC_Pricing_Escalation').GetValue() == "Yes":
                if int(p2row['CY_Quantity']) > int(p2row['PY_Quantity']):
                    p2row['Ext_Holding_Price'] = str((float(p2row['PY_Quantity'])*py_p2unitprice) + ((int(p2row['CY_Quantity']) - int(p2row['PY_Quantity']))*cy_p2unitprice))
                else:
                    p2row['Ext_Holding_Price'] = str(float(p2row['CY_Quantity'])*py_p2unitprice)
            else:
                p2row['Escalation_Price'] = '0'
                p2row['Ext_Holding_Price'] = p2row['CY_ExtHoldingPrice']
            p2row['SR_Price'] = str((eval(p2row['PY_ExtHoldingPrice'])/py_p2Qty)*eval(p2row['SR_Quantity'])) if py_p2Qty != 0 else "0"
            p2row['SA_Price'] = str((eval(p2row['CY_ExtHoldingPrice'])/p2Qty)*eval(p2row['SA_Quantity'])) if p2Qty != 0 else "0"
            p2row['ProductCode'] = prodDist[p2row['Service_Product']]
            p2row.Calculate()
        summaryCont.Calculate()

        replacementCont = Product.GetContainerByName('SC_P1P2_Parts_Replacement_Summary')
        replacementCont.Rows.Clear()
        py_pr_listPrice = 0
        SC_ScopeRemoval = eval(Product.Attr('SC_ScopeRemoval').GetValue()) if Product.Attr('SC_ScopeRemoval').GetValue() != '' else '[]'
        if Product.Attr('SC_P1P2_PartsUsageMethod').GetValue() == "1 Year Pricing":
            row = replacementCont.AddNewRow(False)
            row['Service_Product'] = "Parts Replacement"
            row['Pricing_Method'] = "1 Year Pricing"
            row['Fee_Percentage'] = Product.Attr('SC_P1P2_Fee_Percentage').GetValue()
            row['PY_ExtPrice'] = Product.Attr('SC_P1P2_PY_Parts_Ext_Price').GetValue() if Product.Attr('SC_P1P2_PY_Parts_Ext_Price').GetValue() != "" else "0"
            row['PY_ListPrice'] = Product.Attr('SC_P1P2_PY_ListPrice').GetValue() if Product.Attr('SC_P1P2_PY_ListPrice').GetValue() != "" else "0"
            row['CY_ExtPrice'] = Product.Attr('SC_P1P2_Parts_Ext_Price').GetValue() if Product.Attr('SC_P1P2_Parts_Ext_Price').GetValue() != "" else "0"
            if row['Service_Product'] not in SC_ScopeRemoval:
                row['CY_ListPrice'] = Product.Attr('SC_P1P2_ListPrice').GetValue() if Product.Attr('SC_P1P2_ListPrice').GetValue() != "" else "0"
                row['List_Price'] = Product.Attr('SC_P1P2_ListPrice').GetValue() if Product.Attr('SC_P1P2_ListPrice').GetValue() != "" else "0"
            else:
                row['CY_ListPrice'] = '0'
                row['List_Price'] = '0'
            row['Scope_Change'] = Product.Attr('SC_P1P2_ScopeChange').GetValue() if Product.Attr('SC_P1P2_ScopeChange').GetValue() != "" else "0"
            if float(row['CY_ListPrice'] ) > float(row['PY_ListPrice']):
                row["Comments"] = "Scope Addition"
            elif float(row['CY_ListPrice'] ) < float(row['PY_ListPrice']):
                row["Comments"] = "Scope Reduction"
            else:
                row["Comments"] = "No Scope Change"
            row['ProductCode'] = prodDist[row['Service_Product']]
            py_pr_listPrice = float(row['PY_ListPrice'])
            py_discount = float(compdictwithdiscount.get(row["Service_Product"],0))
            row["PY_Discount"] = str(py_discount * 100)
            row["PY_SellPrice"] = str(float(row['PY_ListPrice']) - (float(row['PY_ListPrice']) * py_discount))
        elif Product.Attr('SC_P1P2_PartsUsageMethod').GetValue() == "List Price with Discount Applied":
            row = replacementCont.AddNewRow(False)
            row['Service_Product'] = "Parts Replacement"
            row['Pricing_Method'] = "List Price with Discount Applied"
            row['Fee_Percentage'] = "NA"
            row['PY_ListPrice'] = Product.Attr('SC_P1P2_LPDA_PY_ListPrice').GetValue() if Product.Attr('SC_P1P2_LPDA_PY_ListPrice').GetValue() != "" else "0"
            if row['Service_Product'] not in SC_ScopeRemoval:
                row['CY_ListPrice'] = Product.Attr('SC_P1P2_LPDA_CY_FinalListPrice').GetValue() if Product.Attr('SC_P1P2_LPDA_CY_FinalListPrice').GetValue() != "" else "0"
                row['List_Price'] = Product.Attr('SC_P1P2_LPDA_CY_FinalListPrice').GetValue() if Product.Attr('SC_P1P2_LPDA_CY_FinalListPrice').GetValue() != "" else "0"
            else:
                row['CY_ListPrice'] = '0'
                row['List_Price'] = '0'
            row['Scope_Change'] = Product.Attr('SC_P1P2_LPDA_ScopeChange').GetValue() if Product.Attr('SC_P1P2_LPDA_ScopeChange').GetValue() != "" else "0"
            if float(row['CY_ListPrice'] ) > float(row['PY_ListPrice']):
                row["Comments"] = "Scope Addition"
            elif float(row['CY_ListPrice'] ) < float(row['PY_ListPrice']):
                row["Comments"] = "Scope Reduction"
            else:
                row["Comments"] = "No Scope Change"
            row['ProductCode'] = prodDist[row['Service_Product']]
            py_pr_listPrice = float(row['PY_ListPrice'])
            py_discount = float(compdictwithdiscount.get(row["Service_Product"],0))
            row["PY_Discount"] = str(py_discount * 100)
            row["PY_SellPrice"] = str(float(row['PY_ListPrice']) - (float(row['PY_ListPrice']) * py_discount))
        elif Product.Attr('SC_P1P2_PartsUsageMethod').GetValue() == "Last 3 Year Average":
            row = replacementCont.AddNewRow(False)
            row['Service_Product'] = "Parts Replacement"
            row['Pricing_Method'] = "Last 3 Year Average"
            row['Fee_Percentage'] = "NA"
            row['PY_ListPrice'] = Product.Attr('SC_P1P2_LTYA_PY_ListPrice').GetValue() if Product.Attr('SC_P1P2_LTYA_PY_ListPrice').GetValue() != "" else "0"
            if row['Service_Product'] not in SC_ScopeRemoval:
                row['CY_ListPrice'] = Product.Attr('SC_P1P2_LTYA_CY_FinalListPrice').GetValue() if Product.Attr('SC_P1P2_LTYA_CY_FinalListPrice').GetValue() != "" else "0"
                row['List_Price'] = Product.Attr('SC_P1P2_LTYA_CY_FinalListPrice').GetValue() if Product.Attr('SC_P1P2_LTYA_CY_FinalListPrice').GetValue() != "" else "0"
            else:
                row['CY_ListPrice'] = '0'
                row['List_Price'] = '0'
            row['Scope_Change'] = Product.Attr('SC_P1P2_LTYA_ScopeChange').GetValue() if Product.Attr('SC_P1P2_LTYA_ScopeChange').GetValue() != "" else "0"
            if float(row['CY_ListPrice'] ) > float(row['PY_ListPrice']):
                row["Comments"] = "Scope Addition"
            elif float(row['CY_ListPrice'] ) < float(row['PY_ListPrice']):
                row["Comments"] = "Scope Reduction"
            else:
                row["Comments"] = "No Scope Change"
            row['ProductCode'] = prodDist[row['Service_Product']]
            py_pr_listPrice = float(row['PY_ListPrice'])
            py_discount = float(compdictwithdiscount.get(row["Service_Product"],0))
            row["PY_Discount"] = str(py_discount * 100)
            row["PY_SellPrice"] = str(float(row['PY_ListPrice']) - (float(row['PY_ListPrice']) * py_discount))
        replacementCont.Calculate()
        Product.ApplyRules()

        sp_dict = {}
        partDetCont = Product.GetContainerByName('SC_P1P2_Parts_Details')
        if partDetCont.Rows.Count:
            for row in partDetCont.Rows:
                row['PY_HoldingFeeListPrice'] = row['PY_HoldingFeeListPrice'] if row['PY_HoldingFeeListPrice'] != "" else '0'
                row['PY_HoldingFeeSellPrice'] = row['PY_HoldingFeeSellPrice'] if row['PY_HoldingFeeSellPrice'] != "" else '0'
                if row['Service_Product'] not in sp_dict.keys():
                    sp_dict[row['Service_Product']] = [str(float(row['PY_HoldingFeeListPrice'])),str(float(row['PY_HoldingFeeSellPrice']))]

                else:
                    lp = str(float(row['PY_HoldingFeeListPrice']) + float(sp_dict.get(row['Service_Product'])[0]))
                    sp = str(float(row['PY_HoldingFeeSellPrice']) + float(sp_dict.get(row['Service_Product'])[1]))
                    sp_dict[row['Service_Product']] = [lp,sp]

        ComparisonCont = Product.GetContainerByName('ComparisonSummary')
        if ComparisonCont.Rows.Count:
            for row in ComparisonCont.Rows:
                if row['Service_Product'] == "Parts Replacement":
                    row["Configured_PY_List_Price"] = str(py_pr_listPrice)
                    row['Configured_PY_Sell_Price'] = str(float(row['Configured_PY_List_Price']) - (float(row['Configured_PY_List_Price']) * float(row['PY_Discount_SFDC']))) if row['PY_Discount_SFDC'] else str(float(row['Configured_PY_List_Price']))
                else:
                    if row['Service_Product'] in sp_dict.keys():
                        row['Configured_PY_List_Price'] = sp_dict.get(row['Service_Product'])[0]
                        if active_contract and prev_quote in ("None",""):
                            row['Configured_PY_Sell_Price'] = sp_dict.get(row['Service_Product'])[1]
                        else:
                            row['Configured_PY_Sell_Price'] = str(float(row['Configured_PY_List_Price']) - (float(row['Configured_PY_List_Price']) * float(row['PY_Discount_SFDC']))) if row['PY_Discount_SFDC'] else str(float(row['Configured_PY_List_Price']))
                    elif row['Service_Product'] not in sp_dict.keys():
                        row['Configured_PY_List_Price'] = '0'
                        row['Configured_PY_Sell_Price'] = '0'
                row.Calculate()
            ComparisonCont.Calculate()