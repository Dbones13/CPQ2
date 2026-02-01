import GS_EGAPCashFlowDetail as CFD

milestonePrice = float(Quote.GetCustomField('EGAP_Milestone_Price').Content)
projectMilestone = Quote.QuoteTables["EGAP_Project_Milestone"]
i = 0
qtColumns = ['EGAP_Proposed_Milestones', 'EGAP_Milestone_Name', 'EGAP_Month_ARO', 'EGAP_Pct_of_Total_Milestone_Payment', 'EGAP_Customer_Signoff_Required', 'EGAP_Milestone_with_Bank_Guarantee',    'EGAP_Amount', 'EGAP_Month_ARC', 'Row_Type','EGAP_Weeks_ARO']
columnName = ''
cf_creditTerms = CFD.getCreditTermsMonths(Quote)
ptmMonthAdj = cf_creditTerms
qt_type = Quote.GetCustomField("Quote Type").Content
while i < len(EventArgs.Cells):
    cell = EventArgs.Cells[i]
    row = cell.Row
    row['EGAP_Month_ARC'] = row['EGAP_Month_ARO']  + ptmMonthAdj
    columnName = cell.ColumnName
    if columnName == "EGAP_Pct_of_Total_Milestone_Payment":
        if cell.Value < 0:
            row[columnName] = EventArgs.OldValues[i]
        row['EGAP_Amount'] =  milestonePrice * row[columnName]/100
    elif columnName == "EGAP_Weeks_ARO":
        if cell.Value < 0:
            row[columnName] = EventArgs.OldValues[i]
        row['EGAP_Month_ARO'] = int(round(row[columnName]/4.345))
        row['Month_ARO'] = (row[columnName]/4.345)
        row['EGAP_Month_ARC'] = row['EGAP_Month_ARO'] + ptmMonthAdj
    elif columnName == "EGAP_Month_ARO":
        if cell.Value < 0:
            row[columnName] = EventArgs.OldValues[i]
        row['EGAP_Month_ARC'] = row['EGAP_Month_ARO'] + ptmMonthAdj
        if qt_type in ('Contract New','Contract Renewal'):
            row['EGAP_Month_ARC'] = row['EGAP_Month_ARO']
    i += 1
'''Update Remaining Milestone Percentage'''
totalMilestonePct = 0
rowIndex = -1
for quoteTableRow in projectMilestone.Rows:
    if quoteTableRow['Row_Type'] == 'Header':
        rowIndex = projectMilestone.Rows.IndexOf(quoteTableRow)
        for col in qtColumns:
            quoteTableRow.Cells.Item[col].AccessLevel = projectMilestone.AccessLevel.ReadOnly
    else:
        totalMilestonePct += quoteTableRow['EGAP_Pct_of_Total_Milestone_Payment']
if rowIndex >=0:
    quoteTableRow = projectMilestone.Rows[rowIndex]
    quoteTableRow['EGAP_Pct_of_Total_Milestone_Payment'] = 100 - totalMilestonePct

projectMilestone.Save()

'''Validating Project Milestone Data'''
if columnName in ['EGAP_Weeks_ARO', 'EGAP_Month_ARO']:
    maxMonthARO = CFD.getMaxMonthARO(Quote)
    Quote.GetCustomField('EGAP_QT_ProjectMilestone_Warning').Content = CFD.validateProjectMilestoneData(projectMilestone, maxMonthARO)
    CFD.populateCashInflowCalculation(Quote, TagParserQuote)