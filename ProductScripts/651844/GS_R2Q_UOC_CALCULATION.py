container = Product.GetContainerByName('R2Q CE_System_Cont')
Node_count, sum_scada_points = 0, 0
sum_modbus_nodes, sum_opc_nodes = 0, 0
has_c300 = False
has_uoc = False
has_3rdparty = False

for prd in container.Rows:
	if 'R2Q 3rd Party Devices/Systems Interface (SCADA)' in prd['Selected_Products']:
		has_3rdparty = True
	if 'R2Q ControlEdge UOC System' in prd['Selected_Products']:
		has_uoc = True
	if 'R2Q C300 System' in prd['Selected_Products']:
		has_c300 = True

if has_3rdparty:
	for prd in container.Rows:
		if 'R2Q 3rd Party Devices/Systems Interface (SCADA)' in prd['Selected_Products']:
			scada_cont = prd.Product.GetContainerByName('Scada_CCR_Unit_Cont')
			if scada_cont.Rows.Count > 0:
				for row2 in scada_cont.Rows:
					ccr_cont1 = row2.Product.GetContainerByName('Modbus/OPC Interfaces')
					for row3 in ccr_cont1.Rows:
						Node_count += 1 if row3['Nodes'] or str(row3['SCADA Points']).isdigit() > 0 else 0
						sum_scada_points += int(row3['SCADA Points']) if str(row3['SCADA Points']).isdigit() else 0
						sum_modbus_nodes += int(row3['Nodes']) if str(row3['Nodes']) else 0
					ccr_cont6 = row2.Product.GetContainerByName('OPC Application Instances')
					for row6 in ccr_cont6.Rows:
						if 'Redirection Manager' not in row6['Third_Party_Devices_Systems_Interface_SCADA']:
							Node_count += 1 if row6['Nodes'] or str(row6['SCADA Points']).isdigit() > 0 else 0
						sum_opc_nodes += int(row6['Nodes']) if str(row6['Nodes']) else 0
					ccr_cont2 = row2.Product.GetContainerByName('IEC/DNP3 Interfaces')
					for row4 in ccr_cont2.Rows:
						Node_count += 1 if row4['Nodes'] or str(row4['SCADA Points']).isdigit() else 0
						sum_scada_points += int(row4['SCADA Points']) if str(row4['SCADA Points']).isdigit() else 0
					ccr_cont3 = row2.Product.GetContainerByName('Leak Detection System Interfaces')
					for row5 in ccr_cont3.Rows:
						Node_count += 1 if row5['Nodes'] or str(row5['SCADA Points']).isdigit() else 0
						sum_scada_points += int(row5['SCADA Points']) if str(row5['SCADA Points']).isdigit() else 0
					ccr_cont4 = row2.Product.GetContainerByName('Allen-Bradley/Siemens Interfaces')
					for row6 in ccr_cont4.Rows:
						Node_count += 1 if row6['Nodes'] or str(row6['SCADA Points']).isdigit() else 0
						sum_scada_points += int(row6['SCADA Points']) if str(row6['SCADA Points']).isdigit() else 0
					ccr_cont5 = row2.Product.GetContainerByName('Flow Computer Interfaces')
					for row7 in ccr_cont5.Rows:
						Node_count += 1 if row7['Nodes'] or str(row7['SCADA Points']).isdigit() else 0
						sum_scada_points += int(row7['SCADA Points']) if str(row7['SCADA Points']).isdigit() else 0
					#Log.Info("node count--- " + str(Node_count) + "----" + str(sum_scada_points))

for rows in container.Rows:

	if 'R2Q ControlEdge UOC System' in rows['Selected_Products']:
		UOC_cont = rows.Product.GetContainerByName('UOC_Labor_Details')
		if UOC_cont.Rows.Count > 0:
			for row in UOC_cont.Rows:
				if has_3rdparty and has_uoc and not has_c300:
					row['UOC_Num_SCADA_Node_Type']   = str(Node_count)
					row['UOC_Num_ThirdParty_SoftIO'] = str(sum_scada_points)
				else:
					row['UOC_Num_SCADA_Node_Type']   = '0'
					row['UOC_Num_ThirdParty_SoftIO'] = '0'
	if 'R2Q C300 System' in rows['Selected_Products']:
		if has_3rdparty and has_c300:
			rows.Product.Attr('Number_of_SCADA_Node_Types_for_C300').AssignValue(str(Node_count))
			rows.Product.Attr('Number_of_Third_Party_Soft_IO_(Serial/SCADA)').AssignValue(str(sum_scada_points))
		else:
			rows.Product.Attr('Number_of_SCADA_Node_Types_for_C300').AssignValue('0')
			rows.Product.Attr('Number_of_Third_Party_Soft_IO_(Serial/SCADA)').AssignValue('0')

cont = Product.GetContainerByName('Labor_details_newexapnsion_cont2')
if cont.Rows.Count > 0:
	for rows in cont.Rows:
		if sum_opc_nodes > 0:
			rows.SetColumnValue('Is OPC Interface in Scope', 'Yes')
			Product.Attr('Is OPC Interface in Scope?').SelectDisplayValue('Yes')
		if sum_modbus_nodes > 0:
			rows.SetColumnValue('Is Modbus Interface in Scope', 'Yes')
			Product.Attr('Is Modbus Interface in Scope?').SelectDisplayValue('Yes')
		Product.Attr('Labor_Loop_Drawings').AssignValue('Yes')

cont = Product.GetContainerByName('R2Q_Project_Questions_Cont')
if cont and cont.Rows:
	for row in cont.Rows:
		exe_year = row['Project_Execution_Year']
		if exe_year:
			Quote.GetCustomField("R2Q_PRJT_Execution_Year").Content = exe_year
		ges_location = row['GES_Location']
		if ges_location:
			Quote.SetGlobal('ExGesLocation', str(ges_location))