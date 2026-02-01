def parseContainer(conDict):
	Trace.Write(conDict)
	if conDict["Method"] == "Sum":
		calValue = 0
		if conDict["ValueType"] == "CTX":
			calValue = sum(map(lambda x: float(x), filter(lambda x: str(x).replace('.','',1).isdigit(), 
													  [product.ParseString(conDict['DataColumn'].format(Index=int(cRow.RowIndex)+1)) 
													   for cRow in product.GetContainerByName(conDict['ContainerName']).Rows 
													   if product.ParseString(conDict['Value'].format(Index=int(cRow.RowIndex)+1))=='1'])))
		product.Attr(conDict["Name"]).AssignValue(str(calValue))

def parseCustom(conDict):
	if conDict["Method"] == "Assign":
		calValue = product.ParseString(conDict["Value"]) if conDict["ValueType"]=="CTX" else conDict["Value"]
		product.Attr(conDict["Name"]).AssignValue(str(calValue))

def parsePayload(part, conDict, payLoad):
	if conDict["Method"] == "Assign":
		calValue = next((item["Quantity"] for item in payLoad if item["Part"] == part), None)
		if calValue:
			if conDict["ValueType"] == "CTX":
				product.ParseString(conDict['Value'].format(calValue))
			else:
				product.Attr(conDict["Name"]).AssignValue(str(calValue))

def executeActions(mData, actionType, payLoad):
	if (mData.PreExecution and actionType == "Pre") or (mData.PostExecution and actionType == "Post"):
		if mData.MappingSource == "Payload" and next((item for item in payLoad if item["Part"] == mData.MappingName), None) == None:
			return
		actData = SqlHelper.GetList("Select TOP 1000 * from R2Q_VRT_Actions where ActionType = '{}' and ActionName = '{}' and ActionStatus = 1 Order by Rank".format(actionType, mData.MappingName))
		for aData in actData:
			if(product.ParseString(aData.ActionCondition) == '1'):
				executeMapping(aData.ActionName, 'product', aData.ExecutionType, aData.ExecutionValue, aData.AttributeType, payLoad)



def executeMapping(mapName, mapSource, exeType, exeValue, attType, payLoad):
	Trace.Write("mapName: {}, mapSource: {}, exeType: {}, exeValue: {}, attType: {}".format(mapName, mapSource, exeType, exeValue, attType))
	if mapSource == "Product":
		if exeType == "Standard":
			product.ParseString(exeValue)
		elif exeType == "Custom":
			if attType == "Container":
				parseContainer(eval(exeValue))
			else:
				parseCustom(eval(exeValue))
	elif mapSource == "Payload":
		if exeType == "Custom":
			parsePayload(mapName, eval(exeValue), payLoad)
	product.ApplyRules()

if Quote.GetGlobal('VrtMappingFlag') == 'True':
	#try:
	payload_val = Param.vrt_list
	product = Param.msidproduct
	Log.Info("XXX :{}".format(payload_val))
	param = payload_val["VrtList"]
	#Log.Info("param:--{}".format(param))
	mapData = SqlHelper.GetList("Select TOP 1000 * from R2Q_VRT_MAPPING where MappingStatus = 1 Order by Rank")
	for mData in mapData:
		Log.Info("insidemdata")
		executeActions(mData, 'Pre', param)
		executeMapping(mData.MappingName, mData.MappingSource, mData.ExecutionType, mData.ExecutionValue, mData.AttributeType, param)
		executeActions(mData, 'Post', param)

	TContner = product.GetContainerByName("Virtualization_partsummary_cont")
	for trow in TContner.Rows:
		Log.Info("RowIndex: {} got executed".format(trow.RowIndex))
		trow.IsSelected = True
		#trow.Product.ApplyRules()
		trow.Product.Attr('ItemQuantity').AssignValue(trow["CE_Final_Quantity"])
		trow.ApplyProductChanges()
		trow.Calculate()
		TContner.Calculate()
	Quote.SetGlobal('VrtMappingFlag', '')
	#except:
		#Trace.Write("Param not found")