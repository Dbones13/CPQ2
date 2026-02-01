def CFValue(Name):
    return Quote.GetCustomField(Name).Content

quoteTotalTable = Quote.QuoteTables["Quote_Details"]
discountApplied = False

for row in quoteTotalTable.Rows:
    if row['Quote_Discount_Percent'] > 0:
        discountApplied = True

#Cextended condition for Service Contract
#CXCPQ - 60771 - 29/9/2023 - Jagruti Chandratre
if discountApplied and CFValue("Discount Request Reason") == '' and CFValue("Booking LOB") == 'LSS' and CFValue("Quote Type") not in ["Projects","Contract New","Contract Renewal"]:
    WorkflowContext.BreakWorkflowExecution = True
    Trace.Write("Discount:{0}".format('Contract'))
    Quote.Messages.Add(Translation.Get("ErrorMessage.DiscountRequestReason"))
