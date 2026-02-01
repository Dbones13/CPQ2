import math
import System
from GS_CashFlowModule import *

def updateCashOutflowCalculation(Quote, cashOutflow, TagParserQuote, saveTrigger = False):
	if cashOutflow.Rows.Count:
		previousMaterialType = currentMaterialType = ''
		cf_creditTerms = 0
		qttype = 'Not SC'
		if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
			qttype = 'SC'
		if Quote.GetCustomField('EGAP_Credit_Terms_Months').Content.strip() != '':
			cf_creditTerms = int(Quote.GetCustomField('EGAP_Credit_Terms_Months').Content)
		for row in cashOutflow.Rows:
			if row['Row_Type'] == 'Header':
				currentMaterialType = row['Cost_Category_Type']
			elif currentMaterialType == 'Honeywell Material' and row['Row_Type'] == 'Item':
				monthARO = row['Month_ARO']
				cost = row['Cost']
				'''Labor Cost'''
				directLaborPct = cashOutflowCostConstants('Cost_PCT', 'direct labor')
				laborCost = cost * directLaborPct
				row['Labor_Cost'] = -laborCost if laborCost > 0 else 0
				'''ARO Labor'''
				lagDays = cashOutflowCostConstants('DAYS', 'lag')
				mfgCycleDays = cashOutflowCostConstants('DAYS', 'mfg cycle')
				aROLabor = round(lagDays/30.0 - mfgCycleDays/30.0 + monthARO)
				row['ARO_Labor'] = aROLabor if aROLabor > 0 else 0
				'''Burden Cost'''
				burdenPCt = cashOutflowCostConstants('Cost_PCT', 'burden')
				burdenCost = cost * burdenPCt
				row['Burden_Cost'] = -burdenCost if burdenCost > 0 else 0
				'''ARO Burden'''
				aROBurden = round(lagDays/30.0 - mfgCycleDays/30.0 + monthARO)
				row['ARO_Burden'] = aROBurden if aROBurden > 0 else 0
				'''Material Cost'''
				materialPct = cashOutflowCostConstants('Cost_PCT', 'material')
				materialCost = cost * materialPct
				row['Material_Cost'] = -materialCost if materialCost > 0 else 0
				'''ARO Material'''
				daysAP = cashOutflowCostConstants('DAYS', 'days AP')
				aROMaterial = round(daysAP/30.0 - mfgCycleDays/30.0 + monthARO)
				row['ARO_Material'] = aROMaterial if aROMaterial > 0 else 0
				'''Purchasing Cost'''
				buyingPct = cashOutflowCostConstants('Cost_PCT', 'buying')
				purchasingCost = cost * buyingPct
				row['Purchasing_Cost'] = -purchasingCost if purchasingCost > 0 else 0
				'''ARO Purchasing'''
				leadTime = cashOutflowCostConstants('DAYS', 'lead time')
				aROPurchasing = round(-leadTime/30.0 - mfgCycleDays/30.0 + lagDays/30.0 + monthARO)
				row['ARO_Purchasing'] = aROPurchasing if aROPurchasing > 0 else 0
				'''Freight Cost'''
				freightPct = cashOutflowCostConstants('Cost_PCT', 'freight')
				freightCost = cost * freightPct
				row['Freight_Cost'] = -freightCost if freightCost > 0 else 0
				'''ARO-Freight'''
				aROFreight = round(daysAP/30.0 - mfgCycleDays/30.0 + monthARO)
				row['ARO_Freight'] = aROFreight if aROFreight > 0 else 0
			elif currentMaterialType == 'Honeywell Software' and row['Row_Type'] == 'Item':
				ptmMonthAdj = cf_creditTerms if qttype != 'SC' else 0
				row['Adj_Month_ARO'] = row['Month_ARO'] + ptmMonthAdj
			elif currentMaterialType in ['Third Party Goods & Services', 'Third Party Buyout']	and row['Row_Type'] == 'Item':
				cBTPQ1 = Quote.GetCustomField('EGAP_Ques_CBTPQ1').Content
				mQ4	   = Quote.GetCustomField('EGAP_Third_Party_Goods_Milestone_Billing_Ques').Content
				vendorPaymentTerm = float(row['Vendor_Payment_Term']) if row['Vendor_Payment_Term'] else 0
				adjMonthARO = row['Month_ARO']
				if cBTPQ1 == 'No':
					adjMonthARO += math.ceil(float(vendorPaymentTerm/30.0))
				elif mQ4 == 'No':
					adjMonthARO += math.ceil(float((vendorPaymentTerm/30.0)+cf_creditTerms))
				else:
					adjMonthARO += math.ceil(float(vendorPaymentTerm/30.0))
				row['Adj_Month_ARO'] = adjMonthARO
				row['Adj_Month_Price'] = row['Month_ARO'] + cf_creditTerms
				row['Price_Receipt'] = getPriceReceipt(Quote, row['Cost'], currentMaterialType)
			elif currentMaterialType == 'Other Goods & Services' and row['Row_Type'] == 'Item':
				cBTPQ2 = Quote.GetCustomField('EGAP_Ques_CBTPQ2').Content
				mQ8	   = Quote.GetCustomField('EGAP_Other_Goods_Milestone_Billing_Ques').Content
				vendorPaymentTerm = float(row['Vendor_Payment_Term']) if row['Vendor_Payment_Term'] else 0
				adjMonthARO = row['Month_ARO']
				if cBTPQ2 == 'No':
					adjMonthARO += math.ceil(float(vendorPaymentTerm/30.0))
				elif mQ8== 'No':
					adjMonthARO += math.ceil(float((vendorPaymentTerm/30.0)+cf_creditTerms))
				else:
					adjMonthARO += math.ceil(float(vendorPaymentTerm/30.0))
				row['Adj_Month_ARO'] = adjMonthARO
				row['Adj_Month_Price'] = row['Month_ARO'] + cf_creditTerms
				row['Price_Receipt'] = getPriceReceipt(Quote, row['Cost'], currentMaterialType)
			elif currentMaterialType == 'Honeywell Subscription Software' and row['Row_Type'] == 'Item':
				row['Adj_Month_Price'] = row['Month_ARO'] + cf_creditTerms
				row['Price_Receipt'] = getPriceReceipt(Quote, row['Cost'], currentMaterialType)
			elif currentMaterialType == 'Honeywell Labor' and row['Row_Type'] == 'Item':
				row['Adj_Month_Price'] = row['Month_ARO'] + cf_creditTerms + 1
				if qttype == 'SC':
					row['Adj_Month_ARO'] = row['Month_ARO']
				row['Price_Receipt'] = getPriceReceipt(Quote, row['Cost'], currentMaterialType)
			elif currentMaterialType == 'Honeywell Hardware' and row['Row_Type'] == 'Item':
				if qttype == 'SC':
					row['Adj_Month_ARO'] = row['Month_ARO']
			elif currentMaterialType in  ['Honeywell HCI Labor & BGP','Honeywell HCI software'] and row['Row_Type'] == 'Item':
				row['Adj_Month_Price'] = row['Month_ARO'] + cf_creditTerms
				if currentMaterialType!= 'Honeywell HCI Labor & BGP':
					row['Price_Receipt'] = getPriceReceipt(Quote, row['Cost'], currentMaterialType)
		'''Update Cashoutflow calculation '''
		populateCashOutflowCalculation(Quote, TagParserQuote, saveTrigger)
		'''Update CashInflow calculation '''
		populateCashInflowCalculation(Quote, TagParserQuote)

