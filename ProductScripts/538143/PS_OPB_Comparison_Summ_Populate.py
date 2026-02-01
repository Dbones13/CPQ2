#Quote Headers
Contract_Number = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
Product_type = Product.Attr('SC_Product_Type').GetValue()
Quote_Number = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
if Product_type == 'Renewal': #and Quote_Number in [None,''] and Contract_Number not in [None, '']:
    Model_Scope = Product.GetContainerByName("SC_Experion_Models_Scope")
    Comp_summ = Product.GetContainerByName("ComparisonSummary")
    Discount = 0
    SP_listPrice = {}
    Total_PY_ListPrice = 0
    if Model_Scope.Rows.Count:
        for row in Model_Scope.Rows:
            Total_PY_ListPrice += float(row["PY_ListPrice"]) if row["PY_ListPrice"] != '' else 0
    #Trace.Write(str(SP_listPrice))

    if Comp_summ.Rows.Count:
        for com_row in Comp_summ.Rows:
            if Total_PY_ListPrice > 0:
                com_row["Configured_PY_List_Price"] = str(Total_PY_ListPrice)
                com_row['Configured_PY_Sell_Price'] = str(float(com_row['Configured_PY_List_Price']) - (float(com_row['Configured_PY_List_Price']) * float(com_row['PY_Discount_SFDC']))) if com_row['PY_Discount_SFDC'] else str(float(com_row['Configured_PY_List_Price']))
            else:
                com_row["Configured_PY_List_Price"] = com_row["PY_List_Price_SFDC"]
                com_row["Configured_PY_Sell_Price"] = com_row["PY_Sell_Price_SFDC"]
            com_row.Calculate()
'''
    #PY sell price code
    if Comp_summ.Rows.Count:
        for row in Comp_summ.Rows:
            discount_percent = ((float(row['PY_List_Price_SFDC']) - float(row['PY_Sell_Price_SFDC']))/float(row['PY_List_Price_SFDC']) if float(row['PY_List_Price_SFDC']) != '' else 0)
            Discount = discount_percent
    if Model_Scope.Rows.Count:
        for hrow in Model_Scope.Rows:
            discount = str(Discount)
            hrow['LY_Discount'] = discount
            hrow['PY_SellPrice'] = str(float(hrow['PY_ListPrice']) - (float(hrow['PY_ListPrice']) * float(discount)))
ScriptExecutor.Execute('PS_SC_Load_Model_Summary')'''