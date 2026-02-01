import math
from System import DBNull

def addToTotal(totalDict , key , value):
	totalDict[key] = totalDict.get(key , 0) + value

def getCFValue(Quote, field):
	return Quote.GetCustomField(field).Content

def GetQuoteTable(Quote, Name):
	return Quote.QuoteTables[Name]

def hideQuoteTableColumn(table,column):
	table.GetColumnByName(column).AccessLevel = table.AccessLevel.Hidden

def deleteRows(table, obsoleteCategoryTypes):
	if table.Rows.Count:
		for row in table.Rows:
			if row['Row_Type'] == 'Header':
				currentMaterialType = row['Cost_Category_Type']
			if currentMaterialType in obsoleteCategoryTypes:
				table.DeleteRow(row.Id)

def makeColumnReadonly(table, columnTobeReadonly, categoryTypes):
	if table.Rows.Count:
		for row in table.Rows:
			if row['Row_Type'] == 'Header':
				currentMaterialType = row['Cost_Category_Type']
			if currentMaterialType not in categoryTypes:
				row.Cells.Item[columnTobeReadonly].AccessLevel = table.AccessLevel.ReadOnly

def getCondition(costCategory):
	conditions = {
		'Other Goods & Services': " WHERE Cost_Category in ('Standard Warranty','Other','Pre-Sales')",
		'Third Party Goods & Services': " WHERE Cost_Category in ('Third-Party Material','Third-Party Labor')",
		'Honeywell Subscription Software': " WHERE Cost_Category ='Honeywell Software' and Sub_LOB like 'SUB%'",
		'Honeywell Material': " WHERE Cost_Category ='Honeywell Material'",
		'Honeywell Labor': " WHERE Cost_Category ='Honeywell Labor'",
		'Honeywell Software': " WHERE Cost_Category ='Honeywell Software' and Sub_LOB not like 'SUB%'",
		'Honeywell HCI software': " WHERE Cost_Category ='Honeywell Software' and LOB ='AS' and Sub_LOB not like 'SUB%'",
		'Honeywell HCI Labor & BGP': " WHERE Cost_Category ='Honeywell Labor' and LOB ='AS'",
		'Honeywell PMC Material': " WHERE Cost_Category ='Honeywell Material' and LOB ='PMC'",
		'Honeywell P3 Material': " WHERE Cost_Category ='Honeywell Material' and LOB ='PAS' and Sub_LOB = 'P3'"
	}
	return conditions.get(costCategory, '')

def populatePlsgData(Quote, categoryType):
	# Create the base SQL query
	base_query = """
		SELECT DISTINCT A.PLSG_Description, A.PLSG_WTW_Cost 
		FROM QT__Product_Line_Sub_Group_Details A 
		JOIN SAP_PLSG_LOB_Mapping B ON A.Product_Line_Sub_Group = B.SAP_PL_PLSG 
		WHERE A.cartId = {} AND A.ownerId = {}
	""".format(Quote.QuoteId, Quote.UserId)

	# Create a dictionary for different category
	category_queries = {
		'Honeywell HCI software': base_query + " AND B.Cost_Category = 'Honeywell Software' AND B.LOB = 'AS' AND B.Sub_LOB NOT LIKE 'SUB%'",
		'Honeywell Labor': base_query + " AND B. Cost_Category ='Honeywell Labor'",
		'Honeywell HCI Labor & BGP': base_query + " AND B.Cost_Category = 'Honeywell Labor' AND B.LOB = 'AS'",
		'Honeywell Subscription Software': base_query + " AND B.Cost_Category = 'Honeywell Software' AND B.Sub_LOB LIKE 'SUB%'"
	}

	# Get the SQL query for the specified categoryType
	sql_query = category_queries.get(categoryType)
	# if Quote.GetCustomField("Booking LOB").Content == "HCP" and categoryType == 'Honeywell Labor':
	if categoryType == 'Honeywell Labor':
		sql_query = sql_query+"AND B.LOB != 'AS'"
	# Execute the SQL query and retrieve results
	sql_result = SqlHelper.GetList(sql_query)

	# Create lists for descriptions and costs
	default_desc, default_wtwcost = [], []
	if sql_result:
		for row in sql_result:
			default_desc.append(row.PLSG_Description)
			default_wtwcost.append(row.PLSG_WTW_Cost)

	return default_desc, default_wtwcost

