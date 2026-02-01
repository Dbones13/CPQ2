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

prd_name = Product.Name

containerAttributeDict = dict()

containerAttributeDict['OPM'] = ["OPM_Basic_Information", "OPM_Node_Configuration"]

for name in containerAttributeDict[Product.Name]:
	container = Product.GetContainerByName(name)
	if container is not None:
		if container.Rows.Count == 0:
			row = container.AddNewRow()
			for i in range(2):
				container.CopyRow(row.RowIndex)
	container.Calculate()

opmBasicInfoCon = get_container('OPM_Basic_Information')
for row in opmBasicInfoCon.Rows:
	row.GetColumnByName('OPM_RESS_Migration_in_scope').ReferencingAttribute.SelectDisplayValue("No")
	row.GetColumnByName('OPM_Migration_Scenario').SetAttributeValue('Off-Process Migration')
	row.GetColumnByName("OPM_Is_the_Experion_System_LCN_Connected").ReferencingAttribute.SelectDisplayValue("No")
	row.GetColumnByName('OPM_Is_this_is_a_Remote_Migration_Service_RMS').ReferencingAttribute.SelectDisplayValue('Yes')
	row.GetColumnByName('OPM_Does_the_customer_have_EBR_installed').SetAttributeValue('No')
	row.GetColumnByName('OPM_Is_this_is_migration_part_of_an_ELCN_migration').SetAttributeValue('No')
	row.GetColumnByName('OPM_Servers_and_Stations_HW_replace_needed').SetAttributeValue('No')
	row.GetColumnByName('OPM_If_AMT_Will_Not_Be_Used').ReferencingAttribute.SelectDisplayValue("No")
	break
#opmBasicInfoCon.Calculate()

nodeConfigurationCon = get_container('OPM_Node_Configuration')
for row in nodeConfigurationCon.Rows:
	row.SetColumnValue("OPM_No_of_Experion_Servers",'0')
	row.SetColumnValue("OPM_No_of_ACET_Servers_LCN_Connected",'0')
	row.SetColumnValue("OPM_No_of_EAPP_Servers_LCN_Connected",'0')
	row.SetColumnValue("OPM_No_of_EST_Rack_mount",'0')
	row.SetColumnValue("OPM_No_of_EST_Tower",'0')
	row.SetColumnValue("OPM_No_of_Other_Servers_to_be_migrated",'0')
	row.SetColumnValue("OPM_Qty_of_ESC_Rack_Mount",'0')
	row.SetColumnValue("OPM_Qty_of_ESC_Tower",'0')
	row.SetColumnValue("OPM_Qty_of_ESF_and_ES-CE_Rack_Mount",'0')
	row.SetColumnValue("OPM_Qty_of_ESF_and_ESCE_Tower",'0')
	row.SetColumnValue("OPM_Qty_of_RPS_and_Thin_Clients",'0')
	row.SetColumnValue("OPM_Qty_of_Series_C_Controllers",'0')
	row.SetColumnValue("OPM_Qty_of_Control_Firewalls_CF9s",'0')
	row.SetColumnValue("OPM_Qty_of_Fieldbus_Interface_Modules",'0')
	row.SetColumnValue("OPM_Qty_of_Profibus_Modules",'0')
	row.SetColumnValue("OPM_Qty_of_Series_C_IO_Modules_excluding_UIO",'0')
	row.SetColumnValue("OPM_Qty_of_UIO_UIO2_Modules",'0')
	break
#nodeConfigurationCon.Calculate()

scope = Product.Attr('Scope').GetValue()
msid_scope = scope if scope else Session['Scope']
Trace.Write("On Load_1"+str(msid_scope))
if True:
	Trace.Write("On Load")
	Tabinformation = SqlHelper.GetList("SELECT * FROM CONTAINER_HIDE_SHOW(NOLOCK) WHERE Tab = '{}' and 	AttributeName ='' ".format(prd_name))

	for tab_info in Tabinformation:
		scope_lst = [i.strip() for i in (tab_info.SCOPE).split(',')]

		scope_flag = True if msid_scope in scope_lst else False
		flag = tab_info.FLAG
		Trace.Write("testing_1"+str(msid_scope)+"test"+str(tab_info.SCOPE))
		if  tab_info.show_container and tab_info.HIDE_CONTAINER and scope_flag:
			if flag == 'H':
				hide_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)
				Trace.Write("test346_1::"+str(tab_info.CompatibleOnlyWith))
			elif flag == 'V' and GetColumnPermission(tab_info.show_container, tab_info.CompatibleOnlyWith) != 'Editable':
				show_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)
		elif  tab_info.show_container and not tab_info.HIDE_CONTAINER and scope_flag:
			if flag == 'H':
				hide_attribute(tab_info.CompatibleOnlyWith)
			elif flag == 'V' and not GetAttributePermission(tab_info.CompatibleOnlyWith):
				show_attribute(tab_info.CompatibleOnlyWith)

		elif not tab_info.show_container and tab_info.HIDE_CONTAINER and scope_flag:
			if flag == 'H':
				hide_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)
			elif flag == 'V' and GetColumnPermission(tab_info.show_container, tab_info.CompatibleOnlyWith) != 'Editable':
				Trace.Write("migrationcolumn"+str(tab_info.show_container)+"visiblecolumn"+str(tab_info.CompatibleOnlyWith))
				show_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)

		'''elif not tab_info.HIDE_CONTAINER and not scope_flag:
			if flag == 'H':
				show_attribute(tab_info.CompatibleOnlyWith)
			elif flag == 'V' :
				hide_attribute(tab_info.CompatibleOnlyWith)'''

		# if not tab_info.show_container and not scope_flag:
		# 	if flag == 'H':
		# 		show_attribute(tab_info.CompatibleOnlyWith)
		# 		Trace.Write("test346_3::"+str(tab_info.CompatibleOnlyWith))
		# 	elif flag == 'V' :
		# 		hide_attribute(tab_info.CompatibleOnlyWith)