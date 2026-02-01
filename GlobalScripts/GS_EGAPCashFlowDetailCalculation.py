import GS_EGAPCashFlowDetail as CFD
import GS_PopulateNonMilestoneQuoteTable as PNM
cashOutflow =  CFD.GetQuoteTable(Quote, "Cash_Outflow")
cashInflowCalculations = CFD.GetQuoteTable(Quote, 'EGAP_Cash_Inflow_Calculations')
quoteType = Quote.GetCustomField('Quote Type').Content
hiddenColumns = ['HW_SW_Labor_Type', 'Adj_Month_ARO', 'Labor_Cost', 'ARO_Labor', 'Burden_Cost', 'ARO_Burden', 'Material_Cost', 'ARO_Material', 'Purchasing_Cost', 'ARO_Purchasing', 'Freight_Cost', 'ARO_Freight', 'Row_Type','Adj_Month_Price','Price_Receipt']
if quoteType not in ('Contract New','Contract Renewal'):
	hiddenColumns.append('Adj_Month_ARO')

'''if not User.BelongsToPermissionGroup('EGAP_Admin_Add_Visibility'):
	for col in hiddenColumns:
		CFD.hideQuoteTableColumn(cashOutflow, col)'''

'''This custom field is used for updating the market type dropdown value '''
cf_CostCategoryType = Quote.GetCustomField('EGAP_Cost_Category_Type')
cf_CostCategoryType.Content = "''"
'''Milestone Billing Questions'''
cf_subSwBillingQuestion = Quote.GetCustomField('EGAP_Subscription_SW_Milestone_Billing_Ques')
cf_laborBillingQuestion = Quote.GetCustomField('EGAP_Project_Labor_Milestone_Billing_Ques')
cf_HWSWBillingQuestion = Quote.GetCustomField('EGAP_Honeywell_Software_Milestone_Billing_Ques')
cf_thirdPartyGoodsBillingQuestion = Quote.GetCustomField('EGAP_Third_Party_Goods_Milestone_Billing_Ques')
cf_otherGoodsBillingQuestion = Quote.GetCustomField('EGAP_Other_Goods_Milestone_Billing_Ques')
cf_HCILaborBillingQuestion = Quote.GetCustomField('EGAP_HCI_Labor_Milestone_Billing_Ques')
cf_HCISwBillingQuestion = Quote.GetCustomField('EGAP_HCI_SW_Milestone_Billing_Ques')
'''Milestone Billing - Custom fields for Sell Price'''
cf_totalLaborSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_Project_Labor')
cf_totalHSSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_Honeywell_Software')
cf_totalThirdPartyGoodsSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_Third_Party_Goods')
cf_totalOtherGoodsSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_Other_Goods')
cf_totalSubSWSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_Subscription_SW')
cf_totalHCILaborSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_HCI_Labor')
cf_totalHCISWSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_HCI_SW')
cf_nonMilestoneBillingTotal = Quote.GetCustomField('EGAP_Non_Milestone_Billing_Total_Sell_Price')
cf_milestonePrice = Quote.GetCustomField('EGAP_Milestone_Price')
'''Set Default Milestone Billing Total Sell price as zero'''
cf_totalSubSWSellPrice.Content = '0'
cf_totalHSSellPrice.Content = '0'
cf_totalLaborSellPrice.Content = '0'
cf_totalThirdPartyGoodsSellPrice.Content = '0'
cf_totalOtherGoodsSellPrice.Content = '0'
cf_totalHCILaborSellPrice.Content = '0'
cf_totalHCISWSellPrice.Content  = '0'
cf_isHLManualEntry = Quote.GetCustomField('EGAP_Ques_Manul_Cost_Entry')
cf_isHCISWManualEntry = Quote.GetCustomField('EGAP_Ques_Manul_Cost_Entry1')
cf_isHCILBManualEntry = Quote.GetCustomField('EGAP_Ques_Manul_Cost_Entry2')
costCategoryType = []
totalSellPriceDict  = dict()
'''Honeywell Labor material flag'''
isHLAvailable = False
isHCILBvailable=False
isHCISWvailable=False
'''Variable to handle Default Answer'''
costCategoryQuesDefaultAns = []
milestoneQuesDefaultAnsDict = dict()

