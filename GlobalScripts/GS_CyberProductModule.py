from System import DateTime
from datetime import date
from GS_CommonConfig import CL_CommonSettings as CS
from GS_Populate_Labour_WTW import populateWTW, populateMPAPrice
from GS_FinalizedActivities import PopulateFinalizedActivities
from GS_GetPriceFromCPS import getPrice

def getFloat(Var):
	try:
		return float(Var)
	except:
		return 0

class CyberProduct:
	def __init__(self, Quote, Product, TagParserQuote):
		self.quote = Quote
		self.product = Product
		self.TagParserQuote = TagParserQuote
		self.excecutionCountry = self.getExecutionCountry()

	def isMPACustomer(self):
		query = self.TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Honeywell_Ref != '' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
		res = SqlHelper.GetList(query)
		if res and len(res) > 0:
			return True
		return False

	def getCfValue(self, name):
		return self.quote.GetCustomField(name).Content

	def setAttrValue(self, name,value):
		self.product.Attr(name).AssignValue(value)

	def getExecutionCountry(self):
		salesOrg = self.quote.GetCustomField('Sales Area').Content
		currency = self.quote.GetCustomField('Currency').Content
		query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
		if query is not None:
			return query.Execution_County

	def getPartDetailDict(self, partsList):
		resDict = dict()
		query = "SELECT A.PRODUCT_CATALOG_CODE, A.PRODUCT_NAME ,B.PARTNUMBER ,B.PLSG,B.PRODUCT_LINE_DESC,B.PRODUCT_LINE_SUBGROUP_DESC  FROM PRODUCTS A JOIN HPS_PRODUCTS_MASTER B ON A.PRODUCT_CATALOG_CODE=B.PARTNUMBER WHERE PRODUCT_CATALOG_CODE in ('{}')"
		query = query.format("','".join(partsList))
		res = SqlHelper.GetList(query)
		for r in res:
			resDict[r.PRODUCT_CATALOG_CODE] = [r.PRODUCT_NAME, r.PLSG, r.PRODUCT_LINE_SUBGROUP_DESC, r.PRODUCT_LINE_DESC]
		return resDict

	def populateprojectManagementSummary(self):
		PMCont = self.product.GetContainerByName('Cyber_Labor_Project_Management')
		regCost = {}
		for row in PMCont.Rows:
			if row['Deliverable'] != 'Total':
				if row['Final_Hrs'] != '':
					if float(row['Final_Hrs']) > 0:
						regCost[row['FO_Eng']] = regCost.get(row['FO_Eng'], 0) + getFloat(row['Final_Hrs'])

		PMSummary = self.product.GetContainerByName('MSID_PM_Added_Parts_Common_Container')
		PMSummary.Rows.Clear()

		partDetails = self.getPartDetailDict(list(regCost.Keys))
		for pn in partDetails:
			newRow = PMSummary.AddNewRow()
			newRow['PartNumber'] = pn
			newRow['PartDescription'] = partDetails[pn][0]
			newRow['PLSG'] = partDetails[pn][1]
			newRow['plsgDescription'] = partDetails[pn][2]
			newRow['Quantity'] = str(regCost[pn])
			newRow['Final Quantity'] = str(regCost[pn])

	def populategenericsystemsummary(self):
		LabCont = self.product.GetContainerByName('Generic_System_Activities')
		regCost = {}
		for row in LabCont.Rows:
			if row['Edit Hours'] != '':
				if float(row['Edit Hours']) > 0:
					regCost[row['PartNumber']] = regCost.get(row['PartNumber'], 0) + getFloat(row['Edit Hours'])
					
		GMSummary = self.product.GetContainerByName('Generic_System_PartsSummary')
		GMSummary.Rows.Clear()

		partDetails = self.getPartDetailDict(list(regCost.Keys))
		for pn in partDetails:
			newRow = GMSummary.AddNewRow()
			newRow['PartNumber'] = pn
			newRow['PartDescription'] = partDetails[pn][0]
			newRow['PLSG'] = partDetails[pn][1]
			newRow['plsgDescription'] = partDetails[pn][3]+"-"+partDetails[pn][2]
			newRow['Quantity'] = str(regCost[pn])
			newRow['Final Quantity'] = str(regCost[pn])

	def hide_year(self, selectedproduct):
		not_allowed = []
		allowed_count = 0
		expected_count = 4
		attribute_dict = {'SMX':'SMX_Execution_Year_Container','Assessments':'Ass_Execution_Year_Container','PCN Hardening':'PCN_Execution_Year_Container','MSS':'MSS_Execution_Year_Container','Cyber App Control':'CAC_Execution_Year_Container','Cyber_Labor_Project_Management':'PM_Cyber_Execution_Year_Container','Custom':'CustomDeliverable_Execution_Year_Container', 'Cyber Generic System':'Generic_Execution_Year_Container'}
		years_list = self.product.Attr(attribute_dict[selectedproduct]).Values
		for year in years_list:
			allowed_count = allowed_count + 1 if year.Allowed else allowed_count
		#condition to run the below script only when the year attribute has more than the expected (4) items
		if allowed_count > expected_count:
			import datetime
			current_year = datetime.datetime.now().year
			max_year = 2037
			#hide years which are less the current year or greater than current year + 4
			years_list = self.product.Attr(attribute_dict[selectedproduct]).Values
			for year in years_list:
				if int(year.ValueCode) in range(current_year + 4, max_year):
					not_allowed.append(year.ValueCode)
				elif int(year.ValueCode) < current_year:
					not_allowed.append(year.ValueCode)
		return not_allowed
	
	def populateprojectManagementCon(self, projectManagementCon):
		queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = 'PM'")
		if queryData is not None:
			newRow = projectManagementCon.AddNewRow(False)
			newRow["Deliverable"] = "Total"
			newRow["Error_Message"] = "True"
			for entry in queryData:
				if entry.Deliverable_Type == "Offsite":
					row = projectManagementCon.AddNewRow(False)
					row["Deliverable"] = entry.Deliverables
					row["Error_Message"] = "True"
					row["FO_Eng_Percentage_Split"] = "100"
					row["Final_Hrs"] = '0'
					row["Calculated_Hrs"] = '0'
					if self.isMPACustomer() == "Yes":
						row["FO_Eng"] = "SVC-PMGT-ST" if entry.Deliverable_Flag == "PM" else "SVC-PADM-ST"
					else:
						row["FO_Eng"] = "SVC-PMGT-ST-NC" if entry.Deliverable_Flag == "PM" else "SVC-PADM-ST-NC"
					row["Execution_Year"] = str(date.today().year)
					row.GetColumnByName('Execution_Year').ReferencingAttribute.SelectDisplayValue(row["Execution_Year"])
					not_allowed = self.hide_year('Cyber_Labor_Project_Management')
					row.Product.DisallowAttrValues('PM_Cyber_Execution_Year_Container', *not_allowed)
					if self.getExecutionCountry():
						row["Execution_Country"] = self.getExecutionCountry()
						row.GetColumnByName('Execution_Country').SetAttributeValue(row["Execution_Country"])
					row.Calculate()


	def getTotalEngHours(self):
		totalFinalHours = 0
		containers = []
		if self.product.Name in CS.getLaborContainer:
			containers = CS.getLaborContainer[self.product.Name]
		for cont in containers:
			if self.product.GetContainerByName(cont):
				for row in self.product.GetContainerByName(cont).Rows:
					if row["Activity"] == "Total":
						totalFinalHours += getFloat(row["Edit Hours"])
						break
		return totalFinalHours

	def getProjectMangementHours(self):
		totalHrs = {'pmOtherActivities' : 0, 'paOtherActivities' : 0, 'paMonthlyProjectManagement' : 0, 'pmEngineeringManagement' : 0}
		EngHours = self.getTotalEngHours()
		if EngHours > 0:
			totalHrs['pmOtherActivities'] = 24
			totalHrs['paOtherActivities'] = 8
		if EngHours <= 160:
			totalHrs['paMonthlyProjectManagement'] = 16
		if EngHours > 160 and EngHours <= 2000:
			totalHrs['pmEngineeringManagement'] = round((EngHours -160) * 0.1)
		elif EngHours > 2000:
			totalHrs['pmEngineeringManagement'] = 176 + round((EngHours - 2000 -160) * 0.05)

		return totalHrs
	def getSalesOrg(self, country):
		query = SqlHelper.GetFirst("select Execution_Country_Sales_Org from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_County = '{}'".format(country))
		if query is not None:
			return query.Execution_Country_Sales_Org

	def laborCostWithCOnversion(self, laborcostParts):
		quoteCurrency = self.quote.GetCustomField('Currency').Content
		costWithConversion = dict()
		if laborcostParts:
			for key in laborcostParts:
				if quoteCurrency == "USD" or laborcostParts[key]["stdcurrency"] == "USD":
					query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(laborcostParts[key]["stdcurrency"],quoteCurrency))
					costWithConversion[key] = getFloat(laborcostParts[key]["cost"]) * getFloat(query.Exchange_Rate)
				else:
					factor = 1.00
					query1 = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(laborcostParts[key]["stdcurrency"],'USD'))
					if query1 is not None:
						factor = factor * getFloat(query1.Exchange_Rate)
						queryUSD = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format('USD',quoteCurrency))
						if queryUSD is not None:
							factor = factor * getFloat(queryUSD.Exchange_Rate)
						else:
							factor = 1.00
					costWithConversion[key] = getFloat(laborcostParts[key]["cost"]) * factor
		return costWithConversion

	def executionYearTrigger(self, Execution_Year, Container, Execution_Year_Msg):
		if self.product.Attr(Execution_Year).GetValue() != '':
			exeYearsRange =  set([DateTime.Now.Year +i for i in range(4)])

			if self.getCfValue("EGAP_Contract_Start_Date") != '' and self.getCfValue("EGAP_Contract_End_Date") != '':
				contractStartYear = UserPersonalizationHelper.CovertToDate(self.getCfValue("EGAP_Contract_Start_Date")).Year
				contractEndYear = UserPersonalizationHelper.CovertToDate(self.getCfValue("EGAP_Contract_End_Date")).Year
				year = int(self.product.Attr(Execution_Year).GetValue()) if self.product.Attr(Execution_Year).GetValue() !='' else 0
				self.setAttrValue(Execution_Year_Msg,'')
				if len(str(year)) < 4 or year < DateTime.Now.Year or year not in exeYearsRange:
					self.setAttrValue(Execution_Year_Msg,'User is allowed to enter current + next 3 years in 20XX format (e.g. 2024, 2025 etc)')
				else:
					if year <= contractEndYear and year >= contractStartYear:
						container =  self.product.GetContainerByName(Container)
						for row in container.Rows:
							if row["Activity"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
								row["Execution_Year"] = str(year)
								row.GetColumnByName('Execution_Year').ReferencingAttribute.SelectDisplayValue(str(year))
					else:
						self.setAttrValue(Execution_Year_Msg,'Execution Year should be in between the Contract start date and Contract end date')
			else:
				year = int(self.product.Attr(Execution_Year).GetValue()) if self.product.Attr(Execution_Year).GetValue() !='' else 0
				self.setAttrValue(Execution_Year_Msg,'')
				if year not in exeYearsRange:
					self.setAttrValue(Execution_Year_Msg,'User is allowed to enter current + next 3 years in 20XX format (e.g. 2024, 2025 etc)')
				else:
					container =  self.product.GetContainerByName(Container)
					for row in container.Rows:
						if row["Activity"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
							row["Execution_Year"] = str(year)
							row.GetColumnByName('Execution_Year').ReferencingAttribute.SelectDisplayValue(str(year))

	def getFopartsCost(self, salesOrg,partNumber,executionYear):
		query = "Select * from HPS_LABOR_COST_DATA where Sales_Org = '{0}' and Part_Number in ('{1}')".format(salesOrg,partNumber)
		res = SqlHelper.GetList(query)
		foCost = dict()
		for i in res:
			if executionYear == str(DateTime.Now.Year):
				foCost[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year1,"stdcurrency":i.Cost_Currency_Code}
			elif executionYear == str(DateTime.Now.Year + 1):
				foCost[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year2,"stdcurrency":i.Cost_Currency_Code}
			elif executionYear == str(DateTime.Now.Year + 2):
				foCost[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year3,"stdcurrency":i.Cost_Currency_Code}
			elif executionYear == str(DateTime.Now.Year + 3):
				foCost[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year4,"stdcurrency":i.Cost_Currency_Code}
		foCostWithConversion = self.laborCostWithCOnversion(foCost)
		return foCostWithConversion

	def populateActivityListPricing(self,cont_name,cellchanged=None):
		if cont_name == 'Cyber_Labor_Project_Management':
			deliverable = 'Deliverable'
			partnumber = 'FO_Eng'
			foListprice = 'FO_ListPrice'
			hours = 'Final_Hrs'
		else:
			deliverable = 'Identifier'
			partnumber = 'PartNumber'
			foListprice = 'FO_List_Price'
			hours = 'Edit Hours'
		activities_cont = self.product.GetContainerByName(cont_name)
		execution_year = self.quote.GetCustomField('R2Q_PRJT_Execution_Year').Content
		priceDict = dict()
		activities_list = [row[partnumber] for row in activities_cont.Rows if row[partnumber]!='']
		list_set = set(activities_list)
		PriceData = getPrice(self.quote,priceDict,list_set,self.TagParserQuote)
		for r in activities_cont.Rows:
			if self.quote.GetCustomField('R2QFlag').Content == 'Yes' and cellchanged == None:
				r["Execution_Year"] = execution_year
				Log.Info(str(execution_year)+"----populateActivityListPricing -- value changes here--->"+str(r["Execution_Year"]))
				'''if r["Execution_Year"]:
					r.GetColumnByName('Execution_Year').ReferencingAttribute.SelectDisplayValue(r["Execution_Year"])'''
			if r[deliverable] not in ['Total','On-Site','Off-Site']:
				if r[hours] not in ['','0.0','0']:
					if r["Execution_Year"] == str(DateTime.Now.Year):
						r["List_Price"] = str((PriceData.get(r[partnumber],'0')))
						r[foListprice] = str(float(PriceData.get(r[partnumber],'0'))*float(r[hours]))
					else:
						if r["Execution_Year"] == str(DateTime.Now.Year + 1):
							power = 1
						elif r["Execution_Year"] == str(DateTime.Now.Year + 2):
							power = 2
						elif r["Execution_Year"] == str(DateTime.Now.Year + 3):
							power = 3	
						salesOrg = self.quote.GetCustomField("Sales Area").Content
						LOB = self.quote.GetCustomField("Booking LOB").Content
						query = "Select * from YOY_INFLATION_RATE where salesOrg = '{0}' and LOB = '{1}'".format(salesOrg,LOB)
						res = SqlHelper.GetFirst(query)
						if power == 1 and res is not None:
							inflationRate1 = res.Inflation_Rate
							price = (float(PriceData.get(r[partnumber],'0')) * float(1 + float(inflationRate1)))
						elif power == 2 and res is not None:
							inflationRate1 = res.Inflation_Rate
							inflationRate2 = res.Inflation_Rate_Year2
							price = (float(PriceData.get(r[partnumber],'0')) * float(1 + float(inflationRate1)) * float(1 + float(inflationRate2)))
						elif power == 3 and res is not None:
							inflationRate1 = res.Inflation_Rate
							inflationRate2 = res.Inflation_Rate_Year2
							inflationRate3 = res.Inflation_Rate_Year3
							price = (float(PriceData.get(r[partnumber],'0')) * float(1 + float(inflationRate1)) * float(1 + float(inflationRate2)) * float(1 + float(inflationRate3)))
						else:
							price = float(PriceData.get(r[partnumber],'0'))
						fo_list_price = price if price else 0
						r["List_Price"] = str(float(fo_list_price))
						r[foListprice] = str(float(fo_list_price) * float(r[hours]))
				else:
					r["List_Price"] = "0"
					r[foListprice] = "0"
				Log.Info(str(PriceData)+"---deliverable-->"+str(r[deliverable])+"---->"+str(r["List_Price"]))

	def UpdateChildActivities(self, Container):
		labor_list = {}
		container =  self.product.GetContainerByName(Container)
		for row in container.Rows:
			labor_list[row['Identifier']]= [row["PartNumber"],row["Activity_Type"],row["Activity"],row["Hours"],row["Edit Hours"],row["List_Price"],row["Productivity"],row["Comments"],row["FOWTWCost"],row["FO_MPA_Price"],row["Error_Message"],row["Execution Country"],row["Execution_Year"],row["Currency"],row["CostCurrency"],row["Pricing"],row['Regional_Cost']]
		SelectedProducts = self.product.GetContainerByName('Cyber Configurations')
		for row in SelectedProducts.Rows:
			if row["Part Desc"] == CS.cyberActivities[Container]:
				activities = row.Product.GetContainerByName('Activities')
				for activity in activities.Rows:
					if activity['Identifier'] in labor_list.keys():
						val = labor_list[activity['Identifier']]
						activity["PartNumber"] = val[0]
						activity["Activity_Type"] = val[1]
						activity["Activity"] = val[2]
						activity["Hours"] = val[3]
						activity["Edit Hours"] = val[4]
						activity["List_Price"] = val[5]
						activity["Productivity"] = val[6]
						activity["Comments"] = val[7]
						activity["FOWTWCost"] = val[8]
						activity["FO_MPA_Price"] = val[9]
						activity["Error_Message"] = val[10]
						activity["Execution Country"] = val[11]
						activity["Execution_Year"] = val[12]
						activity["Currency"] = val[13]
						activity["CostCurrency"] = val[14]
						activity["Pricing"] = val[15]
						activity['Regional_Cost'] = val[16]
				PopulateFinalizedActivities(row.Product)
				row.ApplyProductChanges()

	def populateCost(self, row):
		pm_productivity = self.product.Attr('PM_Adjustment_Productivity').GetValue()
		row["Adjustment_Productivity"] = pm_productivity
		if row["FO_Eng_Percentage_Split"] not in ('0','','0.0') and row["Final_Hrs"] not in ('','0.0','0'):
			if row["Execution_Country"] == self.quote.GetCustomField("Booking Country").Content:
				salesOrg = self.getSalesOrg(row["Execution_Country"])
				foPartsCost = self.getFopartsCost(salesOrg,row["FO_Eng"],row["Execution_Year"])
				if row["FO_Eng"] in foPartsCost and foPartsCost[row["FO_Eng"]]:
					regionalCost = round(getFloat(foPartsCost.get(row["FO_Eng"],0)),2)
					foFinalHours = getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100
					row["Regional_Cost"] = str(regionalCost * foFinalHours)
					row["FOUnitWTWCost"] = str(row["Regional_Cost"])
					row["FO_Unit_Regional_Cost"] = str(regionalCost)
				else:
					row["Regional_Cost"] = "0"
					row["FOUnitWTWCost"] = "0"
					row["FO_Unit_Regional_Cost"] = "0"
			else:
				salesOrg = self.getSalesOrg(row["Execution_Country"])
				foPartsCost = self.getFopartsCost(salesOrg,row["FO_Eng"],row["Execution_Year"])
				if row["FO_Eng"] in foPartsCost and foPartsCost[row["FO_Eng"]]:
					regionalCost = round(getFloat(foPartsCost.get(row["FO_Eng"], 0)), 2) + ((round(getFloat(foPartsCost.get(row["FO_Eng"], 0)), 2) * 10) / 100)
					regionalCost = round(regionalCost, 2)
					foFinalHours = getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100
					row["Regional_Cost"] = str(regionalCost * foFinalHours)
					row["FOUnitWTWCost"] = str(getFloat(row["Regional_Cost"]) / (1 + 0.1))
					row["FO_Unit_Regional_Cost"] = str(regionalCost)
				else:
					row["Regional_Cost"] = "0"
					row["FOUnitWTWCost"] = "0"
					row["FO_Unit_Regional_Cost"] = "0"
		else:
			row["Regional_Cost"] = "0"
			row["FOUnitWTWCost"] = "0"
			row["FO_Unit_Regional_Cost"] = "0"
		populateMPAPrice(row, 'Cyber_Labor_Project_Management' , self.quote, self.product)
		
	def project_management_total(self):
		final_hrs, regional_cost, unit_cost, fowtw_cost, foListprice, mpa_price, listprice, splitpercent, calculated_hrs = 0, 0, 0, 0, 0, 0, 0, 0, 0
		for i in range(0,2):
			for row in self.product.GetContainerByName('Cyber_Labor_Project_Management').Rows:
				if i == 0:
					if row['Deliverable'] != 'Total':
						if row['Final_Hrs'] != '':
							final_hrs += float(row['Final_Hrs'])
							calculated_hrs += float(row['Calculated_Hrs'])
							regional_cost += float(row['Regional_Cost']) if row['Regional_Cost'] != '' else 0
							unit_cost += float(row["FO_Unit_Regional_Cost"]) if row["FO_Unit_Regional_Cost"] !='' else 0
							fowtw_cost += float(row['FOUnitWTWCost']) if row['FOUnitWTWCost'] != '' else 0
							foListprice += float(row['FO_ListPrice']) if row['FO_ListPrice'] != '' else 0
							mpa_price += float(row['FO_MPA_Price']) if row['FO_MPA_Price'] != '' else 0
							listprice += float(row['List_Price']) if row['List_Price'] else 0
						splitpercent += float(row['FO_Eng_Percentage_Split']) if row['FO_Eng_Percentage_Split'] else 0
				else:
					if row['Deliverable'] == 'Total':
						row['Final_Hrs'] = str(int(final_hrs))
						row["Calculated_Hrs"] = str(calculated_hrs)
						row['Regional_Cost'] = str(regional_cost)
						row["FO_Unit_Regional_Cost"] = str(unit_cost)
						row['FOUnitWTWCost'] = str(fowtw_cost)
						row['FO_ListPrice'] = str(foListprice)
						row['FO_MPA_Price'] = str(mpa_price)
						row['List_Price'] = str(listprice)
						row['FO_Eng_Percentage_Split'] = str(splitpercent/4)
		
	def setDefaultLaborAttrValues(self):
		salesOrg = self.quote.GetCustomField('Sales Area').Content
		laborAttrDict = CS.getCyberLaborAttr
		for prod in laborAttrDict:
			self.product.Attr(laborAttrDict[prod]['country']).SelectDisplayValue(str(self.excecutionCountry))
			self.product.Attr(laborAttrDict[prod]['productivity']).AssignValue('1')
			self.product.Attr(laborAttrDict[prod]['salesOrg']).AssignValue(str(salesOrg))
			self.product.Attr(laborAttrDict[prod]['year']).AssignValue(str(date.today().year))
	
	def PopulateFinalQuantity(self, EventArgs):
		count = 0
		container = EventArgs.Container
		changedCell = EventArgs.ChangedCell
		oldValue = changedCell.OldValue
		newValue = changedCell.NewValue
		changedColumn = changedCell.ColumnName
		rowIndex = changedCell.RowIndex
		row = container.Rows[rowIndex]
		if changedColumn == 'Adj Quantity':
			if (row['PartNumber']).StartsWith('SVC'):
				row['Adj Quantity'] = '0'
				row['Final Quantity'] = str(int(float(row['Quantity']) + float(row['Adj Quantity'])))
			else:
				adj_quantity = 0 if row['Adj Quantity'] == '' else round(float(row['Adj Quantity']))
				row['Final Quantity'] = str(int(float(row['Quantity']) + adj_quantity))
				if (int(row['Final Quantity'])) < 0:
					row['Adj Quantity'] = '0'
					row['Final Quantity'] = str(int(float(row['Quantity'])))
				else:
					adj_quantity = 0 if row['Adj Quantity'] == '' else round(float(row['Adj Quantity']))
					row['Final Quantity'] = str(int(float(row['Quantity']) + adj_quantity))
		for row in container.Rows:
			row["container_index"] = "0"
			if row["Attribute"] != 'labor' and (str(row["Final Quantity"]) != '0' and str(row["Final Quantity"]) != '0.0'):
				count += 1
				row["container_index"] = str(count)
	
	def applyparts_function(self, activities, execution_prefix,Execution_Year_Msg):
		activities_rows = self.product.GetContainerByName(activities).Rows
		if activities_rows.Count > 0:
			country = self.product.Attr(execution_prefix+'Country')
			year = self.product.Attr(execution_prefix+'Year')
			Execution_country = country.GetValue()
			Execution_year = year.GetValue()
			Salesorg = self.product.ParseString("<* TABLE ( SELECT Execution_Country_Sales_Org FROM NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING WHERE Execution_County = '{}' ) *>".format(Execution_country))
			quotesalesOrg = self.quote.GetCustomField('Sales Area').Content
			currency = self.quote.GetCustomField('Currency').Content
			for row in activities_rows:
				if row.IsSelected:
					if Salesorg !='':
						cost_currency = self.product.ParseString("<* TABLE ( SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = '<* TABLE ( SELECT Cost_Currency_Code FROM HPS_Labor_Cost_Data WHERE Sales_Org = '{}' AND Part_Number = '{}' ) *>' AND To_Currency = '{}' ) *>".format(Salesorg,row["PartNumber"],currency))
						if row['Activity'] not in ['Total', 'On-Site', 'Off-Site']:
							if str(Execution_country) != '':
								row['Execution Country'] = str(Execution_country)
								row.GetColumnByName('Execution Country').SetAttributeValue(Execution_country)
							if str(Execution_year) != '':
								row['Execution_Year'] = str(Execution_year)
								row.GetColumnByName('Execution_Year').ReferencingAttribute.SelectDisplayValue(Execution_year)
							if cost_currency != '':
								row['Currency'] = currency
								row["CostCurrency"] = cost_currency
								cost = self.product.ParseString("<* TABLE ( SELECT Cost_CurrentMonth_Year1 FROM HPS_Labor_Cost_Data WHERE Sales_Org = '{}' AND Part_Number = '{}' ) *> ".format(quotesalesOrg,row["PartNumber"]))
								cost_val = cost if cost !='' else 0.00
								unit_cost = float(cost_val) * float(row["CostCurrency"])
								row["Pricing"] = str(round(unit_cost,2))
			self.executionYearTrigger(execution_prefix+'Year', activities, Execution_Year_Msg)
			populateWTW([activities], self.product, self.quote, True)
			if activities != 'Generic_System_Activities':
				self.UpdateChildActivities(activities)
			# To reset Execution year and Country in header level
			country.SelectValue('')
			year.AssignValue('')

	def projectmanagement_ExecutionYearTrigger(self, pm_execution_year):
		exeYearsRange =  set([DateTime.Now.Year +i for i in range(4)])
		
		if self.getCfValue("EGAP_Contract_Start_Date") != '' and self.getCfValue("EGAP_Contract_End_Date") != '':
			contractStartYear = UserPersonalizationHelper.CovertToDate( self.getCfValue("EGAP_Contract_Start_Date")).Year
			contractEndYear = UserPersonalizationHelper.CovertToDate(self.getCfValue("EGAP_Contract_End_Date")).Year			
			year = int(pm_execution_year) if pm_execution_year != '' else 0
			self.setAttrValue("Labor_PM_Message",'')
			if len(str(year)) < 4 or year < DateTime.Now.Year or year not in exeYearsRange:
				self.setAttrValue("Labor_PM_Message",'User is allowed to enter current + next 3 years in 20XX format (e.g. 2023, 2025 etc)')
				self.setAttrValue("PM_Execution_Year",'')
			else:
				if year <= contractEndYear and year >= contractStartYear:
					container =  self.product.GetContainerByName("Cyber_Labor_Project_Management")
					for row in container.Rows:
						if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
							row["Execution_Year"] = str(year)
							row.GetColumnByName('Execution_Year').ReferencingAttribute.SelectDisplayValue(str(year))
							self.populateCost(row)
					self.setAttrValue("PM_Execution_Year",'')
				else:
					self.etAttrValue("Labor_PM_Message",'Execution Year should be in between the Contract start date and Contract end date')
					self.setAttrValue("PM_Execution_Year",'')
		else:
			year = int(pm_execution_year) if pm_execution_year != '' else 0
			self.setAttrValue("Labor_PM_Message",'')
			if year not in exeYearsRange:
				self.setAttrValue("Labor_PM_Message",'User is allowed to enter current + next 3 years in 20XX format (e.g. 2023, 2025 etc)')
				self.setAttrValue("PM_Execution_Year",'')
			else:
				container =  self.product.GetContainerByName("Cyber_Labor_Project_Management")
				for row in container.Rows:
					if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
						row["Execution_Year"] = str(year)
						row.GetColumnByName('Execution_Year').ReferencingAttribute.SelectDisplayValue(str(year))
						self.populateCost(row)

	def projectmanagement_ExecutionCountryTrigger(self):
		pm_execution_year = self.product.Attr('PM_Execution_Year').GetValue()
		executionCountry = self.product.Attr('PM_Execution_Country').GetValue()
		if pm_execution_year != '':
			self.projectmanagement_ExecutionYearTrigger(pm_execution_year)
		if executionCountry != '':
			projectManagementCon =  self.product.GetContainerByName("Cyber_Labor_Project_Management")
			executionCountry = self.product.Attr('PM_Execution_Country').GetValue()
			for row in projectManagementCon.Rows:
				salesOrg = self.getSalesOrg(executionCountry)
				foPartsCost = self.getFopartsCost(salesOrg,row["FO_Eng"],row["Execution_Year"])
				if foPartsCost.Count != 0:
					if row["Deliverable"] not in ('Total','Off-Site','On-Site') and row.IsSelected:
						row["Execution_Country"] = executionCountry
						row.GetColumnByName('Execution_Country').SetAttributeValue(executionCountry)
						if row["Deliverable"] != 'Total':
							self.populateCost(row)
					row["Error_Message"] = 'True'
				else:
					row["Error_Message"] = ''
				if row['Deliverable'] in ['Total', 'On-Site', 'Off-Site']:
					row["Error_Message"] = 'True'

		self.product.Attr("PM_Execution_Country").SelectValue('')
		self.product.Attr('PM_Execution_Year').AssignValue('')