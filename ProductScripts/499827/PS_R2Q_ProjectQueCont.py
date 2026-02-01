def updateProjectCont(containerDict):
	container = Product.GetContainerByName('CE_Project_Questions_Cont')
	try:
		if container.Rows.Count > 0:
			for row in container.Rows:
				for key, values in containerDict.items():
					if values and len(values) > 0 and values[0] is not None:
						for value in values[0]:
							if key == 'R2Q_Project_Questions_Cont':
								for col_name, col_value in value.items():
									ctx_string = ''
									if col_name == 'GES_Location':
										ctx_string = '<*CTX ( Container(CE_Project_Questions_Cont).Row(1).Column(GES_Location).Set("' + str(col_value) + '") )*>'
										row.GetColumnByName(col_name).SetAttributeValue(col_value)
									elif col_name == 'Languages':
										ctx_string = '<*CTX ( Container(CE_Project_Questions_Cont).Row(1).Column(Languages).Set("' + str(col_value) + '") )*>'
									elif col_name == 'Project Categorization':
										ctx_string = '<*CTX ( Container(CE_Project_Questions_Cont).Row(1).Column(Project Categorization).Set("' + str(col_value) + '") )*>'
										row.GetColumnByName(col_name).SetAttributeValue(col_value)
									elif col_name == 'Is HMI Engineering in Scope?':
										ctx_string = '<*CTX ( Container(CE_Project_Questions_Cont).Row(1).Column(Is HMI Engineering in Scope?).Set("' + str(col_value) + '") )*>'
									elif col_name == 'Estimated_Project_Value_Cost':
										row.SetColumnValue(col_name, '3')
										row.GetColumnByName(col_name).SetAttributeValue('$1M - $5M')
										#row[col_name] = '3'
									if ctx_string:
										Product.ParseString(ctx_string)
									else:
										row[col_name] = col_value
							if key == 'R2Q_Project_Questions_TAS_Cont':
								for col_name, col_value in value.items():
									if col_name == 'Type_of_TAS_System':
										ctx_string = '<*CTX ( Container(CE_Project_Questions_Cont).Row(1).Column(Type_of_Tas_System).Set("' + str(col_value) + '") )*>'
										Product.ParseString(ctx_string)
										row[col_name] = col_value
										row.GetColumnByName(col_name).SetAttributeValue(col_value)
										Product.Attr('R2Q_Type_of_TAS_System').SelectDisplayValue(col_value)
	except Exception as e:
		Log.Info("error in updateProjectCont function " +str(e))

def setcontainervalue(ctx_string,row,column_name,values):
	try:
		Product.ParseString(ctx_string)
		row[column_name] = str(values)
	except Exception as e:
		Trace.Write("Error in setcontainervalue function: " + str(e))
		row[column_name] = str(values)

def updatelaborCont(containerDict):    
	container_mappings = {
		'Labor_details_newexapnsion_cont2': {
			'Is Fieldbus Interface in Scope?': 'Is Fieldbus Interface in Scope',
			'Is Profibus Interface in Scope?': 'Is Profibus Interface in Scope',
			'Is EtherNet IP Interface in Scope?': 'Is EtherNet IP Interface in Scope',
			'Is Modbus Interface in Scope?': 'Is Modbus Interface in Scope',
			'Is OPC Interface in Scope?': 'Is OPC Interface in Scope',
			'Is HMI Engineering in Scope?': 'Is HMI Engineering in Scope'
		},
		'Labor_Details_New/Expansion_Cont': {
			'Labor_Loop_Drawings': 'Labor_Loop_Drawings',
			'Labor_Marshalling_Database': 'Labor_Marshalling_Database'
		},
		'ExpProject_Que_Right': {
			'Project Duration (in weeks)': 'Project Duration in weeks',
			'FAT Duration in weeks': 'FAT Duration in weeks'
		},
		'CE_SystemGroup_Cont' :{
			'Labor_Percentage_FAT': 'Labor_Percentage_FAT',
			'Labor_Loop_Drawings': 'Labor_Loop_Drawings',
			'Labor_Marshalling_Database': 'Labor_Marshalling_Database'
		}
	}

	try:
		for cont_name, attr_mapping in container_mappings.items():
			container = Product.GetContainerByName(cont_name)
			if container.Rows.Count > 0:
				for row in container.Rows:
					for key, values in containerDict.items():
						if values and len(values) > 0 and values[0] is not None:
							if key in attr_mapping:
								column_name = attr_mapping[key]
								#Log.Write('---column_name-' + str(attr_mapping[key]))
								ctx_string = '<*CTX ( Container("'+str(cont_name)+'").Row(1).Column("'+str(column_name)+'").Set("'+str(values)+'") )*>'
								#TagParserProduct.ParseString(ctx_string)
								if cont_name == 'CE_SystemGroup_Cont':
									if key != 'Labor_Percentage_FAT' or row['Labor_Percentage_FAT'] == '':
										#result = TagParserProduct.ParseString(ctx_string)
										setcontainervalue(ctx_string,row,column_name,values)
								else:
									setcontainervalue(ctx_string,row,column_name,values)
								#Log.Write('---ctx_string-' + str(ctx_string))
	except Exception as e:
		Log.Info("Error in updatelaborCont function: " + str(e))