def updateProjectMilestone(Quote, projectMilestone, ptmMonthAdj, milestonePrice, TagParserQuote):
	defaultData = {'EGAP_Proposed_Milestones':'','EGAP_Milestone_Name':'', 'EGAP_Milestone_Description':'','EGAP_Pct_of_Total_Milestone_Payment':0,'EGAP_Weeks_ARO': 0,'EGAP_Customer_Signoff_Required':'','EGAP_Milestone_with_Bank_Guarantee':'','EGAP_Amount':0,'EGAP_Month_ARO':0,'EGAP_Month_ARC':0,'Row_Type':'Item'}
	if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
		paymentMilestonesSource = GetQuoteTable(Quote, "SC_Milestone_Table")
		qttype = 'SC'
		defaultData = {'EGAP_Proposed_Milestones':'','EGAP_Milestone_Name':'', 'EGAP_Milestone_Description':'','EGAP_Pct_of_Total_Milestone_Payment':0,'EGAP_Weeks_ARO': 0,'EGAP_Customer_Signoff_Required':'No','EGAP_Milestone_with_Bank_Guarantee':'No','EGAP_Amount':0,'EGAP_Month_ARO':0,'EGAP_Month_ARC':0,'Row_Type':'Item'}
	else:
		paymentMilestonesSource = GetQuoteTable(Quote, "Payment_MileStones")
		qttype = 'Not SC'
	sourceData = []
	toBeDeleted = []
	if paymentMilestonesSource.Rows.Count:
		for row in paymentMilestonesSource.Rows:
			rowDict = {}
			if qttype == 'SC':
				rowDict['EGAP_Proposed_Milestones'] = row['Milestone_Number']
				rowDict['EGAP_Milestone_Name'] = row['Milestone_Number']
				rowDict['EGAP_Milestone_Description'] = row['Milestone_Description']
				rowDict['EGAP_Pct_of_Total_Milestone_Payment'] = row['Percentage_Amount']
				rowDict['EGAP_Amount'] = row['Value']
			else:
				rowDict['EGAP_Proposed_Milestones'] = row['Milestone_Number']
				if Quote.GetCustomField('Booking LOB').Content == 'PMC':
					rowDict['EGAP_Milestone_Name'] = row['PMC_Milestone']
					rowDict['EGAP_Milestone_Description'] = row['Milestone']
				elif Quote.GetCustomField('Booking LOB').Content == 'HCP':
					rowDict['EGAP_Milestone_Name'] = row['HCP_Milestone']
					rowDict['EGAP_Milestone_Description'] = row['Milestone_Description']
				else:
					rowDict['EGAP_Milestone_Name'] = row['Billing_Milestone']
					rowDict['EGAP_Milestone_Description'] = row['Milestone_Description']
				rowDict['EGAP_Pct_of_Total_Milestone_Payment'] = row['_Amount']
				rowDict['EGAP_Amount'] = (milestonePrice * row['_Amount'])/100
			sourceData.append(rowDict)
	if projectMilestone.Rows.Count:
		i = 0
		projectMilestoneCount = 0
		for row in projectMilestone.Rows:
			if i < len(sourceData):
				sourceRow = sourceData[i]
				'''Update the existing record'''
				for col in sourceRow.keys():
					row[col] = sourceRow[col]
				row['EGAP_Month_ARC'] = row['EGAP_Month_ARO'] + ptmMonthAdj
				if qttype == 'SC':
					row['EGAP_Month_ARC'] = row['EGAP_Month_ARO']
				projectMilestoneCount +=1
			else:
				toBeDeleted.append(row.Id)
			i +=1
		'''Remove all mismatch records'''
		if len(toBeDeleted) > 0:
			for id in toBeDeleted:
				projectMilestone.DeleteRow(id)
		'''Add new delta records'''
		if paymentMilestonesSource.Rows.Count != projectMilestoneCount:
			deltaData = sourceData[projectMilestoneCount:]
			for sourceRow in deltaData:
				addNewRowProjectMilestone(projectMilestone, defaultData, sourceRow)
	else:
		'''Add new project milestones'''
		for sourceRow in sourceData:
			addNewRowProjectMilestone(projectMilestone, defaultData, sourceRow)
	if projectMilestone.Rows.Count:
		populateCashInflowCalculation(Quote, TagParserQuote)

