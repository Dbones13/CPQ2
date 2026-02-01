def get_container(name):
	return Product.GetContainerByName(name)

def hide_attribute(attribute_name):
	Product.DisallowAttr(attribute_name)

def show_attribute(attribute_name):
	Product.AllowAttr(attribute_name)

def GetAttributePermission(name):
	return Product.Attr(name).Allowed

Session['3rd_party_BOM'] = Product.Attr('PLC_UOC_BOM_Items').GetValue()
msid_scope = Product.Attr('Scope').GetValue()
value_list = []
PLC_container = get_container('LSS_Configuration_for_Rockwell_transpose')
attr_visibility = [
	'LSS_Experion_UOC_PROFINET_Usage_Licenses', 'LSS_Total_Experion_UOC_Batch_Points', 
	'LSS_Total_Experion_UOC_Advanced_Batch_Points', 'LSS_Experion_UOC_Regulatory_Compliance_Points']


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

		

for row in PLC_container.Rows:
	value_list.append(row['LSS_PLC_ControlEdge_PLC_UOC_or_vUOC'])
if 'UOC' in value_list or 'vUOC' in value_list or int(Product.Attr('LSS_PLC_Number_of_ControlEdge_UOC_vUOC_confi_req').GetValue()) > 0:
	for attr in attr_visibility:
		if not GetAttributePermission(attr):
			show_attribute(attr)
	
	
			
else:
	for attr in attr_visibility:
		if GetAttributePermission(attr):
			hide_attribute(attr)
	
	


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
preSelectDict = {'LSS_PLC_EPKS_Software_Release': 'R511.x', 'LSS_PLC_Server_Redundancy': 'Redundant', 'LSS_Are_you_using_existing_PLC_logicmigration_tool': 'Yes', 'LSS_PLC_Select_the_Experion_Node_to_be_installed': 'Flex Station', 'LSS_TDI_Power_Supply_Cable_Length': '48 in', 'LSS_Front_only_TDI_Power_Supply_Cable_Length' : '48 in'}

preSelectDictkey = preSelectDict.Keys

for attribute in preSelectDictkey:

    attr = Product.Attr(attribute)

    if attr.Allowed == True and not attr.GetValue():

        attr.SelectValue(preSelectDict[attribute])
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
		#for i in Product.GetContainerByName("CONT_MSID_SUBPRD").Rows:
		for r in part_numbers_keys:
			setAtvQty(Product, "PLC_UOC_BOM_Items", r, sum(parts_to_update[r]))
popthirdPartSummary(Product)
if Product.Attr('PLC_UOC_BOM_Items').GetValue() != '':
	resetAtvQty(Product,'PLC_UOC_BOM_Items')