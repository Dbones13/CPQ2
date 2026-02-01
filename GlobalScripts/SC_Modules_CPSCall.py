import GS_CostAPI_Module
import GS_GetPriceFromCPS

def getFloat(Var):
	if Var:
		return float(Var)
	return 0

#Get host name from environment
def getHost():
	hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
	if hostquery is not None:
		return hostquery.HostName
	return ''

#Call API to fetch cost and assign to Quote Item fields
def fn_getCost(host,p_Material,p_fme,p_plant):
	Trace.Write('In CC_GetCost_Plant_Change fn_getCost')
	req_payload=GS_CostAPI_Module.gen_Item_PayLoad(Quote,p_Material,p_fme,p_plant)
	accessTkn = GS_CostAPI_Module.getAccessToken(host)
	CostAPIResp_Json = GS_CostAPI_Module.getCost(host, accessTkn,req_payload)
	return CostAPIResp_Json

def fetchCost(model,plantCode):
	responseCost = "0"
	try:
		_responseCost = fn_getCost(host,model,'',plantCode)
		if _responseCost is not None and _responseCost['vcMaterialCostResponse'] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse'] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse']["item"] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse']["item"][0] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse']["item"][0]['totalCost'] is not None:
			responseCost = str(_responseCost['vcMaterialCostResponse']['vcCostResponse']["item"][0]['totalCost'])
	except:
		responseCost = '0'
	return responseCost

def populateInvalidWEP(cont,model,desc,qty,reason):
	inValidRow = cont.AddNewRow(False)
	inValidRow["Model"] = model
	inValidRow["Description"] = desc
	inValidRow["Quantity"] = qty
	inValidRow["Reason"] = reason

def populateInvalidMES(cont,model,desc,qty,reason,product_type):
	inValidRow = cont.AddNewRow(False)
	Trace.Write("adding row")
	inValidRow["MES Models"] = model
	inValidRow["Description"] = desc
	if product_type == "New":
		inValidRow["Quantity"] = qty
	elif product_type == "Renewal":
		inValidRow["PY_Quantity"] = "0"
		inValidRow["Renewal_Quantity"] = qty
	inValidRow["Reason"] = reason

def callInvalid(name):
	m.append(row.RowIndex)
	if name == "MES Performix":
		if SC_Product_Type == 'New':
			populateInvalidMES(inValidModelCont,row["MES Models"],row["Description"],row["Quantity"],"List Price is not available in Pricing Database",SC_Product_Type)
		elif SC_Product_Type == 'Renewal':
			populateInvalidMES(inValidModelCont,row["MES Models"],row["Description"],row["Renewal_Quantity"],"List Price is not available in Pricing Database",SC_Product_Type)
	elif name == "Workforce Excellence Program":
		populateInvalidWEP(invalidModelsCont,row["Model"],row["Description"],row["Quantity"],"List Price is not available in Pricing Database")

host=getHost()
partNumberrList = []
priceDict = {}
salesOrg = Quote.GetCustomField('Sales Area').Content

if Product.Name == "MES Performix":
	SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
	m = []
	validModelCont = Product.GetContainerByName("SC_MES_Models_Scope")
	inValidModelCont = Product.GetContainerByName("SC_MES_Invalid_Models")
	if validModelCont.Rows.Count:
		for row in validModelCont.Rows:
			partNumberrList.append(row["MES Models"])
	priceDict = GS_GetPriceFromCPS.getPrice(Quote,priceDict,partNumberrList,TagParserQuote,Session)
	if len(priceDict) > 0:
		if validModelCont.Rows.Count:
			for row in validModelCont.Rows:
				if priceDict.get(row["MES Models"],"0") not in ("0.00","0",""):
					if SC_Product_Type == 'New':
						row["Unit_Price"] = priceDict[row["MES Models"]]
					elif SC_Product_Type == 'Renewal':
						row["HW_UnitPrice"] = priceDict[row["MES Models"]]
					row["Hidden_UnitPrice"] = priceDict[row["MES Models"]]
				else:
					callInvalid(Product.Name)
	else:
		for row in validModelCont.Rows:
			callInvalid(Product.Name)
	m.reverse()
	for i in m:
		validModelCont.DeleteRow(i)
	validModelCont.Calculate()

