from GS_R2Q_Product_Attribute_ContColms import MigrationProductsAttributesContainerColumns as PRD
import GS_DOC_3rdparty_LSS_UOC
import GS_DOC_3rdparty_LSS_PLC

flags = {
	"cnt_uoc": 0,
	"UOCFlag": False,
	"cnt_plc": 0,
	"PLCFlag": False
}

def getbom_parts(container,product,table):
	counter = 1
	for row in container.Rows:
		if 'SVC' in row["Partnumber"]:
			continue
		if row["Partnumber"] and str(row["Final Quantity"])!='0':
			row1 = table.AddNewRow()
			row1["Item_Number"] = counter
			row1["Part_Number"] = row["Partnumber"]
			row1["Part_Description"] = row["PartDescription"]
			row1["Product_Name"] = product
			quantity = int(float(row["Final Quantity"])) if row["Final Quantity"] else 0
			row1["Quantity"] = str(quantity)
			counter += 1
	table.Save()

def getbom_parts_3rdParty(partsdict,table):
	counter = 1
	for part in partsdict.Keys:
		row1 = table.AddNewRow()
		row1["Item_Number"] = counter
		row1["Part_Number"] = part
		row1["Part_Description"] = partsdict[part][0]
		row1["Product_Name"] = partsdict[part][1]
		row1["Quantity"] = partsdict[part][2]
		counter += 1
	table.Save()

def getSelectedProducts(item):
	selectedProducts = next((attr.Values[0].Display.split('<br>') for attr in item.SelectedAttributes
		if attr.Name == "MSID_Selected_Products"), [])
	return selectedProducts

def bom_migration(item,Quote):
	table = Quote.QuoteTables["R2Q_Migration_BOM"]
	table.Rows.Clear()
	if item.ProductName in ("MSID_New") :
		selectedProducts = getSelectedProducts(item)
		for product in selectedProducts:
			if product == '3rd Party PLC to ControlEdge PLC/UOC':
				bom_migration_3rdParty(item,table)
			else:
				container = item.SelectedAttributes.GetContainerByName(PRD.contProductMap.get(product))
				if container:
					getbom_parts(container,product,table)

def addpart(partsdict,item,product):
	if item.PartNumber.startswith('SVC'):
		return partsdict
	else:
		if item.PartNumber not in partsdict:
			partsdict[item.PartNumber] = [item.Description,product,item.Quantity]
		else:
			quan = partsdict[item.PartNumber][2]
			partsdict[item.PartNumber] = [item.Description,product,item.Quantity+quan]
		return partsdict

def bom_migration_3rdParty(item,table,partsdict = {}):
	for module in item.Children:
		product = module.ProductName
		if product == '3rd Party PLC to ControlEdge PLC/UOC':
			for prod in module.Children:
				if prod.ProductName in ('ControlEdge PLC System Migration','ControlEdge UOC System Migration'):
					for cg in prod.Children:
						if cg.ProductName in ('CE PLC Control Group','UOC Control Group'):
							for rg in cg.Children:
								if rg.ProductName in ('CE PLC Remote Group','UOC Remote Group'):
									for part in rg.Children:
										partsdict = addpart(partsdict,part,product)
								else:
									partsdict = addpart(partsdict,rg,product)
						else:
							partsdict = addpart(partsdict,cg,product)
				else:
					partsdict = addpart(partsdict,prod,product)
			getbom_parts_3rdParty(partsdict,table)

def sellprice_proposal(item,Quote):
	if item.PartNumber=='FSC to SM IO Audit':
		Quote.GetCustomField("R2Q Total Audit Sell Price").Content = str(item.ExtendedAmount)
	if item.PartNumber=='FSC to SM Audit':
		Quote.GetCustomField("R2Q_Total_Audit_FSC_SM_SP").Content = str(item.ExtendedAmount)

def thirdrd_Party_proposal(item, Quote, flags):
	if item.ProductName == 'ControlEdge UOC System Migration' and not flags["UOCFlag"]:
		flags["UOCFlag"] = True
		flags["cnt_uoc"] = 1
		uoc = GS_DOC_3rdparty_LSS_UOC.populateUOCData(Quote)

	if item.ProductName == 'ControlEdge PLC System Migration' and not flags["PLCFlag"]:
		flags["PLCFlag"] = True
		flags["cnt_plc"] = 1
		plc = GS_DOC_3rdparty_LSS_PLC.populatePASData(Quote)

def thirdpartyprop(item,Quote):
	flags = {
		"cnt_uoc": 0,
		"UOCFlag": False,
		"cnt_plc": 0,
		"PLCFlag": False
	}
	thirdrd_Party_proposal(item, Quote, flags)