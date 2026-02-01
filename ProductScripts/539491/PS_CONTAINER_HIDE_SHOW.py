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

def disallow_attribute(attribute_name):
	Product.DisallowAttr(attribute_name)

def allow_attribute(attribute_name):
	Product.AllowAttr(attribute_name)

scope = Product.Attr('Scope').GetValue()
msid_scope = scope if scope else Session["Scope"]
prd_name = Product.Name
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
	elif tab_info.show_container == '' and tab_info.AttributeName :
		attributeValue = Product.Attr(tab_info.AttributeName).GetValue().lower()
	if tab_info.Container1 != '' and tab_info.Question1:
		Container1 =  get_container(tab_info.Container1)
		if Container1.Rows.Count > 0:
			rows1 = Container1.Rows[0]
			attributeValue1 = str(rows1[tab_info.Question1]).lower()
	elif tab_info.Container1 == '' and tab_info.Question1:
		attributeValue1 = Product.Attr(tab_info.Question1).GetValue().lower()
	flag = tab_info.FLAG
	scope_lst = [i.strip() for i in (tab_info.SCOPE).split(',')]
	scope_flag = True if msid_scope in scope_lst else False
	answer_list = [i.strip().lower() for i in (tab_info.DisplayIfAnySelected).split(',')]
	answer_list1 = [i.strip().lower() for i in (tab_info.Answer1).split(',')]
	if (tab_info.AttributeName and tab_info.Question1  and attributeValue1 in answer_list1  and attributeValue in answer_list and tab_info.HIDE_CONTAINER and tab_info.show_container and scope_flag):
		if flag == 'H':
			hide_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)
	if (tab_info.AttributeName and tab_info.Question1  and attributeValue1 in answer_list1  and attributeValue in answer_list  and not tab_info.HIDE_CONTAINER and tab_info.show_container and scope_flag):
		if flag == 'H':
			hide_attribute(tab_info.CompatibleOnlyWith)
	if (tab_info.AttributeName and attributeValue in answer_list and not tab_info.HIDE_CONTAINER and tab_info.show_container and scope_flag and tab_info.Question1 == '' ):
		if flag == 'H':
			hide_attribute(tab_info.CompatibleOnlyWith)
	if (tab_info.AttributeName and tab_info.Question1  and attributeValue1 in answer_list1  and attributeValue in answer_list and not tab_info.HIDE_CONTAINER and not tab_info.show_container and scope_flag):
		if flag == 'H':
			hide_attribute(tab_info.CompatibleOnlyWith)
	if (tab_info.AttributeName and tab_info.Question1  and attributeValue1 in answer_list1  and attributeValue in answer_list and  tab_info.HIDE_CONTAINER and not tab_info.show_container and scope_flag):
		if flag == 'H':
			hide_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)
	if (tab_info.AttributeName and attributeValue in answer_list and tab_info.HIDE_CONTAINER and tab_info.show_container and scope_flag and tab_info.Question1 ==''):
		if flag == 'H':
			hide_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)
	if (tab_info.AttributeName and attributeValue in answer_list and tab_info.HIDE_CONTAINER and not tab_info.show_container and scope_flag and tab_info.Question1 ==''):
		Trace.Write("hidecolumn"+str(tab_info.HIDE_CONTAINER)+"compatible"+str(tab_info.CompatibleOnlyWith)+"attributeValue"+str(attributeValue)+"answer_list"+str(answer_list))
		if flag == 'H':
			hide_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)
	elif (tab_info.AttributeName and attributeValue in answer_list and not tab_info.HIDE_CONTAINER and tab_info.show_container and scope_flag and  tab_info.Question1 == '' ):
		if flag == 'H':
			hide_attribute(tab_info.CompatibleOnlyWith)
	if (tab_info.AttributeName and attributeValue in answer_list and not tab_info.HIDE_CONTAINER and not tab_info.show_container and scope_flag and tab_info.Question1 == '' ):
		if flag == 'H':
			hide_attribute(tab_info.CompatibleOnlyWith)
	if (tab_info.AttributeName == '' and not tab_info.HIDE_CONTAINER and not tab_info.show_container and scope_flag and tab_info.Question1 == ''  ):
		if flag == 'H':
			hide_attribute(tab_info.CompatibleOnlyWith)	
	if (tab_info.AttributeName == '' and tab_info.HIDE_CONTAINER and not tab_info.show_container and scope_flag and tab_info.Question1 == '' ):
		Trace.Write("hide_1"+str(tab_info.HIDE_CONTAINER)+"compatible"+str(tab_info.CompatibleOnlyWith))
		if flag == 'H':
			hide_column(tab_info.HIDE_CONTAINER,tab_info.CompatibleOnlyWith)
