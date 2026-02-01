from System import DateTime

def getContainer(Name, Product):
	return Product.GetContainerByName(Name)

def getCfValue(Name, Quote):
	return Quote.GetCustomField(Name).Content
	
def getFloat(Var):
	if Var:
		return float(Var)
	return 0
	
def getSalesOrg(country):
	query = SqlHelper.GetFirst("select Execution_Country_Sales_Org from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_County = '{}'".format(country))
	if query is not None:
		return query.Execution_Country_Sales_Org

def laborCostWithCOnversion(laborcostParts, Quote):
	quoteCurrency = Quote.GetCustomField('Currency').Content
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

def getFopartsCost(salesOrg,partNumber,executionYear, Quote):
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
	foCostWithConversion = laborCostWithCOnversion(foCost, Quote)
	return foCostWithConversion

def getDefaultExecutionYear(Quote):
	executionYear = str(DateTime.Now.Year)
	yearsList = []
	currentYear = DateTime.Now.Year
	i = 0
	while i < 4:
		year = currentYear + i
		yearsList.append(year)
		i += 1
	if getCfValue("EGAP_Contract_Start_Date", Quote) != '':
		year = UserPersonalizationHelper.CovertToDate(getCfValue("EGAP_Contract_Start_Date", Quote)).Year
		if year in yearsList:
			executionYear = year
		else:
			executionYear = yearsList[-1] if len(yearsList) > 0 else str(DateTime.Now.Year)
	return executionYear

	
def getExecutionCountry(Quote):
	salesOrg = Quote.GetCustomField('Sales Area').Content
	currency = Quote.GetCustomField('Currency').Content
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
	if query is not None:
		return query.Execution_County
	
def currencyCOnversion(Price,Quote):
	quoteCurrency = Quote.GetCustomField('Currency').Content
	priceWithConversion = dict()
	if Price:
		for key in Price:
			Trace.Write(Price[key]["stdcurrency"])
			query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(Price[key]["stdcurrency"],quoteCurrency))
			if query is not None:
				priceWithConversion[key] = getFloat(Price[key]["price"]) * getFloat(query.Exchange_Rate)
			else:
				priceWithConversion[key] = getFloat(Price[key]["price"])
	return priceWithConversion

def getMPAPrice(salesOrg, partNumber, honeywellRef, totalManHours, Quote):
	mpaPrice = {}
	query_template = (
		"SELECT Unit_MPA_Price, Currency, Service_Material "
		"FROM GES_MPA_PRICE "
		"WHERE SalesOrg = '{0}' AND Service_Material = '{1}' "
		"AND HoneywellRef = '{2}'"
	).format(salesOrg, partNumber, honeywellRef)

	if honeywellRef == "1-CUN51UZ":
		query = query_template + " AND cast(Minimum_MH as float) <= {0} AND cast(Maximum_MH as float) > {1}".format(
			totalManHours, totalManHours
		)
	else:
		query = query_template

	res = SqlHelper.GetFirst(query)
	if res is not None and res.Unit_MPA_Price:
		mpaPrice[res.Service_Material] = {
			"price": res.Unit_MPA_Price,
			"stdcurrency": res.Currency
		}
	unitMPAPrice = currencyCOnversion(mpaPrice, Quote)
	return getFloat(unitMPAPrice.get(partNumber, 0)) if partNumber in unitMPAPrice else 0

def val_totalManHours(container_name,Product):
	if container_name == "Cyber_Labor_Project_Management":
		hours = "Final_Hrs"
		activity = "Deliverable"
	else:
		hours = "Edit Hours"
		activity = "Activity"
	totalManHours = 0.00
	Container = Product.GetContainerByName(container_name)
	for row in Container.Rows:
		if row[activity] == 'Total':
			if row[hours] !='':
				totalManHours = totalManHours + float(row[hours])
			break
	return totalManHours

