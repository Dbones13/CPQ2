from datetime import datetime
from GS_HCI_LABOR_CommonModule import HCIModule

class uploadModule:
	def __init__(self, Quote, Product, ProductHelper):
		self.quote = Quote
		self.Product = Product 
		self.ProductHelper = ProductHelper
		self.GesLoc = Product.Attr('AR_HCI_GES Location')
		self.HCIMod = HCIModule(Quote, Product)

	def Execute(self,workbook):
		sheetInterface = workbook.GetSheet("WBS")
		rowCount = sheetInterface.Cells.GetRowCount
		if not sheetInterface: return
		cellRange = sheetInterface.Cells.GetRange("A1", "AE"+str(rowCount))
		execution_year = self.quote.GetCustomField("EGAP_Contract_Start_Date").Content
		[TaskName, Index, Execution, ProductLine, BillingTask, P401, P405, P410, P310, P345, P350, P505, P210, P215, P700, PCA, Total, Source, Input, Desc] = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 22, 23, 24, 25, 26]
		CountryCode = {'GES India': 'IN','GES China': 'CN','GES Uzbekistan': 'UZ'}
		labor_container = self.Product.GetContainerByName("AR_HCI_LABOR_CONTAINER")
		productivityVal = (self.Product.Attr('AR_HCI_PRODUCTIVITY').GetValue() or 1)
		exec_cntry = self.Product.Attr('AR_HCI_Executioncountry').GetValue()
		exec_year = self.Product.Attr('AR_HCI_EXECUTION_YEAR').GetValue()
		labor_container.Clear()
		current_year = datetime.now().year
		if not exec_cntry:
			region = self.HCIMod.salesorg_region
			self.Product.Attr('AR_HCI_Executioncountry').SelectDisplayValue(region)
		else:
			region = exec_cntry 
		gesLocation = self.GesLoc.GetValue()
		currencyvalue = self.HCIMod.salesorg_curr
		if not gesLocation:
			self.GesLoc.SelectDisplayValue('GES India')		
		if not exec_year:
			execution_year = current_year if not execution_year else '20'+execution_year.split('/')[2]
			if str(execution_year).startswith('20'):
				pass
			else:
				execution_year = '20'+execution_year
			self.Product.Attr('AR_HCI_EXECUTION_YEAR').SelectDisplayValue(str(execution_year))
		else:
			execution_year = exec_year
			 
		gesLocation = self.GesLoc.GetValue()
		for i in range(0, rowCount):
			if (cellRange[i, Index])!="" and str(cellRange[i, TaskName]) not in ["WBS For Export","Task Name"] and (cellRange[i, Execution])!="Summary Deliverable":
				for x in range(7,23):
					if str(cellRange[i, x]) not in ["0",""]:
						activity_type = str(cellRange[7, x])
						product_line = str(cellRange[i, ProductLine])
						if activity_type.endswith('B') and self.Product.Attr('AR_HCI_GES Location').SelectedValue:
							service_material = 'ADV_GES_'+activity_type+'_'+str(CountryCode[self.Product.Attr('AR_HCI_GES Location').GetValue()])
							EACValueDict = self.HCIMod.EACdict.get(service_material,{})
							if EACValueDict:
								EACValue = self.HCIMod.QuoteCurrencyConversion(currencyvalue,self.HCIMod.Quotecurrency,EACValueDict.get('EACValue'),EACValueDict.get('EACCurr'))
							W2WFactor = (self.HCIMod.W2WDict.get(service_material) or 0.0)

						else:
							if activity_type == 'P610':
								service_material = 'HPS_SYS_'+product_line+'_'+activity_type
							else:
								service_material = 'HPS_ADV_'+product_line+'_'+activity_type
							W2WFactor = 0.1
							EACValue = 0
						if '_CN' in service_material or '_UZ' in service_material:
							getcostquery = SqlHelper.GetFirst("SELECT Cost_CurrentMonth_Year1,Cost_CurrentMonth_Year2,Cost_CurrentMonth_Year3,Cost_CurrentMonth_Year4,Cost_Currency_Code FROM HPS_LABOR_COST_DATA WHERE Sales_Org = '{0}' and Part_Number = '{1}' ".format('',str(service_material)))
							if getcostquery:
								cost = [getcostquery.Cost_CurrentMonth_Year1,getcostquery.Cost_CurrentMonth_Year2,getcostquery.Cost_CurrentMonth_Year3,getcostquery.Cost_CurrentMonth_Year4]
								CurrofCost = getcostquery.Cost_Currency_Code
							else:
								cost = [0.0,0.0,0.0,0.0]
								
						else:
							if 'GES' not in service_material and str(self.HCIMod.salesorg_region)!= region:
								exec_salesorg, exec_currency = self.HCIMod.getSalesOrg(exec_cntry)
								currencyvalue = exec_currency
								cost = self.HCIMod.LaborCostDict(exec_salesorg).get(service_material,[0.0,0.0,0.0,0.0,''])
								Trace.Write(str(['--cost import-->',cost,service_material]))
								CurrofCost = cost[4] if cost else ''
							else:
								exec_salesorg, exec_currency = self.HCIMod.getSalesOrg(exec_cntry)
								self.HCIMod.LaborcostDictValue(exec_salesorg)
								cost = self.HCIMod.LaborcostDict.get(str(service_material),[0.0,0.0,0.0,0.0])
								CurrofCost = None
						totalprice, transfercost = 0, 0
						service_material_sumup = [row for row in labor_container.Rows if row['LaborResource'] == str(service_material) and row["WBS Deliverable Text"] == str(cellRange[i, Execution]) and row["ExecutionYear"] == str(execution_year) and row["ExecutionCountry"] == str(region)]
						if len(service_material_sumup) == 0:
							labor = labor_container.AddNewRow(False)
							labor['Desc'] = labor['Engr'] = self.HCIMod.materialDesc.get(service_material)
							labor['LaborResource'] = self.HCIMod.materials.get(labor['Desc']) 
							labor.Product.Attr('AR_HCI_ServiceProduct_Labor').SelectDisplayValue(self.HCIMod.materials.get(labor['Desc']) )
							labor.Product.Attr('AR_HCI_EXECUTION_DELIVERABLES').SelectDisplayValue(str(cellRange[i, Execution]))
							labor.Product.Attr('ItemQuantity').AssignValue(str(cellRange[i, x]))
							labor["ProductLine"] = product_line
							labor['WBS Deliverable Text'] = str(cellRange[i, Execution])
							labor['Deliverable'] = str(cellRange[i, Execution])
							labor["ExecutionYear"]= str(execution_year)
							labor["ExecutionCountry"] = str(region)
							labor["ExecutionTask"] =  str(cellRange[i, TaskName])
							labor["CalculatedHours"] =  cellRange[i, x]
							labor["ActivityType"] = activity_type
							labor["Productivity"] = str(productivityVal)
							if service_material:
								prod = SqlHelper.GetFirst("select PRODUCT_ID  from products where SYSTEM_ID = '{}'".format(str(service_material)))
								if prod:
									productID = int(prod.PRODUCT_ID)
									Addproduct =self.ProductHelper.CreateProduct(productID)
									Trace.Write(str(service_material)+'-created product-'+str(Addproduct.TotalPrice))
									if Addproduct.TotalPrice:
										totalprice = Addproduct.TotalPrice
							totalprice_org = totalprice
							Trace.Write(str(['-getlaborPrices-->',cost,totalprice,execution_year,current_year,currencyvalue,CurrofCost]))
							transfercost, totalprice = self.HCIMod.getlaborPrices(cost,totalprice,execution_year,current_year,CurrofCost)
							Trace.Write(str([transfercost, totalprice])+'return--'+str(cost))
							if 'GES' not in service_material:
								if str(self.HCIMod.salesorg_region)!= str(labor["ExecutionCountry"]):
									transfercost = self.HCIMod.cost_increment(transfercost)								
									calculatedW2W = str(float(transfercost)/(1.00+float(W2WFactor)))
								else:
									calculatedW2W = transfercost
								labor["TransferCost"] = str(transfercost)
								labor["W2WCost"] = str(calculatedW2W)
							else:
								transcost=float(transfercost)+float(EACValue)
								w2wCost=str(float(transcost)/(1.00+float(W2WFactor)))
								labor["TransferCost"] = str(transcost)
								labor["W2WCost"] = w2wCost
							Trace.Write(str([str(labor['TransferCost']), str(labor['W2WCost'])])+'return else')

							#labor["Desc"] = self.HCIMod.materialDesc.get(service_material)
							labor.Product.Attr('AR_HCI_EngDesc').SelectDisplayValue(labor['Desc'])
							labor["UnitListPrice"] = str(totalprice)
							labor["ProductListPrice"] = str(totalprice_org)
							labor["TotalListPrice"] = (str(float(totalprice) * float(cellRange[i, x])))
							
						else:
							for labor in service_material_sumup:
								labor["CalculatedHours"] = str(float(labor["CalculatedHours"])+float(cellRange[i, x]))
								labor.Product.Attr('ItemQuantity').AssignValue(str(labor["CalculatedHours"]))
						labor.Calculate()
						labor.ApplyProductChanges()
		
		#UpdateMPAPrice(quote,product)
		self.Product.GetContainerByName('AR_HCI_LABOR_CONTAINER').Calculate()
		self.HCIMod.addupdateTotalRow(labor_container)