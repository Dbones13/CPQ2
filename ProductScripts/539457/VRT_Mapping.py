def parseContainer(conDict):
	if conDict["Method"] == "Sum":
		calValue = 0
		if conDict["ValueType"] == "CTX":
			calValue = sum(map(lambda x: float(x), filter(lambda x: str(x).replace('.','',1).isdigit(), 
													  [Product.ParseString(conDict['DataColumn'].format(Index=int(cRow.RowIndex)+1)) 
													   for cRow in Product.GetContainerByName(conDict['ContainerName']).Rows 
													   if Product.ParseString(conDict['Value'].format(Index=int(cRow.RowIndex)+1))=='1'])))
		Product.Attr(conDict["Name"]).AssignValue(str(calValue))

def parseCustom(conDict):
	if conDict["Method"] == "Assign":
		calValue = Product.ParseString(conDict["Value"]) if conDict["ValueType"]=="CTX" else conDict["Value"]
		Product.Attr(conDict["Name"]).AssignValue(str(calValue))

def parsePayload(part, conDict, payLoad):
	if conDict["Method"] == "Assign":
		calValue = next((item["Quantity"] for item in payLoad if item["Part"] == part), None)
		if calValue:
			if conDict["ValueType"] == "CTX":
				Product.ParseString(conDict['Value'].format(calValue))
			else:
				
				Product.Attr(conDict["Name"]).AssignValue(str(calValue))

def executeActions(mData, actionType, payLoad):
	if (mData.PreExecution and actionType == "Pre") or (mData.PostExecution and actionType == "Post"):
		if mData.MappingSource == "Payload" and next((item for item in payLoad if item["Part"] == mData.MappingName), None) == None:
			return
		actData = SqlHelper.GetList("Select TOP 1000 * from R2Q_VRT_Actions where ActionType = '{}' and ActionName = '{}' and ActionStatus = 1 Order by Rank".format(actionType, mData.MappingName))
		for aData in actData:
			if(Product.ParseString(aData.ActionCondition) == '1'):
				executeMapping(aData.ActionName, 'Product', aData.ExecutionType, aData.ExecutionValue, aData.AttributeType, payLoad)



def executeMapping(mapName, mapSource, exeType, exeValue, attType, payLoad):
	if mapSource == "Product":
		if exeType == "Standard":
			Product.ParseString(exeValue)
		elif exeType == "Custom":
			if attType == "Container":
				parseContainer(eval(exeValue))
			else:
				parseCustom(eval(exeValue))
	elif mapSource == "Payload":
		if exeType == "Custom":
			parsePayload(mapName, eval(exeValue), payLoad)
	Product.ApplyRules()

if Quote.GetGlobal('VrtMappingFlag') == 'True':
	try:
		
		param = eval(Param)
		mapData = SqlHelper.GetList("Select TOP 1000 * from R2Q_VRT_MAPPING where MappingStatus = 1 Order by Rank")
		for mData in mapData:
			executeActions(mData, 'Pre', param)
			executeMapping(mData.MappingName, mData.MappingSource, mData.ExecutionType, mData.ExecutionValue, mData.AttributeType, param)
			executeActions(mData, 'Post', param)

		TContner = Product.GetContainerByName("Virtualization_partsummary_cont")
		for trow in TContner.Rows:
			
			trow.IsSelected = True
			#trow.Product.ApplyRules()
			trow.ApplyProductChanges()
			trow.Calculate()
		TContner.Calculate()
		Quote.SetGlobal('VrtMappingFlag', '')
	except:
		Trace.Write("Param not found")