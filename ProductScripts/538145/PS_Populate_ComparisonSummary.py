tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Scope Summary' in tabs and Product.Attr('SC_Product_Type').GetValue() == "Renewal":

    summaryCont = Product.GetContainerByName('SC_Trace_Summary')
    listPrice_PY = 0
    for row in summaryCont.Rows:
        listPrice_PY = float(row['PY_ListPrice']) if row['PY_ListPrice'] != "" else 0
    comparisonCont = Product.GetContainerByName('ComparisonSummary')

    if comparisonCont.Rows.Count:
        for row in comparisonCont.Rows:
            if listPrice_PY > 0:
                row["Configured_PY_List_Price"] = str(listPrice_PY)
            else:
                row["Configured_PY_List_Price"] = row["PY_List_Price_SFDC"]
            row["Configured_PY_Sell_Price"] = str(float(row['Configured_PY_List_Price']) - (float(row['Configured_PY_List_Price']) * float(row['PY_Discount_SFDC']))) if row['PY_Discount_SFDC'] else str(float(row['Configured_PY_List_Price']))
            row.Calculate()