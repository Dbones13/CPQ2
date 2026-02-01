EC = Product.Attr('AR_HCI_Executioncountry').GetValue()
EY = Product.Attr('AR_HCI_EXECUTION_YEAR').GetValue()
PR = Product.Attr('AR_HCI_PRODUCTIVITY').GetValue()
from datetime import datetime
from GS_HCI_LABOR_CommonModule import HCIModule
HCIMod = HCIModule(Quote, Product)
current_year = datetime.now().year
execution_year = Product.Attr('AR_HCI_EXECUTION_YEAR').GetValue() if Product.Attr('AR_HCI_EXECUTION_YEAR').GetValue() else current_year
currencyvalue = HCIMod.salesorg_curr
Trace.Write('check HCI Labor Upload execution')

for i in Product.GetContainerByName("AR_HCI_LABOR_CONTAINER").Rows:
	if i.IsSelected:
		#if i['ExecutionCountry']:
			#HCIMod.adjust_cost(i)
		if EC:
			i["ExecutionCountry"] = str(EC)
		if EY:
			i.GetColumnByName("ExecutionYear").SetAttributeValue(str(EY))
			i['ExecutionYear'] = str(EY)
		if PR:
			i["Productivity"] = str(PR)
		if i["ProductLine"] and i["ActivityType"].endswith('B') and Product.Attr('AR_HCI_GES Location').GetValue():
			product_line = i["ProductLine"]
			activity_type = i['ActivityType']
			service_material = 'ADV_GES_'+activity_type+'_'+str(Product.Attr('AR_HCI_GES Location').SelectedValue.ValueCode)
			i["LaborResource"] = service_material
		exec_salesorg, exec_currency = HCIMod.getSalesOrg(i["ExecutionCountry"])
		if i["ActivityType"].endswith('B'):
			EACValueDict = HCIMod.EACdict.get(str(i["LaborResource"]),{})
			if EACValueDict:
				EACValue = HCIMod.QuoteCurrencyConversion(currencyvalue,HCIMod.Quotecurrency,EACValueDict.get('EACValue'),EACValueDict.get('EACCurr'))
			W2WFactor = (HCIMod.W2WDict.get(str(i["LaborResource"])) or 0)
		else:
			W2WFactor = 0.1
			EACValue = 0
		totalprice = i['ProductListPrice'] or 0.0
		transfercost = 0.0
		if '_CN' in str(i["LaborResource"]) or '_UZ' in str(i["LaborResource"]):
			getcostquery = SqlHelper.GetFirst("SELECT Cost_CurrentMonth_Year1,Cost_CurrentMonth_Year2,Cost_CurrentMonth_Year3,Cost_CurrentMonth_Year4,Cost_Currency_Code FROM HPS_LABOR_COST_DATA WHERE Sales_Org = '{0}' and Part_Number = '{1}' ".format('',str(i["LaborResource"])))
			if getcostquery:
				cost = [getcostquery.Cost_CurrentMonth_Year1,getcostquery.Cost_CurrentMonth_Year2,getcostquery.Cost_CurrentMonth_Year3,getcostquery.Cost_CurrentMonth_Year4]
				Trace.Write('cost ges -'+str(cost))
				CurrofCost = getcostquery.Cost_Currency_Code
				transfercost, totalprice = HCIMod.getlaborPrices(cost,totalprice,i['ExecutionYear'],current_year,CurrofCost,CurrofCost)
				Trace.Write('strvc-'+str(transfercost))
			else:
				cost = [0.0,0.0,0.0,0.0]
		else:
			cost = HCIMod.LaborcostDict.get(str(i["LaborResource"]),[0.0,0.0,0.0,0.0])
			transfercost, totalprice = HCIMod.getlaborPrices(cost,totalprice,i['ExecutionYear'],current_year,None)
			if 'GES' not in str(i["LaborResource"]):
				if str(HCIMod.salesorg_region)!= str(i["ExecutionCountry"]):
					getcostquery = SqlHelper.GetFirst("SELECT Cost_CurrentMonth_Year1,Cost_CurrentMonth_Year2,Cost_CurrentMonth_Year3,Cost_CurrentMonth_Year4,Cost_Currency_Code FROM HPS_LABOR_COST_DATA WHERE Sales_Org = '{0}' and Part_Number = '{1}' ".format(str(exec_salesorg),str(i["LaborResource"])))
					if getcostquery:
						cost = [getcostquery.Cost_CurrentMonth_Year1,getcostquery.Cost_CurrentMonth_Year2,getcostquery.Cost_CurrentMonth_Year3,getcostquery.Cost_CurrentMonth_Year4]
						Trace.Write('cost ges -'+str(cost))
						CurrofCost = getcostquery.Cost_Currency_Code
						transfercost, totalprice = HCIMod.getlaborPrices(cost,totalprice,i['ExecutionYear'],current_year,exec_currency,CurrofCost)
						Trace.Write('strvc-'+str(transfercost))
			
		#cost = HCIMod.LaborcostDict.get(str(i["LaborResource"]),[0.0,0.0,0.0,0.0])
		if 'GES' not in str(i["LaborResource"]):
			calculatedW2W = transfercost
			if str(HCIMod.salesorg_region)!= str(i["ExecutionCountry"]):
				transfercost = HCIMod.cost_increment(transfercost)								
				calculatedW2W = str(float(transfercost)/(1.00+float(W2WFactor)))
			i["TransferCost"] = str(transfercost)
			i["W2WCost"] = str(calculatedW2W)
		else:
			transfercost=float(transfercost)+float(EACValue)
			calculatedW2W=str(float(transfercost)/(1.00+float(W2WFactor)))
			i["TransferCost"] = str(transfercost)
			i["W2WCost"] = str(calculatedW2W)
		
		i['UnitListPrice'] = str(totalprice)
		i['Desc'] = i['Engr'] = HCIMod.materialDesc.get(str(i["LaborResource"]))
		i['LaborResource'] = HCIMod.materials.get(str(i["Desc"]))
		i.Product.Attr('AR_HCI_EngDesc').SelectDisplayValue(i['Desc'])
		i.Product.Attr('AR_HCI_ServiceProduct_Labor').SelectDisplayValue(i["LaborResource"])
		if i["CalculatedHours"] and i["Productivity"]:
			i.Product.Attr('ItemQuantity').AssignValue(str(float(i["CalculatedHours"]) * float(i["Productivity"])))
		if i["UnitListPrice"] and i.Product.Attr('ItemQuantity').GetValue():
			i["TotalListPrice"] = str(float(i["UnitListPrice"]) * float(i.Product.Attr('ItemQuantity').GetValue()))
Product.GetContainerByName('AR_HCI_LABOR_CONTAINER').Calculate()
HCIMod.addupdateTotalRow(Product.GetContainerByName('AR_HCI_LABOR_CONTAINER'))
Product.ResetAttr('AR_HCI_Executioncountry')
Product.Attr('AR_HCI_EXECUTION_YEAR').SelectDisplayValue('')
Product.Attr('AR_HCI_PRODUCTIVITY').AssignValue('')
Product.Attr('AR_HCI_GES Location').SelectDisplayValue('')