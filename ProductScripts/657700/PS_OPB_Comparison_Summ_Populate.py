#Quote Headers
Contract_Number = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
Product_type = Product.Attr('SC_Product_Type').GetValue()
Quote_Number = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
if Product_type == 'Renewal': #and Quote_Number in [None,''] and Contract_Number not in [None, '']:
    Model_Scope = Product.GetContainerByName("SC_GN_AT_Models_Scope_Cont")
    Comp_summ = Product.GetContainerByName("ComparisonSummary")
    SP_Discount = {}
    SP_listPrice = {}
    SP_Discount_Cy = {}
    if Model_Scope.Rows.Count:
        for row in Model_Scope.Rows:
            SP_listPrice[row["Service_Product"]] = SP_listPrice.get(row["Service_Product"],0) + float(row["PY_ListPrice"])
    #Trace.Write(str(SP_listPrice))

    if Comp_summ.Rows.Count:
        for com_row in Comp_summ.Rows:
            if com_row["Service_Product"] in SP_listPrice.Keys and SP_listPrice[com_row["Service_Product"]] not in [0,0.0,'']:
                com_row["Configured_PY_List_Price"] = str(SP_listPrice[com_row["Service_Product"]])
                com_row['Configured_PY_Sell_Price'] = str(float(com_row['Configured_PY_List_Price']) - (float(com_row['Configured_PY_List_Price']) * float(com_row['PY_Discount_SFDC']))) if com_row['PY_Discount_SFDC'] else str(float(com_row['Configured_PY_List_Price']))
            elif com_row["CY_Service_Product"] in SP_listPrice.Keys and SP_listPrice[com_row["CY_Service_Product"]] not in ['']:
                com_row["Configured_PY_List_Price"] = str(SP_listPrice[com_row["CY_Service_Product"]])
                com_row["Configured_PY_Sell_Price"] = str(float(com_row['Configured_PY_List_Price']) - (float(com_row['Configured_PY_List_Price']) * float(com_row['PY_Discount_SFDC']))) if com_row['PY_Discount_SFDC'] else str(float(com_row['Configured_PY_List_Price']))
            else:
                com_row["Configured_PY_List_Price"] = com_row["PY_List_Price_SFDC"]
                com_row["Configured_PY_Sell_Price"] = com_row["PY_Sell_Price_SFDC"]
            com_row.Calculate()

    #PY sell price code
    if Comp_summ.Rows.Count:
        for row in Comp_summ.Rows:
            if row['PY_Sell_Price_SFDC'] == "" :
                row['PY_Sell_Price_SFDC'] = "0"
            discount_percent = ((float(row['PY_List_Price_SFDC']) - float(row['PY_Sell_Price_SFDC']))/float(row['PY_List_Price_SFDC']) if float(row['PY_List_Price_SFDC']) != '' else 0)
            SP_Discount[row['Service_Product']] = discount_percent
            SP_Discount_Cy[row['CY_Service_Product']] = discount_percent
    if Model_Scope.Rows.Count:
        for hrow in Model_Scope.Rows:
            if hrow['Service_Product'] in SP_Discount.Keys:
                discount = SP_Discount[hrow['Service_Product']]
                hrow['PY_Discount'] = str(discount)
                hrow['PY_SellPrice'] = str(float(hrow['PY_ListPrice']) - (float(hrow['PY_ListPrice']) * float(discount)))
            elif hrow['Service_Product'] in SP_Discount_Cy.Keys:
                discount = SP_Discount_Cy[hrow['Service_Product']]
                hrow['PY_Discount'] = str(discount)
                hrow['PY_SellPrice'] = str(float(hrow['PY_ListPrice']) - (float(hrow['PY_ListPrice']) * discount))
            else:
                hrow['PY_SellPrice'] = "0"
ScriptExecutor.Execute('PS_GN_Scope_Summary')