#PS_HideUOC_Attr 
'''if not scope:
	Product.Attr('Scope').AssignValue(msid_scope)
value_list = []
PLC_container = get_container('LSS_Configuration_for_Rockwell_transpose')
attr_visibility = [
	'LSS_Experion_UOC_PROFINET_Usage_Licenses', 'LSS_Total_Experion_UOC_Batch_Points', 
	'LSS_Total_Experion_UOC_Advanced_Batch_Points', 'LSS_Experion_UOC_Regulatory_Compliance_Points']
Listofatr = ['LSS_Number_of_hard_wired_Analog_Input_for_CE_UOC','LSS_Number_of_hard_wired_Analog_Output_for_CE_UOC',
'LSS_Number_of_hard_wired_Digital_Input_for_CE_UOC','LSS_Number_of_hard_wired_Digital_Output_for_CE_UOC']

PLC_attr_visibility = {
			'HW/SW': [
				'LSS_PLC_EPKS_Software_Release', 'LSS_PLC_Server_Redundancy', 'LSS_PLC_Total_Number_of_new_SCADA_point_License',
				'LSS_PLC_Total_Number_of_new_PCDI_License', 'LSS_PLC_Total_number_of_Panel_PCs_required'
			],
			'LABOR': [
				'LSS_PLC_Total_Number_of_new_SCADA_point_License', 'LSS_PLC_Total_Number_of_new_PCDI_License', 
				'LSS_PLC_Total_of_3rd_Party_PLC_via_Scada', 'LSS_PLC_Total_of_3rd_Party_PLC_via_PCDI', 
				'LSS_PLC_Total_of_3rd_Party_PLC_via_HPM_SI', 'LSS_PLC_Total_of_3rd_Party_PLC_via_EPLCG'
			],
			'HW/SW/LABOR': [
				'LSS_PLC_EPKS_Software_Release', 'LSS_PLC_Server_Redundancy', 'LSS_PLC_Total_Number_of_new_SCADA_point_License',
				'LSS_PLC_Total_Number_of_new_PCDI_License', 'LSS_PLC_Total_number_of_Panel_PCs_required', 
				'LSS_PLC_Total_of_3rd_Party_PLC_via_Scada', 'LSS_PLC_Total_of_3rd_Party_PLC_via_PCDI', 
				'LSS_PLC_Total_of_3rd_Party_PLC_via_HPM_SI', 'LSS_PLC_Total_of_3rd_Party_PLC_via_EPLCG'
			] 
		}
service_visible = [
				'LSS_Number_of_hard_wired_Analog_Input_for_CE_PLC', 'LSS_Number_of_hard_wired_Analog_Output_for_CE_PLC',
				'LSS_Number_of_hard_wired_Digital_Input_for_CE_PLC', 'LSS_Number_of_hard_wired_Digital_Output_for_CE_PLC',
				'LSS_Number_of_Soft_IO_for_CE_PLC', 'LSS_Are_you_using_existing_PLC_logicmigration_tool'
			]

for row in PLC_container.Rows:
	value_list.append(row['LSS_PLC_ControlEdge_PLC_UOC_or_vUOC'])
if 'UOC' in value_list or 'vUOC' in value_list or int(Product.Attr('LSS_PLC_Number_of_ControlEdge_UOC_vUOC_confi_req').GetValue()) > 0:
	for attr in attr_visibility:
		if not GetAttributePermission(attr):
			allow_attribute(attr)
	for servicesttribute in  Listofatr:
		if not GetAttributePermission(servicesttribute):
			allow_attribute(servicesttribute)
	for plc_service in  service_visible:
		if  GetAttributePermission(plc_service):
			disallow_attribute(plc_service)
			
else:
	for attr in attr_visibility:
		if GetAttributePermission(attr):
			disallow_attribute(attr)
	for servicesttribute in  Listofatr:
		if  GetAttributePermission(servicesttribute):
			disallow_attribute(servicesttribute)
	
if 'PLC' in value_list or int(Product.Attr('LSS_PLC_Number_of_ControlEdge_PLC_Groups_required').GetValue()) > 0:
	for i in PLC_attr_visibility[msid_scope]:
		if not GetAttributePermission(i):
			allow_attribute(i)
	for plc_visible in service_visible:
		if not GetAttributePermission(plc_visible):
			allow_attribute(plc_visible)
		
else:
	for i in PLC_attr_visibility[msid_scope]:
		if GetAttributePermission(i):
			disallow_attribute(i)
			
	disallow_attribute('LSS_PLC_Select_the_Experion_Node_to_be_installed')
	for plc_visible in service_visible:
		if GetAttributePermission(plc_visible):
			disallow_attribute(plc_visible)'''