def get_float_value(row, key):
	try:
		return float(row[key])
	except:
		return 0.0

def updateexperioncont():
	container = Product.GetContainerByName('CE_SystemGroup_Cont') #new and exp
	sum_modbus_nodes, sum_opc_nodes = 0,0
	CC_IP0101_qty = 0
	CC_PEIM01_qty = 0
	HMIValue = ''
	tas_system = Product.Attr('R2Q_Type_of_TAS_System').GetValue()
	system_Network = Product.Attr('Is System Network Engineering in Scope?').GetValue()
	modbus_scope = Product.Attr('Is Modbus Interface in Scope?').GetValue()
	AA=Product.GetContainerByName('CE_Project_Questions_Cont')
	for row in AA.Rows:
		HMIValue = row['Is HMI Engineering in Scope?']
	if container.Rows.Count > 0:
		for row in container.Rows:
			if '3rd Party Devices/Systems Interface (SCADA)' in row['Selected_Products']:
				system_cont = row.Product.GetContainerByName('CE_System_Cont') #system
				for rows in system_cont.Rows:
					if rows['Product Name'] ==  '3rd Party Devices/Systems Interface (SCADA)':
						scada_cont = rows.Product.GetContainerByName('Scada_CCR_Unit_Cont') #scada cont
						for row2 in scada_cont.Rows:
							ccr_cont1 = row2.Product.GetContainerByName('Modbus/OPC Interfaces')
							for row3 in ccr_cont1.Rows:
								sum_modbus_nodes += int(row3['Nodes']) if str(row3['Nodes']) else 0
							ccr_cont6 = row2.Product.GetContainerByName('OPC Application Instances')
							for row6 in ccr_cont6.Rows:
								sum_opc_nodes += int(row6['Nodes']) if str(row6['Nodes']) else 0
			if 'C300 System' in row['Selected_Products']:
				system_cont = row.Product.GetContainerByName('CE_System_Cont')
				for sys_row in system_cont.Rows:
					if sys_row['Product Name'] == 'C300 System':
						control_cont = sys_row.Product.GetContainerByName('Series_C_Control_Groups_Cont')
						for group_row in control_cont.Rows:
							part_summary = group_row.Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
							for part_row in part_summary.Rows:
								if part_row['PartNumber'] == 'CC-IP0101':
									CC_IP0101_qty = part_row['Part_Qty']
								elif part_row['PartNumber'] == 'CC-PEIM01':
									CC_PEIM01_qty = part_row['Part_Qty']

		for row in container.Rows:
			system_cont = row.Product.GetContainerByName('CE_System_Cont')
			for sys_row in system_cont.Rows:
				if sys_row['Product Name'] == 'Experion Enterprise System':
					sys_row.Product.Attr('Number of Profibus Interface Cards').AssignValue(str(CC_IP0101_qty))
					sys_row.Product.Attr('Number of EtherNet IP Interface Cards').AssignValue(str(CC_PEIM01_qty))
					sys_row.Product.Attr('Is HMI Engineering in Scope?').SelectDisplayValue(str(HMIValue))
					sys_row.Product.Attr('Is System Network Engineering in Scope?').SelectDisplayValue(str(system_Network))
					sys_row.Product.Attr('Is Modbus Interface in Scope?').SelectDisplayValue(str(modbus_scope))
				if sys_row['Product Name'] == 'HC900 System':
					sys_row['Type_of_TAS_System'] = tas_system
					sys_row.Product.Attr('R2Q_Type_of_TAS_System').SelectValue(str(tas_system))
					hc900_system = sys_row.Product.GetContainerByName('HC900_Cont')
					for row in hc900_system.Rows:
						row.Product.Attr('R2Q_Type_of_TAS_System').SelectValue(str(tas_system))
					

	cont = Product.GetContainerByName('Labor_details_newexapnsion_cont2')
	if cont.Rows.Count > 0:
		for rows in cont.Rows:
			for col in rows.Columns:
				if (col.Name == 'Is OPC Interface in Scope') and (sum_opc_nodes > 0):
					ctx_string = '<*CTX ( Container("Labor_details_newexapnsion_cont2").Row(1).Column("Is OPC Interface in Scope").Set("Yes") )*>'
					Product.ParseString(ctx_string)
				if (col.Name == 'Is Modbus Interface in Scope') and (sum_modbus_nodes > 0):
					ctx_string = '<*CTX ( Container("Labor_details_newexapnsion_cont2").Row(1).Column("Is Modbus Interface in Scope").Set("Yes") )*>'
					Product.ParseString(ctx_string)

saveAction = Quote.GetCustomField("R2Q_Save").Content
isR2QRequest = Quote.GetCustomField("isR2QRequest").Content
isR2Qquote = True if Quote.GetCustomField("R2QFlag").Content else False
if saveAction != 'Save' and isR2Qquote:
	dictdata = eval(Quote.GetGlobal('R2Qdata'))
	Log.Info("test dictdata =="+str(dictdata))
	if dictdata:
		Product.Attr('CE_Scope_Choices').SelectDisplayValue(dictdata.get('CE_Scope_Choices', ''))
		updateProjectCont(dictdata)
		updatelaborCont(dictdata)
	updateexperioncont()
	#ScriptExecutor.Execute('PS_Populate_PM_Labor_Price_Cost')