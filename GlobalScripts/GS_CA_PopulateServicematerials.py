def getFloat(Var):
	if Var:
		return float(Var)
	return 0

def getCFValue(CFName):
  return Quote.GetCustomField(CFName).Content

def addValues(totalDict , partNumber,key, value):
	partDict = totalDict.get(partNumber,dict())
	partDict[key] = getFloat(partDict.get(key , 0)) + getFloat(value)
	totalDict[partNumber] = partDict

def getItemsData(module):
	for part in module.Children:
		if part.ProductTypeName.lower() == "honeywell labor":
			#partNumbers[part.PartNumber] = part.ProductName
			addValues(itemData,part.PartNumber,"Hours",part.Quantity)
			addValues(itemData,part.PartNumber,"Unit_Cost",part.Cost)
			addValues(itemData,part.PartNumber,"Total_Cost",part.ExtendedCost)
			addValues(itemData,part.PartNumber,"Unit_Sell_Price",part.NetPrice)
			addValues(itemData,part.PartNumber,"Total_Sell_Price",part.ExtendedAmount)
			itemData[part.PartNumber]["Service_Material_Name"] = part.ProductName

def populateQuoteTable(serviceTable,msid,itemDataDict,header):
	addRow = serviceTable.AddNewRow()
	addRow["Service_Materials"] = "Total"
	addRow["MSID"] = msid.PartNumber if msid else ''
	addRow["Quote_Item_GuId"] = msid.QuoteItemGuid if msid else ''
	addRow["IsHeader"] = header
	for partnumber in itemDataDict:
		addRow = serviceTable.AddNewRow()
		partData = itemDataDict[partnumber]
		#addRow["MSID"] = msid.PartNumber
		addRow["Service_Material_Name"] = partData.get("Service_Material_Name",'')
		addRow["Service_Materials"] = partnumber
		addRow["Hours"] = round(partData.get("Hours",0),2)
		#addRow["Unit_Cost"] = round(partData.get("Unit_Cost",0),2)
		addRow["Unit_Cost"] = round(partData.get("Total_Cost",0),2)/round(partData.get("Hours",0),2) if round(partData.get("Hours",0),2) != 0 else 0
		addRow["Total_Cost"] = round(partData.get("Total_Cost",0),2)
		#addRow["Unit_Sell_Price"] = round(partData.get("Unit_Sell_Price",0),2)
		addRow["Unit_Sell_Price"] = round(partData.get("Total_Sell_Price",0),2)/round(partData.get("Hours",0),2) if round(partData.get("Hours",0),2) != 0 else 0
		addRow["Total_Sell_Price"] = round(partData.get("Total_Sell_Price",0),2)
		addRow["Quote_Item_GuId"] = msid.QuoteItemGuid if msid else ''
		addRow["IsHeader"] = header

def calculateTotals(serviceTable,msid):
	if serviceTable.Rows.Count > 0:
		totalHours = 0
		totalcost = 0
		totalSellPrice = 0
		for row in serviceTable.Rows:
			if row["Quote_Item_GuId"] == msid.QuoteItemGuid:
				totalHours += getFloat(row["Hours"])
				totalcost += getFloat(row["Total_Cost"])
				totalSellPrice += getFloat(row["Total_Sell_Price"])
		for row in serviceTable.Rows:
			if row["Quote_Item_GuId"] == msid.QuoteItemGuid:
				if row["Service_Materials"] == "Total":
					row["Hours"] = totalHours
					row["Total_Cost"] = totalcost
					row["Total_Sell_Price"] = totalSellPrice
				else:
					row["Percentage"] = str(round((getFloat(row["Hours"]) / totalHours) * 100,1))

if getCFValue("Quote Type") == "Projects" and (getCFValue("Booking LOB") == "LSS" or getCFValue("Booking LOB") == "PAS" or getCFValue("Booking LOB") == "PMC" ) or getCFValue("cyberProductPresent") == "Yes" or getCFValue("Booking LOB") == "HCP":
	partNumbers = dict()
	serviceTable = Quote.QuoteTables["Service_Materials_Table_Excel_Pull"]
	serviceTable.Rows.Clear()
	for item in Quote.MainItems:
		if item.PartNumber == "Migration":
			for msid in item.Children:
				itemData = dict()
				#Trace.Write(msid.PartNumber)
				for module in msid.Children:
					#Trace.Write(module.PartNumber)
					getItemsData(module)
				#Trace.Write(str(partNumbers))
				#Trace.Write(str(itemData))
				populateQuoteTable(serviceTable,msid,itemData,"No")
				calculateTotals(serviceTable,msid)
		if item.PartNumber == "Trace Software":
			itemData = dict()
			getItemsData(item)
			for module in item.Children :   # do something for this
				Trace.Write(module.Description)
				getItemsData(module)
			populateQuoteTable(serviceTable,item,itemData,"No")
			calculateTotals(serviceTable,item)
		if item.PartNumber == "HCI_Labor_config":
			itemData = dict()
			for module in item.Children :
				getItemsData(module)
			populateQuoteTable(serviceTable,item,itemData,"No")
			calculateTotals(serviceTable,item)
		if item.PartNumber =="HCI_LABOR":
			itemData = dict()
			getItemsData(item)
			populateQuoteTable(serviceTable,item,itemData,"No")
			calculateTotals(serviceTable,item)
		if item.PartNumber == "CYBER":
			itemData = dict()
			for module in item.Children :
				getItemsData(module)
			populateQuoteTable(serviceTable,item,itemData,"No")
			calculateTotals(serviceTable,item)

	serviceTableData = dict()
	for row in serviceTable.Rows:
		if row["Service_Materials"] != "Total":
			addValues(serviceTableData,row["Service_Materials"],"Hours",row["Hours"])
			addValues(serviceTableData,row["Service_Materials"],"Unit_Cost",row["Unit_Cost"])
			addValues(serviceTableData,row["Service_Materials"],"Total_Cost",row["Total_Cost"])
			addValues(serviceTableData,row["Service_Materials"],"Unit_Sell_Price",row["Unit_Sell_Price"])
			addValues(serviceTableData,row["Service_Materials"],"Total_Sell_Price",row["Total_Sell_Price"])
			serviceTableData[row["Service_Materials"]]["Service_Material_Name"] = row["Service_Material_Name"]
	Trace.Write(str(serviceTableData))

	headerserviceTable = Quote.QuoteTables["Header_Service_Materials_Table_Excel_Pull"]
	headerserviceTable.Rows.Clear()
	populateQuoteTable(headerserviceTable,'',serviceTableData,"Yes")
	if headerserviceTable.Rows.Count > 0:
		totalHours = 0
		totalcost = 0
		totalSellPrice = 0
		for row in headerserviceTable.Rows:
			if row["IsHeader"] == "Yes":
				totalHours += getFloat(row["Hours"])
				totalcost += getFloat(row["Total_Cost"])
				totalSellPrice += getFloat(row["Total_Sell_Price"])
		for row in headerserviceTable.Rows:
			if row["IsHeader"] == "Yes":
				if row["Service_Materials"] == "Total":
					row["Hours"] = totalHours
					row["Total_Cost"] = totalcost
					row["Total_Sell_Price"] = totalSellPrice
				else:
					row["Percentage"] = str(round((getFloat(row["Hours"]) / totalHours) * 100,1))
	serviceTable.Save()
	headerserviceTable.Save()
ScriptExecutor.Execute('GS_CA_PopulatelaborTypesTable')