def resetAtvQty(Product,AttrName):
	pvs=Product.Attr(AttrName).Values
	for av in pvs:
		if int(av.Quantity) == 0:
			av.IsSelected=False
			av.Quantity = 0

def setAtvQty(Product,AttrName,sv,qty):
	pvs=Product.Attr(AttrName).Values
	for av in pvs:
		if av.Display == sv:
			av.IsSelected=True
			av.Quantity=qty
			break

def popthirdPartSummary(Product):
	parts_to_update = {}
	base_media_delivery = Product.Attr('LSS_PLC_Base_Media_Delivery').GetValue()
	for row in Product.GetContainerByName('LSS_Configuration_for_Rockwell_transpose').Rows:
		controller_migrated = row['LSS_PLC_controllers_intend_to_migrate']
		sql_res = SqlHelper.GetList("Select * from LSS_3RD_PARTY_CONTROLEDGE_PLC_BOM where ('{}' = isPLC or '{}' = isUOC or '{}' = isvUOC) and (Operating_Temperature = '{}' or Operating_Temperature = '') and (Controller_Type = '{}' or Controller_Type = '') and (Power_Input_Type = '{}' or Power_Input_Type = '') and (Power_Supply_Type='{}' or Power_Supply_Type = '') and (Power_Status_Module_for_Redundant_Power_Supply='{}' or Power_Status_Module_for_Redundant_Power_Supply = '') and (Redundant_Controller_Physical_Separation_Required='{}' or Redundant_Controller_Physical_Separation_Required = '') and (IO_Rack_Type='{}'  or IO_Rack_Type = '') and (ControlEdge_PLC_System_Software_Release='{}' or ControlEdge_PLC_System_Software_Release = '') and (Base_Media_Delivery='{}' or Base_Media_Delivery = '') and (Ethernet_Switch_Type='{}' or Ethernet_Switch_Type = '') and (Ethernet_Switch_Ports='{}' or Ethernet_Switch_Ports = '') and (Network_Topology='{}' or Network_Topology = '') and (G3_Option_Ethernet_Switch='{}' or G3_Option_Ethernet_Switch = '')".format(row['LSS_PLC_ControlEdge_PLC_UOC_or_vUOC'],row['LSS_PLC_ControlEdge_PLC_UOC_or_vUOC'],row['LSS_PLC_ControlEdge_PLC_UOC_or_vUOC'],row['LSS_PLC_Operating_temp_for_Controller_Module'], row['LSS_PLC_Controller_Type'], row['LSS_PLC_Power_Input_Type'], row['LSS_PLC_Power_Supply_Type'], row['LSS_PLC_Power_Status_Module_for_Redundant_Pwr_Sply'], row['LSS_PLC_Redundant_Controller_Phy_Sep_Req'], row['LSS_PLC_IO_Rack_Type'], row['LSS_PLC_ControlEdge_PLC_System_Software_Release'], base_media_delivery,row['LSS_PLC_Ethernet_Switch_Type'], row['LSS_Ethernet_Switch_Ports'], row['LSS_PLC_Network_Topology'], "No" if row['LSS_PLC_G3_Option_Ethernet_Switch']=="" else row['LSS_PLC_G3_Option_Ethernet_Switch']))
		for i in sql_res:
			if i.Part_Number in ['SP-EMD170-ESD','SP-EMD171-ESD','SP-EMD172-ESD','SP-EMD174-ESD','SP-EMD170','SP-EMD171','SP-EMD172','SP-EMD174']:
				part_number1_sum=sum(parts_to_update.get('900CP1-0200',list()))
				part_number2_sum=sum(parts_to_update.get('900CP1-0300',list()))
				if part_number1_sum <= 0 and part_number2_sum <= 0:
					continue
			part_number = parts_to_update.get(i.Part_Number,list())
			try:
				part_number.append(int(i.Qty) * int(controller_migrated))
			except:
				if row[i.Qty] =='':
					part_number.append(0)
				else:
					part_number.append(int(row[i.Qty]) * int(controller_migrated))
			parts_to_update[i.Part_Number]= part_number

	if len(parts_to_update)>0:
		part_numbers_keys=[]
		for i in parts_to_update:
			if sum(parts_to_update[i]) != '0':
				part_numbers_keys.append(i)
		for r in part_numbers_keys:
			setAtvQty(Product, "PLC_UOC_BOM_Items", r, sum(parts_to_update[r]))
			Trace.Write("-r--"+str(r)+"--sum-"+str(parts_to_update[r]))
			'''lineItemContainer = Product.GetContainerByName("MSID_Added_Parts_Common_Container")
			lineItemContainer.Clear()
			for r in parts_to_update:
				Trace.Write("znndn"+str(lineItemContainer.Rows.Count))
			#if (parts_to_update[r]):
				part_number = r
				part_quantity = sum(parts_to_update[r])
				if part_quantity > 0:
					childRow = lineItemContainer.AddNewRow(False)
					childRow["PartNumber"] = part_number
					Trace.Write("lineItemContainer"+str(lineItemContainer.Rows.Count))
					childRow["Quantity"] = str(part_quantity)
					childRow.IsSelected = True
					if not childRow.Product:
						return'''
