def CFValue(Name):
    return Quote.GetCustomField(Name).Content

MultiplePricePlanPresent = False
mpa = Quote.GetCustomField('AccountId').Content
sf_agg_id = SqlHelper.GetFirst("SELECT Salesforce_Agreement_ID FROM MPA_ACCOUNT_MAPPING WHERE Salesforce_ID='{}'".format(mpa))
if sf_agg_id:
    query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Salesforce_Agreement_ID = '"+str(sf_agg_id.Salesforce_Agreement_ID)+"' and Price_Plan_Status= 'Active' and [IF]([EQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects)){Price_Plan_Systems_Discount}{Price_Plan_Parts_Discount}[ENDIF] = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
else:
    query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Price_Plan_Status= 'Active' and [IF]([EQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects)){Price_Plan_Systems_Discount}{Price_Plan_Parts_Discount}[ENDIF] = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
res = SqlHelper.GetList(query)
if res and len(res) > 0:
    MultiplePricePlanPresent = True

if CFValue("Quote Type") not in ["Contract New","Contract Renewal"] and CFValue("Booking LOB") not in('CCC','PMC') and CFValue("MPA")!= "":
    if MultiplePricePlanPresent and CFValue("MPA Price Plan") == '':
        WorkflowContext.BreakWorkflowExecution = True
        Quote.Messages.Add("Select Price plan")

quoteTotalTable = Quote.QuoteTables["Quote_Details"]
discountApplied = False

for row in quoteTotalTable.Rows:
    if row['Quote_Discount_Percent'] > 0:
        discountApplied = True
'''
if discountApplied and CFValue("Discount Request Reason") == '' and CFValue("Booking LOB") == 'LSS' and CFValue("Quote Type") != "Projects":
        WorkflowContext.BreakWorkflowExecution = True
        Quote.Messages.Add(Translation.Get("ErrorMessage.DiscountRequestReason"))
'''

#Commented above code and extended condition for Service Contract
#CXCPQ - 60771 - 29/9/2023 - Jagruti Chandratre
if discountApplied and CFValue("Discount Request Reason") == '' and CFValue("Booking LOB") == 'LSS' and CFValue("Quote Type") not in ["Projects","Contract New","Contract Renewal"]:
    WorkflowContext.BreakWorkflowExecution = True
    Quote.Messages.Add(Translation.Get("ErrorMessage.DiscountRequestReason"))

if CFValue("Payment Terms") == '' or CFValue("Proposal Validity") == '':
    WorkflowContext.BreakWorkflowExecution = True
    Quote.Messages.Add(Translation.Get("ErrorMessage.PaymentTerms.ProposalValidity"))
