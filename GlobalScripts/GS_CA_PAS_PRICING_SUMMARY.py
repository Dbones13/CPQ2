QT_Table = Quote.QuoteTables["PAS_DCS_Pricing_Summary"]
QT_Table.Rows.Clear()
product_types = ["Hardware and Software", "Project Management and Engineering Services", "Measurement IQ Annual Fee", "Other","Total Price"]
for type_name in product_types:
    newRow = QT_Table.AddNewRow()
    newRow["PRODUCT_TYPE"] = type_name
total_price = 0
for row in QT_Table.Rows:
    list_price = 0
    proj_price = 0
    miq_price = 0
    others_LP = 0
    #Category = ''
    for Item in Quote.Items: 
        Category = ''       
        query = "SELECT ProductCategory FROM WriteInProducts WHERE Product = '"+str(Item.PartNumber)+"'"
        result = SqlHelper.GetFirst(query)
        if result:
            Category = str(result.ProductCategory)
            Trace.Write("Category:" +str(Category))
        else:
            if Item.ProductName == 'TPC_Product':
                Category = str(Item.QI_ProjectType.Value)
            else:
                Category = str(Item.ProductTypeName)
            Trace.Write("Product Type:" +str(Category))           
        if (("Software" in Category) or ("Material" in Category))  and row["PRODUCT_TYPE"] == "Hardware and Software" and Item.PartNumber != "Write-In MIQ Optimize Annual Update Fee":
            list_price += (Item.NetPrice)*(Item.Quantity)
            row["SELLING_PRICE"] = ('{:,.2f}'.format(float(list_price)))
            row["CURRENCY"] = Quote.SelectedMarket.CurrencyCode
            Trace.Write("LIST:" +str(list_price))
            total_price += float((Item.NetPrice)*(Item.Quantity))
        elif ("Labor" in Category) and row["PRODUCT_TYPE"] == "Project Management and Engineering Services":
            proj_price += (Item.NetPrice)*(Item.Quantity)
            row["SELLING_PRICE"] = ('{:,.2f}'.format(float(proj_price)))
            row["CURRENCY"] = Quote.SelectedMarket.CurrencyCode
            total_price += float((Item.NetPrice)*(Item.Quantity))                
        elif ("Other" in Category) and row["PRODUCT_TYPE"] == "Other":
            others_LP += (Item.NetPrice)*(Item.Quantity)
            row["SELLING_PRICE"] = ('{:,.2f}'.format(float(others_LP)))
            row["CURRENCY"] = Quote.SelectedMarket.CurrencyCode
            total_price += float((Item.NetPrice)*(Item.Quantity))
            #Trace.Write("total:" +str(total_price))
        #CXCPQ-51002 - Start - Added this section to add new row in the PAS_DCS_Pricing_Summary for MIQ Write-in Annual Fee.
        elif Item.PartNumber == "Write-In MIQ Optimize Annual Update Fee" and row["PRODUCT_TYPE"] == "Measurement IQ Annual Fee":
            miq_price += (Item.ListPrice)*(Item.Quantity)
            row["SELLING_PRICE"] = ('{:,.2f}'.format(float(miq_price)))
            row["CURRENCY"] = Quote.SelectedMarket.CurrencyCode
            total_price += float((Item.ListPrice)*(Item.Quantity)) 
        #CXCPQ-51002 - End
        elif row["PRODUCT_TYPE"] == "Total Price":
            row["SELLING_PRICE"] = ('{:,.2f}'.format(float(total_price)))
            row["CURRENCY"] = Quote.SelectedMarket.CurrencyCode
        elif row["SELLING_PRICE"] == "":
            row["SELLING_PRICE"] = "0.00"
            row["CURRENCY"] = "$0.00"
    QT_Table.Save()