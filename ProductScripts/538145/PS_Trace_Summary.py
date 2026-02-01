if Product.Attr('SC_Product_Type').GetValue() == "New":
    tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
    licenseType = Product.Attr("SC_License_type").GetValue()

    if 'Scope Summary' in tabs:
        modelCode = Product.Attr("SC_Trace_Backend_String").GetValue()
        from GS_CostAPI_Module import gen_Item_PayLoad, getCost, getAccessToken, getHost
        from GS_LSG_Pricing import GetListPriceFromCPS
        hostname = getHost()

        if licenseType == "Term":
            ##### COST #####
            responseToken = getAccessToken(hostname)
            responsePayload = gen_Item_PayLoad(Quote,"AS-UTRACS",modelCode)
            try:
                _responseCost = getCost(Quote, responseToken, responsePayload)
            except:
                _responseCost = None
            responseCost = ''
            if _responseCost is not None and _responseCost['vcMaterialCostResponse'] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse'] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse']["item"] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse']["item"][0] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse']["item"][0]['totalCost'] is not None:
                responseCost = str(_responseCost['vcMaterialCostResponse']['vcCostResponse']["item"][0]['totalCost'])
                Trace.Write("COST ------>" + str(responseCost))
            else:
                responseCost = '0.00'

        ###### PRICE ######
        partNumberList =[]
        _dict = {modelCode:'AS-UTRACS'}
        partNumberList.append(_dict)
        try:
            _responsePrice = GetListPriceFromCPS(Quote, partNumberList, ProductHelper, TagParserQuote,hostname)
        except:
            _responsePrice = None
        responsePrice = ''
        if _responsePrice != None and _responsePrice != '':
            responsePrice = str(_responsePrice)
            Trace.Write("PRICE ------>" + str(_responsePrice))
        else:
            responsePrice = '0.00'

    if 'Scope Summary' in tabs:
        Trace_Summary = Product.GetContainerByName("SC_Trace_Summary")
        Trace_Summary.Rows.Clear()
        pmultiplier = 0.00
        tmultiplier = 0.00
        price = float(responsePrice) #price from SAP
        if licenseType == "Term":
            cost = float(responseCost) #cost from SAP

        if licenseType == "Perpetual":
            supportYears = Product.Attr("SC_Years_of_Support").GetValue()
            if supportYears == "1":
                pmultiplier = 0.20
            elif supportYears == "2":
                pmultiplier = 0.18
            elif supportYears == "3":
                pmultiplier = 0.16
            row = Trace_Summary.AddNewRow(False)
            row["Service_Product"] = "Trace Software Support"
            row["Quantity"] = "1"
            row["Unit_Price"] = str(price)
            row["UI_Price"] = str(eval(row["Unit_Price"])*pmultiplier)
            row["Unit_Cost"] = str(eval(row["Unit_Price"])*pmultiplier*0.40)
            row.Calculate()
            Product.Attr('SC_Trace_CY_ListPrice').AssignValue(str(eval(row["UI_Price"]) * eval(row["Quantity"])))
            Product.Attr('SC_Trace_CY_CostPrice').AssignValue(str(eval(row["Unit_Cost"]) * eval(row["Quantity"])))
        elif licenseType == "Term":
            licenseYears = Product.Attr("SC_License_period_Year").GetValue()
            for i in range(0,int(licenseYears)):
                row = Trace_Summary.AddNewRow(False)
                row["Service_Product"] = "Trace Subscription Service"
                row["Quantity"] = "1"
                row["Year"] = str(i+1)
                row["Unit_Price"] = str(price)
                if i == 0:
                    row["UI_Price"] = str(price)
                    row["Unit_Cost"] = str(cost)
                else:
                    row["UI_Price"] = str(eval(escalatedprice) + 0.05*eval(escalatedprice))
                    row["Unit_Cost"] = str(eval(escalatedcost) + 0.05*eval(escalatedcost))
                
                escalatedprice = row["UI_Price"]
                escalatedcost = row["Unit_Cost"]
                row.Calculate()
        Trace_Summary.Calculate()

