#Added For OPB Comparision Container
tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Scope Summary' in tabs and Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    delta = SqlHelper.GetFirst("select Value from SC_HARDCODE_VALUES where Name = 'Comparison Summary Delta Allowance (%)'")
    deltaFactor = eval(delta.Value)/100 if delta is not None else 0
    comparision_cont = Product.GetContainerByName("ComparisonSummary")
    Product.Attr('SC_Labor_Popup_Msg').AssignValue('False')
    for row in comparision_cont.Rows:
        row['List_Price_Delta'] = row['List_Price_Delta'] if row['List_Price_Delta'] != '' else '0'
        row['Sell_Price_Delta'] = row['Sell_Price_Delta'] if row['Sell_Price_Delta'] != '' else '0'
        row['PY_List_Price_SFDC'] = row['PY_List_Price_SFDC'] if row['PY_List_Price_SFDC'] != '' else '0'
        row['PY_Sell_Price_SFDC'] = row['PY_Sell_Price_SFDC'] if row['PY_Sell_Price_SFDC'] != '' else '0'
        if row.IsSelected == False:
            if abs(float(row['List_Price_Delta'])) > (deltaFactor*float(row['PY_List_Price_SFDC'])) or abs(float(row['Sell_Price_Delta'])) > (deltaFactor*float(row['PY_Sell_Price_SFDC'])):
                Product.Attr('SC_Labor_Popup_Msg').AssignValue('True')
                break