if Quote.Items.Count > 0:
	'''Set Default value for Honeywell Labor Manual Cost Entry Custom Field'''
	if cf_isHLManualEntry.Content.strip() == '':
		cf_isHLManualEntry.Content = cf_isHLManualEntry.CalculationFormula
	if cf_isHCILBManualEntry.Content.strip() == '':
		cf_isHCILBManualEntry.Content = cf_isHCILBManualEntry.CalculationFormula
	if cf_isHCISWManualEntry.Content.strip() == '':
		cf_isHCISWManualEntry.Content = cf_isHCISWManualEntry.CalculationFormula
	'''Readonly Header columns'''
	readOnlyColumns = ['Shipment_Number', 'Shipment_Description', 'Cost', 'Month_ARO', 'Vendor_Payment_Term','P3_Product_Type']
	wtcCostDict    = dict()
	sellPriceDict = dict()
	costCategory = []
	costCategoryDict =  []

	'''Collect WTC Cost and Sell Price of each item'''
	# moduleCondition = " and SC_Module = 'NULL'"
	sqlResult = None
	if quoteType in ('Contract New','Contract Renewal'):
		sqlQuery = "Select SC_Module as Module, SAP_PL_PLSG, Cost_Category, LOB, Sub_LOB from  SAP_PLSG_LOB_MAPPING where SC_Module != 'NULL'"
		# moduleCondition = " and SC_Module != 'NULL'"
		sqlResult = SqlHelper.GetList(sqlQuery)
		if sqlResult is not None and len(sqlResult) > 0:
			for row in sqlResult:
				costCategoryDict.extend(row.Module.split('|'))
		for item in Quote.Items:
			if item.AsMainItem and len(list(item.AsMainItem.Children)):
				if item.PartNumber in costCategoryDict:
					if float(item.QI_ExtendedWTWCost.Value) >= 0 and item.QI_PLSG.Value != '':
						CFD.addToTotal(wtcCostDict, item.QI_PLSG.Value,  round(item.QI_ExtendedWTWCost.Value,2))
						if not item.QI_PLSG.Value in  costCategory:
							costCategory.append(item.QI_PLSG.Value)
					if float(item.ExtendedAmount) >= 0:
						CFD.addToTotal(sellPriceDict, item.QI_PLSG.Value,  round(item.ExtendedAmount,2))
			#changing the label for the cost and project duration custom fields
			cashOutflow =  CFD.GetQuoteTable(Quote, "Cash_Outflow")
			cashOutflow.GetColumnByName('Cost').Label = 'Cost Price'
			#changing the label for Cash_Inflow_Month column
			cashInflowCalculations.GetColumnByName('Cash_Inflow_Month').Label = 'Adj Month ARO'

			hideColumns = ['Honeywell_Labor_not_in_milestone', 'Subscription_Software_not_in_milestone', 'Third_Party_not_in_milestone', 'Other_not_in_milestone', 'AS_Labor', 'AS_SW']
			for col in hideColumns:
				CFD.hideQuoteTableColumn(cashInflowCalculations, col)

			Quote.GetCustomField("EGAP_Milestone_Project_Duration_Months").Label = "Contract Duration(Months)"

			'''Hide columns which is not related to Service contract from the cash outflow table'''
			CFD.hideQuoteTableColumn(cashOutflow, 'P3_Product_Type')

			'''Hide columns which are not related to Service contract from the cash outflow calculation table'''
			cashOutflowCalc =  CFD.GetQuoteTable(Quote, "EGAP_Cash_Outflow_Calculations")
			cashOutflowCalc.GetColumnByName('Cash_Outflow_Month').Label = 'Adj Month ARO'
			#hiddenOutflowColumns = ['Honeywell_Material', 'Honeywell_PMC_Material', 'Honeywell_Subscription_Software', 'Third_Party_Goods_Services', 'Other_Goods_Services', 'Honeywell_P3_Material', 'Honeywell_AS_Software', 'Honeywell_AS_Labor']
			hiddenOutflowColumns = ['Honeywell_Material', 'Honeywell_PMC_Material', 'Honeywell_Subscription_Software', 'Other_Goods_Services', 'Honeywell_P3_Material', 'Honeywell_AS_Software', 'Honeywell_AS_Labor', 'Third_Party_Buyout']
			for col in hiddenOutflowColumns:
				CFD.hideQuoteTableColumn(cashOutflowCalc, col)

			'''Hide columns which are not related to Service contract from the project milestone table'''
			projectMilestone = Quote.QuoteTables["EGAP_Project_Milestone"]
			hiddenPMColumns = ['EGAP_Weeks_ARO', 'EGAP_Month_ARC']
			for col in hiddenPMColumns:
				CFD.hideQuoteTableColumn(projectMilestone, col)
			'''Change Month ARO column as editable'''
			projectMilestone.GetColumnByName('EGAP_Month_ARO').AccessLevel = projectMilestone.AccessLevel.Editable
	else:
		for item in Quote.Items:
			if item.AsMainItem and len(list(item.AsMainItem.Children)):
				continue
			if float(item.QI_ExtendedWTWCost.Value) >= 0:
				# CFD.addToTotal(wtcCostDict, item.QI_PLSG.Value,  round(item.QI_ExtendedWTWCost.Value,2))
				CFD.addToTotal(wtcCostDict, item.QI_PLSG.Value,  item.QI_ExtendedWTWCost.Value)
				if not item.QI_PLSG.Value in  costCategory:
					costCategory.append(item.QI_PLSG.Value)
			if float(item.ExtendedAmount) >= 0:
				CFD.addToTotal(sellPriceDict, item.QI_PLSG.Value,  round(item.ExtendedAmount,2))
	'''Group WTC Cost and Sell Price based on the Cash Category Type'''
	totalWtcCostDict    = dict()
	if len(costCategory):
		costCategoryList = ', '.join("'{}'".format(category) for category in costCategory)
		bookingTabLOB = Quote.GetCustomField('Booking LOB').Content
		#if not sqlResult or quoteType not in ('Contract New','Contract Renewal'):
		SqlQuery = "SELECT SAP_PL_PLSG, Cost_Category, LOB, Sub_LOB FROM SAP_PLSG_LOB_Mapping WHERE SAP_PL_PLSG in ({}) {}"
		sqlResult = SqlHelper.GetList(SqlQuery.format(costCategoryList, ''))
		if sqlResult is not None and len(sqlResult) > 0:
			for row in sqlResult:
				sapPLSG = row.SAP_PL_PLSG
				costCategory = row.Cost_Category
				lob    = row.LOB
				subLOB    = row.Sub_LOB
				#wtcCost = wtcCostDict[sapPLSG]
				wtcCost = wtcCostDict.get(sapPLSG,0)
				#sellPrice = sellPriceDict[sapPLSG]
				sellPrice = sellPriceDict.get(sapPLSG,0)
				if quoteType in ('Contract New','Contract Renewal'):
					#category = costCategory
					category = 'Third Party Goods & Services' if costCategory in ['Third-Party Material', 'Third-Party Labor'] else costCategory
					cf_isHLManualEntry.Content = 'Yes'
				else:
					category = CFD.getCostCategoryType(costCategory, lob, bookingTabLOB, subLOB)
				if category != '':
					if category == 'Honeywell Labor':
						isHLAvailable = True
					if category == 'Honeywell HCI Labor & BGP':
						isHCILBvailable=True
					if category == 'Honeywell HCI software':
						isHCISWvailable=True
					'''if Manual Entry is No then ignore the Honeywell Labor wtc cost'''
					if (cf_isHLManualEntry.Content == 'Yes' and category == 'Honeywell Labor') or category not in ['Honeywell Labor', 'Honeywell HCI Labor & BGP', 'Honeywell HCI software'] :
						CFD.addToTotal(totalWtcCostDict, category,  wtcCost)
					if (cf_isHCISWManualEntry.Content == 'Yes' and category == 'Honeywell HCI software') :
						CFD.addToTotal(totalWtcCostDict, category,  wtcCost)
					if (cf_isHCILBManualEntry.Content == 'Yes' and category == 'Honeywell HCI Labor & BGP'):
						CFD.addToTotal(totalWtcCostDict, category,  wtcCost)
						PLSGUserInputDescTable = CFD.GetQuoteTable(Quote, "Honeywell_HCI_Labor_BGP_PLSG")
						PLSGUserInputDescTable.Rows.Clear()
						Quote.QuoteTables['Honeywell_HCI_Labor_BGP_Cost_Curve'].Rows.Clear()
					CFD.addToTotal(totalSellPriceDict, category,  sellPrice)
	'''Insert/update Cost category type into Cash Outflow Quote table'''
	if len(totalWtcCostDict):
		costCategoryTypeDict = dict()
		for key,value in totalWtcCostDict.items():
			costCategoryTypeDict[key] = value
		'''Compare the Quote table data with Cart Item data'''
		toBeDeleted, toBeSkipped, row_dict = CFD.getDifference(Quote, cashOutflow, costCategoryTypeDict, readOnlyColumns)
		'''Delete Obsolete items'''
		if len(toBeDeleted):
			CFD.deleteRows(cashOutflow, toBeDeleted)
		'''Making Vendor Payment Term column as readonly for other than Third Party Goods & Services and Other Goods & Services'''
		if  len(toBeSkipped):
			CFD.makeColumnReadonly(cashOutflow, 'Vendor_Payment_Term', ['Third Party Goods & Services','Other Goods & Services'])
			CFD.makeColumnReadonly(cashOutflow, 'P3_Product_Type', ['Honeywell P3 Material'])#added by Abhijeet
		for key,value in totalWtcCostDict.items():
			if key not in toBeSkipped and key not in costCategoryType:
				row = cashOutflow.AddNewRow()
				row['Cost_Category_Type']     = key
				row['Shipment_Description'] = ''
				#row['Cost'] = value
				row['Cost'] = round(value,2)
				row['Row_Type'] = 'Header'
				for col in readOnlyColumns:
					row.Cells.Item[col].AccessLevel = cashOutflow.AccessLevel.ReadOnly
				defaultRows = [{'Shipment_Number':'Shipment 1','Row_Type':'Item'}, {'Shipment_Number':'Total of Entered Shipment','Row_Type':'Total'}]
				CFD.addDefaultRows(Quote, cashOutflow, defaultRows, key, readOnlyColumns,row_dict)
			costCategoryType.append(key)
		if ( len(costCategoryType) ):
			'''Hide Cost category questions and Milestone billing questions based on cost category type'''
			if 'Honeywell Subscription Software' not in costCategoryType:
				Quote.CustomFields.Disallow('EGAP_Subscription_SW_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Subscription_SW')
			else:
				Quote.CustomFields.Allow('EGAP_Subscription_SW_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Subscription_SW')
				milestoneQuesDefaultAnsDict['EGAP_Subscription_SW_Milestone_Billing_Ques'] = 'Yes'
			if 'Honeywell HCI software' not in costCategoryType:
				Quote.CustomFields.Disallow('EGAP_Honeywell_Software_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Honeywell_Software')
			else:
				Quote.CustomFields.Allow('EGAP_Honeywell_Software_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Honeywell_Software')
				milestoneQuesDefaultAnsDict['EGAP_Honeywell_Software_Milestone_Billing_Ques'] = 'Yes'
			if 'Third Party Goods & Services' not in costCategoryType:
				Quote.CustomFields.Disallow('EGAP_Ques_MQ4','EGAP_Ques_CBTPQ1','EGAP_Third_Party_Goods_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Third_Party_Goods')
			else:
				Quote.CustomFields.Allow('EGAP_Ques_CBTPQ1','EGAP_Third_Party_Goods_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Third_Party_Goods')
				costCategoryQuesDefaultAns.append('EGAP_Ques_CBTPQ1')
				milestoneQuesDefaultAnsDict['EGAP_Third_Party_Goods_Milestone_Billing_Ques'] = 'Yes'
			if 'Other Goods & Services' not in costCategoryType:
				Quote.CustomFields.Disallow('EGAP_Ques_MQ8','EGAP_Ques_CBTPQ2','EGAP_Other_Goods_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Other_Goods')
			else:
				Quote.CustomFields.Allow('EGAP_Ques_CBTPQ2','EGAP_Other_Goods_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Other_Goods')
				costCategoryQuesDefaultAns.append('EGAP_Ques_CBTPQ2')
				milestoneQuesDefaultAnsDict['EGAP_Other_Goods_Milestone_Billing_Ques'] = 'Yes'
			cf_CostCategoryType.Content = ', '.join("'{}'".format(category) for category in costCategoryType)
	else:
		'''Hide all Cost category questions and Milestone billing questions'''
		if Quote.GetCustomField('Booking LOB').Content == 'HCP':
			cashOutflow.Rows.Clear()
		Quote.CustomFields.Disallow('EGAP_Subscription_SW_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Subscription_SW','EGAP_Honeywell_Software_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Honeywell_Software','EGAP_Ques_MQ4','EGAP_Ques_CBTPQ1','EGAP_Third_Party_Goods_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Third_Party_Goods','EGAP_Ques_MQ8','EGAP_Ques_CBTPQ2','EGAP_Other_Goods_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Other_Goods')
	'''Hiding HCI billing question and total sell prcie since it is not part of this release'''
	Quote.CustomFields.Disallow('EGAP_HCI_Labor_Milestone_Billing_Ques','EGAP_HCI_SW_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_HCI_Labor','EGAP_Total_Sell_Price_of_HCI_SW')