popthirdPartSummary(Product)
if Product.Attr('PLC_UOC_BOM_Items').GetValue() != '':
	resetAtvQty(Product,'PLC_UOC_BOM_Items')

contObj = Product.GetContainerByName('LSS_PLC_connection_transpose')
if contObj.Rows.Count > 0:
	for row in contObj.Rows:
		row.Product.Attr('MIgration_Scope_Choices').SelectDisplayValue(msid_scope)

contObj = Product.GetContainerByName('LSS_UOC_connection_transpose')
if contObj.Rows.Count > 0:
	for row in contObj.Rows:
		row.Product.Attr('MIgration_Scope_Choices').SelectDisplayValue(msid_scope)
Product.Attr('MIgration_Scope_Choices').SelectDisplayValue(msid_scope)


preSelectDict = {'LSS_PLC_EPKS_Software_Release': 'R511.x', 'LSS_PLC_Server_Redundancy': 'Redundant', 'LSS_Are_you_using_existing_PLC_logicmigration_tool': 'Yes', 'LSS_PLC_Select_the_Experion_Node_to_be_installed': 'Flex Station', 'LSS_TDI_Power_Supply_Cable_Length': '48 in', 'LSS_Front_only_TDI_Power_Supply_Cable_Length' : '48 in'}
preSelectDictkey = preSelectDict.Keys
for attribute in preSelectDictkey:
	if GetAttributePermission(attribute):
		attr = Product.Attr(attribute)
		if attr.Allowed == True and not attr.GetValue():
			attr.SelectValue(preSelectDict[attribute])
Product.Attr('Flag').SelectValue('1')
#Session["Product Loading"]=True
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
lss_rockwell_data = Product.GetContainerByName("LSS_Configuration_for_Rockwell_transpose").Rows
if Checkproduct == "Migration" and lss_rockwell_data.Count:
    for row in lss_rockwell_data:
        lss_power_supply_value = row.Product.Attr("LSS_PLC_Power_Supply_Type").GetValue()
        if not row.Product.Attr("LSS_PLC_Controller_Type").GetValue():
            row.Product.Attr("LSS_PLC_Controller_Type").SelectDisplayValue("Redundant")
        if lss_power_supply_value == "Redundant":
            if row.Product.Attr("LSS_PLC_Power_Status_Module_for_Redundant_Pwr_Sply").GetValue() in ("","None"):
                row.Product.Attr("LSS_PLC_Power_Status_Module_for_Redundant_Pwr_Sply").SelectDisplayValue("No")