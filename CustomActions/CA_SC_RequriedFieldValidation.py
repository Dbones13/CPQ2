from GS_SC_Extension_Error_Msg import *
Booking_Info_Tab = ['Booking Tab Customer Requested Date','PurchaseOrderDate','ProfitCentre','Profit Centre Description','PONumber','NetTerms','Incoterms on Sales Order','EndUse']
Commercial_Info_Tab =['Proposal Validity']
Quotation_Tab = ['SC_CF_AGREEMENT_TYPE','SC_CF_CURANNDELENDT','SC_CF_CURANNDELSTDT','SC_CF_LOCAL_REF','EGAP_Proposal_Type']

#MilestoneTable Validation
table = Quote.QuoteTables["SC_Milestone_Table"]
r_count = 0
for row in table.Rows:
    if str(row.GetColumnValue('Start_Date')) == 'None' or str(row.GetColumnValue('End_Date')) == 'None':
        r_count +=1

#Opportuni Info
userTable = Quote.QuoteTables['SC_SFDC_Data_QuoteTable']
Quote.GetCustomField('SC_CF_SFDCROLE_MESSAGE').Content = ''
Quote.GetCustomField('SC_CF_SFDCROLE_MESSAGE').Visible = False
Quote.Messages.Clear()
missingList = list()
Agreement_type = Quote.GetCustomField("SC_CF_AGREEMENT_TYPE").Content
countFlag = 0
roleOrderDict = {}

role_mapping = {
    'GSM Contract Manager': 'Contract Manager',
    'GSM ISA Manager': 'ISA Manager',
    'GSM Regional Contract Manager': 'RSOM',
    'GSM Field Service Manager': 'FSM',
    'GSM Service Business Leader': 'SBD',
    'GSM Renewal Specialist': 'CSS'
    }
if Quote.GetCustomField('Quote Type').Content == 'Contract New':
    mandatoryRoles = ['Contract Manager', 'ISA Manager', 'RSOM', 'SBD']
elif Quote.GetCustomField('Quote Type').Content == 'Contract Renewal':
    mandatoryRoles = ['Contract Manager', 'ISA Manager', 'RSOM', 'SBD','CSS']

if Quote.GetCustomField("Quote Type").Content in ['Contract New','Contract Renewal']:
    if Agreement_type != "ISA":
        mandatoryRoles.remove("ISA Manager")
    for row in Quote.QuoteTables['SC_SFDC_Data_QuoteTable'].Rows:
        if row["Role"] in role_mapping and role_mapping[row["Role"]] in mandatoryRoles:
            mandatoryRoles.remove(role_mapping[row["Role"]])
            if row["Role"]:
                if row["Role"] in roleOrderDict:
                    if roleOrderDict[row["Role"]] >= 1:
                        countFlag = 1
                    else:
                        roleOrderDict[row["Role"]] = 1
                else:
                    roleOrderDict[row["Role"]] = 1

Q_lst = []
C_lst = []

for CF in Quotation_Tab:
        if Quote.GetCustomField(CF).Content == '':  #or Quote.GetCustomField(CF).Content == 'None':
            Q_lst.append(Quote.GetCustomField(CF).Label)

for CF in Commercial_Info_Tab:
        if Quote.GetCustomField(CF).Content == '':  #or Quote.GetCustomField(CF).Content == None:
            C_lst.append(Quote.GetCustomField(CF).Label)

Q_CF_str = ", ".join(str(bit) for bit in Q_lst)
C_CF_str = ", ".join(str(bit) for bit in C_lst)

P_count = Quote.Items.Count

#Quote.Messages.Clear()
Cashflow_Health = Quote.GetCustomField('EGAP_CFD_Cashflow_Health').Content

approvalMethod = Quote.GetCustomField('SC_CF_FIN_APPROVAL_METHOD').Content

if approvalMethod == 'eGap':
    Cashflow_Health = Quote.GetCustomField('EGAP_CFD_Cashflow_Health').Content
else:
    Cashflow_Health = 'In balance'

is_Extension = Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content

#Sell_Price = Quote.GetCustomField('Total Sell Price(USD)').Content
Header_tot_sell_price = (Quote.GetCustomField('Total Sell Price(USD)').Content[4:]).replace(",", "")
Inv_Freq = Quote.GetCustomField('SC_CF_INV_FREQUENCY').Content