else:
	cashOutflow.Rows.Clear()
	Quote.CustomFields.Disallow('EGAP_Ques_Manul_Cost_Entry', 'EGAP_Ques_MQ4', 'EGAP_Ques_CBTPQ1', 'EGAP_Ques_MQ8', 'EGAP_Ques_CBTPQ2', 'EGAP_Cost_Category_Type', 'EGAP_Material_Type', 'EGAP_No_of_Shipment', 'EGAP_Subscription_SW_Milestone_Billing_Ques', 'EGAP_Project_Labor_Milestone_Billing_Ques','EGAP_Honeywell_Software_Milestone_Billing_Ques','EGAP_Third_Party_Goods_Milestone_Billing_Ques', 'EGAP_Other_Goods_Milestone_Billing_Ques', 'EGAP_HCI_Labor_Milestone_Billing_Ques', 'EGAP_HCI_SW_Milestone_Billing_Ques', 'EGAP_Total_Sell_Price_of_Subscription_SW', 'EGAP_Total_Sell_Price_of_Project_Labor', 'EGAP_Total_Sell_Price_of_Third_Party_Goods', 'EGAP_Total_Sell_Price_of_Other_Goods', 'EGAP_Total_Sell_Price_of_HCI_Labor', 'EGAP_Total_Sell_Price_of_HCI_SW', 'EGAP_Non_Milestone_Billing_Total_Sell_Price','EGAP_Ques_Manul_Cost_Entry1','EGAP_Ques_Manul_Cost_Entry2')