def populateMPAPrice(row,container,Quote,Product):
	alternate_execution_country = Quote.GetCustomField('R2Q_Alternate_Execution_Country').Content
	if container == "Cyber_Labor_Project_Management":
		hours = row["Final_Hrs"]
		deliverable = row["FO_Eng"]
		execution_country = row["Execution_Country"]
	else:
		hours = row["Edit Hours"]
		deliverable = row["PartNumber"]
		execution_country = row["Execution Country"]
	if hours not in ('','0'):
		salesOrg = getSalesOrg(execution_country)
		honeywellRef = Quote.GetCustomField('MPA Honeywell Ref').Content
		totalManHours = val_totalManHours(container,Product)
		foMPAPrice = getMPAPrice(salesOrg,deliverable,honeywellRef,totalManHours,Quote)
		#Trace.Write("foMPAPrice----->"+str(foMPAPrice))
		if foMPAPrice and foMPAPrice !='None':
			MPAPrice = round(getFloat(foMPAPrice),2)
			foFinalHours = round(getFloat(hours),2)
			row["FO_MPA_Price"] = str(MPAPrice * foFinalHours)
		else:
			row["FO_MPA_Price"] = "0"
	else:
		row["FO_MPA_Price"] = "0"

def populateWTWCost(row,defaultExecutionYear, Quote, cellchanged):
	alternate_execution_country = Quote.GetCustomField('R2Q_Alternate_Execution_Country').Content
	execution_year = Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content
	Log.Info("custom field execution year--->"+str(execution_year))
	if Quote.GetCustomField('R2QFlag').Content == 'Yes' and cellchanged == None:
		row["Execution_Year"] = execution_year
		Log.Info("value changes here--->"+str(row["Execution_Year"]))
		'''if row["Execution_Year"]:
			row.GetColumnByName('Execution_Year').ReferencingAttribute.SelectDisplayValue(row["Execution_Year"])'''
	row["Error_Message"] = "True"
	#bookingCountry = getCfValue("Booking Country", Quote).title()
	bookingCountry = getExecutionCountry(Quote)
	if row["Edit Hours"] not in ('','0.0','0'):
		if row["Execution Country"] == bookingCountry:
			salesOrg = getSalesOrg(row["Execution Country"])
			foPartsCost = getFopartsCost(salesOrg,row["PartNumber"],row["Execution_Year"], Quote)
			Log.Info(str(row["Execution_Year"])+"--year--->"+str(cellchanged)+"---cellchanged---"+str(foPartsCost.get(row["PartNumber"]))+"---if---foPartsCost---"+str(type(foPartsCost.get(row["PartNumber"]))))
			if Quote.GetCustomField('R2QFlag').Content == 'Yes' and foPartsCost.get(row["PartNumber"]) in (0.00,0.0,0,None,'') and cellchanged == None:
				row["Execution Country"] = alternate_execution_country
				row.GetColumnByName('Execution Country').SetAttributeValue(row["Execution Country"])
				salesOrg = getSalesOrg(alternate_execution_country)
				foPartsCost = getFopartsCost(salesOrg,row["PartNumber"],row["Execution_Year"], Quote)
			if row["Execution_Year"] == defaultExecutionYear:
				row["Pricing"] = str(round(getFloat(foPartsCost.get(row["PartNumber"],0)),2))
				regionalCost = round(getFloat(row["Pricing"]),2)
				foFinalHours = round(getFloat(row["Edit Hours"]),2)
				row["Regional_Cost"] = str(regionalCost * foFinalHours)
				row["FOWTWCost"] = str(row["Regional_Cost"])
			else:
				if row["PartNumber"] in foPartsCost and foPartsCost[row["PartNumber"]]:
					row["Pricing"] = str(round(getFloat(foPartsCost.get(row["PartNumber"],0)),2))
					regionalCost = round(getFloat(foPartsCost.get(row["PartNumber"],0)),2)
					foFinalHours = round(getFloat(row["Edit Hours"]))
					row["Regional_Cost"] = str(regionalCost * foFinalHours)
					row["FOWTWCost"] = str(row["Regional_Cost"])
				else:
					row["Regional_Cost"] = "0"
					row["FOWTWCost"] = "0"
					row["Pricing"] = "0"
					row["Error_Message"] = ""
		else:
			salesOrg = getSalesOrg(row["Execution Country"])
			foPartsCost = getFopartsCost(salesOrg,row["PartNumber"],row["Execution_Year"], Quote)
			Log.Info(str(row["Execution_Year"])+"--year--->"+str(cellchanged)+"---cellchanged---"+str(foPartsCost.get(row["PartNumber"]))+"---else---foPartsCost---"+str(type(foPartsCost.get(row["PartNumber"]))))
			if Quote.GetCustomField('R2QFlag').Content == 'Yes' and foPartsCost.get(row["PartNumber"]) in (0.00,0.0,0,None,'') and cellchanged == None:
				row["Execution Country"] = alternate_execution_country
				row.GetColumnByName('Execution Country').SetAttributeValue(row["Execution Country"])
				salesOrg = getSalesOrg(alternate_execution_country)
				foPartsCost = getFopartsCost(salesOrg,row["PartNumber"],row["Execution_Year"], Quote)
			if row["PartNumber"] in foPartsCost and foPartsCost[row["PartNumber"]]:
				row["Pricing"] = str(round(getFloat(foPartsCost.get(row["PartNumber"],0)),2))
				regionalCost = round(getFloat(foPartsCost.get(row["PartNumber"],0)),2) + ((round(getFloat(foPartsCost.get(row["PartNumber"],0)),2) * 10) / 100)
				foFinalHours = round(( getFloat(row["Edit Hours"])))
				row["Regional_Cost"] = str(regionalCost * foFinalHours)
				row["FOWTWCost"] = str(getFloat(row["Regional_Cost"]) / (1 + 0.1))
			else:
				row["Regional_Cost"] = "0"
				row["FOWTWCost"] = "0"
				row["Pricing"] = "0"
				row["Error_Message"] = ""
	else:
		row["Regional_Cost"] = "0"
		row["FOWTWCost"] = "0"
		row["Pricing"] = "0"

