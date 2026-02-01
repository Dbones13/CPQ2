from CPQ_SF_SC_Modules import CL_SC_Modules
class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None,Session)
#RolesList   = ['GSM Contract Manager - LSS','GSM ISA Manager - LSS','GSM Regional Contract Manager - LSS','GSM Field Service Manager - LSS','GSM Service Business Leader - LSS','GSM Renewal Specialist - LSS']
Opp_ID      = Quote.GetCustomField("CPQ_SF_OPPORTUNITY_ID").Content
Trace.Write(str(Opp_ID))
if Quote.GetCustomField("Quote Type").Content=="Contract Renewal":
    table = Quote.QuoteTables['SC_SFDC_Data_QuoteTable']
    column='Role'
    #table.GetColumnByName(column).AccessLevel = table.AccessLevel.ToString()
    table.GetColumnByName('Role').AccessLevel.ToString()
    ab=table.GetColumnByName('Role').DataType.GetType()
    Trace.Write("ab "+str(ab))
    resp = class_contact_modules.get_RenewalTeamRoles_Data(Opp_ID)
elif Quote.GetCustomField("Quote Type").Content=="Contract New":
	resp = class_contact_modules.get_TeamRoles_Data(Opp_ID)
else:
    resp = class_contact_modules.get_TeamRoles_Data(Opp_ID)
#Trace.Write(str(resp))
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
                    Trace.Write(newRow["Role"])
                    #newRow["Role1"]=record["Team_role__c"]
                    Trace.Write("Lahu>>>>>>>>>>>>>>>"+str(record["Team_role__c"]))
            newRow["Name"] = userData["Name"]
            newRow['Contact_Number'] = userData["Phone"]
            newRow['Email'] = userData["Email"]
            newRow['SFDC_ID'] = userData["Id"]
            if Quote.GetCustomField('Quote Type').Content in ['Contract New']:
            	newRow['Manager_Email'] = userData["Manager"]["Email"] if str(userData["Manager"]) else ''
    if Quote.GetCustomField("Quote Type").Content=="Contract Renewal":
        table = Quote.QuoteTables['SC_SFDC_Data_QuoteTable']
        column='Role'
        table.GetColumnByName(column).AccessLevel = table.AccessLevel.ReadOnly
    elif Quote.GetCustomField("Quote Type").Content=="Contract New" and Quote.OrderStatus.Name not in ['Preparing']:
        #populateQuoteTable(resp)
        Trace.Write('True')
        table = Quote.QuoteTables['SC_SFDC_Data_QuoteTable']
        column='Role'
        table.GetColumnByName(column).AccessLevel = table.AccessLevel.ReadOnly
    for row in userTable.Rows:
        for key,val in dictR.items():
            #Trace.Write(key + val)
            if row['Name'] == key:
                row['Role'] = val
                #Trace.Write(row['Role'])
       
    userTable.Save()
           

populateQuoteTable(resp)