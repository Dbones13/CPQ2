tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
UI_QCS_One_Time_Price = Product.Attr('UI_QCS_One_Time_Price').GetValue() if Product.Attr('UI_QCS_One_Time_Price').GetValue() != "" else "0"
#Trace.Write("UI_QCS_One_Time_Price "+str(UI_QCS_One_Time_Price))
if 'Scope Summary' in tabs:
    value1 = "0"
    value2 = "0"
    PY_ListPrice_QCS = 0
    PY_ListPrice_Support = 0
    SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
    if SC_Product_Type == 'Renewal':
        QCS_Cont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont_Hidden')
        if QCS_Cont.Rows.Count:
            for row in QCS_Cont.Rows:
                if row['Service Product'] == "QCS 4.0":
                    if row['PY_ListPrice'] in ("0.0","0",""):
                        value1 = "1"
                    else:
                        PY_ListPrice_QCS = row['PY_ListPrice']
                elif row['Service Product'] == "QCS Support Center":
                    if row['PY_ListPrice'] in ("0.0","0",""):
                        Trace.Write("QCS Support Center")
                        value2 = "2"
                    else:
                        PY_ListPrice_Support = row['PY_ListPrice']
        ComparisonSummary = Product.GetContainerByName("ComparisonSummary")
        if ComparisonSummary.Rows.Count:
            for row in ComparisonSummary.Rows:
                if row['Service_Product'] == "QCS 4.0" or row['CY_Service_Product'] == "QCS 4.0":
                    if value1 == "1":
                        row['Configured_PY_List_Price'] = row['PY_List_Price_SFDC']
                        row['Configured_PY_Sell_Price'] = row['PY_Sell_Price_SFDC']
                    else:
                        row['Configured_PY_List_Price'] = str(float(PY_ListPrice_QCS) + float(UI_QCS_One_Time_Price))
                        row['Configured_PY_Sell_Price'] = str(float(row['Configured_PY_List_Price']) - (float(row['Configured_PY_List_Price']) * float(row['PY_Discount_SFDC']))) if row['PY_Discount_SFDC'] else str(float(row['Configured_PY_List_Price']))
                elif row['Service_Product'] == "QCS Support Center" or row['CY_Service_Product'] == "QCS Support Center":
                    if value2 == "2":
                        row['Configured_PY_List_Price'] = row['PY_List_Price_SFDC']
                        row['Configured_PY_Sell_Price'] = row['PY_Sell_Price_SFDC']
                    else:
                        row['Configured_PY_List_Price'] = str(PY_ListPrice_Support)
                        row['Configured_PY_Sell_Price'] = str(float(row['Configured_PY_List_Price']) - (float(row['Configured_PY_List_Price']) * float(row['PY_Discount_SFDC']))) if row['PY_Discount_SFDC'] else str(float(row['Configured_PY_List_Price']))
                else:
                    row['Configured_PY_List_Price'] = row['PY_List_Price_SFDC']
                    row['Configured_PY_Sell_Price'] = row['PY_Sell_Price_SFDC']
                if row['Configured_PY_List_Price'] == "0":
                    row['Configured_PY_List_Price'] = row['PY_List_Price_SFDC']
                row.Calculate()
            ComparisonSummary.Calculate()
    #PY sell price code
    SP_Discount = {}
    SP_Discount_Cy = {}
    QCS_Cont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont_Hidden')
    ComparisonSummary = Product.GetContainerByName("ComparisonSummary")
    if ComparisonSummary.Rows.Count:
        for row in ComparisonSummary.Rows:
            if row['PY_Sell_Price_SFDC'] == "" :
                row['PY_Sell_Price_SFDC'] = "0"
            if row['PY_List_Price_SFDC'] == "":
                row['PY_List_Price_SFDC'] = "0"
            discount_percent = ((float(row['PY_List_Price_SFDC']) - float(row['PY_Sell_Price_SFDC']))/float(row['PY_List_Price_SFDC']) if float(row['PY_List_Price_SFDC']) != '' else 0)
            SP_Discount[row['Service_Product']] = discount_percent
            SP_Discount_Cy[row['CY_Service_Product']] = discount_percent
    if QCS_Cont.Rows.Count:
        for hrow in QCS_Cont.Rows:
            if hrow['Service Product'] in SP_Discount.Keys:
                discount = SP_Discount[hrow['Service Product']]
                hrow['PY_SellPrice'] = str(float(hrow['PY_ListPrice']) - (float(hrow['PY_ListPrice']) * discount)) if hrow['PY_ListPrice'] else "0"
                hrow['LY_Discount'] = str(discount)
            elif hrow['Service Product'] in SP_Discount_Cy.Keys:
                discount = SP_Discount_Cy[hrow['Service Product']]
                hrow['PY_SellPrice'] = str(float(hrow['PY_ListPrice']) - (float(hrow['PY_ListPrice']) * discount)) if hrow['PY_ListPrice'] else "0"
                hrow['LY_Discount'] = str(discount)
            Trace.Write("hrow['PY_SellPrice'] " +str(hrow['PY_SellPrice']))
SC_ScopeRemoval = Product.Attr('SC_ScopeRemoval').GetValue()
if "QCS Support Center" in SC_ScopeRemoval:
    Product.Attr('SC_QCS_No_Of_Machines').AssignValue("0")