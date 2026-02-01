def addFinalHours(totalDict, partNumber, key, value):
	partDict = totalDict.get(partNumber, dict())
	partDict[key] = getFloat(partDict.get(key, 0)) + getFloat(value)
	totalDict[partNumber] = partDict

def getFloat(Var):
	if Var:
		return float(Var)
	return 0

def adjustRegionalCost(totalDict):
	for partNumber, partDict in totalDict.items():
		if partDict.get('count', 0) >= 1:
			partDict['RegionalCost'] = partDict.get('RegionalCost', 0) / partDict.get('Quantity', 0)
			partDict['WTWCost'] = partDict.get('WTWCost', 0) / partDict.get('Quantity', 0)
			partDict['UnitListPrice'] = partDict.get('UnitListPrice', 0) / partDict.get('Quantity', 0)
			#Trace.Write(str(partDict['RegionalCost'])+"--000-->"+str(partDict['WTWCost'])+"--->"+str(partDict['UnitListPrice'])+"--->"+str(partDict))
            #partDict['RegionalCost'] = partDict.get('RegionalCost', 0) / partDict.get('count', 0)
            #Log.Info("-------recheck--laborupload--->"+str(partDict['RegionalCost']))
            #partDict['WTWCost'] = partDict.get('WTWCost', 0) / partDict.get('count', 0)
            #partDict['UnitListPrice'] = partDict.get('UnitListPrice', 0) / partDict.get('count', 0)

Laborcont = Product.GetContainerByName("AR_HCI_LABOR_CONTAINER")
partsNumbers = dict()
for row in Laborcont.Rows:
	partNumber = row['LaborResource']
	
	if partNumber not in partsNumbers:
		partsNumbers[partNumber] = {'count': 0}
	
	partsNumbers[partNumber]['count'] += 1
	'''if str(row["TransferCost"]) != '':
		addFinalHours(partsNumbers, partNumber, 'RegionalCost', row["TransferCost"]
	if str(row['W2WCost']) != '':
		addFinalHours(partsNumbers, partNumber, 'WTWCost', row["W2WCost"])
	if str(row['UnitListPrice']) != '':
		addFinalHours(partsNumbers, partNumber, 'UnitListPrice', row["UnitListPrice"]) '''
	if str(row["TransferCost"]) != '' and str(row['FinalHours']) != '':
		#Trace.Write(str(partNumber)+"-finalll--->"+str(row["TransferCost"]))
		addFinalHours(partsNumbers, partNumber, 'RegionalCost', float(row["TransferCost"]) * float(row["FinalHours"]))
	if str(row['W2WCost']) != '' and str(row['FinalHours']) != '':
		addFinalHours(partsNumbers, partNumber, 'WTWCost', float(row["W2WCost"]) * float(row["FinalHours"]))
	if str(row['UnitListPrice']) != '' and str(row['FinalHours']) != '':
		addFinalHours(partsNumbers, partNumber, 'UnitListPrice', float(row["UnitListPrice"]) * float(row["FinalHours"]))
	if str(row['FinalHours']) != '':
		addFinalHours(partsNumbers, partNumber, 'Quantity', row["FinalHours"])
##Trace.Write(str(partsNumbers))
adjustRegionalCost(partsNumbers)
Trace.Write('partsNumbers----' + str(partsNumbers))
Quote.GetCustomField("LaborPricesDict").Content = str(partsNumbers)
Session['LaborPricesDict'] = str(partsNumbers)