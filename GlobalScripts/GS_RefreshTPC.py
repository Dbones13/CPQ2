from GS_Winest_Labor_Price_Cost import createItemDataDict, transferQuoteDataToContainer, updateReportsContainer

for Item in Quote.MainItems:
	if Item.ProductName == 'TPC System Name' :#and Quote.GetCustomField("SC_CF_RENEWAL_FLAG").Content == "1":
		product = Item.EditConfiguration()
		product.ParseString('<* ExecuteScript(UpdateQuoteData) *>')
		product.UpdateQuote()
	elif Item.ProductName == "Winest Labor Import":
		prod = Item.AsMainItem.EditConfiguration()
		reportCont = prod.GetContainerByName("Winest Reports Container")
		reportCont.Rows.Clear()
		updateReportsContainer(prod, reportCont)
		qDiscDict = createItemDataDict(Item)
		transferQuoteDataToContainer(reportCont, qDiscDict)
		prod.UpdateQuote()