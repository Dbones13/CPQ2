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
	except Exception as e:
		Log.Info("error in updateProjectCont function " +str(e))
		
def setcontainervalue(ctx_string,row,column_name,values):
	try:
		TagParserProduct.ParseString(ctx_string)
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
								ctx_string = ''
								column_name = attr_mapping[key]
								#Log.Write('---column_name-' + str(attr_mapping[key]))
								ctx_string = '<*CTX ( Container("'+str(cont_name)+'").Row(1).Column("'+str(column_name)+'").Set("'+str(values)+'") )*>'
								
								if cont_name == 'CE_SystemGroup_Cont':
									if key != 'Labor_Percentage_FAT' or row['Labor_Percentage_FAT'] == '':
										#result = TagParserProduct.ParseString(ctx_string)
										setcontainervalue(ctx_string,row,column_name,values)
										
									
								else:
									setcontainervalue(ctx_string,row,column_name,values)
									

	except Exception as e:
		Log.Info("Error in updatelaborCont function: " + str(e))


		

def get_float_value(row, key):
	try:
		return float(row[key])
	except:
		return 0.0

def updateexperioncont():
	

	cont = Product.GetContainerByName('Labor_details_newexapnsion_cont2')
	if cont.Rows.Count > 0:
		for rows in cont.Rows:
			for col in rows.Columns:
				if (col.Name == 'Is OPC Interface in Scope') and (sum_opc_nodes > 0):
					ctx_string = '<*CTX ( Container("Labor_details_newexapnsion_cont2").Row(1).Column("Is OPC Interface in Scope").Set("Yes") )*>'
					TagParserProduct.ParseString(ctx_string)
				if (col.Name == 'Is Modbus Interface in Scope') and (sum_modbus_nodes > 0):
					ctx_string = '<*CTX ( Container("Labor_details_newexapnsion_cont2").Row(1).Column("Is Modbus Interface in Scope").Set("Yes") )*>'
					TagParserProduct.ParseString(ctx_string)



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
#Product.ApplyRules()
	#ScriptExecutor.Execute('PS_Populate_PM_Labor_Price_Cost')