def setAccessLevels(row, cashOutflow, categoryType, readOnlyColumns):
	if row['Row_Type'] == 'Total':
		for col in readOnlyColumns:
			row.Cells.Item[col].AccessLevel = cashOutflow.AccessLevel.ReadOnly
	else:
		if categoryType not in ['Third Party Goods & Services', 'Other Goods & Services', 'Third Party Buyout']:
			row.Cells.Item['Vendor_Payment_Term'].AccessLevel = cashOutflow.AccessLevel.ReadOnly
		if categoryType not in ['Honeywell P3 Material']:
			row.Cells.Item['P3_Product_Type'].AccessLevel = cashOutflow.AccessLevel.ReadOnly

def addDefaultRows(Quote, cashOutflow, defaultRows, categoryType, readOnlyColumns, row_dict = None):
	# Define the specific categories for updated_rows
	specific_categories = ['Honeywell HCI software', 'Honeywell HCI Labor & BGP', 'Honeywell Subscription Software','Honeywell Labor']
	
	if categoryType in specific_categories:
		# Populate data for specific categories
		default_desc, default_wtwcost = populatePlsgData(Quote, categoryType)

		getDesc = row_dict.get(categoryType, {})
		updated_rows = []
		for i, (desc, cost) in enumerate(zip(default_desc, default_wtwcost)):
			row = {
				'Shipment_Number': 'Shipment ' + str(i + 1),
				'Shipment_Description': desc,
				'Cost': float(cost),
				'Row_Type': 'Item'
			}
			if desc in getDesc:
				row['Month_ARO'] = getDesc[desc]
			updated_rows.append(row)

		updated_rows.append({'Shipment_Number': 'Total of Entered Shipment', 'Row_Type': 'Total'})
		rows_to_add = updated_rows
	else:
		rows_to_add = defaultRows
	# Add rows to cashOutflow and set access levels
	for data in rows_to_add:
		row = cashOutflow.AddNewRow()
		for key in data.keys():
			row[key] = data[key]
			Trace.Write("key-->"+str(data[key]))
		setAccessLevels(row, cashOutflow, categoryType, readOnlyColumns)


def getDifference(Quote, cashOutflow, costCategoryTypeDict, readOnlyColumns):
	toBeDeleted = []
	toBeSkipped = []
	row_dict = {}
	sqlTotal = "Select Row_Type from QT__Cash_Outflow where ownerid={} and cartid={} and Row_Type='{}'"
	sqlRes = SqlHelper.GetFirst(sqlTotal.format(Quote.UserId,Quote.QuoteId,'Total'))
	if sqlRes is None:
		cashOutflow.Rows.Clear()
	else:
		for row in cashOutflow.Rows:
			qtCostCategoryType = row['Cost_Category_Type']
			qtCost = row['Cost']
			'''Making the selected column as readonly'''
			if row['Row_Type'] in ['Header', 'Total']:
				for col in readOnlyColumns:
					row.Cells.Item[col].AccessLevel = cashOutflow.AccessLevel.ReadOnly
				if qtCostCategoryType in costCategoryTypeDict.keys():
					toBeSkipped.append(qtCostCategoryType)
					if round(costCategoryTypeDict[qtCostCategoryType],2) != qtCost:
						hcicostcategorylist = ['Honeywell HCI software', 'Honeywell HCI Labor & BGP', 'Honeywell Subscription Software']
						if qtCostCategoryType in hcicostcategorylist:
							Trace.Write('Delete and update cashflow')
							row_dict = getCategoriesRows(cashOutflow, hcicostcategorylist)
							#deleteRows(cashOutflow, qtCostCategoryType)
							toBeDeleted.append(qtCostCategoryType)
							toBeSkipped.remove(qtCostCategoryType)
						else:
							row['Cost'] = costCategoryTypeDict[qtCostCategoryType]
				elif qtCostCategoryType != '':
					toBeDeleted.append(qtCostCategoryType)
	return toBeDeleted, toBeSkipped, row_dict

def getCostCategoryType(costCategory, LOB, bookingLOB, subLOB):
	if costCategory == 'Honeywell Material':
		return 'Honeywell PMC Material' if LOB == 'PMC' else 'Honeywell P3 Material' if LOB == 'PAS' and subLOB == 'P3' else 'Honeywell Material'
	elif costCategory == 'Honeywell Software':
		if subLOB.lower().startswith('sub'):
			return 'Honeywell Subscription Software'
		return 'Honeywell HCI software' if LOB == 'AS' else 'Honeywell Software'
	elif costCategory == 'Honeywell Labor':
		return 'Honeywell HCI Labor & BGP' if LOB == 'AS' else 'Honeywell Labor'
	elif costCategory in ['Standard Warranty', 'Other', 'Pre-Sales']:
		return 'Other Goods & Services'
	elif costCategory in ['Third-Party Material', 'Third-Party Labor']:
		return 'Third Party Goods & Services'
	return costCategory

