Product.Attributes.GetByName('R2QRequest').AssignValue(str(Quote.GetCustomField("isR2QRequest").Content))
if Quote.GetCustomField('R2QFlag').Content == 'Yes' and Product.Name =="HCI Labor Config":
	Product.Attributes.GetByName('HCI_PHD_IsReports').AssignValue('False')
	if Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows.Count>0:
		inputt2 = Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows[0]
		if inputt2['Graphics and Reports'] == 'Yes':
			Product.Attributes.GetByName('HCI_PHD_IsReports').AssignValue('True')
			Product.AllowAttr('HCI_PHD_NewDisplaysforInsight')
			Product.AllowAttr('HCI_PHD_ExcelReports')
		else:
			Product.Attributes.GetByName('HCI_PHD_IsReports').AssignValue('False')
			Product.DisallowAttr('HCI_PHD_NewDisplaysforInsight')
			Product.DisallowAttr('HCI_PHD_ExcelReports')

if Product.Attributes.GetByName('R2QRequest').GetValue() == 'Yes':
	r1 = Product.ParseString('<*CTX( Container(HCI_PHD_Tech_Scope).Row(1).Column(Number of Collected Tags).Get )*>')
	r2 = Product.ParseString('<*CTX( Container(HCI_PHD_Tech_Scope).Row(2).Column(Number of Collected Tags).Get )*>')
	Trace.Write(str(r1)+'-----------R2Q Hide attributes----------------'+str(r2))
	if r1 and r2:
		tech_scope = int(r1) + int(r2)
		Product.Attributes.GetByName('PRD_Error').AssignValue('')
		if tech_scope > 2000000:
			Product.Attributes.GetByName('PRD_Error').AssignValue('True')
			#Product.ErrorMessages.Add("The PHD Tech Scope, It can't be greater than 2M")
	Product.Attributes.GetByName('AR_HCI_No_FO_ENG').SelectDisplayValue('1')
	'''Product.Attributes.GetByName('AR_HCI_No_GES_ENG').SelectDisplayValue('None')
	if Product.Attributes.GetByName('HCI_PHD_GES_Location').GetValue():'''
	#Product.Attributes.GetByName('AR_HCI_No_GES_ENG').SelectDisplayValue('1')
	Product.Attr('AR_HCI_No_FO_ENG').Access = AttributeAccess.Hidden
	Product.Attr('AR_HCI_No_GES_ENG').Access = AttributeAccess.Hidden
	Product.Attr('HCI_PHD_GES_Location').Access = AttributeAccess.Hidden
	Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(ReadOnly) )*>'.format('HCI_PHD_Tech_Scope','System to be interfaced to'))
	hideColumns = ['Activity Type','Participation','Number of trips per engineer','Hours per trip']
	for cols in hideColumns:
		Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('HCI_PHD_Fo_Eng',str(cols)))

	hideColumns = ['User Requirements','Project Set Up','KOM type']
	for cols in hideColumns:
		Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('HCI_Labor_common_prj_input1',str(cols)))
	Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('HCI_Labor_common_prj_input2','Site Specific Documentation'))
	projinputs = {'AR_HCI_PHD_ProjectInputs1':['Scope of Work','Material Ordering','Staging Area Hardware and LAN Setup','Build and Configure'], 'AR_HCI_PHD_ProjectInputs2':['Post-Go-Live Activities','Post Delivery Support','USM Implementation','Uniformance Insight Implementation','Travel Time','Number of engineers traveling','Number of trips per engineer','Hours per trip']}
	for i in projinputs.keys():
		for col in projinputs[i]:
			Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(i,col))
	if Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows.Count>0:
		inputt2 = Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows[0]
		if inputt2['Graphics and Reports'] == 'No':
			Product.Attributes.GetByName('HCI_PHD_IsReports').AssignValue('False')
			Product.DisallowAttr('HCI_PHD_NewDisplaysforInsight')
			Product.DisallowAttr('HCI_PHD_ExcelReports')
		else:
			Product.Attributes.GetByName('HCI_PHD_IsReports').AssignValue('True')
			Product.AllowAttr('HCI_PHD_NewDisplaysforInsight')
			Product.AllowAttr('HCI_PHD_ExcelReports')
	if Product.Attributes.GetByName('HCI_PHD_GES_Location').GetValue():
		Product.AllowAttr('HCI_PHD_GES_Eng')
	else:
		Product.DisallowAttr('HCI_PHD_GES_Eng')