def populateCashInflowCalculation(Quote, TagParserQuote):
	maxMonthARO = getMaxMonthARONew(Quote, 'Project_Milestone')
	maxMonthAROCashOutflow = getMaxMonthARONew(Quote, 'Cash_Outflow')
	if Quote.GetCustomField('Booking LOB').Content == 'HCP':
		maxMonthAROCostCurve = getMaxMonthARONew(Quote, 'Honeywell_HCI_Labor_BGP_Cost_Curve')
		maxMonthAROCashOutflow = maxMonthAROCostCurve if maxMonthAROCostCurve > maxMonthAROCashOutflow else maxMonthAROCashOutflow
	maxMonthARO = maxMonthAROCashOutflow if maxMonthAROCashOutflow > maxMonthARO else maxMonthARO
	if maxMonthARO > 0:
		creditTermsMonths = getCreditTermsMonths(Quote)
		#ptmMonthAdj = round(creditTermsMonths/30)
		ptmMonthAdj = creditTermsMonths
		monthARORange = range(maxMonthARO+1)
		exchangeRate = float(Quote.GetCustomField('Exchange Rate').Content)
		DCFAtGMLevel = float(Quote.GetCustomField('EGAP_DCF_At_GM_Level').Content)
		cashInflowCalculations = GetQuoteTable(Quote, 'EGAP_Cash_Inflow_Calculations')
		MQ3 = 'Yes'
		if Quote.GetCustomField('EGAP_Project_Labor_Milestone_Billing_Ques').Content != '':
			MQ3 = Quote.GetCustomField('EGAP_Project_Labor_Milestone_Billing_Ques').Content
		MQ4 = 'Yes'
		if Quote.GetCustomField('EGAP_Third_Party_Goods_Milestone_Billing_Ques').Content != '':
			MQ4 = Quote.GetCustomField('EGAP_Third_Party_Goods_Milestone_Billing_Ques').Content
		MQ7 = 'Yes'
		if Quote.GetCustomField('EGAP_Subscription_SW_Milestone_Billing_Ques').Content != '':
			MQ7 = Quote.GetCustomField('EGAP_Subscription_SW_Milestone_Billing_Ques').Content
		MQ8 = 'Yes'
		if Quote.GetCustomField('EGAP_Other_Goods_Milestone_Billing_Ques').Content != '':
			MQ8 = Quote.GetCustomField('EGAP_Other_Goods_Milestone_Billing_Ques').Content
		manulCostEntry = 'No'
		if Quote.GetCustomField('EGAP_Ques_Manul_Cost_Entry').Content != '':
			manulCostEntry = Quote.GetCustomField('EGAP_Ques_Manul_Cost_Entry').Content
		MQ9 = 'Yes'
		if Quote.GetCustomField('EGAP_Honeywell_Software_Milestone_Billing_Ques').Content != '':
			MQ9 = Quote.GetCustomField('EGAP_Honeywell_Software_Milestone_Billing_Ques').Content
		#cashInflowCalculations.Rows.Clear()
		cashOutflow = GetQuoteTable(Quote, 'Cash_Outflow')
		if cashInflowCalculations.Rows.Count == 0 or cashInflowCalculations.Rows.Count != (maxMonthARO+1):
			cashInflowCalculations.Rows.Clear()
			for monthARO in monthARORange:
				row = cashInflowCalculations.AddNewRow()
				hLNotInMilestone = 0
				subsSWNotInMilestone = 0
				thirdPartyNotInMilestone = 0
				otherNotInMilestone = 0
				hSNotInMilestone = 0
				totalPriceReceiptDict = getCashOutflowPriceReceiptByMonthARO(Quote, cashOutflow, monthARO)
				if MQ3 == 'No':
					hLNotInMilestone = totalPriceReceiptDict.get('Honeywell_Labor', 0)
					if manulCostEntry == 'No':
						hLNotInMilestone = getQuoteTableData(Quote, 'Sum(Price_Receipt)', 'QT__EGAP_Honeywell_Labor_Cost_Curve', ' and Adj_Month_Price = {}'.format(monthARO))
				if MQ4 == 'No':
					thirdPartyNotInMilestone = totalPriceReceiptDict.get('Third_Party_Goods_Services', 0)
				if MQ7 == 'No':
					subsSWNotInMilestone = totalPriceReceiptDict.get('Honeywell_Subscription_Software', 0)
				if MQ8 == 'No':
					otherNotInMilestone = totalPriceReceiptDict.get('Other_Goods_Services', 0)
				if MQ9 == 'No':
					hSNotInMilestone = totalPriceReceiptDict.get('Honeywell_HCI_software', 0)

				row['Cash_Inflow_Month_ARO'] = monthARO
				row['Cash_Inflow_Month'] = monthARO + ptmMonthAdj
				cashInflowMilestone = getSumOfProjectMilestone(Quote, monthARO)
				cashInflowTotal = cashInflowMilestone + hLNotInMilestone + thirdPartyNotInMilestone + subsSWNotInMilestone + otherNotInMilestone + hSNotInMilestone
				row['Cash_Inflow_Total'] = cashInflowTotal
				row['Cash_Inflow_Total_in_USD'] = row['Cash_Inflow_Total'] / exchangeRate
				row['Cash_Inflow_Discounted_Monthly_Inflows'] = row['Cash_Inflow_Total'] / ((1+DCFAtGMLevel)**monthARO)
				row['Cash_Inflow_Date'] = getContractDateFormat(Quote, TagParserQuote, monthARO, 'dd/MM/yy')
				row['Cash_Inflow_Year'] = int(getContractDateFormat(Quote, TagParserQuote, monthARO, 'yy'))
				row['Cash_Inflow_Milestone'] = cashInflowMilestone
				row['Honeywell_Labor_not_in_milestone'] = hLNotInMilestone
				row['Subscription_Software_not_in_milestone'] = subsSWNotInMilestone
				row['Third_Party_not_in_milestone'] = thirdPartyNotInMilestone
				row['Other_not_in_milestone'] = otherNotInMilestone
				row['AS_SW'] = hSNotInMilestone
		else:
			for row in cashInflowCalculations.Rows:
				monthARO = row['Cash_Inflow_Month_ARO']
				hLNotInMilestone = 0
				subsSWNotInMilestone = 0
				thirdPartyNotInMilestone = 0
				otherNotInMilestone = 0
				hSNotInMilestone = 0
				totalPriceReceiptDict = getCashOutflowPriceReceiptByMonthARO(Quote, cashOutflow, monthARO)
				if MQ3 == 'No':
					hLNotInMilestone = totalPriceReceiptDict.get('Honeywell_Labor', 0)
					if manulCostEntry == 'No':
						hLNotInMilestone = getQuoteTableData(Quote, 'Sum(Price_Receipt)', 'QT__EGAP_Honeywell_Labor_Cost_Curve', ' and Adj_Month_Price = {}'.format(monthARO))
				if MQ4 == 'No':
					thirdPartyNotInMilestone = totalPriceReceiptDict.get('Third_Party_Goods_Services', 0)
				if MQ7 == 'No':
					subsSWNotInMilestone = totalPriceReceiptDict.get('Honeywell_Subscription_Software', 0)
				if MQ8 == 'No':
					otherNotInMilestone = totalPriceReceiptDict.get('Other_Goods_Services', 0)
				if MQ9 == 'No':
					hSNotInMilestone = totalPriceReceiptDict.get('Honeywell_HCI_software', 0)
				row['Cash_Inflow_Month'] = monthARO + ptmMonthAdj
				cashInflowMilestone = getSumOfProjectMilestone(Quote, monthARO)
				cashInflowTotal = cashInflowMilestone + hLNotInMilestone + thirdPartyNotInMilestone + subsSWNotInMilestone + otherNotInMilestone + hSNotInMilestone
				row['Cash_Inflow_Total'] = cashInflowTotal
				row['Cash_Inflow_Total_in_USD'] = row['Cash_Inflow_Total'] / exchangeRate
				row['Cash_Inflow_Discounted_Monthly_Inflows'] = row['Cash_Inflow_Total'] / ((1+DCFAtGMLevel)**monthARO)
				row['Cash_Inflow_Date'] = getContractDateFormat(Quote, TagParserQuote, monthARO, 'dd/MM/yy')
				row['Cash_Inflow_Year'] = int(getContractDateFormat(Quote, TagParserQuote, monthARO, 'yy'))
				row['Cash_Inflow_Milestone'] = cashInflowMilestone
				row['Honeywell_Labor_not_in_milestone'] = hLNotInMilestone
				row['Subscription_Software_not_in_milestone'] = subsSWNotInMilestone
				row['Third_Party_not_in_milestone'] = thirdPartyNotInMilestone
				row['Other_not_in_milestone'] = otherNotInMilestone
				row['AS_SW'] = hSNotInMilestone
	
		cashInflowCalculations.Save()
		populateNetCashBalance(Quote, False)