def addNewRecords(newRecord, noOfNewRecords, resultArray, shipmentNumber):
	for n in range(noOfNewRecords):
		updatedRecord = newRecord.copy()
		updatedRecord['Shipment_Number'] = 'Shipment {}'.format(shipmentNumber)
		resultArray.append(updatedRecord)
		shipmentNumber += 1
	return resultArray, noOfNewRecords

def makeQuoteTableColumnsReadonly(cashOutflow, columns, columnTobeReadonly, categoryTypes):
	for row in cashOutflow.Rows:
		if row['Row_type'] in ['Header', 'Total']:
			if row['Row_type'] == 'Header':
				currentMaterialType = row['Cost_Category_Type']
			for col in columns:
				row.Cells.Item[col].AccessLevel = cashOutflow.AccessLevel.ReadOnly
		elif currentMaterialType not in categoryTypes:
			row.Cells.Item[columnTobeReadonly].AccessLevel = cashOutflow.AccessLevel.ReadOnly
	cashOutflow.Save()

def getHeadersRowId(Quote):
	sqlResult = SqlHelper.GetList("Select Id,Cost from QT__Cash_Outflow where ownerid={} and cartid={} and Row_Type='{}'".format(Quote.UserId,Quote.QuoteId,'Header'))
	headerRowIds = []
	wtwCosts = dict()
	for row in sqlResult:
		headerRowIds.append(row.Id)
		wtwCosts[row.Id] = row.Cost
	return wtwCosts, headerRowIds

def updateTotalCost(Quote, cashOutflow):
	currentMaterialType = ''
	errorMessage = []
	for row in cashOutflow.Rows:
		if row['Row_Type'] == 'Header':
			currentMaterialType = row['Cost_Category_Type']
			Trace.Write('Header currentWTWCost='+str(row['Cost']))
 			if Quote.GetCustomField('Quote Type').Content in('Contract Renewal','Contract New'):
 				currentWTWCost = row['Cost']
 			else:
 				currentWTWCost = round(row['Cost'],2)
			row['Shipment_Description'] = ''
			totalWTWCost = 0
			shipmentNumber = 1
		elif row['Cost_Category_Type']  == '' and row['Row_Type'] == 'Item':
			totalWTWCost += row['Cost']
			Trace.Write('Item totalWTWCost='+str(row['Cost']))
			row['Shipment_Number'] = 'Shipment {}'.format(shipmentNumber)
			shipmentNumber +=1
			errorString = ''
			if Quote.GetCustomField('Quote Type').Content == 'Contract Renewal' and Quote.GetCustomField('EGAP_Project_Duration_Months').Content == '' and Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content.lower() == 'true':
				cf_projectDuration = int(Quote.GetCustomField('SC_CF_Term_duration_Months').Content) if Quote.GetCustomField('SC_CF_Term_duration_Months').Content.strip() != '' else 0
			else:
				cf_projectDuration = int(Quote.GetCustomField('EGAP_Project_Duration_Months').Content) if Quote.GetCustomField('EGAP_Project_Duration_Months').Content.strip() != '' else 0
			if row['Month_ARO'] <= 0:
				errorString = "Month ARO entered is less than or equal to 0  - {}".format(currentMaterialType)
			elif row['Month_ARO'] > cf_projectDuration:
				errorString = "Month ARO entered is not within the project duration({}) - {}".format(cf_projectDuration, currentMaterialType)
			if errorString not in errorMessage and errorString != '':
				errorMessage.append(errorString)
		elif row['Row_Type'] == 'Total':
			row['Cost'] = totalWTWCost
			errorString = "WTW cost calculated does not match with Total of shipment cost entered for the cost category - {}".format(currentMaterialType)
			Trace.Write('totalWTWCost='+str(row['Cost'])+"==currentWTWCost=="+str(currentWTWCost))
			if float(row['Cost']) != currentWTWCost and errorString not in errorMessage:
				Trace.Write('inside if totalWTWCost='+str(row['Cost'])+"==currentWTWCost=="+str(currentWTWCost))
				errorMessage.append(errorString)
	#cashOutflow.Save()
	if len(errorMessage):
		return ', '.join(errorMessage)
	else:
		return

