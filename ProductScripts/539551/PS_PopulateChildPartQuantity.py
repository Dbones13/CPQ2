def getQuantityDict(msidProduct , quantityDict,MSIDdict, MSID ,SystemNumber):
	container = msidProduct.GetContainerByName("MSID_Product_Container")
	for row in container.Rows:
		childProduct = row.Product
		childPartContainer = childProduct.GetContainerByName("MSID_Added_Parts_Common_Container")
		if childPartContainer is not None:
			for childRow in childPartContainer.Rows:
				Log.Info('PartNumber --- >> '+str(childRow["PartNumber"])+' --Quantity --->> '+str(childRow["Quantity"]))
				quantityDict[childRow.UniqueIdentifier] = childRow["Quantity"]
				MSIDdict[childRow.UniqueIdentifier] = MSID + " - " + SystemNumber

def getQuantityDictfsc(msidProduct , quantityDict,MSIDdict, MSID ,SystemNumber):
	container = msidProduct.GetContainerByName("MSID_Product_Container_FSC_hidden")
	for row in container.Rows:
		childProduct = row.Product
		childPartContainer = childProduct.GetContainerByName("MSID_Added_Parts_Common_Container")
		for childRow in childPartContainer.Rows:
			quantityDict[childRow.UniqueIdentifier] = childRow["Quantity"]
			MSIDdict[childRow.UniqueIdentifier] = MSID + " - " + SystemNumber

def getQuantityDictvirt(msidProduct , quantityDict,MSIDdict, MSID, SystemNumber):
	container = msidProduct.GetContainerByName("CONT_MSID_SUBPRD")
	for row in container.Rows:
		childProduct = row.Product
		childPartContainer = childProduct.GetContainerByName("MSID_Added_Parts_Common_Container")
		for childRow in childPartContainer.Rows:
			quantityDict[childRow.UniqueIdentifier] = childRow["Quantity"]
			MSIDdict[childRow.UniqueIdentifier] = MSID + " - " + SystemNumber
		if row['selected_Products'] in ('Virtualization System Migration', 'Virtualization System'):
			childPartSummContainer = childProduct.GetContainerByName("Virtualization_partsummary_cont")
			for childRow in childPartSummContainer.Rows:
				MSIDdict[childRow.UniqueIdentifier] = MSID + " - " + SystemNumber

def getQuantityDictgen(msidProduct , quantityDict,MSIDdict, MSID, SystemNumber):
	container = msidProduct.GetContainerByName("MSID_Product_Container_Generic_hidden")
	for row in container.Rows:
		childProduct = row.Product
		childPartContainer = childProduct.GetContainerByName("MSID_Added_Parts_Common_Container")
		for childRow in childPartContainer.Rows:
			quantityDict[childRow.UniqueIdentifier] = childRow["Quantity"]
			MSIDdict[childRow.UniqueIdentifier] = MSID + " - " + SystemNumber

quantityDict = dict()
MSIDdict = dict()
msidContainer = Product.GetContainerByName("CONT_Migration_MSID_Selection")
Log.Info('PS_PopulateChildPartQuantity')
for row in msidContainer.Rows:
	msidProduct = row.Product
	getQuantityDict(msidProduct , quantityDict,MSIDdict,row['MSID'], row['System_Number'])
	getQuantityDictfsc(msidProduct , quantityDict,MSIDdict,row['MSID'],row['System_Number'])
	getQuantityDictvirt(msidProduct , quantityDict,MSIDdict,row['MSID'], row['System_Number'])
	getQuantityDictgen(msidProduct , quantityDict,MSIDdict,row['MSID'], row['System_Number'])
items = arg.QuoteItemCollection
for item in items:
	if quantityDict.get(item.QuoteItemGuid):
		Log.Info("item.Quantity="+str(item.Quantity) +" -item.PartNumber"+str(item.PartNumber)+' -- quantityDict-- '+str(quantityDict))
		item.Quantity = float(quantityDict.get(item.QuoteItemGuid))
		Log.Info("After value set item.Quantity 2 -- ="+str(item.Quantity) +" -item.PartNumber"+str(item.PartNumber)+' --QuoteItemGuid-- '+str(item.QuoteItemGuid)+' --quantityDict-- '+str(quantityDict))
		item["QI_Area"].Value = (MSIDdict.get(item.QuoteItemGuid))
	elif MSIDdict.get(item.QuoteItemGuid):
		Log.Info("item.Quantity 2 -- ="+str(item.Quantity) +" -item.PartNumber"+str(item.PartNumber))
		item["QI_Area"].Value = (MSIDdict.get(item.QuoteItemGuid))
		
def populateYears(SuperParentRolledUpQuoteItem,Year):
	for item in Quote.MainItems:
		if item.RolledUpQuoteItem == SuperParentRolledUpQuoteItem:
			item["QI_Year"].Value = Year
			item["QI_Year_Visibility"].Value = "0"
			continue
		if item.RolledUpQuoteItem.startswith(SuperParentRolledUpQuoteItem + '.'):
			item["QI_Year"].Value = Year
			item["QI_Year_Visibility"].Value = "0"
if Quote.GetCustomField("Quote Type").Content == 'Projects':
	for item in items:
		IsMultiYear = False
		if item.PartNumber == "Migration" :
			for selAttr in item.SelectedAttributes:
				if selAttr.Name == "LCM_Multiyear_Selection":
					IsMultiYear = True
					for val in selAttr.Values:
						populateYears(item.RolledUpQuoteItem,(val.ValueCode))
			if IsMultiYear == False:
				populateYears(item.RolledUpQuoteItem,'')
			break
SellPricesStrategy = Product.Attr('Sell Price Strategy').GetValue()
customerBudget = Product.Attr('Customer_Budget_TextField').GetValue()
Quote.GetCustomField("CustomerBudget").Content= customerBudget
Quote.GetCustomField("SellPricestrategy").Content = SellPricesStrategy
if Quote.GetCustomField('R2QFlag').Content == 'Yes':
	query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Honeywell_Ref !='' and Price_Plan_Status= 'Active' and [IF]([EQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects)){Price_Plan_Systems_Discount}{Price_Plan_Parts_Discount}[ENDIF] = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and ( Price_Plan_End_Date  IS NULL  or Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>')")
	Log.Info("res calculate reprice:"+str(query))
	from GS_SetDefaultPricePlan import setDefaultMpa
	setDefaultMpa(Quote,TagParserQuote)
Quote.Save(False)

#Log.Write(str(item.Quantity))