if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
    licenseType = Product.Attr("SC_License_type").GetValue()

    if 'Scope Summary' in tabs:
        modelCode = Product.Attr("SC_Trace_Backend_String").GetValue()
        from GS_CostAPI_Module import gen_Item_PayLoad, getCost, getAccessToken, getHost
        from GS_LSG_Pricing import GetListPriceFromCPS
        hostname = getHost()

        ###### PRICE ######
        partNumberList =[]
        _dict = {modelCode:'AS-UTRACS'}
        partNumberList.append(_dict)
        try:
            _responsePrice = GetListPriceFromCPS(Quote, partNumberList, ProductHelper, TagParserQuote,hostname)
        except:
            _responsePrice = None
        responsePrice = ''
        if _responsePrice != None and _responsePrice != '':
            responsePrice = str(_responsePrice)
            Trace.Write("PRICE ------>" + str(_responsePrice))
        else:
            responsePrice = '0.00'

    if 'Scope Summary' in tabs:
        Trace_Summary = Product.GetContainerByName("SC_Trace_Summary")
        Trace_Summary.Rows.Clear()
        pmultiplier = 0.00
        tmultiplier = 0.00
        price = float(responsePrice) #price from SAP
        SC_Pricing_Escalation = Product.Attr('SC_Pricing_Escalation').GetValue()

        comparisonCont = Product.GetContainerByName('ComparisonSummary')
        compDict = {}
        PY_List_Price_SFDC = 0
        if comparisonCont.Rows.Count:
            for compRow in comparisonCont.Rows:
                compDict[compRow["Service_Product"]] = compRow["PY_Discount_SFDC"] if compRow["PY_Discount_SFDC"] else '0'
                PY_List_Price_SFDC = compRow['PY_List_Price_SFDC']

        prev_cost = '0'
        prev_list = '0'
        reference_number = Quote.GetCustomField("SC_CF_PREVIOUS_QUOTE_NO").Content
        query = SqlHelper.GetFirst("Select Product,QuoteDetails from CT_SC_RENEWAL_QUOTE_TABLE where QuoteID = '{}' and Product = '{}'".format(reference_number,'Trace'))
        if query is not None:
            quote_details = eval(query.QuoteDetails)
            key = 'Year-1|Trace Service|Trace Subscription Service'
            if key in quote_details.keys():
                prev_cost = quote_details[key]['Cost_Price']
                prev_cost = prev_cost[4:]
                prev_list = quote_details[key]['ListPrice']


        if licenseType == "Perpetual":
            supportYears = Product.Attr("SC_Years_of_Support").GetValue()
            if supportYears == "1":
                pmultiplier = 0.20
            elif supportYears == "2":
                pmultiplier = 0.18
            elif supportYears == "3":
                pmultiplier = 0.16
            row = Trace_Summary.AddNewRow(False)
            row["Service_Product"] = "Trace Software Support"
            if Product.Attr('SC_ScopeRemoval').GetValue() == "True":
                row["Quantity"] = "0"
            else:
                row["Quantity"] = "1"
            row["Unit_Price"] = str(price)
            row["UI_Price"] = str(eval(row["Unit_Price"])*pmultiplier)
            Trace.Write('check1'+str(row["UI_Price"]))
            row["Unit_Cost"] = str(eval(row["Unit_Price"])*pmultiplier*0.40)

            if Product.Attr('SC_License_type_PY').GetValue() == "Perpetual":
                row['PY_ListPrice'] = Product.Attr('SC_Trace_PY_ListPrice').GetValue() if Product.Attr('SC_Trace_PY_ListPrice').GetValue() != "" else '0'
                row['PY_CostPrice'] = Product.Attr('SC_Trace_PY_CostPrice').GetValue() if Product.Attr('SC_Trace_PY_CostPrice').GetValue() != "" else '0'
                if Product.Attr('SC_Trace_PYListPrice').GetValue() != "":
                    row['PY_ListPrice'] = Product.Attr('SC_Trace_PYListPrice').GetValue()
                if Product.Attr('SC_Trace_PYCostPrice').GetValue() != "":
                    row['PY_CostPrice'] = Product.Attr('SC_Trace_PYCostPrice').GetValue()
                if eval(row['PY_ListPrice']) > (eval(row["UI_Price"]) * eval(row["Quantity"])):
                    row['SR_Price'] = str((eval(row["UI_Price"]) * eval(row["Quantity"])) - eval(row['PY_ListPrice']))
                    row['Comments'] = 'Scope Reduction'
                else:
                    row['SR_Price'] = '0'
                if eval(row['PY_ListPrice']) < (eval(row["UI_Price"]) * eval(row["Quantity"])):
                    row['SA_Price'] = str((eval(row["UI_Price"]) * eval(row["Quantity"])) - eval(row['PY_ListPrice']))
                    row['Comments'] = 'Scope Addition'
                else:
                    row['SA_Price'] = '0'
                if eval(row['PY_ListPrice']) == (eval(row["UI_Price"]) * eval(row["Quantity"])):
                    row['Comments'] = 'No Scope Change'
                if SC_Pricing_Escalation == "Yes":
                    row['Escalation_Price'] = str(eval(row['PY_ListPrice']) * eval(row["Quantity"]))
                    row['List_Price'] = row['PY_ListPrice'] # as previous and current year quantity is always 1
                else:
                    row['Escalation_Price'] = '0'
                    row['List_Price'] = row['CY_ListPrice']
                py_discount = float(compDict.get(row["Service_Product"],0))
                row["PY_Discount"] = str(py_discount * 100)
                if row['PY_ListPrice'] not in ('',0,'0','0.00',0.00):
                    row["PY_SellPrice"] = str(float(row['PY_ListPrice']) - (float(row['PY_ListPrice']) * py_discount))
                else:
                    row["PY_SellPrice"] = PY_List_Price_SFDC
            elif Product.Attr('SC_License_type_PY').GetValue() == "Term":
                if Product.Attr('SC_Trace_PYListPrice').GetValue() != "":
                    row['PY_ListPrice'] = Product.Attr('SC_Trace_PYListPrice').GetValue()
                else:
                    row['PY_ListPrice'] = prev_list
                row['Escalation_Price'] = str(eval(row['PY_ListPrice']) * eval(row["Quantity"]))
                if Product.Attr('SC_Trace_PYCostPrice').GetValue() != "":
                    row['PY_CostPrice'] = Product.Attr('SC_Trace_PYCostPrice').GetValue()
                else:
                    row['PY_CostPrice'] = prev_cost
                row['SR_Price'] = str(-eval(row['PY_ListPrice']))
                row['SA_Price'] = '0'
                row['Comments'] = 'Scope Reduction'
                Trace.Write('check2'+str(row['Comments']))
                if SC_Pricing_Escalation == "Yes":
                    row['Escalation_Price'] = str(eval(row['PY_ListPrice']) * eval(row["Quantity"]))
                    row['List_Price'] = row['PY_ListPrice'] # as previous and current year quantity is always 1
                else:
                    row['Escalation_Price'] = '0'
                    row['List_Price'] = row['CY_ListPrice']
                py_discount = float(compDict.get(row["Service_Product"],0))
                row["PY_Discount"] = str(py_discount * 100)
                if row['PY_ListPrice'] not in ('',0,'0','0.00',0.00):
                    row["PY_SellPrice"] = str(float(row['PY_ListPrice']) - (float(row['PY_ListPrice']) * py_discount))
                else:
                    row["PY_SellPrice"] = PY_List_Price_SFDC
            row.Calculate()
            Product.Attr('SC_Trace_CY_ListPrice').AssignValue(str(eval(row["UI_Price"]) * eval(row["Quantity"])))
            Product.Attr('SC_Trace_CY_CostPrice').AssignValue(str(eval(row["Unit_Cost"]) * eval(row["Quantity"])))
        Trace_Summary.Calculate()