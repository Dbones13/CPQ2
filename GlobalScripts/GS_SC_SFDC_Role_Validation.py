## updated the code for Log error.##
def SC_SFDC_Role_Validation(Quote):
	Quote_Type = Quote.GetCustomField("Quote Type").Content
	from GS_SC_ErrorMessages import MessageHandler
	MsgHandler = MessageHandler(Quote)
	ISA= "ISA Manager"
	if Quote_Type in ('Contract New'):
		mandatoryRoles=[]
		userTable = Quote.QuoteTables['SC_SFDC_Data_QuoteTable']
		Quote.QuoteTables['SC_SFDC_Data_QuoteTable'].Save()
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
		if Quote_Type == 'Contract New':
			mandatoryRoles = ['Contract Manager', 'ISA Manager', 'RSOM', 'SBD']
		if Agreement_type != "ISA" and ISA in mandatoryRoles:
				mandatoryRoles.remove("ISA Manager")

		for row in userTable.Rows:
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
		if mandatoryRoles:
			Error_msg = "Roles {} are mandatory selections.".format(', '.join(mandatoryRoles))
			kk = MsgHandler.AddMessage("Team_Details", "Error", Error_msg, 1)
			cc=Quote.GetCustomField('SC_CF_Error_Msg').Content
			Trace.Write('Jagrutitest'+cc)
		else:
			MsgHandler.DeleteMessage("Team_Details", 1)
		if countFlag == 1:
			Error_msg = "Selected role already assigned to a different user. Please select a different role."
			kk = MsgHandler.AddMessage("Team_Details", "Error", Error_msg, 2) 
			#cc=Quote.GetCustomField('SC_CF_Error_Msg').Content
		else:
			MsgHandler.DeleteMessage("Team_Details", 2)
	##################################
	#added as a part of CXCPQ-78706
	##################################
	table = Quote.QuoteTables['SC_SFDC_Data_QuoteTable']
	if (Quote_Type=="Contract New" and Quote.OrderStatus.Name not in ['Preparing']) or (Quote_Type=="Contract Renewal"):
		table.GetColumnByName("Role").AccessLevel = table.AccessLevel.ReadOnly
	elif Quote_Type=="Contract New" and Quote.OrderStatus.Name in ['Preparing']:
		table.GetColumnByName("Role").AccessLevel = table.AccessLevel.Editable