if Product.Name == "Workforce Excellence Program":
	tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
	m = []
	if 'Training' in tabs:
		validModelsCont = Product.GetContainerByName('SC_WEP_Models_Scope_Training')
		invalidModelsCont = Product.GetContainerByName('SC_WEP_Invalid_Models_Training')
	elif 'HALO OA' in tabs:
		validModelsCont = Product.GetContainerByName('SC_WEP_Models_Scope_Halo')
		invalidModelsCont = Product.GetContainerByName('SC_WEP_Invalid_Models_Halo')
	elif 'Immersive Field Simulator' in tabs:
		validModelsCont = Product.GetContainerByName('SC_WEP_Models_Scope_IFS')
		invalidModelsCont = Product.GetContainerByName('SC_WEP_Invalid_Models_IFS')
	elif 'Training Needs Assessment' in tabs:
		validModelsCont = Product.GetContainerByName('SC_WEP_Models_Scope_TNA')
		invalidModelsCont = Product.GetContainerByName('SC_WEP_Invalid_Models_TNA')

	if validModelsCont.Rows.Count:
		for row in validModelsCont.Rows:
			partNumberrList.append(row['Model'])
	priceDict = GS_GetPriceFromCPS.getPrice(Quote,priceDict,partNumberrList,TagParserQuote,Session)
	costQuery = SqlHelper.GetFirst("select Plant_Code from SC_Plant_SalesOrg_Mapping where Sales_Org='{}'".format(salesOrg))
	if len(priceDict) > 0:
		if validModelsCont.Rows.Count:
			for row in validModelsCont.Rows:
				if priceDict.get(row["Model"],"0") not in ("0.00","0",""):
					row["Unit_Price"] = priceDict[row["Model"]]
					cost = fetchCost(row["Model"],costQuery.Plant_Code) if costQuery is not None else "0"
					row["Unit_Cost"] = cost if cost != "0" else str(float(row["Unit_Price"])/2)
				else:
					if row['Product_Type'] != "Renewal":
						callInvalid(Product.Name)
	else:
		for row in validModelsCont.Rows:
			if row['Product_Type'] != "Renewal":
				callInvalid(Product.Name)
	m.reverse()
	for i in m:
		validModelsCont.DeleteRow(i)
	validModelsCont.Calculate()

if Product.Name == "Parts Management":
	validPartsCont = Product.GetContainerByName("SC_P1P2_Parts_Details")
	if validPartsCont.Rows.Count:
		for row in validPartsCont.Rows:
			partNumberrList.append(row['Part_Number'])
	priceDict = GS_GetPriceFromCPS.getPrice(Quote,priceDict,partNumberrList,TagParserQuote,Session)
	if len(priceDict) > 0:
		if validPartsCont.Rows.Count:
			for row in validPartsCont.Rows:
				if priceDict.get(row['Part_Number']):
					row["Unit_Price"] = priceDict[row['Part_Number']]
				else:
					row["Unit_Price"] = "0"
	else:
		if validPartsCont.Rows.Count:
			for row in validPartsCont.Rows:
				row["Unit_Price"] = "0"

if Product.Name == "Service Contract Products":
	SC_Cont = Product.GetContainerByName('Service Contract Modules')
	if SC_Cont.Rows.Count:
		for scrow in SC_Cont.Rows:
			if scrow['Module'] == 'Parts Management':
				validPartsCont = scrow.Product.GetContainerByName("SC_P1P2_Parts_Details")
				if validPartsCont.Rows.Count:
					for row in validPartsCont.Rows:
						partNumberrList.append(row['Part_Number'])
				priceDict = GS_GetPriceFromCPS.getPrice(Quote,priceDict,partNumberrList,TagParserQuote,Session)
				if len(priceDict) > 0:
					if validPartsCont.Rows.Count:
						for row in validPartsCont.Rows:
							if priceDict.get(row['Part_Number']):
								row["Unit_Price"] = priceDict[row['Part_Number']]
							else:
								row["Unit_Price"] = "0"
				else:
					if validPartsCont.Rows.Count:
						for row in validPartsCont.Rows:
							row["Unit_Price"] = "0"