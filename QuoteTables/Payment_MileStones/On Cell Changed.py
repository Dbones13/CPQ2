def getCfValue(cfName):
  return Quote.GetCustomField(cfName).Content

mileStoneTable = EventArgs.Table
changedCellIndex = len(EventArgs.Cells) - 1
changedCell = EventArgs.Cells[changedCellIndex]
changedRow = changedCell.Row
newValue = changedCell.Value

if changedCell.ColumnName == "Billing_Milestone" and newValue != '':
    if (getCfValue("Quote Type") == "Projects" and getCfValue("Booking LOB") in("PAS","CCC") ) or (getCfValue("Quote Type") == "Parts and Spot" and getCfValue("Booking LOB") in("CCC")):
        changedRow["Milestone_Description"] = changedRow["Billing_Milestone"]
    else:
        query = SqlHelper.GetFirst("select Description from MILESTONE_DESCRIPTION where Billing_Milestone = '{}'".format(newValue))
        if query is not None:
            changedRow["Milestone_Description"] = query.Description
    mileStoneTable.Save()

Quote.GetCustomField("Milestone_total").Content = ""
qt = Quote.QuoteTables["Payment_MileStones"]
sum = 0
for row in qt.Rows:
    sum = sum + row["_Amount"]
Quote.Messages.Remove('Sum of % milestone payment is not equal to 100%')
if getCfValue("Booking LOB") in("CCC") and (sum>100 or sum<100):
    Quote.Messages.Add('Sum of % milestone payment is not equal to 100%')
    Quote.GetCustomField('sum_of_milestone_flag').Content = '1'
    Quote.GetCustomField('EGAP_Cashflow_Health').Content = 'Out of Balance'
elif getCfValue("Booking LOB") in("CCC") and sum == 100:
    Quote.GetCustomField('sum_of_milestone_flag').Content = '0'
    Quote.GetCustomField('EGAP_Cashflow_Health').Content = 'In Balance'

Quote.GetCustomField("Milestone_total").Content = str(sum)
Quote.Save(False)