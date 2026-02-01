quote_type = Quote.GetCustomField('Quote Type').Content
Trace.Write(str(quote_type))
Prod_list = []
if quote_type == 'Contract Renewal':
    for item in Quote.MainItems:
        if item.ProductName == "Service Contract Products":
            item.EditConfiguration()
            cont = Product.GetContainerByName("Service Contract Modules")
            for row in cont.Rows:
                if row['Product_Status'] == 'Incomplete':
                    Prod_list.append(row["Module"])
                    #row.QI_SC_ItemFlag.Value = 'Hidden'
            break
    if Prod_list:
        Trace.Write(str(Prod_list))
        for item in Quote.MainItems:
            if item.ProductName in Prod_list:
                Trace.Write("item.ProductName: "+str(item.ProductName))
                item.QI_SC_ItemFlag.Value = 'Hidden'
            Quote.Save(False)