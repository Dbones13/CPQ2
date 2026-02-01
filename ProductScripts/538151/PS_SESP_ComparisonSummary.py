PY_Coverage = Product.Attr('PY_SC_Coverage').GetValue()
#SC_Training_Match_Contract_Value = Product.Attr('SC_Training_Match_Contract_Value').GetValue()
SC_Training_Match_Contract_Value_PY =  Product.Attr('SC_Training_Match_Contract_Value_PY').GetValue()
tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Scope Summary' in tabs:
    SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
    Py_List_Price = Product.Attr('SESP_Py_List_Price').GetValue()
    Py_Sell_Price = Product.Attr('SESP_Py_Sell_Price').GetValue()
    Trace.Write("Py_List_Price "+str(Py_List_Price))
    Trace.Write("Py_Sell_Price "+str(Py_Sell_Price))
    if SC_Product_Type == 'Renewal':
        ComparisonSummary = Product.GetContainerByName("ComparisonSummary")
        if ComparisonSummary.Rows.Count:
            for row in ComparisonSummary.Rows:
                row['Configured_PY_List_Price'] = Py_List_Price
                row['Configured_PY_Sell_Price'] = str(float(row['Configured_PY_List_Price']) - (float(row['Configured_PY_List_Price']) * float(row['PY_Discount_SFDC']))) if row['PY_Discount_SFDC'] else str(float(row['Configured_PY_List_Price']))
                row['PY_Coverage'] = PY_Coverage
                #row['PY_Training_Match_SFDC'] = SC_Training_Match_Contract_Value_PY
                row.Calculate()
            ComparisonSummary.Calculate()