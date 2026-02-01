"""import GS_EGAPCashFlowDetail as CFD

cashOutflow =  Quote.QuoteTables["Cash_Outflow"]
i = 0
wTWCostTotal = 0
Quote.GetCustomField('EGAP_QT_CashOutflow_Warning').Content = ''
while i < len(EventArgs.Cells):
	columnName     = EventArgs.Cells[i].ColumnName
	if columnName == 'Cost':
		oldValue     = EventArgs.OldValues[i]
		currentRow   = EventArgs.Cells[i].Row
		currentRowId = currentRow.Id
		wtwCosts, headerRowIds = CFD.getHeadersRowId(Quote)
		lastRowId = headerRowIds[-1]
		if currentRowId > lastRowId:
			startId = endId = lastRowId
			wTWCostTotal = wtwCosts[startId]
		else:
			totalHeaderRows = len(headerRowIds)
			for j in range(totalHeaderRows-1):
				nextId = j+1
				#Trace.Write("NextVal={} val ={}".format(nextId,headerRowIds[nextId]))
				if headerRowIds[j] < currentRowId and currentRowId < headerRowIds[nextId]:
					startId = headerRowIds[j]
					endId = headerRowIds[nextId]
					wTWCostTotal = wtwCosts[startId]
					break
		if wTWCostTotal:
			currentWTWCost = currentRow['Cost']
			wTWCostGroupTotal = 0
			if startId == endId:
				sqlQuery = "Select SUM(Cost) as totalCost from QT__Cash_Outflow where ownerid={} and cartid={} and Id > {} and Id != {} and Row_Type='{}'"
				sqlResult = SqlHelper.GetFirst(sqlQuery.format(Quote.UserId,Quote.QuoteId,startId,currentRowId,'Item'))
			else:
				sqlQuery = "Select SUM(Cost) as totalCost from QT__Cash_Outflow where ownerid={} and cartid={} and Id > {} and Id < {} and  Id != {} and Row_Type='{}'"
				sqlResult = SqlHelper.GetFirst(sqlQuery.format(Quote.UserId,Quote.QuoteId,startId,endId,currentRowId,'Item'))
			if sqlResult:
				wTWCostGroupTotal = sqlResult.totalCost if sqlResult.totalCost else 0
				wTWCostGroupTotal += currentWTWCost
			'''if currentWTWCost > wTWCostTotal or wTWCostTotal < 1 or wTWCostGroupTotal > wTWCostTotal:
				currentRow['Cost'] = oldValue
				Quote.GetCustomField('EGAP_QT_CashOutflow_Warning').Content = 'Row #:{} WTW cost calculated does not match with Total of shipment cost entered for the cost category.'.format(currentRowId)
		else:
			currentRow['Cost'] = 0
			Quote.GetCustomField('EGAP_QT_CashOutflow_Warning').Content = 'Row #:{} WTW cost calculated does not match with Total of shipment cost entered for the cost category.'.format(currentRowId)'''
	i += 1

'''Update Total of shipment cost'''
Quote.GetCustomField('EGAP_QT_CashOutflow_Warning').Content = CFD.updateTotalCost(Quote, cashOutflow)
columns = ['Shipment_Number', 'Shipment_Description', 'Cost', 'Month_ARO',    'Vendor_Payment_Term','P3_Product_Type']
columnTobeReadonly = 'Vendor_Payment_Term'
columnTobeReadonlyP3 = 'P3_Product_Type'
categoryTypes = ['Third Party Goods & Services','Other Goods & Services', 'Third Party Buyout']
categoryTypesP3 = ['Honeywell P3 Material']
'''Cash outflow Calculation'''
CFD.updateCashOutflowCalculation(Quote, cashOutflow, TagParserQuote)
CFD.makeQuoteTableColumnsReadonly(cashOutflow, columns, columnTobeReadonly, categoryTypes)
CFD.makeQuoteTableColumnsReadonly(cashOutflow, columns, columnTobeReadonlyP3, categoryTypesP3)
cashOutflow.Save()"""
import GS_EGAPCashFlowDetail as CFD
cashOutflow =  Quote.QuoteTables["Cash_Outflow"]
columns = ['Shipment_Number', 'Shipment_Description', 'Cost', 'Month_ARO',    'Vendor_Payment_Term','P3_Product_Type']
columnTobeReadonly = 'Vendor_Payment_Term'
columnTobeReadonlyP3 = 'P3_Product_Type'
categoryTypes = ['Third Party Goods & Services','Other Goods & Services', 'Third Party Buyout']
categoryTypesP3 = ['Honeywell P3 Material']
CFD.makeQuoteTableColumnsReadonly(cashOutflow, columns, columnTobeReadonly, categoryTypes)
CFD.makeQuoteTableColumnsReadonly(cashOutflow, columns, columnTobeReadonlyP3, categoryTypesP3)