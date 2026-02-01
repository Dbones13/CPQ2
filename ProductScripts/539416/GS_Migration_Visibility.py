if Product.ParseString("<*CTX( Product.RootProduct.SystemId )*>") == 'Migration2_cpq':
	def get_container(containerName):
		return Product.GetContainerByName(containerName)

	def hide_column(container, Column):
		Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(container, Column))
		Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set() )*>'.format(container, Column))

	def show_column(container, Column):
		Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(container, Column))

	def hide_attribute(attributename):
		for i in attributename.split(','):
			Product.DisallowAttr(i.strip())

	def show_attribute(attributename):
		for i in attributename.split(','):
			if not GetAttributePermission(i.strip()):
				Product.AllowAttr(i.strip())
		
	def update_read_only(attrname):
		Product.Attr(attrname).Access = AttributeAccess.ReadOnly

	def update_editable(attrname):
		Product.Attr(attrname).Access = AttributeAccess.Editable
		
	def GetColumnPermission(container, columnName):
		baseString = '<*CTX( Container({}).Column({}).GetPermission() )*>'
		return Product.ParseString(baseString.format(container, columnName))

	def GetAttributePermission(name):
		return Product.Attr(name).Allowed

	scope = Product.Attr('Scope').GetValue()
	msid_scope = scope if scope else Session["Scope"]
	prd_name = Product.Name

	if prd_name == '3rd Party PLC to ControlEdge PLC/UOC':
		
		Product.Attr('MIgration_Scope_Choices').SelectDisplayValue(msid_scope)
		

	Session["ProductName"] = Session["ProductName"] if Session["ProductName"] else []
	sessionval = Session["ProductName"]
	if prd_name not in sessionval:
		sessionval.append(prd_name)

	Tabinformation = SqlHelper.GetList("SELECT * FROM CONTAINER_HIDE_SHOW(NOLOCK) WHERE Tab = '{}' ".format(prd_name))

	attributeValue = ''
	attribute = ""
	attribute1 =''
	attributeValue1 =''
	for tab_info in Tabinformation:
		if tab_info.show_container and tab_info.AttributeName:
			cont_val = get_container(tab_info.show_container)
			if cont_val.Rows.Count > 0:
				rows = cont_val.Rows[0]
				attributeValue = str(rows[tab_info.AttributeName]).lower()

			else:
				attributeValue = None
			visiblerows = tab_info.CompatibleOnlyWith

		elif tab_info.show_container == '' and tab_info.AttributeName and tab_info.AttributeName != 'MSID_Current_Experion_Release':
			attributeValue = Product.Attr(tab_info.AttributeName).GetValue().lower()
		elif tab_info.show_container == '' and tab_info.AttributeName and tab_info.AttributeName == 'MSID_Current_Experion_Release':
			attributeValue = (Product.Attr('MSID_Current_Experion_Release').GetValue() or Session["MSID_Current_Experion_Release"]).lower()
		
		if tab_info.Container1 != '' and tab_info.Question1:
			Container1 =  get_container(tab_info.Container1)
			if Container1.Rows.Count > 0:
				rows1 = Container1.Rows[0]
				attributeValue1 = str(rows1[tab_info.Question1]).lower()

		elif tab_info.Container1 == '' and tab_info.Question1 and tab_info.Question1 != 'MSID_Future_Experion_Release' :
			attributeValue1 = Product.Attr(tab_info.Question1).GetValue().lower()

		elif tab_info.Container1 == '' and tab_info.Question1 and tab_info.Question1 == 'MSID_Future_Experion_Release' :
			attributeValue1 = (Product.Attr('MSID_Future_Experion_Release').GetValue() or Session["MSID_Future_Experion_Release"]).lower()
		
		flag = tab_info.FLAG
		isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
		if isR2Qquote:
			if Product.GetContainerByName('OPM_Node_Configuration') and Product.GetContainerByName('OPM_Node_Configuration').Rows.Count > 0:
				label = Product.GetContainerByName('OPM_Node_Configuration').Rows[0]
				label.GetColumnByName('OPM_No_of_ACET_Servers_LCN_Connected').HeaderLabel = "Number of ACET/EAPP Servers LCN Connected (0 - 100)"
			if tab_info.CompatibleOnlyWith in ['OPM_No_of_EAPP_Servers_LCN_Connected']:
				flag = 'H'
			'''if tab_info.CompatibleOnlyWith in ['TPS_EX_Non_Reduntant_Conversion_ESVT','TPS_EX_Redundant_Conversion_ESVT']:
				flag = 'V'
				non_Redundant_Conversation = Product.Attr('TPS_EX_Non_Reduntant_Conversion_ESVT').GetValue()
				Redundant_Conversation = Product.Attr('TPS_EX_Redundant_Conversion_ESVT').GetValue()
				if ((non_Redundant_Conversation == "Yes" and tab_info.CompatibleOnlyWith in ['TPS_EX_Redundant_Conversion_ESVT'])):
					flag = 'H'
				elif(Redundant_Conversation =='Yes' and tab_info.CompatibleOnlyWith in ['TPS_EX_Non_Reduntant_Conversion_ESVT']):
						flag = 'H'
				if non_Redundant_Conversation == "":
					Product.Attr('TPS_EX_Non_Reduntant_Conversion_ESVT').SelectDisplayValue('No')
				elif Redundant_Conversation =='':
					Product.Attr('TPS_EX_Redundant_Conversion_ESVT').SelectDisplayValue('No')'''
		scope_lst = [i.strip() for i in (tab_info.SCOPE).split(',')]
		scope_flag = True if msid_scope in scope_lst else False
		answer_list = [i.strip().lower() for i in (tab_info.DisplayIfAnySelected).split(',')]
		answer_list1 = [i.strip().lower() for i in (tab_info.Answer1).split(',')]
		
		

		if (tab_info.AttributeName and tab_info.Question1  and attributeValue1 in answer_list1  and attributeValue in answer_list and tab_info.HIDE_CONTAINER and tab_info.show_container and scope_flag):
			if flag == 'H':
				hide_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)
			elif flag == 'V' and GetColumnPermission(tab_info.HIDE_CONTAINER, tab_info.CompatibleOnlyWith) != 'Editable':
				show_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)

		if (tab_info.AttributeName and tab_info.Question1  and attributeValue1 in answer_list1  and attributeValue in answer_list  and not tab_info.HIDE_CONTAINER and tab_info.show_container and scope_flag):
			if flag == 'H':
				hide_attribute(tab_info.CompatibleOnlyWith)
			elif flag == 'V':
				show_attribute(tab_info.CompatibleOnlyWith)

		if (tab_info.AttributeName and attributeValue in answer_list and not tab_info.HIDE_CONTAINER and tab_info.show_container and scope_flag and tab_info.Question1 == '' ):
			if flag == 'V':
				show_attribute(tab_info.CompatibleOnlyWith)
			elif flag == 'H':
				hide_attribute(tab_info.CompatibleOnlyWith)
				
		if (tab_info.AttributeName and tab_info.Question1  and attributeValue1 in answer_list1  and attributeValue in answer_list and not tab_info.HIDE_CONTAINER and not tab_info.show_container and scope_flag):
			if flag == 'H':
				hide_attribute(tab_info.CompatibleOnlyWith)
			elif flag == 'V':
				show_attribute(tab_info.CompatibleOnlyWith)
		if (tab_info.AttributeName and tab_info.Question1  and attributeValue1 in answer_list1  and attributeValue in answer_list and  tab_info.HIDE_CONTAINER and not tab_info.show_container and scope_flag):
			if flag == 'H':
				hide_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)
			elif flag == 'V' and GetColumnPermission(tab_info.HIDE_CONTAINER, tab_info.CompatibleOnlyWith) != 'Editable':
				show_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)

		if (tab_info.AttributeName and attributeValue in answer_list and tab_info.HIDE_CONTAINER and tab_info.show_container and scope_flag and tab_info.Question1 ==''):
			if flag == 'H':
				hide_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)
			elif flag == 'V' and GetColumnPermission(tab_info.HIDE_CONTAINER, tab_info.CompatibleOnlyWith) != 'Editable':
				show_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)

		if (tab_info.AttributeName and attributeValue in answer_list and tab_info.HIDE_CONTAINER and not tab_info.show_container and scope_flag and tab_info.Question1 ==''):
			
			if flag == 'H':
				hide_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)
			elif flag == 'V' and GetColumnPermission(tab_info.HIDE_CONTAINER, tab_info.CompatibleOnlyWith) != 'Editable':
				show_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)

		elif (tab_info.AttributeName and attributeValue in answer_list and not tab_info.HIDE_CONTAINER and tab_info.show_container and scope_flag and  tab_info.Question1 == '' ):
			if flag == 'V':
				show_attribute(tab_info.CompatibleOnlyWith)
			elif flag == 'H':
				hide_attribute(tab_info.CompatibleOnlyWith)

		if (tab_info.AttributeName and attributeValue in answer_list and not tab_info.HIDE_CONTAINER and not tab_info.show_container and scope_flag and tab_info.Question1 == '' ):
			if flag == 'V':
				show_attribute(tab_info.CompatibleOnlyWith)
			elif flag == 'H':
				hide_attribute(tab_info.CompatibleOnlyWith)
		
		if (tab_info.AttributeName == '' and not tab_info.HIDE_CONTAINER and not tab_info.show_container and scope_flag and tab_info.Question1 == ''  ):
			if flag == 'H':
				hide_attribute(tab_info.CompatibleOnlyWith)
			elif flag == 'V':
				show_attribute(tab_info.CompatibleOnlyWith)
		if (tab_info.AttributeName == '' and tab_info.HIDE_CONTAINER and not tab_info.show_container and scope_flag and tab_info.Question1 == '' ):
			if flag == 'H':
				hide_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)
			elif flag == 'V' and GetColumnPermission(tab_info.HIDE_CONTAINER, tab_info.CompatibleOnlyWith) != 'Editable':
				show_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)

		if attributeValue and (attributeValue.lower() in answer_list) and flag == "Editable" and scope_flag:
			update_editable(tab_info.CompatibleOnlyWith)
		elif attributeValue and (attributeValue.lower() in answer_list) and flag == "Readonly" and scope_flag:
			update_read_only(tab_info.CompatibleOnlyWith)
		elif (not tab_info.AttributeName and not tab_info.DisplayIfAnySelected and flag == "Hide" and scope_flag):
			hide_attribute(tab_info.CompatibleOnlyWith)
		Session["traceOnload"] = ''