projectMilestone = Quote.QuoteTables["EGAP_Project_Milestone"]
nonMilestoneBillingTotal = 0
if Quote.Items.Count > 0:
	'''Honewell labor questions'''
	if not isHLAvailable:
		Quote.CustomFields.Disallow('EGAP_Ques_Manul_Cost_Entry','EGAP_Project_Labor_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Project_Labor')
	else:
		Quote.CustomFields.Allow('EGAP_Ques_Manul_Cost_Entry','EGAP_Project_Labor_Milestone_Billing_Ques','EGAP_Total_Sell_Price_of_Project_Labor')
		milestoneQuesDefaultAnsDict['EGAP_Project_Labor_Milestone_Billing_Ques'] = 'Yes'
		'''Standard timleine for the Cost curve calculcation'''
		if cf_isHLManualEntry.Content == 'No':
			projectDurationMonths = 0
			if Quote.GetCustomField('EGAP_Milestone_Project_Duration_Months').Content:
				projectDurationMonths = int(Quote.GetCustomField('EGAP_Milestone_Project_Duration_Months').Content)
			HLWTWCost, sellPrice_p = CFD.getWTWCost_sellprice(Quote, 'Honeywell Labor')
			honeywellLaborCostCurve =  CFD.GetQuoteTable(Quote, "EGAP_Honeywell_Labor_Cost_Curve")
			Trace.Write("projectduration in labor:{}--{}".format(projectDurationMonths,HLWTWCost))
			honeywellLaborCostCurve.Rows.Clear()
			CFD.standardCostCurveCalculation(Quote, honeywellLaborCostCurve, projectDurationMonths, HLWTWCost, 'Honeywell Labor')
	if not isHCILBvailable:
		PLSGUserInputDescTable = CFD.GetQuoteTable(Quote, "Honeywell_HCI_Labor_BGP_PLSG")
		PLSGUserInputDescTable.Rows.Clear()
		Quote.QuoteTables['Honeywell_HCI_Labor_BGP_Cost_Curve'].Rows.Clear()
		Quote.CustomFields.Disallow('EGAP_Ques_Manul_Cost_Entry2')
	else:
		Quote.CustomFields.Allow('EGAP_Ques_Manul_Cost_Entry2')
		'''Standard timleine for the Cost curve calculcation'''
		if cf_isHCILBManualEntry.Content == 'No':
			projectDurationMonths = 0
			if Quote.GetCustomField('EGAP_Milestone_Project_Duration_Months').Content:
				projectDurationMonths = int(Quote.GetCustomField('EGAP_Milestone_Project_Duration_Months').Content)
			HLWTWCost, sellPrice_p = CFD.getWTWCost_sellprice(Quote, 'Honeywell HCI Labor & BGP')
			honeywellLaborCostCurve =  CFD.GetQuoteTable(Quote, "EGAP_Honeywell_Labor_Cost_Curve")
			Trace.Write("projectduration:{}".format(projectDurationMonths))
			#CFD.standardCostCurveCalculation(Quote, honeywellLaborCostCurve, projectDurationMonths, HLWTWCost,'Honeywell HCI Labor & BGP')
			CFD.manualBGPLaborCost(Quote)
	if not isHCISWvailable:
		Quote.CustomFields.Disallow('EGAP_Ques_Manul_Cost_Entry1')
	else:
		Quote.CustomFields.Allow('EGAP_Ques_Manul_Cost_Entry1')
		'''Standard timleine for the Cost curve calculcation'''
		if cf_isHCISWManualEntry.Content == 'No':
			projectDurationMonths = 0
			if Quote.GetCustomField('EGAP_Milestone_Project_Duration_Months').Content:
				projectDurationMonths = int(Quote.GetCustomField('EGAP_Milestone_Project_Duration_Months').Content)
			HLWTWCost, sellPrice_p = CFD.getWTWCost_sellprice(Quote, 'Honeywell HCI software')
			honeywellLaborCostCurve =  CFD.GetQuoteTable(Quote, "EGAP_Honeywell_Labor_Cost_Curve")
			#Trace.Write("projectduration:{}".format(projectDurationMonths))
			CFD.standardCostCurveCalculation(Quote, honeywellLaborCostCurve, projectDurationMonths, HLWTWCost, 'Honeywell HCI software')
	'''Set Default Answer for Cost Category Type Questions'''
	if len(costCategoryQuesDefaultAns):
		for field in costCategoryQuesDefaultAns:
			costCategoryCustomField = Quote.GetCustomField(field)
			if costCategoryCustomField.Content.strip() == '':
				Quote.GetCustomField(field).Content = costCategoryCustomField.CalculationFormula
	'''Set Default Answer for Milestone Billing Questions'''
	if len(milestoneQuesDefaultAnsDict):
		for field in milestoneQuesDefaultAnsDict.keys():
			if Quote.GetCustomField(field).Content.strip() == '':
				Quote.GetCustomField(field).Content = milestoneQuesDefaultAnsDict[field]
	'''Non Milestone Billing Total Calculation'''
	if cf_laborBillingQuestion.Content.strip() == 'No' and isHLAvailable:
		nonMilestoneBillingTotal += totalSellPriceDict.get('Honeywell Labor',0)
		cf_totalLaborSellPrice.Content = str(totalSellPriceDict.get('Honeywell Labor',0))
	if (len(costCategoryType)):
		if cf_subSwBillingQuestion.Content.strip() == 'No' and 'Honeywell Subscription Software' in costCategoryType:
			nonMilestoneBillingTotal += totalSellPriceDict.get('Honeywell Subscription Software',0)
			cf_totalSubSWSellPrice.Content = str(totalSellPriceDict.get('Honeywell Subscription Software',0))
		if cf_thirdPartyGoodsBillingQuestion.Content.strip() == 'No' and 'Third Party Goods & Services' in costCategoryType:
			nonMilestoneBillingTotal += totalSellPriceDict.get('Third Party Goods & Services',0)
			cf_totalThirdPartyGoodsSellPrice.Content = str(totalSellPriceDict.get('Third Party Goods & Services',0))
		if cf_otherGoodsBillingQuestion.Content.strip() == 'No' and 'Other Goods & Services' in costCategoryType:
			nonMilestoneBillingTotal += totalSellPriceDict.get('Other Goods & Services',0)
			cf_totalOtherGoodsSellPrice.Content = str(totalSellPriceDict.get('Other Goods & Services',0))
		if cf_HCILaborBillingQuestion.Content.strip() == 'No' and  'HCI Labor' in costCategoryType:
			nonMilestoneBillingTotal += totalSellPriceDict.get('HCI Labor',0)
			cf_totalHCILaborSellPrice.Content = str(totalSellPriceDict.get('HCI Labor',0))
		if cf_HCISwBillingQuestion.Content.strip() == 'No' and  'HCI Software' in costCategoryType:
			nonMilestoneBillingTotal += totalSellPriceDict.get('HCI Software',0)
			cf_totalHCISWSellPrice.Content = str(totalSellPriceDict.get('HCI Software',0))
		if cf_HWSWBillingQuestion.Content.strip() == 'No' and 'Honeywell HCI software' in costCategoryType:
			nonMilestoneBillingTotal += totalSellPriceDict.get('Honeywell HCI software',0)
			cf_totalHSSellPrice.Content = str(totalSellPriceDict.get('Honeywell HCI software',0))
	'''Milestone Price'''
	walkAwayPrice = TagParserQuote.ParseString('<*CTX( Number(<*Round (<* GetFirstFromQuoteTable(Quote_Details,Walk_away_Sales_Price) *>,0)*>).Format )*>')
	walkAwayPrice = float(walkAwayPrice.replace(',',''))
	cf_milestonePrice.Content = str(round(walkAwayPrice - nonMilestoneBillingTotal))

	'''Refresh Project Milestones Quote table'''
	milestonePrice = float(cf_milestonePrice.Content)
	cf_creditTerms = CFD.getCreditTermsMonths(Quote)
	CFD.updateProjectMilestone(Quote, projectMilestone, cf_creditTerms, milestonePrice, TagParserQuote)
	projectMilestone.Save()

	'''Cash outflow Calculation'''
	#CFD.updateCashOutflowCalculation(Quote, cashOutflow, TagParserQuote, True)
	#cashOutflow.Save()
	'''Cash inflow Calculation'''
	#CFD.populateCashInflowCalculation(Quote, TagParserQuote)
	#cashInflowCalculations.Save()
	'''Update Total of shipment cost and cash outflow Warning message'''
	cashOutflowWarning=''
	cashOutflowWarning = CFD.updateTotalCost(Quote, cashOutflow) if Quote.GetCustomField('EGAP_CFD_Cashflow_Health').Content != 'In Balance' else ''
	#Log.Info("Cflow2=>"+str(Quote.GetCustomField('EGAP_QT_CashOutflow_Warning').Content))
	'''Validating Project Milestone Data'''
	maxMonthARO = CFD.getMaxMonthARO(Quote) 
	'''Update Project Milestone Warning message'''
	Quote.GetCustomField('EGAP_QT_ProjectMilestone_Warning').Content = ''
	if quoteType not in ('Contract New','Contract Renewal'):
		Quote.GetCustomField('EGAP_QT_ProjectMilestone_Warning').Content = CFD.validateProjectMilestoneData(projectMilestone, maxMonthARO)
	else:
		if cashOutflowWarning:
			cashOutflowWarning = cashOutflowWarning.replace("WTW cost", "Cost Price")
	Quote.GetCustomField('EGAP_QT_CashOutflow_Warning').Content = cashOutflowWarning

else:
	cf_milestonePrice.Content = '0'
	projectMilestone.Rows.Clear()
	cashInflowCalculations = CFD.GetQuoteTable(Quote, 'EGAP_Cash_Inflow_Calculations')
	cashInflowCalculations.Rows.Clear()

'''Update Non-Milestone Billing Total'''
cf_nonMilestoneBillingTotal.Content = str(nonMilestoneBillingTotal)
#Added this Code to be editable only for P3 HoneywellMaterial 
columns = ['Shipment_Number', 'Shipment_Description', 'Cost', 'Month_ARO','Vendor_Payment_Term','P3_Product_Type']
columnTobeReadonly = 'Vendor_Payment_Term'
columnTobeReadonlyP3 = 'P3_Product_Type'
categoryTypes = ['Third Party Goods & Services','Other Goods & Services', 'Third Party Buyout']
categoryTypesP3 = ['Honeywell P3 Material']

CFD.makeQuoteTableColumnsReadonly(cashOutflow, columns, columnTobeReadonly, categoryTypes)
CFD.makeQuoteTableColumnsReadonly(cashOutflow, columns, columnTobeReadonlyP3, categoryTypesP3)
PNM.PopulateNonMilestone(Quote)