'''#Added For OPB Comparision Container
comparision_cont = Product.GetContainerByName("ComparisonSummary")
Product.Attr('SC_Labor_Popup_Msg').AssignValue('False')
for row in comparision_cont.Rows:
    if float(row['List_Price_Delta']) != 0 or float(row['Sell_Price_Delta']) != 0:
        Product.Attr('SC_Labor_Popup_Msg').AssignValue('True')
        break'''
#Added For OPB Comparision Container
if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    delta = SqlHelper.GetFirst("select Value from SC_HARDCODE_VALUES where Name = 'Comparison Summary Delta Allowance (%)'")
    deltaFactor = eval(delta.Value)/100 if delta is not None else 0
    comparision_cont = Product.GetContainerByName("ComparisonSummary")
    Product.Attr('SC_Labor_Popup_Msg').AssignValue('False')
    for row in comparision_cont.Rows:
        if row.IsSelected == False:
            if abs(float(row['List_Price_Delta'])) > (deltaFactor*float(row['PY_List_Price_SFDC'])) or abs(float(row['Sell_Price_Delta'])) > (deltaFactor*float(row['PY_Sell_Price_SFDC'])):
                Product.Attr('SC_Labor_Popup_Msg').AssignValue('True')
                break