def getCashOutflowPriceReceiptByMonthARO(Quote, cashOutflow, inputMonthARO):
	totalPriceReceiptDict = {}
	if cashOutflow.Rows.Count:
		previousMaterialType = currentMaterialType = ''
		for row in cashOutflow.Rows:
			if row['Row_Type'] == 'Header':
				currentMaterialType = row['Cost_Category_Type']
			elif currentMaterialType == 'Honeywell Subscription Software' and row['Row_Type'] == 'Item':
				outputKey = "Honeywell_Subscription_Software"
				if row['Adj_Month_Price'] == inputMonthARO:
					addToTotal(totalPriceReceiptDict , outputKey , row['Price_Receipt'])
			elif currentMaterialType == 'Honeywell Labor' and row['Row_Type'] == 'Item':
				outputKey = "Honeywell_Labor"
				if row['Adj_Month_Price'] == inputMonthARO:
					addToTotal(totalPriceReceiptDict , outputKey , row['Price_Receipt'])
			elif currentMaterialType == 'Third Party Goods & Services' and row['Row_Type'] == 'Item':
				outputKey = "Third_Party_Goods_Services"
				if row['Adj_Month_Price'] == inputMonthARO:
					addToTotal(totalPriceReceiptDict , outputKey , row['Price_Receipt'])
			elif currentMaterialType == 'Other Goods & Services' and row['Row_Type'] == 'Item':
				outputKey = "Other_Goods_Services"
				if row['Adj_Month_Price'] == inputMonthARO:
					addToTotal(totalPriceReceiptDict , outputKey , row['Price_Receipt'])
			elif currentMaterialType == 'Honeywell HCI software' and row['Row_Type'] == 'Item':
				outputKey = "Honeywell_HCI_software"
				if row['Adj_Month_Price'] == inputMonthARO:
					addToTotal(totalPriceReceiptDict , outputKey , row['Price_Receipt'])
	return totalPriceReceiptDict

