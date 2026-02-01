from CPQ_SF_SC_Modules import CL_SC_Modules
from GS_SC_ErrorMessages import MessageHandler
MsgHandler = MessageHandler(Quote)

class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None,Session)
is_extension = Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content
WhereCond = "Opportunity__c" if is_extension == 'True' else "Renewal_Opportunity__c"
Opp_ID      = Quote.GetCustomField("CPQ_SF_OPPORTUNITY_ID").Content
if Quote.GetCustomField("Quote Type").Content=="Contract Renewal":
    resp = class_contact_modules.get_RenewalTeamRoles_Data(Opp_ID,WhereCond)
elif Quote.GetCustomField("Quote Type").Content=="Contract New":
	resp = class_contact_modules.get_TeamRoles_Data(Opp_ID)

def populateQuoteTable(resp):

    userTable = Quote.QuoteTables['SC_SFDC_Data_QuoteTable']
    dictR = {}
    for row in userTable.Rows:
        dictR[row["Name"]] = row["Role"]
    userTable.Rows.Clear()
    if resp and "records" in resp:
        recordList = resp["records"]
        for record in recordList:
            userData = record["User__r"]
            newRow = userTable.AddNewRow()
            if Quote.GetCustomField('Quote Type').Content in ['Contract Renewal']:
                if str(record["Team_role__c"]) in ["GSM Contract Manager","GSM ISA Manager","GSM Service Business Leader","GSM Field Service Manager","GSM Regional Contract Manager","GSM Renewal Specialist","GSM GCC Contract Admin"]:
                    newRow["Role"]=record["Team_role__c"]
            newRow["Name"] = userData["Name"]
            newRow['Contact_Number'] = userData["Phone"]
            newRow['Email'] = userData["Email"]
            newRow['SFDC_ID'] = userData["Id"]
            newRow['Manager_Email'] = userData["Manager"]["Email"] if str(userData["Manager"]) else ''
    userTable.Save()
table = Quote.QuoteTables['SC_SFDC_Data_QuoteTable']
column='Role'
if Quote.GetCustomField('Quote Type').Content in ['Contract New']:
    empty=0
    for row in table.Rows:
        if row["Role"]!='':
            empty +=1
    if str(empty) =='0':
        populateQuoteTable(resp)
    mandatoryRoles = ['Contract Manager', 'ISA Manager', 'RSOM', 'SBD']
    Erro_msg = "Roles {} are mandatory selections.".format(', '.join(mandatoryRoles))
    kk = MsgHandler.AddMessage("Team_Details", "Error", Erro_msg, 2)
    if Quote.OrderStatus.Name not in ['Preparing']:
        table.GetColumnByName(column).AccessLevel = table.AccessLevel.ReadOnly
elif Quote.GetCustomField("Quote Type").Content=="Contract Renewal":
    populateQuoteTable(resp)
    table.GetColumnByName(column).AccessLevel = table.AccessLevel.ReadOnly
else:
    table.Rows.Clear()