sell_price_lst = []
escalation_validation_lst = []
for item in Quote.MainItems:
    if 'Year' in item.PartNumber:
        sell_price_lst.append(float(item.ExtendedAmount))
    if item.QI_SC_Escalation_Percent.Value < 5 and len(item.QI_SC_ItemFlag.Value)>0 and item.QI_SC_ItemFlag.Value[0] == '1' and item.PartNumber == 'Other cost details':
        escalation_validation_lst.append(item.RolledUpQuoteItem)

#Check Product Configuration Status
Check_Prod_Config_Status = Quote.MainItems[0].IsComplete

if Quote.GetCustomField("Quote Type").Content in ['Contract New']:
    if  Q_CF_str != '' or C_CF_str != '' or P_count == 0 or Cashflow_Health == 'Out of Balance' or Header_tot_sell_price == 0 or len(mandatoryRoles)!=0 or len(escalation_validation_lst)>0 or Check_Prod_Config_Status == False or r_count > 0:
        if Q_CF_str != '':
            Quote.Messages.Add(Translation.Get('Please enter mandatory fields of Quotation Tab such as '+ Q_CF_str))
        elif C_CF_str != '':
            Quote.Messages.Add(Translation.Get('Please enter mandatory fields of Commercial Info Tab such as '+ C_CF_str))
        elif P_count == 0:
            Quote.Messages.Add(Translation.Get('Please add product before request for approval'))
        elif Inv_Freq == 'Adhoc' and float(Header_tot_sell_price) != float(sum(sell_price_lst)):
            Quote.Messages.Add(Translation.Get('Adjust the milestone data in commercial info tab.'))
        elif r_count > 0:
            Quote.Messages.Add(Translation.Get('Please review the data in milestone table. Blank rows are not allowed.'))
        elif Cashflow_Health == 'Out of Balance':
            Quote.Messages.Add(Translation.Get('Cashflow is Out of Balance'))
        elif Header_tot_sell_price == 0:
            Quote.Messages.Add(Translation.Get('Product with zero price is not allowed'))
        elif mandatoryRoles:
            Quote.Messages.Add("Please update the Honeywell Sales Team in the opportunity for roles - "+str(" ,".join(mandatoryRoles)))
        elif Check_Prod_Config_Status == False:
            Quote.Messages.Add(Translation.Get('Please complete Product configuration before requesting for approval '))
        if escalation_validation_lst:
            Quote.Messages.Add("For item : '{}', Escalation % for Other cost details should not be less than 5%".format(str(", ".join(escalation_validation_lst))))
        WorkflowContext.BreakWorkflowExecution = True

if Quote.GetCustomField("Quote Type").Content in ['Contract Renewal']:
    if  Q_CF_str != '' or C_CF_str != '' or P_count == 0 or Cashflow_Health == 'Out of Balance' or Header_tot_sell_price == 0 or len(escalation_validation_lst)>0 or Check_Prod_Config_Status == False or r_count > 0 or is_Extension == 'True':
        breakWorkflow = True
        Trace.Write('Jagruti')
        if Q_CF_str != '':
            Quote.Messages.Add(Translation.Get('Please enter mandatory fields of Quotation Tab such as '+ Q_CF_str))
        elif C_CF_str != '':
            Quote.Messages.Add(Translation.Get('Please enter mandatory fields of Commercial Info Tab such as '+ C_CF_str))
        elif P_count == 0:
            Quote.Messages.Add(Translation.Get('Please add product before request for approval'))
        elif Inv_Freq == 'Adhoc' and float(Header_tot_sell_price) != float(sum(sell_price_lst)):
            Quote.Messages.Add(Translation.Get('Adjust the milestone data in commercial info tab.'))
        elif r_count > 0:
            Quote.Messages.Add(Translation.Get('Please review the data in milestone table. Blank rows are not allowed.'))
        elif Cashflow_Health == 'Out of Balance':
            approvalMethod = Quote.GetCustomField('SC_CF_FIN_APPROVAL_METHOD').Content
            if approvalMethod == 'eGap':
                Quote.Messages.Add(Translation.Get('Cashflow is Out of Balance'))
            else:
                breakWorkflow = False
        elif Header_tot_sell_price == 0:
            Quote.Messages.Add(Translation.Get('Product with zero price is not allowed'))
        elif Check_Prod_Config_Status == False:
            Quote.Messages.Add(Translation.Get('Please complete Product configuration before requesting for approval '))
        elif is_Extension == 'True':
            if Extension_Func(Quote) == 1 :
                breakWorkflow = False
        if escalation_validation_lst:
            Quote.Messages.Add("For item : '{}', Escalation % for Other cost details should not be less than 5%".format(str(", ".join(escalation_validation_lst))))
        if breakWorkflow:
            WorkflowContext.BreakWorkflowExecution = True