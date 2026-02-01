from GS_Winest_Labor_Price_Cost import createItemDataDict, transferQuoteDataToContainer, updateReportsContainer

for item in Quote.MainItems:
    if item.ProductName == "Winest Labor Import":
        prod = item.AsMainItem.EditConfiguration()
        reportCont = prod.GetContainerByName("Winest Reports Container")
        reportCont.Rows.Clear()
        updateReportsContainer(prod, reportCont)
        qDiscDict = createItemDataDict(item)
        transferQuoteDataToContainer(reportCont, qDiscDict)
        prod.UpdateQuote()