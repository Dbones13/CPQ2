#CXCPQ-50540: Added updateOrAddSurChargeWarranty for PMC 
def updateOrAddSurChargeWarranty():
    flag = 'No'
    for item in Quote.Items:
        if item.Description == 'Inflation Surcharge':
            flag = 'Yes'
            break

    if flag == 'No':
        writeInProductQuery = SqlHelper.GetFirst("SELECT Product,Category,Description, ProductLine, ProductLineDescription, ProductLineSubGroupDescription, ProductLineSubGroup, UnitofMeasure from WriteInProducts where Product = 'Write-In Surcharge'")
        if writeInProductQuery is not None:
            WriteInItem = ProductHelper.CreateProduct('WriteIn_cpq')
            WriteInItem.Attr('Writein_Category').SelectValue(str(writeInProductQuery.Category))
            WriteInItem.Attr('WriteInProductsChoices').SelectValue(str(writeInProductQuery.Product))
            WriteInItem.Attr('Selected_WriteIn').AssignValue(str(writeInProductQuery.Product))
            WriteInItem.Attr('Description').AssignValue(str(writeInProductQuery.Description))
            WriteInItem.Attr('Product Line').AssignValue(str(writeInProductQuery.ProductLine))
            WriteInItem.Attr('Product Line Description').AssignValue(str(writeInProductQuery.ProductLineDescription))
            WriteInItem.Attr('Product line sub group').AssignValue(str(writeInProductQuery.ProductLineSubGroup))
            WriteInItem.Attr('PLSG description').AssignValue(str(writeInProductQuery.ProductLineSubGroupDescription))
            WriteInItem.Attr('Unit of Measure').AssignValue(str(writeInProductQuery.UnitofMeasure))
            WriteInItem.Attr('ItemQuantity').AssignValue('1')
            WriteInItem.Attr('Extended Description').AssignValue('Inflation Surcharge')
            WriteInItem.ApplyRules()
            x = WriteInItem.AddToQuote()

            sellPrice = (2*float(Quote.GetCustomField('Total Sell Price').Content.replace(',','')))/100
            for item in Quote.Items:
                if item.Description == 'Inflation Surcharge':
                    item.Cost = 0
                    item.ListPrice = sellPrice
                    Trace.Write(str(item.ListPrice))
                    break
            Quote.Calculate()

#CXCPQ-50540: Added Inflation Surcharge logic for PMC
if Quote.GetCustomField('Booking LOB').Content == "PMC" and Quote.GetCustomField('Quote Type').Content == "Parts and Spot":
    Trace.Write("Not Added Inflation Surcharge if PMC & Parts & Spot")
elif Quote.GetCustomField('Booking LOB').Content == "PMC" and Quote.Items.Count:
    CF_Opportunity_Record_Type = Quote.GetCustomField('Opportunity Record Type').Content
    CF_Booking_Country = Quote.GetCustomField('Booking Country').Content
    query = SqlHelper.GetFirst("Select Region from PMC_Country_Region_Mapping where Country = '{}'".format(CF_Booking_Country))
    if query is not None:
        if (query.Region == "AMER") or (query.Region == "EMEA" and CF_Opportunity_Record_Type == "Indirect Sales"):
            updateOrAddSurChargeWarranty()