def cashOutflowCostConstants(keyType, keyName):
	sqlRes = SqlHelper.GetFirst("Select Key_Value from EGAP_CashOutflow_Cost_Constants Where Key_Type = '{}' and Key_Name ='{}'".format(keyType, keyName))
	res = 0
	if sqlRes is not None:
		res = float(sqlRes.Key_Value) if keyType == 'DAYS' else float(sqlRes.Key_Value)/100
	return res

def getPriceReceipt(Quote, cost, costCategory):
	condition = getCondition(costCategory)
	#if Quote.GetCustomField("Booking LOB").Content == "HCP" and costCategory == 'Honeywell Labor':
	if costCategory == 'Honeywell Labor':
		condition = condition+"and LOB !='AS'"

	#sellPrice = getSellPrice(Quote, condition)
	WTWCost, sellPrice = getWTWCost_sellprice(Quote, condition)
	#WTWCost = getWTWCost(Quote, condition)
	div = (1 - (sellPrice - WTWCost) / sellPrice) if sellPrice > 0 else 0
	priceReceipt = cost / div if div > 0 else 0
	return round(priceReceipt, 2)

def addNewRowProjectMilestone(projectMilestone, defaultData, sourceRow):
	newRow = projectMilestone.AddNewRow()
	for col in defaultData.keys():
		if col in sourceRow.keys():
			newRow[col] = sourceRow[col]
		else:
			newRow[col] = defaultData[col]

def getQuoteTableData(Quote, column, quoteTableName, condition):
	query = "Select {} as output from {} where ownerid={} and cartid={} {} ".format(column, quoteTableName, Quote.UserId, Quote.QuoteId, condition)
	qtResult = SqlHelper.GetFirst(query)
	output = 0
	if qtResult is not None and len(qtResult) > 0:
		output = qtResult.output if qtResult.output != DBNull.Value else 0
	return output

def getCreditTermsMonths(Quote):
	creditTermsMonths = 0
	cf_creditTermsMonths = Quote.GetCustomField('EGAP_Credit_Terms_Months')
	if cf_creditTermsMonths.Content:
		if int(cf_creditTermsMonths.Content) >0:
			creditTermsMonths = int(cf_creditTermsMonths.Content)
	return creditTermsMonths

def getMaxMonthARO(Quote):
	maxMonthARO = 0
	cf_MilestoneProjectDurationMonths = Quote.GetCustomField('EGAP_Milestone_Project_Duration_Months')
	if cf_MilestoneProjectDurationMonths.Content:
		if float(cf_MilestoneProjectDurationMonths.Content) >0:
			maxMonthARO = math.ceil(float(cf_MilestoneProjectDurationMonths.Content))
	return maxMonthARO

def getMaxMonthARONew(Quote, table):
	sqlQuery = ''
	maxMonthARO = 0
	if table == 'Cash_Outflow':
		sqlQuery = "SELECT MAX(MaxMonthARO) as MaxMonthARO from (SELECT MAX(Adj_Month_ARO) MaxMonthARO  From QT__Cash_Outflow where ownerid={} and cartid={} Union SELECT MAX(ARO_Labor) MaxMonthARO  From QT__Cash_Outflow where ownerid={} and cartid={} Union SELECT MAX(ARO_Burden) MaxMonthARO  From QT__Cash_Outflow where ownerid={} and cartid={} Union SELECT MAX(ARO_Material) MaxMonthARO  From QT__Cash_Outflow where ownerid={} and cartid={} Union SELECT MAX(ARO_Purchasing) MaxMonthARO  From QT__Cash_Outflow where ownerid={} and cartid={} Union SELECT MAX(ARO_Freight) MaxMonthARO  From QT__Cash_Outflow where ownerid={} and cartid={} Union SELECT MAX(Adj_Month_Price) MaxMonthARO  From QT__Cash_Outflow where ownerid={} and cartid={} Union SELECT MAX(Adj_Month_Price) MaxMonthARO  From QT__EGAP_Honeywell_Labor_Cost_Curve where ownerid={} and cartid={} ) as temp".format(Quote.UserId,Quote.QuoteId,Quote.UserId,Quote.QuoteId,Quote.UserId,Quote.QuoteId,Quote.UserId,Quote.QuoteId,Quote.UserId,Quote.QuoteId,Quote.UserId,Quote.QuoteId,Quote.UserId,Quote.QuoteId,Quote.UserId,Quote.QuoteId)
	elif table == 'Project_Milestone':
		sqlQuery = "SELECT MAX(EGAP_Month_ARC) as MaxMonthARO FROM QT__EGAP_Project_Milestone where ownerid={} and cartid={} ".format(Quote.UserId,Quote.QuoteId)
	elif table == "Honeywell_HCI_Labor_BGP_Cost_Curve":
		sqlQuery = "SELECT MAX(cast(Month_ARO as INT)) as MaxMonthARO FROM QT__Honeywell_HCI_Labor_BGP_Cost_Curve where ownerid={} and cartid={} ".format(Quote.UserId,Quote.QuoteId)
	if sqlQuery != '':
		sqlResult = SqlHelper.GetFirst(sqlQuery)
		if sqlResult is not None and sqlResult.MaxMonthARO != DBNull.Value:
			maxMonthARO = sqlResult.MaxMonthARO
	projectDurationMonths = int(getMaxMonthARO(Quote))
	maxMonthARO = maxMonthARO if maxMonthARO > projectDurationMonths else projectDurationMonths
	return maxMonthARO

