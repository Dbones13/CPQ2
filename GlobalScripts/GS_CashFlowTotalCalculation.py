import GS_EGAPCashFlowDetail as CFD
from System import DBNull
cashOutflow =  Quote.QuoteTables["Cash_Outflow"]
Quote.GetCustomField('EGAP_QT_CashOutflow_Warning').Content = ''
Log.Info("Pam -------- > GS_CashFlowTotalCalculation")
Quote.GetCustomField('EGAP_QT_CashOutflow_Warning').Content = CFD.updateTotalCost(Quote, cashOutflow)
Log.Info("Cflow1=>"+str(Quote.GetCustomField('EGAP_QT_CashOutflow_Warning').Content))
columns = ['Shipment_Number', 'Shipment_Description', 'Cost', 'Month_ARO',    'Vendor_Payment_Term','P3_Product_Type']
columnTobeReadonly = 'Vendor_Payment_Term'
columnTobeReadonlyP3 = 'P3_Product_Type'
categoryTypes = ['Third Party Goods & Services','Other Goods & Services', 'Third Party Buyout']
categoryTypesP3 = ['Honeywell P3 Material']
'''Cash outflow Calculation'''
CFD.updateCashOutflowCalculation(Quote, cashOutflow, TagParserQuote)
CFD.makeQuoteTableColumnsReadonly(cashOutflow, columns, columnTobeReadonly, categoryTypes)
CFD.makeQuoteTableColumnsReadonly(cashOutflow, columns, columnTobeReadonlyP3, categoryTypesP3)
cashOutflow.Save()
def getQuoteTableData(Quote, column, quoteTableName, condition):
	query = "Select {} as output from {} where ownerid={} and cartid={} {} ".format(column, quoteTableName, Quote.UserId, Quote.QuoteId, condition)
	qtResult = SqlHelper.GetFirst(query)
	output = 0
	if qtResult is not None and len(qtResult) > 0:
		output = qtResult.output if qtResult.output != DBNull.Value else 0
	return output
cf_cashflowHealth = Quote.GetCustomField('EGAP_Cashflow_Health')
cf_cashflowHealth_cfd = Quote.GetCustomField('EGAP_CFD_Cashflow_Health')
totalCashInflow = getQuoteTableData(Quote, 'Sum(Cash_Inflow_Total)', 'QT__EGAP_Cash_Inflow_Calculations', '')
walkawaySalesPrice = getQuoteTableData(Quote, 'Walk_away_Sales_Price', 'QT__Quote_Details', '')
remainingCashInflow = totalCashInflow - walkawaySalesPrice

totalCashOutflow = getQuoteTableData(Quote, 'Sum(Cash_Outflow_Total)', 'QT__EGAP_Cash_Outflow_Calculations', '')
quoteWTWCost =  getQuoteTableData(Quote, 'Quote_WTW_Cost', 'QT__Quote_Details', '')
remainingCashOutflow = totalCashOutflow + quoteWTWCost

absNet = abs(round(remainingCashInflow+remainingCashOutflow))
cf_cashflowHealth.Content = 'Out of Balance'
cf_cashflowHealth_cfd.Content = 'Out of Balance'
if absNet < (0.0001 * walkawaySalesPrice) and Quote.GetCustomField('EGAP_QT_CashOutflow_Warning').Content == '':
	cf_cashflowHealth.Content = 'In Balance'
	cf_cashflowHealth_cfd.Content = 'In Balance'
'''Validating Project Milestone Data'''
projectMilestone = Quote.QuoteTables["EGAP_Project_Milestone"]
maxMonthARO = CFD.getMaxMonthARO(Quote)
Quote.GetCustomField('EGAP_QT_ProjectMilestone_Warning').Content = CFD.validateProjectMilestoneData(projectMilestone, maxMonthARO)
CFD.populateCashInflowCalculation(Quote, TagParserQuote)
CFD.populateCashOutflowCalculation(Quote, TagParserQuote, True)
Quote.GetCustomField('EGAP_CFD_Cash_Flow_Quality').Content = 0 if Quote.GetCustomField('Booking LOB').Content == 'CCC' else Quote.GetCustomField('EGAP_Cash_Flow_Quality').Content
Quote.GetCustomField('Save Trigger').Content = 'true'
projectMilestone.Save()
Quote.Save(False)