CYB_Models_Cont = Product.GetContainerByName('SC_Cyber_Models_Cont')
CYB_Models_Hid_Cont = Product.GetContainerByName('SC_Cyber_Models_Cont_Hidden')
SearchText = Product.Attr('SC_Cyber_Model_Search').GetValue()
CYB_Models_Cont.Clear()
quotetype = Quote.GetCustomField("Quote Type").Content
SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if quotetype == 'Contract Renewal' and SC_Product_Type == 'New':
    serprod = {}
    if SearchText == "" or SearchText == None:
        for row in CYB_Models_Hid_Cont.Rows:
            if row['Service_Product'] in serprod.keys():
                serprod[row['Service_Product']]['Listprice'] += float(row['List_Price'])
                serprod[row['Service_Product']]['Costprice'] += float(row['Cost_Price'])
            else:
                serprod[row['Service_Product']] = {'Listprice' : float(row['List_Price']), 'Costprice' : float(row['Cost_Price'])}
    else:
        for row in CYB_Models_Hid_Cont.Rows:
            if SearchText.lower() in row['Service_Product'].lower():
                if row['Service_Product'] in serprod.keys():
                    serprod[row['Service_Product']]['Listprice'] += float(row['List_Price'])
                    serprod[row['Service_Product']]['Costprice'] += float(row['Cost_Price'])
                else:
                    serprod[row['Service_Product']] = {'Listprice' : float(row['List_Price']), 'Costprice' : float(row['Cost_Price'])}
    for i in serprod:
        newrow = CYB_Models_Cont.AddNewRow()
        newrow['Service_Product'] = i
        newrow['List_Price'] = str(serprod[i]['Listprice'])
        newrow['Cost_Price'] = str(serprod[i]['Costprice'])
else:
    if SearchText == "" or SearchText == None:
        for row in CYB_Models_Hid_Cont.Rows:
            i = CYB_Models_Cont.AddNewRow()
            i['Service_Product'] = row['Service_Product']
            i['List_Price'] = row['List_Price']
            i['Cost_Price'] = row['Cost_Price']
    else:
        for row in CYB_Models_Hid_Cont.Rows:
            if SearchText.lower() in row['Service_Product'].lower():
                i = CYB_Models_Cont.AddNewRow()
                i['Service_Product'] = row['Service_Product']
                i['List_Price'] = row['List_Price']
                i['Cost_Price'] = row['Cost_Price']
CYB_Models_Cont.Calculate()