def validateProjectMilestoneData(projectMilestone, maxMonthARO):
	errorMessage = []
	i = 1
	totalMilestonePct = 0
	for row in projectMilestone.Rows:
		if row['Row_Type'] != 'Header':
			if row['Month_ARO'] > float(maxMonthARO) or row['Month_ARO'] < 0.0:
				errorMessage.append("Row {}: Month ARO is not within Contract Period".format(i))
			totalMilestonePct += row['EGAP_Pct_of_Total_Milestone_Payment']
		i += 1
	
	if totalMilestonePct != 100:
		errorMessage.append("Sum of % milestone payment is not equal to 100%")
	if len(errorMessage):
		return ', '.join(errorMessage)
	else:
		return

def getWTWCost_sellprice(Quote, costCategoryCondition):
    wtcCost = 0
    pLSG = []
    if costCategoryCondition == 'Honeywell Labor':
        costCategoryCondition = " WHERE Cost_Category ='Honeywell Labor' and LOB != 'AS'"
        #if Quote.GetCustomField("Booking LOB").Content == "HCP":
            #costCategoryCondition = costCategoryCondition+"AND LOB != 'AS'"
    elif costCategoryCondition == 'Honeywell HCI Labor & BGP':
        costCategoryCondition = " WHERE Cost_Category ='Honeywell Labor' and LOB ='AS'"
    elif costCategoryCondition == 'Honeywell HCI software':
        costCategoryCondition = " WHERE Cost_Category ='Honeywell Software' and LOB ='AS' and Sub_LOB not like 'SUB%'"
    SqlQuery = "SELECT Distinct SAP_PL_PLSG FROM SAP_PLSG_LOB_Mapping {}".format(costCategoryCondition)
    SqlResult = SqlHelper.GetList(SqlQuery)
    if SqlResult is not None and len(SqlResult) > 0:
        for row in SqlResult:
            pLSG.append(row.SAP_PL_PLSG)
    sellPrice = 0
    pLSG = []
    SqlQuery = "SELECT Distinct SAP_PL_PLSG FROM SAP_PLSG_LOB_Mapping {}".format(costCategoryCondition)
    SqlResult = SqlHelper.GetList(SqlQuery)
    if SqlResult is not None and len(SqlResult) > 0:
        for row in SqlResult:
            pLSG.append(row.SAP_PL_PLSG)
            
    if Quote.Items.Count > 0:
        for item in Quote.Items:
            if item.AsMainItem and len(list(item.AsMainItem.Children)):
                continue
            if float(item.QI_ExtendedWTWCost.Value) >= 0 and item.QI_PLSG.Value in pLSG:
                #wtcCost += round(item.QI_ExtendedWTWCost.Value,2)
                wtcCost += float(item.QI_ExtendedWTWCost.Value)
            if float(item.ExtendedAmount) >= 0 and item.QI_PLSG.Value in pLSG:
                sellPrice += round(item.ExtendedAmount,2)
    return wtcCost, sellPrice

