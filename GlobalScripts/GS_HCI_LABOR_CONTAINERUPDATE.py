from datetime import datetime
from GS_HCI_LABOR_CommonModule import HCIModule

class Eventmodule:
	def __init__(self, Quote, Product, ProductHelper, EventArgs):
		self.quote = Quote
		self.Product = Product 
		self.EventArgs = EventArgs
		self.ProductHelper = ProductHelper
		self.HCIMod = HCIModule(Quote, Product)
		self.booking_country = Quote.GetCustomField('Booking Country').Content
		self.honeywellRef = Quote.GetCustomField('MPA Honeywell Ref').Content
		self.gesLocation = Product.Attr('AR_HCI_GES Location').GetValue()


	def CellEdit_LaborContainer(self):
		index = self.EventArgs.ChangedCell.RowIndex
		row = self.EventArgs.Container.Rows[index]
		CellValue = self.EventArgs.ChangedCell.NewValue
		ColumnEdited = self.EventArgs.ChangedCell.ColumnName
		execution_year = row['ExecutionYear']
		exec_salesorg, exec_currency = self.HCIMod.getSalesOrg(row["ExecutionCountry"])
		self.HCIMod.LaborcostDictValue(exec_salesorg)
		current_year = datetime.now().year
		if str(execution_year)== '':
			execution_year =(self.Product.Attr('AR_HCI_EXECUTION_YEAR').GetValue() or current_year)
		currencyvalue = self.HCIMod.salesorg_curr
		FinalHours = (row.Item["FinalHours"] or 0)
		engDesc = row.Item["Desc"]
		if ColumnEdited == 'Select' and str(CellValue) == 'False':
			self.Product.Attr('AR_HCI_SELECTALL').SelectValue('No')
		if ColumnEdited == 'FinalHours':
			row.Item['Productivity'] = str(float(CellValue)/ float(row.Item['CalculatedHours']))
		if engDesc and ColumnEdited not in ('Select','Deliverable'):
			if ColumnEdited == 'Desc':
				row.Item["LaborResource"] = self.HCIMod.materials.get(engDesc)
				value = str(row.Item["LaborResource"]).split('_')
				if 'GES' not in value:
					row.Item["ActivityType"] = value[3]
					row.Item["ProductLine"] = value[2]
				else:
					row.Item['ActivityType'] = value[2]
					row.Item["ProductLine"] = value[0]
			
			prod = SqlHelper.GetFirst("select PRODUCT_ID  from products where SYSTEM_ID = '{}'".format(str(row.Item["LaborResource"])))
			row.Product.Attr('AR_HCI_ServiceProduct_Labor').SelectDisplayValue(row.Item["LaborResource"])
			if prod:
				i=self.ProductHelper.CreateProduct(prod.PRODUCT_ID)
				if i.TotalPrice:
					row.Item["UnitListPrice"] = str(i.TotalPrice)
					row.Item["TotalListPrice"] = str(float(i.TotalPrice) * float(FinalHours))
					row.Item["ProductListPrice"] = str(i.TotalPrice)
				else:
					row.Item["UnitListPrice"] = str(0.00)
					row.Item["TotalListPrice"] = str(0.00)
					row.Item["ProductListPrice"] = str(0.00)
			if row.Item["ActivityType"].endswith('B'):
				EACValueDict = self.HCIMod.EACdict.get(str(row.Item["LaborResource"]),{})
				if EACValueDict:
					EACValue = self.HCIMod.QuoteCurrencyConversion(currencyvalue,self.HCIMod.Quotecurrency,EACValueDict.get('EACValue'),EACValueDict.get('EACCurr'))
				W2WFactor = self.HCIMod.W2WDict.get(str(row.Item["LaborResource"]),0.0)
			else:
				W2WFactor = 0.1
				EACValue = 0
			if '_CN' in str(row.Item["LaborResource"]) or '_UZ' in str(row.Item["LaborResource"]):
				getcostquery = SqlHelper.GetFirst("SELECT Cost_CurrentMonth_Year1,Cost_CurrentMonth_Year2,Cost_CurrentMonth_Year3,Cost_CurrentMonth_Year4,Cost_Currency_Code FROM HPS_LABOR_COST_DATA WHERE Sales_Org = '{0}' and Part_Number = '{1}' ".format('',str(row.Item["LaborResource"])))
				if getcostquery:
					cost = [getcostquery.Cost_CurrentMonth_Year1,getcostquery.Cost_CurrentMonth_Year2,getcostquery.Cost_CurrentMonth_Year3,getcostquery.Cost_CurrentMonth_Year4]
					CurrofCost = getcostquery.Cost_Currency_Code
				else:
					cost = [0.0,0.0,0.0,0.0]
					
			else:
				cost = self.HCIMod.LaborcostDict.get(str(row.Item["LaborResource"]),[0.0,0.0,0.0,0.0])
				CurrofCost = None
				
			totalprice = row.Item["UnitListPrice"]
			Trace.Write(str('-->cell edit '+str([cost,totalprice,execution_year,current_year,CurrofCost])))
			transfercost, totalprice = self.HCIMod.getlaborPrices(cost,totalprice,execution_year,current_year,CurrofCost)
			Log.Info("totalprice>Loke")
			if 'GES' not in str(row.Item["LaborResource"]) and str(self.HCIMod.salesorg_region)!= str(self.Product.Attr('AR_HCI_Executioncountry').GetValue()):
				getcostquery = SqlHelper.GetFirst("SELECT Cost_CurrentMonth_Year1,Cost_CurrentMonth_Year2,Cost_CurrentMonth_Year3,Cost_CurrentMonth_Year4,Cost_Currency_Code FROM HPS_LABOR_COST_DATA WHERE Sales_Org = '{0}' and Part_Number = '{1}' ".format(str(exec_salesorg),str(row.Item["LaborResource"])))
				if getcostquery:
					cost = [getcostquery.Cost_CurrentMonth_Year1,getcostquery.Cost_CurrentMonth_Year2,getcostquery.Cost_CurrentMonth_Year3,getcostquery.Cost_CurrentMonth_Year4]
					CurrofCost = getcostquery.Cost_Currency_Code
					transfercost, totalprice = self.HCIMod.getlaborPrices(cost,totalprice,row.Item['ExecutionYear'],current_year,exec_currency,CurrofCost)
					Log.Info("totalprice>Loke1>>")
				else:
					cost = [0.0,0.0,0.0,0.0]
					
			if 'GES' not in str(row.Item["LaborResource"]):
				calculatedW2W = transfercost
				if str(self.HCIMod.salesorg_region)!= str(row.Item["ExecutionCountry"]) and W2WFactor is not None:
					transfercost = self.HCIMod.cost_increment(transfercost)								
					calculatedW2W = str(float(transfercost)/(1.00+float(W2WFactor)))
				row.Item["TransferCost"] = str(transfercost)
				row.Item["W2WCost"] = str(calculatedW2W)
			else:
				transfercost=float(transfercost)+float(EACValue)
				calculatedW2W=str(float(transfercost)/(1.00+float(W2WFactor)))
				row.Item["TransferCost"] = str(transfercost)
				row.Item["W2WCost"] = calculatedW2W
			row.Item['UnitListPrice'] = str(totalprice)
			if row.Item["UnitListPrice"]:
				row.Item["TotalListPrice"] = str(float(row.Item["UnitListPrice"]) * float(FinalHours))
			row.Item["Engr"] = row.Item["Desc"]
		self.HCIMod.addupdateTotalRow(self.Product.GetContainerByName('AR_HCI_LABOR_CONTAINER'))
		row.ApplyProductChanges()
		row.Calculate()
		row.Product.ApplyRules()
		self.Product.GetContainerByName('AR_HCI_LABOR_CONTAINER').Calculate()