def getCashOutflowCalculationByMonthARO(Quote, cashOutflow, inputMonthARO):
	totalCostDict = {}
	cashCurverTableBGP = GetQuoteTable(Quote, 'Honeywell_HCI_Labor_BGP_Cost_Curve')
	if cashOutflow.Rows.Count:
		previousMaterialType = currentMaterialType = ''
		cf_creditTerms = 0
		if Quote.GetCustomField('EGAP_Credit_Terms_Months').Content.strip() != '':
			cf_creditTerms = float(Quote.GetCustomField('EGAP_Credit_Terms_Months').Content)
		for row in cashOutflow.Rows:
			if row['Row_Type'] == 'Header':
				currentMaterialType = row['Cost_Category_Type']
			elif currentMaterialType == 'Honeywell Material' and row['Row_Type'] == 'Item':
				outputKey = "Honeywell_Material"
				if row['ARO_Labor'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Labor_Cost'])
				if row['ARO_Burden'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Burden_Cost'])
				if row['ARO_Material'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Material_Cost'])
				if row['ARO_Purchasing'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Purchasing_Cost'])
				if row['ARO_Freight'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Freight_Cost'])
			elif currentMaterialType == 'Honeywell Software' and row['Row_Type'] == 'Item':
				outputKey = "Honeywell_Software"
				if row['Adj_Month_ARO'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Cost'])
			elif currentMaterialType == 'Honeywell PMC Material' and row['Row_Type'] == 'Item':
				outputKey = "Honeywell_PMC_Material"
				if row['Month_ARO'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Cost'])
			elif currentMaterialType == 'Honeywell HCI software' and row['Row_Type'] == 'Item':
				outputKey = "Honeywell_AS_Software"
				if row['Month_ARO'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Cost'])
			elif currentMaterialType == 'Honeywell HCI Labor & BGP' and row['Row_Type'] == 'Item':
				outputKey = "Honeywell_AS_Labor"
				if row['Month_ARO'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Cost'])
			elif currentMaterialType == 'Honeywell Subscription Software' and row['Row_Type'] == 'Item':
				outputKey = "Honeywell_Subscription_Software"
				if row['Month_ARO'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Cost'])
			elif currentMaterialType == 'Honeywell P3 Material' and row['Row_Type'] == 'Item':
				outputKey = "Honeywell_P3_Material"
				if row['ARO_Labor'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Labor_Cost'])
				if row['ARO_Burden'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Burden_Cost'])
				if row['ARO_Material'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Material_Cost'])
				if row['ARO_Purchasing'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Purchasing_Cost'])
				if row['ARO_Freight'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Freight_Cost'])
			elif currentMaterialType == 'Honeywell Labor' and row['Row_Type'] == 'Item':
				outputKey = "Honeywell_Labor"
				if row['Month_ARO'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Cost'])
			elif currentMaterialType in ['Third Party Goods & Services', 'Third Party Buyout'] and row['Row_Type'] == 'Item':
				outputKey = "Third_Party_Goods_Services" if currentMaterialType == 'Third Party Goods & Services' else 'Third_Party_Buyout'
				if row['Adj_Month_ARO'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Cost'])
			elif currentMaterialType == 'Other Goods & Services' and row['Row_Type'] == 'Item':
				outputKey = "Other_Goods_Services"
				if row['Adj_Month_ARO'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Cost'])
			elif currentMaterialType == 'Honeywell Hardware' and row['Row_Type'] == 'Item':
				outputKey = "Honeywell_Hardware"
				if row['Month_ARO'] == inputMonthARO:
					addToTotal(totalCostDict , outputKey , row['Cost'])
	# if Quote.GetCustomField('Booking LOB').Content == 'HCP':
	for row in cashCurverTableBGP.Rows:
 		if int(row['Month_ARO']) == inputMonthARO:
 			addToTotal(totalCostDict , 'Honeywell_AS_Labor' , row['Cost_Curve'])
	return totalCostDict

def populateCashOutflowCalculation(Quote, TagParserQuote, saveTrigger = False):
	totalCostDict = {}
	materials = ['Honeywell_Material', 'Honeywell_PMC_Material', 'Honeywell_Software', 'Honeywell_Subscription_Software', 'Honeywell_Labor', 'Third_Party_Goods_Services', 'Other_Goods_Services', 'Honeywell_P3_Material', 'Honeywell_AS_Software', 'Honeywell_AS_Labor', 'Honeywell_Hardware', 'Third_Party_Buyout']
	creditTermsMonths = getCreditTermsMonths(Quote)
	ptmMonthAdj = creditTermsMonths
	maxMonthARO = getMaxMonthARONew(Quote, 'Project_Milestone')
	maxMonthAROCashOutflow = getMaxMonthARONew(Quote, 'Cash_Outflow')
	if Quote.GetCustomField('Booking LOB').Content == 'HCP':
		maxMonthAROCostCurve = getMaxMonthARONew(Quote, 'Honeywell_HCI_Labor_BGP_Cost_Curve')
		maxMonthAROCashOutflow = maxMonthAROCostCurve if maxMonthAROCostCurve > maxMonthAROCashOutflow else maxMonthAROCashOutflow
	maxMonthARO = maxMonthAROCashOutflow if maxMonthAROCashOutflow > maxMonthARO else maxMonthARO
	if maxMonthARO > 0:
		monthARORange = range(maxMonthARO+1)
		exchangeRate = float(Quote.GetCustomField('Exchange Rate').Content)
		DCFAtGMLevel = float(Quote.GetCustomField('EGAP_DCF_At_GM_Level').Content)
		manulCostEntry = Quote.GetCustomField('EGAP_Ques_Manul_Cost_Entry').Content
		cashOutflowCalculations = GetQuoteTable(Quote, 'EGAP_Cash_Outflow_Calculations')
		cashOutflow = GetQuoteTable(Quote, 'Cash_Outflow')
		honeywellLaborCostCurve = GetQuoteTable(Quote, 'EGAP_Honeywell_Labor_Cost_Curve')
		if cashOutflowCalculations.Rows.Count == 0 or cashOutflowCalculations.Rows.Count != (maxMonthARO+1):
			cashOutflowCalculations.Rows.Clear()
			for monthARO in monthARORange:
				row = cashOutflowCalculations.AddNewRow()
				row['Cash_Outflow_Month_ARO'] = monthARO
				totalCostDict = getCashOutflowCalculationByMonthARO(Quote, cashOutflow, monthARO)
				'''Honeywell Labor cost calculation for manual entry'''
				if manulCostEntry == 'No' and honeywellLaborCostCurve.Rows.Count > 0:
					outputKey = "Honeywell_Labor"
					sumOfCost = getQuoteTableData(Quote, 'Sum(Cost_Curve)', 'QT__EGAP_Honeywell_Labor_Cost_Curve', ' and Month_ARO = {}'.format(monthARO))
					addToTotal(totalCostDict , outputKey , sumOfCost)
				total = 0
				for material in materials:
					totalCost = totalCostDict.get(material, 0)
					if totalCost > 0 and material != 'Honeywell_Material':
						totalCost = -totalCost
					row[material] = totalCost
					total += row[material]
				row['Cash_Outflow_Month'] = monthARO + ptmMonthAdj
				row['Cash_Outflow_Total'] = total
				row['Cash_Outflow_Total_in_USD'] = row['Cash_Outflow_Total'] / exchangeRate
				if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
					row['Cash_Outflow_Total_in_USD'] = row['Cash_Outflow_Total'] / float(Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content)
				row['Cash_Outflow_Discounted_Monthly_Outflows'] = row['Cash_Outflow_Total'] / ((1+DCFAtGMLevel)**monthARO)
				row['Cash_Outflow_Date'] = getContractDateFormat(Quote, TagParserQuote, monthARO, 'dd/MM/yy')
				row['Cash_Outflow_Year'] = int(getContractDateFormat(Quote, TagParserQuote, monthARO, 'yy'))
		else:
			for row in cashOutflowCalculations.Rows:
				monthARO = row['Cash_Outflow_Month_ARO'] 
				totalCostDict = getCashOutflowCalculationByMonthARO(Quote, cashOutflow, monthARO)
				'''Honeywell Labor cost calculation for manual entry'''
				if manulCostEntry == 'No' and honeywellLaborCostCurve.Rows.Count > 0:
					outputKey = "Honeywell_Labor"
					sumOfCost = getQuoteTableData(Quote, 'Sum(Cost_Curve)', 'QT__EGAP_Honeywell_Labor_Cost_Curve', ' and Month_ARO = {}'.format(monthARO))
					addToTotal(totalCostDict , outputKey , sumOfCost)
				total = 0
				for material in materials:
					totalCost = totalCostDict.get(material, 0)
					if totalCost > 0 and material != 'Honeywell_Material':
						totalCost = -totalCost
					row[material] = totalCost
					total += row[material]
				row['Cash_Outflow_Month'] = monthARO + ptmMonthAdj
				row['Cash_Outflow_Total'] = total
				row['Cash_Outflow_Total_in_USD'] = row['Cash_Outflow_Total'] / exchangeRate
				if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
					row['Cash_Outflow_Total_in_USD'] = row['Cash_Outflow_Total'] / float(Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content)
				row['Cash_Outflow_Discounted_Monthly_Outflows'] = row['Cash_Outflow_Total'] / ((1+DCFAtGMLevel)**monthARO)
				row['Cash_Outflow_Date'] = getContractDateFormat(Quote, TagParserQuote, monthARO, 'dd/MM/yy')
				row['Cash_Outflow_Year'] = int(getContractDateFormat(Quote, TagParserQuote, monthARO, 'yy'))
	
		cashOutflowCalculations.Save()
		populateNetCashBalance(Quote, False)

def populateNetCashBalance(Quote, saveTrigger = False):
	maxMonthAROOutFlow = getMaxMonthARONew(Quote, 'Cash_Outflow')
	maxMonthAROInFlow = getMaxMonthARONew(Quote, 'Project_Milestone')
	maxMonthARO = maxMonthAROInFlow
	if maxMonthAROOutFlow > maxMonthARO:
		maxMonthARO = maxMonthAROOutFlow
	if maxMonthARO > 0:
		monthARORange = range(maxMonthARO+1)
		exchangeRate = float(Quote.GetCustomField('Exchange Rate').Content)
		netCashBalance = GetQuoteTable(Quote, 'EGAP_Net_Cash_Balance')
		previousCumUndiscounted = 0
		previousNegCashFlow = 0
		if netCashBalance.Rows.Count == 0 or netCashBalance.Rows.Count != (maxMonthARO+1):
			netCashBalance.Rows.Clear()
			for monthARO in monthARORange:
				row = netCashBalance.AddNewRow()
				row['Month_ARO'] = monthARO
				cashInflowTotal = getQuoteTableData(Quote, 'Cash_Inflow_Total', 'QT__EGAP_Cash_Inflow_Calculations', ' and Cash_Inflow_Month_ARO = {}'.format(monthARO))
				cashOutflowTotal = getQuoteTableData(Quote, 'Cash_Outflow_Total', 'QT__EGAP_Cash_Outflow_Calculations', ' and Cash_Outflow_Month_ARO = {}'.format(monthARO))
				netTotal = cashInflowTotal + cashOutflowTotal
				row['Undiscounted_Cashflow_GM_level'] = netTotal
				row['Cumulative_Undiscounted_Cashflow'] = previousCumUndiscounted + netTotal
				previousCumUndiscounted = row['Cumulative_Undiscounted_Cashflow']
				row['Net_Cash_in_USD'] = netTotal / exchangeRate
				row['Max_Number_of_Consecutive_Months_w_Negative_Cash_Flow'] = 1 + previousNegCashFlow
				if row['Cumulative_Undiscounted_Cashflow'] >= 0:
					row['Max_Number_of_Consecutive_Months_w_Negative_Cash_Flow'] = 0
				previousNegCashFlow = row['Max_Number_of_Consecutive_Months_w_Negative_Cash_Flow']
				cashDiscountedInflows = getQuoteTableData(Quote, 'Cash_Inflow_Discounted_Monthly_Inflows', 'QT__EGAP_Cash_Inflow_Calculations', ' and Cash_Inflow_Month_ARO = {}'.format(monthARO))
				cashDiscountedOutflows = getQuoteTableData(Quote, 'Cash_Outflow_Discounted_Monthly_Outflows', 'QT__EGAP_Cash_Outflow_Calculations', ' and Cash_Outflow_Month_ARO = {}'.format(monthARO))
				row['Net_Disc_Monthly_Cash_Flows'] = cashDiscountedInflows + cashDiscountedOutflows
		else:
			for row in netCashBalance.Rows:
				monthARO = row['Month_ARO']
				cashInflowTotal = getQuoteTableData(Quote, 'Cash_Inflow_Total', 'QT__EGAP_Cash_Inflow_Calculations', ' and Cash_Inflow_Month_ARO = {}'.format(monthARO))
				cashOutflowTotal = getQuoteTableData(Quote, 'Cash_Outflow_Total', 'QT__EGAP_Cash_Outflow_Calculations', ' and Cash_Outflow_Month_ARO = {}'.format(monthARO))
				netTotal = cashInflowTotal + cashOutflowTotal
				row['Undiscounted_Cashflow_GM_level'] = netTotal
				row['Cumulative_Undiscounted_Cashflow'] = previousCumUndiscounted + netTotal
				previousCumUndiscounted = row['Cumulative_Undiscounted_Cashflow']
				row['Net_Cash_in_USD'] = netTotal / exchangeRate
				row['Max_Number_of_Consecutive_Months_w_Negative_Cash_Flow'] = 1 + previousNegCashFlow
				if row['Cumulative_Undiscounted_Cashflow'] >= 0:
					row['Max_Number_of_Consecutive_Months_w_Negative_Cash_Flow'] = 0
				previousNegCashFlow = row['Max_Number_of_Consecutive_Months_w_Negative_Cash_Flow']
				cashDiscountedInflows = getQuoteTableData(Quote, 'Cash_Inflow_Discounted_Monthly_Inflows', 'QT__EGAP_Cash_Inflow_Calculations', ' and Cash_Inflow_Month_ARO = {}'.format(monthARO))
				cashDiscountedOutflows = getQuoteTableData(Quote, 'Cash_Outflow_Discounted_Monthly_Outflows', 'QT__EGAP_Cash_Outflow_Calculations', ' and Cash_Outflow_Month_ARO = {}'.format(monthARO))
				row['Net_Disc_Monthly_Cash_Flows'] = cashDiscountedInflows + cashDiscountedOutflows
		netCashBalance.Save()
		calculateGrossMargin(Quote, saveTrigger)

def calculateGrossMargin(Quote, saveTrigger = False):
	sumOfInflow = getQuoteTableData(Quote, 'Sum(Cash_Inflow_Total)', 'QT__EGAP_Cash_Inflow_Calculations', '')
	sumOfOutflow = getQuoteTableData(Quote, 'Sum(Cash_Outflow_Total)', 'QT__EGAP_Cash_Outflow_Calculations', '')
	if sumOfInflow >0:
		grossMargin = (sumOfInflow + sumOfOutflow)/sumOfInflow
		Quote.GetCustomField('EGAP_Cross_Margin').Content = str(grossMargin)
	populateCFQBaseline(Quote, saveTrigger)

def populateCFQBaseline(Quote, saveTrigger = False):
	grossMargin = 0
	if Quote.GetCustomField('EGAP_Cross_Margin').Content:
		grossMargin = float(Quote.GetCustomField('EGAP_Cross_Margin').Content)
	maxMonthARO = getMaxMonthARONew(Quote, 'Project_Milestone')
	maxMonthAROCashOutflow = getMaxMonthARONew(Quote, 'Cash_Outflow')
	if Quote.GetCustomField('Booking LOB').Content == 'HCP':
		maxMonthAROCostCurve = getMaxMonthARONew(Quote, 'Honeywell_HCI_Labor_BGP_Cost_Curve')
		maxMonthAROCashOutflow = maxMonthAROCostCurve if maxMonthAROCostCurve > maxMonthAROCashOutflow else maxMonthAROCashOutflow
	maxMonthARO = maxMonthAROCashOutflow if maxMonthAROCashOutflow > maxMonthARO else maxMonthARO
	if maxMonthARO > 0:
		monthARORange = range(maxMonthARO+1)
		preCummulativeOutflow = 0
		preBaselineCFQ = 0
		CFQBaseline = GetQuoteTable(Quote, 'EGAP_CFQ_Baseline')
		if CFQBaseline.Rows.Count == 0 or CFQBaseline.Rows.Count != (maxMonthARO+1):
			CFQBaseline.Rows.Clear()
			for monthARO in monthARORange:
				row = CFQBaseline.AddNewRow()
				row['Month_ARO'] = monthARO
				cashOutflowTotal = getQuoteTableData(Quote, 'Cash_Outflow_Total', 'QT__EGAP_Cash_Outflow_Calculations', ' and Cash_Outflow_Month_ARO = {}'.format(monthARO))
				row['Cash_Outflow'] = cashOutflowTotal
				row['Baseline_CFQ_monthly_cash'] = (-row['Cash_Outflow']/(1-grossMargin))+row['Cash_Outflow'] if grossMargin != 1.0 else 0
				row['Cummulative_Outflow'] = row['Cash_Outflow'] + preCummulativeOutflow
				preCummulativeOutflow = row['Cummulative_Outflow']
				row['Baseline_CFQ_Cumulative'] = row['Baseline_CFQ_monthly_cash'] + preBaselineCFQ
				preBaselineCFQ = row['Baseline_CFQ_Cumulative']
		else:
			for row in CFQBaseline.Rows:
				monthARO = row['Month_ARO']
				cashOutflowTotal = getQuoteTableData(Quote, 'Cash_Outflow_Total', 'QT__EGAP_Cash_Outflow_Calculations', ' and Cash_Outflow_Month_ARO = {}'.format(monthARO))
				row['Cash_Outflow'] = cashOutflowTotal
				row['Baseline_CFQ_monthly_cash'] = (-row['Cash_Outflow']/(1-grossMargin))+row['Cash_Outflow'] if grossMargin != 1.0 else 0
				row['Cummulative_Outflow'] = row['Cash_Outflow'] + preCummulativeOutflow
				preCummulativeOutflow = row['Cummulative_Outflow']
				row['Baseline_CFQ_Cumulative'] = row['Baseline_CFQ_monthly_cash'] + preBaselineCFQ
				preBaselineCFQ = row['Baseline_CFQ_Cumulative']
		CFQBaseline.Save()
		populateCFQ(Quote, maxMonthARO, saveTrigger)

def populateCFQ(Quote, maxMonthARO, saveTrigger = False):
	grossMargin = 0
	if Quote.GetCustomField('EGAP_Cross_Margin').Content:
		grossMargin = float(Quote.GetCustomField('EGAP_Cross_Margin').Content)
	DCFAtGMLevel = float(Quote.GetCustomField('EGAP_DCF_At_GM_Level').Content)
	CFQ = GetQuoteTable(Quote, 'EGAP_CFQ')
	#CFQ.Rows.Clear()
	maxMonthAROOutFlow = getMaxMonthARONew(Quote, 'Cash_Outflow')
	maxMonthAROInFlow = getMaxMonthARONew(Quote, 'Project_Milestone')
	maxMonthARO = maxMonthAROInFlow
	if Quote.GetCustomField('Booking LOB').Content == 'HCP':
		maxMonthAROCostCurve = getMaxMonthARONew(Quote, 'Honeywell_HCI_Labor_BGP_Cost_Curve')
		maxMonthARO = maxMonthAROCostCurve if maxMonthAROCostCurve > maxMonthARO else maxMonthARO
	if maxMonthAROOutFlow > maxMonthARO:
		maxMonthARO = maxMonthAROOutFlow
	monthARORange = range(maxMonthARO+1)
	initialCashRecoverytoMarginlevel = 0
	cashRecoverytoMarginlevels = []
	sumOfCashInflowTotalInUSD = 0
	if CFQ.Rows.Count == 0 or CFQ.Rows.Count != (maxMonthARO+1):
		CFQ.Rows.Clear()
		for monthARO in monthARORange:
			row = CFQ.AddNewRow()
			netCashInUSD = getQuoteTableData(Quote, 'Net_Cash_in_USD', 'QT__EGAP_Net_Cash_Balance', ' and Month_ARO = {}'.format(monthARO))
			cashInflowTotalInUSD = getQuoteTableData(Quote, 'Cash_Inflow_Total_in_USD', 'QT__EGAP_Cash_Inflow_Calculations', ' and Cash_Inflow_Month_ARO = {}'.format(monthARO))
			sumOfCashInflowTotalInUSD += cashInflowTotalInUSD
			row['Month_ARO'] = monthARO
			row['Net_Cash_in_USD'] = netCashInUSD
			row['NPV_USD'] = netCashInUSD/((1+DCFAtGMLevel)**monthARO)
			row['Cash_Recovery_to_Margin_level'] = cashInflowTotalInUSD * grossMargin
			if monthARO == 0:
				initialCashRecoverytoMarginlevel = row['Cash_Recovery_to_Margin_level']
			else:
				cashRecoverytoMarginlevels.append(row['Cash_Recovery_to_Margin_level'])
	else:
		for row in CFQ.Rows:
			monthARO = row['Month_ARO']
			netCashInUSD = getQuoteTableData(Quote, 'Net_Cash_in_USD', 'QT__EGAP_Net_Cash_Balance', ' and Month_ARO = {}'.format(monthARO))
			cashInflowTotalInUSD = getQuoteTableData(Quote, 'Cash_Inflow_Total_in_USD', 'QT__EGAP_Cash_Inflow_Calculations', ' and Cash_Inflow_Month_ARO = {}'.format(monthARO))
			sumOfCashInflowTotalInUSD += cashInflowTotalInUSD
			row['Net_Cash_in_USD'] = netCashInUSD
			row['NPV_USD'] = netCashInUSD/((1+DCFAtGMLevel)**monthARO)
			row['Cash_Recovery_to_Margin_level'] = cashInflowTotalInUSD * grossMargin
			if monthARO == 0:
				initialCashRecoverytoMarginlevel = row['Cash_Recovery_to_Margin_level']
			else:
				cashRecoverytoMarginlevels.append(row['Cash_Recovery_to_Margin_level'])
	CFQ.Save()
	otherCFQCalculation(Quote, initialCashRecoverytoMarginlevel, DCFAtGMLevel,cashRecoverytoMarginlevels,sumOfCashInflowTotalInUSD, saveTrigger)

def otherCFQCalculation(Quote, initialCashRecoverytoMarginlevel, DCFAtGMLevel,cashRecoverytoMarginlevels, cashInflowTotalInUSD, saveTrigger = False):
	exchangeRate = float(Quote.GetCustomField('Exchange Rate').Content)
	values = System.Array[float](cashRecoverytoMarginlevels)
	netPVal = getNPV(DCFAtGMLevel, values)
	cf_cashRecoverytoMarginlevel = Quote.GetCustomField('EGAP_Cash_Recovery_to_Margin_level')
	cashRecoverytoMarginlevel = initialCashRecoverytoMarginlevel + netPVal
	cf_cashRecoverytoMarginlevel.Content = str(cashRecoverytoMarginlevel)
	sumOfNPV = getQuoteTableData(Quote, 'Sum(NPV_USD)', 'QT__EGAP_CFQ', '')
	CFQ = 0
	if cashInflowTotalInUSD > 0:
		CFQ = (sumOfNPV - cashRecoverytoMarginlevel)/cashInflowTotalInUSD
	CFQ = round((CFQ*100.0),2)
	Quote.GetCustomField('EGAP_Cash_Flow_Quality').Content = "{}%".format(str(CFQ))
	cf_lowestCumCFinanySingleMonthUSD = Quote.GetCustomField('EGAP_Lowest_Cum_CF_in_any_Single_Month_USD')
	cf_maxConsecMonthsNegCumCashFlows = Quote.GetCustomField('EGAP_Max_Consec_Months_Neg_Cum_Cash_Flows')
	cf_monthsNegativeCumulativeCashFlows = Quote.GetCustomField('EGAP_Months_Negative_Cumulative_Cash_Flows')
	cf_revenueImpact = Quote.GetCustomField('EGAP_Revenue_Impact_Change_in_Currency_USD')
	if Quote.GetCustomField('Currency').Content == 'USD':
		cf_revenueImpact.Content = '0'
	else:
		walkAwayPrice = getQuoteTableData(Quote, 'EGAP_USD_Currency', 'QT__EGAP_Revenue_Margin', "and EGAP_Field_Details='Walk-away Sell Price'")
		walkAwayPrice=float(walkAwayPrice.replace(',','')) if walkAwayPrice else 0
		revenueImpact = round((0.05*walkAwayPrice),2)
		cf_revenueImpact.Content = str(revenueImpact)
	cf_NPV = Quote.GetCustomField('EGAP_NPV')
	minNetCashInUSD = getQuoteTableData(Quote, 'Min(Cumulative_Undiscounted_Cashflow)', 'QT__EGAP_Net_Cash_Balance', ' and Month_ARO > 1')
	minNetCashInUSD = minNetCashInUSD/exchangeRate if exchangeRate > 0 else 0
	cf_lowestCumCFinanySingleMonthUSD.Content = str(round(minNetCashInUSD,2))
	maxConsecMonthsNegCumCashFlows = getQuoteTableData(Quote, 'Max(Max_Number_of_Consecutive_Months_w_Negative_Cash_Flow)', 'QT__EGAP_Net_Cash_Balance', '')
	cf_maxConsecMonthsNegCumCashFlows.Content = str(maxConsecMonthsNegCumCashFlows)
	monthsNegativeCumulativeCashFlows = getQuoteTableData(Quote, 'count(Cumulative_Undiscounted_Cashflow)', 'QT__EGAP_Net_Cash_Balance', ' and Cumulative_Undiscounted_Cashflow < 0')
	cf_monthsNegativeCumulativeCashFlows.Content = str(monthsNegativeCumulativeCashFlows)
	sumCashInflowDiscountedMonthlyInflows = getQuoteTableData(Quote, 'Sum(Cash_Inflow_Discounted_Monthly_Inflows)', 'QT__EGAP_Cash_Inflow_Calculations', '')
	sumCashOutflowDiscountedMonthlyOutflows = getQuoteTableData(Quote, 'Sum(Cash_Outflow_Discounted_Monthly_Outflows)', 'QT__EGAP_Cash_Outflow_Calculations', '')
	npvContent = str(sumCashInflowDiscountedMonthlyInflows+sumCashOutflowDiscountedMonthlyOutflows)
	if cf_NPV.Content != npvContent:
		cf_NPV.Content = npvContent

def manualBGPLaborCost(Quote):
	costs_dict = {}
	PLSGUserInputDescTable = GetQuoteTable(Quote, "Honeywell_HCI_Labor_BGP_PLSG")
	getHCILaborCostBGP = SqlHelper.GetList("SELECT DISTINCT PLSG_Code FROM Cost_Curve_timeline_laborBGP(NOLOCK)")
	HCILaborCostBGP = [i.PLSG_Code for i in getHCILaborCostBGP]
	HCILaborCostBGPCodes = ['7242-7990', '7243-7992', '7245-7996', '7246-7998','7247-7A01', '7248-7A03', '7249-7A05', '7686-7B48', '7688-7B50']

	inputRows = [i['PLSG_Code'] for i in PLSGUserInputDescTable.Rows]
	for item in Quote.Items:
		if str(item.QI_PLSG.Value) in HCILaborCostBGP  or str(item.QI_PLSG.Value) in HCILaborCostBGPCodes:
			key = item.QI_PLSG.Value
			if key in costs_dict:
				costs_dict[key]['Cost'] += item.QI_ExtendedWTWCost.Value
			else:
				costs_dict[key] = {
					'Product_Description': item.QI_ProductLineDesc.Value,
					'Cost': item.QI_ExtendedWTWCost.Value,
					'PLSG_Code': key
				}
	for value in costs_dict.values():
		if value['PLSG_Code'] not in inputRows and int(value['Cost'])>0:
			newRow = PLSGUserInputDescTable.AddNewRow()
			newRow['Product_Description'] = value['Product_Description']
			newRow['Cost'] = value['Cost']
			newRow['PLSG_Code'] = value['PLSG_Code']

	PLSGUserInputDescTable.Save()