def standardCostCurveCalculation(Quote, honeywellLaborCostCurve, projectDurationMonths, WTWCost, costCategory='Honeywell Labor'):
	#qtTotalCost = 0
	cf_creditTerms = 0
	if Quote.GetCustomField('EGAP_Credit_Terms_Months').Content.strip() != '':
		cf_creditTerms = int(Quote.GetCustomField('EGAP_Credit_Terms_Months').Content)
	'''qtResult = SqlHelper.GetFirst("Select SUM(Cost_Curve) as total from QT__EGAP_Honeywell_Labor_Cost_Curve where ownerid={} and cartid={}".format(Quote.UserId,Quote.QuoteId))
	if qtResult is not None:
		if qtResult.total != DBNull.Value:
			qtTotalCost = qtResult.total'''
	Trace.Write("WTWCost:{}".format(WTWCost))
	if WTWCost >=0:
		honeywellLaborCostCurve.Rows.Clear()
		SqlQuery = "SELECT Standard_Timeline,Revised_Cost_Pct FROM EGAP_StndardTimeline_Cost_Curve_Calc_Constants"
		SqlResult = SqlHelper.GetList(SqlQuery)
		rows = []
		if SqlResult is not None and len(SqlResult) > 0:
			for row in SqlResult:
				monthARO = math.ceil(row.Standard_Timeline * projectDurationMonths)
				costCurve = row.Revised_Cost_Pct * WTWCost
				rowDict = {}
				#qtRow = honeywellLaborCostCurve.AddNewRow()
				rowDict['Month_ARO'] = monthARO
				rowDict['Cost_Curve'] = costCurve
				rowDict['Adj_Month_Price'] = monthARO + cf_creditTerms + 1
				rowDict['Price_Receipt'] = getPriceReceipt(Quote, costCurve, costCategory)
				rows.append(rowDict)
			if honeywellLaborCostCurve.Rows.Count == len(rows):
				i = 0
				for qtRow in honeywellLaborCostCurve.Rows:
					#Trace.Write(i)
					newData = rows[i]
					for col in newData.keys():
						qtRow[col] = newData[col]
					i += 1
					#Trace.Write(i)
			else:
				honeywellLaborCostCurve.Rows.Clear()
				for newData in rows:
					qtRow = honeywellLaborCostCurve.AddNewRow()
					for col in newData.keys():
						qtRow[col] = newData[col]
			honeywellLaborCostCurve.Save()

def removeCostCategory(cashOutflow, costCategory):
	toBeDeletedIDs = []
	for row in cashOutflow.Rows:
		if row['Row_type'] == 'Header':
			currentMaterialType = row['Cost_Category_Type']
		if currentMaterialType == costCategory:
			toBeDeletedIDs.append(row.Id)
		elif len(toBeDeletedIDs):
			break
	if len(toBeDeletedIDs):
		for Id in toBeDeletedIDs:
			cashOutflow.DeleteRow(Id)

def getSumOfProjectMilestone(Quote, monthARC = -1):
	sumOfProjectMilestone = 0
	query = "Select SUM(EGAP_Amount) as total from QT__EGAP_Project_Milestone where ownerid={} and cartid={} ".format(Quote.UserId,Quote.QuoteId)
	if monthARC >= 0:
		query = "Select SUM(EGAP_Amount) as total from QT__EGAP_Project_Milestone where ownerid={} and cartid={} and EGAP_Month_ARC={} ".format(Quote.UserId,Quote.QuoteId,monthARC)
	qtResult = SqlHelper.GetFirst(query)
	if qtResult is not None:
		if qtResult.total != DBNull.Value:
			sumOfProjectMilestone = qtResult.total
	return sumOfProjectMilestone

def getContractDateFormat(Quote, TagParserQuote, day, format):
	result = 0
	cf_contractStartDate = Quote.GetCustomField('EGAP_Contract_Start_Date')
	if cf_contractStartDate.Content.strip() != '':
		result = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Contract_Start_Date).AddMonths({}).Format({}) )*>".format(day, format))
	return result

def getNPV(rate, cashflows):
	npv = 0
	for t,cashflow in enumerate(cashflows):
		npv+=cashflow/(1+rate)**(t+1)
	return round(npv, 2)

def getCategoriesRows(cashOutflow, hcicostcategorylist):
	row_dict = {}
	for i in cashOutflow.Rows:
		costtype = i['Cost_Category_Type']
		if costtype in hcicostcategorylist:
			if i['Row_Type'] not in ['Header', 'Total'] and str(i['Month_ARO'])!='0':
				row_dict[costtype] = {i['Shipment_Description']:i['Month_ARO']}
	return row_dict