def populateWTW(cont_list, Product, Quote, cellchanged=None):
	executionCountry = getExecutionCountry(Quote)
	bookingCountry = getCfValue("Booking Country", Quote).title()
	defaultExecutionYear = str(getDefaultExecutionYear(Quote))

	for container in cont_list:
		for row in getContainer(container, Product).Rows:
			if row["Activity"] not in ('Total', 'Off-Site', 'On-Site'):
				populateWTWCost(row, defaultExecutionYear, Quote, cellchanged)
				populateMPAPrice(row, container, Quote, Product)
		getContainer(container, Product).Calculate()

	activity_data = {
		'Onsite': {'Hours': 0, 'Edit Hours': 0, 'Pricing': 0.0, 'List_Price': 0.0, 'FO_List_Price': 0.0, 'FO_MPA_Price': 0.0, 'Regional_Cost': 0.0, 'FOWTWCost': 0.0},
		'Offsite': {'Hours': 0, 'Edit Hours': 0, 'Pricing': 0.0, 'List_Price': 0.0, 'FO_List_Price': 0.0, 'FO_MPA_Price': 0.0, 'Regional_Cost': 0.0, 'FOWTWCost': 0.0}
	}

	def accumulate_values(activity_type, row):
		if activity_type in activity_data:
			activity_data[activity_type]['Hours'] += int(float(row['Hours'])) if row['Hours'] !='' else 0.00
			activity_data[activity_type]['Edit Hours'] += int(float(row['Edit Hours'])) if row['Edit Hours'] !='' else 0.00
			activity_data[activity_type]['Pricing'] += round(float(row['Pricing']),2) if row['Pricing'] !='' else 0.00
			activity_data[activity_type]['List_Price'] += round(float(row['List_Price']),2) if row['List_Price'] !='' else 0.00
			activity_data[activity_type]['FO_List_Price'] += round(float(row['FO_List_Price']),2) if row['FO_List_Price'] !='' else 0.00
			activity_data[activity_type]['FO_MPA_Price'] += round(float(row['FO_MPA_Price']),2) if row['FO_MPA_Price'] !='' else 0.00
			activity_data[activity_type]['Regional_Cost'] += round(float(row['Regional_Cost']),2) if row['Regional_Cost'] !='' else 0.00
			activity_data[activity_type]['FOWTWCost'] += round(float(row['FOWTWCost']),2) if row['FOWTWCost'] !='' else 0.00

	for container in cont_list:
		for row in getContainer(container, Product).Rows:
			accumulate_values(row['Activity_Type'], row)

	for container in cont_list:
		for row in getContainer(container, Product).Rows:
			if row['Identifier'] == 'Total':
				for key in activity_data['Onsite']:
					Trace.Write(str(key)+"--final--"+str((activity_data['Onsite'][key]) + (activity_data['Offsite'][key])))
					row[key] = str((activity_data['Onsite'][key]) + (activity_data['Offsite'][key]))
			elif row['Identifier'] == 'On-Site':
				for key in activity_data['Onsite']:
					row[key] = str(activity_data['Onsite'][key])
			elif row['Identifier'] == 'Off-Site':
				for key in activity_data['Offsite']:
					row[key] = str(activity_data['Offsite'][key])