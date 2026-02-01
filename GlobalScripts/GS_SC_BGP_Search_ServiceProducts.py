BGP_Models_Cont = Product.GetContainerByName('SC_BGP_Models_Cont')
BGP_Models_Hid_Cont = Product.GetContainerByName('SC_BGP_Models_Cont_Hidden')
SearchText = Product.Attr('SC_BGP_Model_Search').GetValue()
BGP_Models_Cont.Clear()
if SearchText == "" or SearchText == None:
    for row in BGP_Models_Hid_Cont.Rows:
        i = BGP_Models_Cont.AddNewRow()
        i['Service_Product'] = row['Service_Product']
        i['Quantity'] = row['Quantity']
        i['List_Price'] = row['List_Price']
        i['Cost_Price'] = row['Cost_Price']
else:
    for row in BGP_Models_Hid_Cont.Rows:
        if SearchText.lower() in row['Service_Product'].lower():
            i = BGP_Models_Cont.AddNewRow()
            i['Service_Product'] = row['Service_Product']
            i['Quantity'] = row['Quantity']
            i['List_Price'] = row['List_Price']
            i['Cost_Price'] = row['Cost_Price']
BGP_Models_Cont.Calculate()