def int_handler(val):
	return int(val or 0)

def populatePLCproposal(Quote, PLCItem, guid):
	sys_columns = sys_columns = {'PLC_Common_Questions_Cont':['PLC_IO_Spare', 'PLC_IO_Slot_Spare'], 'PLC_Labour_Details':['PLC_Marshalling_Cabinet_Cont']}
	sys_columns_seq = ['PLC_IO_Spare', 'PLC_IO_Slot_Spare', 'PLC_Marshalling_Cabinet_Cont']

	cabinets_columns = ['Cabinet_cnt']
	cabinet_columns_seq = ['Cabinet_cnt']

	cg_column = {'PLC_CG_Cabinet_Cont':['PLC_Cabinet_Spare_Space','PLC_Integrated_Marshalling_Cabinet'], 'PLC_CG_Other_IO_Cont':['PLC_Universal_Analog_Input8','PLC_Universal_Analog_Input8_TCRTDmVOhm','PLC_Analog_Input16','PLC_Analog_Output4','PLC_Analog_Output8_Internal','PLC_Analog_Output8_External','PLC_Pulse_Input_Freq_Input4','PLC_Quadrature_Input','PLC_Pulse_Output4','PLC_Digital_Input32','PLC_Digital_Input16_120240VAC','PLC_Digital_Input_Contact_Type16','PLC_Digital_Input16_125VDC','PLC_Digital_Output32','PLC_Digital_Output8','PLC_Digital_Output_Relay8'], 'PLC_CG_UIO_Cont':['PLC_AI_Points','PLC_AI_HART_Points','PLC_AO_100_250','PLC_AO_250_499','PLC_AO_500','PLC_AO_HART_100_250','PLC_AO_HART_250_499','PLC_AO_HART_500','PLC_DI_Points','PLC_DO_10_250','PLC_DO_250_500']}

	cg_columns_seq = ['PLC_AI_Points', 'PLC_AI_Points_R', 'PLC_AI_HART_Points', 'PLC_AO', 'PLC_AO_R', 'PLC_AO_HART', 'PLC_Universal', 'PLC_Analog_Input16', 'PLC_Analog_Output4', 'PLC_Analog_Output8_Internal', 'PLC_Analog_Output8_External', 'PLC_DI_Points', 'PLC_DI_Points_R', 'PLC_DO_Points', 'PLC_DO_Points_R', 'PLC_Digital_Input32','PLC_DI_Points_16', 'PLC_Digital_Input_Contact_Type16', 'PLC_Pulse_Input_Freq_Input4', 'PLC_Quadrature_Input', 'PLC_Pulse_Output4', 'PLC_Digital_Output32', 'PLC_Digital_Output8', 'PLC_Digital_Output_Relay8','PLC_AI_HART_Points_R','PLC_AO_HART_R', 'PLC_Cabinet_Spare_Space', 'PLC_Integrated_Marshalling_Cabinet']

	rg_columns = {'PLC_RG_Other_IO_Cont':['PLC_Universal_Analog_Input8','PLC_Universal_Analog_Input8_TCRTDmVOhm','PLC_Analog_Input16','PLC_Analog_Output4','PLC_Analog_Output8_Internal','PLC_Analog_Output8_External','PLC_Pulse_Input_Freq_Input4','PLC_Quadrature_Input','PLC_Pulse_Output4','PLC_Digital_Input32','PLC_Digital_Input16_120240VAC','PLC_Digital_Input_Contact_Type16','PLC_Digital_Input16_125VDC','PLC_Digital_Output32','PLC_Digital_Output8','PLC_Digital_Output_Relay8'], 'PLC_RG_UIO_Cont':['PLC_AI_Points','PLC_AI_HART_Points','PLC_AO_100_250','PLC_AO_250_499','PLC_AO_500','PLC_AO_HART_100_250','PLC_AO_HART_250_499','PLC_AO_HART_500','PLC_DI_Points','PLC_DO_10_250','PLC_DO_250_500']}

	rg_columns_seq = ['PLC_AI_Points', 'PLC_AI_Points_R', 'PLC_AI_HART_Points', 'PLC_AO', 'PLC_AO_R', 'PLC_AO_HART', 'PLC_Universal', 'PLC_Analog_Input16', 'PLC_Analog_Output4', 'PLC_Analog_Output8_Internal', 'PLC_Analog_Output8_External', 'PLC_DI_Points', 'PLC_DI_Points_R', 'PLC_DO_Points', 'PLC_DO_Points_R', 'PLC_Digital_Input32', 'PLC_DI_Points_16', 'PLC_Digital_Input_Contact_Type16', 'PLC_Pulse_Input_Freq_Input4', 'PLC_Quadrature_Input', 'PLC_Pulse_Output4', 'PLC_Digital_Output32', 'PLC_Digital_Output8', 'PLC_Digital_Output_Relay8','PLC_AI_HART_Points_R','PLC_AO_HART_R']

	QT_Table = Quote.QuoteTables["PAS_Document_Data"]
	#QT_Table.Rows.Clear()
	CGn = 0
	LST_CG_GUID = None

	#for level 2
	newRow = QT_Table.AddNewRow()
	sys_name = PLCItem.ProductName
	newRow["System_Name"] = sys_name
	sys_name_guid = PLCItem.QuoteItemGuid
	newRow["System_Item_GUID"] = sys_name_guid
	sys_grp = guid[PLCItem.ParentItemGuid]
	newRow["System_Group"] = sys_grp
	sys_grp_guid = PLCItem.ParentItemGuid
	newRow["System_Grp_GUID"] = sys_grp_guid
	newRow["RolledUpQuoteItem"] = PLCItem.RolledUpQuoteItem
	Sysdic = {}
	for attr in sys_columns:
		attr_container = PLCItem.SelectedAttributes.GetContainerByName(attr).Rows[0]
		for column in sys_columns[attr]:
			Sysdic[column] = attr_container[column]
	expectedResult = [Sysdic[d] for d in sys_columns_seq if d in Sysdic.keys()]
	newRow['System'] = "|".join(expectedResult)

	for Item in PLCItem.Children:
		#for level 3
		if Item.ProductName == "CE PLC Control Group":
			newRow = QT_Table.AddNewRow()
			newRow["CG_Name"] = Item.PartNumber
			newRow["CG_Item_GUID"] = Item.QuoteItemGuid
			newRow["System_Name"] = sys_name
			newRow["System_Item_GUID"] = sys_name_guid
			newRow["System_Group"] = sys_grp
			newRow["System_Grp_GUID"] = sys_grp_guid
			newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem
			if LST_CG_GUID == Item.ParentItemGuid and newRow["CG_Name"] != '':
				CGn += int(1) 
				newRow["CG_No"] = str(CGn)
			elif newRow["CG_Name"] != '':
				CGn = 1
				newRow["CG_No"] = str(CGn)
				LST_CG_GUID = Item.ParentItemGuid

			CGdic = {}
			LIO_CNT = 0
			for attr in cg_column:
				PLC_AO = 0
				PLC_AO_R = 0
				PLC_AO_HART = 0
				PLC_Universal = 0
				PLC_DO = 0
				PLC_DO_R = 0
				PLC_DI_Points_16 = 0
				PLC_AI_HART_Points_R = 0
				PLC_AO_HART_R = 0
				cabinet_rows = Item.SelectedAttributes.GetContainerByName(attr)
				if cabinet_rows:
					attr_container = cabinet_rows.Rows[0]
					for column in cg_column[attr]:
						if column in ['PLC_AO_100_250', 'PLC_AO_250_499', 'PLC_AO_500']:
							PLC_AO = int_handler(PLC_AO) + int_handler(attr_container[column])
							CGdic["PLC_AO"] = str(PLC_AO)
							LIO_CNT += int_handler(attr_container[column])
						elif column in ['PLC_AO_HART_100_250', 'PLC_AO_HART_250_499', 'PLC_AO_HART_500']:
							PLC_AO_HART = int_handler(PLC_AO_HART) + int_handler(attr_container[column])
							CGdic["PLC_AO_HART"] = str(PLC_AO_HART)
							LIO_CNT += int_handler(attr_container[column])
						elif column in ['PLC_Universal_Analog_Input8', 'PLC_Universal_Analog_Input8_TCRTDmVOhm']:
							PLC_Universal = int_handler(PLC_Universal) + int_handler(attr_container[column])
							CGdic["PLC_Universal"] = str(PLC_Universal)
							LIO_CNT += int_handler(attr_container[column])
						elif column in ['PLC_DO_10_250', 'PLC_DO_250_500']:
							PLC_DO = int_handler(PLC_DO) + int_handler(attr_container[column])
							CGdic["PLC_DO_Points"] = str(PLC_DO)
							LIO_CNT += int_handler(attr_container[column])
						elif column in ['PLC_Digital_Input16_125VDC', 'PLC_Digital_Input16_120240VAC']:
							PLC_DI_Points_16 = int_handler(PLC_DI_Points_16) + int_handler(attr_container[column])
							CGdic["PLC_DI_Points_16"] = str(PLC_DI_Points_16)
							LIO_CNT += int_handler(attr_container[column])
						elif column in ['PLC_Cabinet_Spare_Space', 'PLC_Integrated_Marshalling_Cabinet']:
							CGdic[column] = attr_container[column]
						else:
							LIO_CNT += int_handler(attr_container[column])
							CGdic[column] = attr_container[column]

				if attr == 'PLC_CG_UIO_Cont':
					cg_cabinet_rows = Item.SelectedAttributes.GetContainerByName(attr)
					if cg_cabinet_rows:
						attr_container = cg_cabinet_rows.Rows[1]
						for column in cg_column[attr]:
							if column == 'PLC_AI_Points': 
								CGdic["PLC_AI_Points_R"] = attr_container[column]
								LIO_CNT += int_handler(attr_container[column])
							elif column in ['PLC_AO_100_250', 'PLC_AO_250_499', 'PLC_AO_500']:
								PLC_AO_R = int_handler(PLC_AO_R) + int_handler(attr_container[column])
								CGdic["PLC_AO_R"] = str(PLC_AO_R)
								LIO_CNT += int_handler(attr_container[column])
							elif column == 'PLC_DI_Points':
								CGdic["PLC_DI_Points_R"] = attr_container[column]
								LIO_CNT += int_handler(attr_container[column])
							elif column in ['PLC_DO_10_250', 'PLC_DO_250_500']:
								PLC_DO_R = int_handler(PLC_DO_R) + int_handler(attr_container[column])
								CGdic["PLC_DO_Points_R"] = str(PLC_DO_R)
								LIO_CNT += int_handler(attr_container[column])
							elif column in ['PLC_AO_HART_100_250', 'PLC_AO_HART_250_499', 'PLC_AO_HART_500']:
								PLC_AO_HART_R = int_handler(PLC_AO_HART_R) + int_handler(attr_container[column])
								CGdic["PLC_AO_HART_R"] = str(PLC_AO_HART_R)
								LIO_CNT += int_handler(attr_container[column])
							elif column == 'PLC_AI_HART_Points':
								PLC_AI_HART_Points_R = int_handler(PLC_AI_HART_Points_R) + int_handler(attr_container[column])
								CGdic["PLC_AI_HART_Points_R"] = str(PLC_AI_HART_Points_R)
								LIO_CNT += int_handler(attr_container[column])
			expectedResult = [CGdic[d] for d in cg_columns_seq if d in CGdic.keys()]
			Trace.Write("Expected Result: "+str(expectedResult))
			newRow['CG'] = "|".join(expectedResult)
			newRow['Local_IO'] = LIO_CNT
			newRow['Remote_IO'] = '0'
			newRow['Remote_Qty'] = '0'

			#for level 4
			n = 0 
			RIO_CNT = 0
			for ChildItem in Item.Children:
				if ChildItem.ProductName == "CE PLC Remote Group":
					RGdic = {}
					n = n + 1
					for attr in rg_columns:
						PLC_AO = 0
						PLC_AO_R = 0
						PLC_AO_HART = 0
						PLC_Universal = 0
						PLC_DO = 0
						PLC_DO_R = 0
						PLC_DI_Points_16 = 0
						PLC_AI_HART_Points_R = 0
						PLC_AO_HART_R = 0
						rgMaincabinet_rows = ChildItem.SelectedAttributes.GetContainerByName(attr)
						if rgMaincabinet_rows:
							attr_container = rgMaincabinet_rows.Rows[0]
							for column in rg_columns[attr]:
								if column in ['PLC_AO_100_250', 'PLC_AO_250_499', 'PLC_AO_500']:
									plc_ao = int_handler(attr_container[column]) if attr_container[column] else 0
									PLC_AO = int_handler(PLC_AO) + plc_ao
									RGdic["PLC_AO"] = str(PLC_AO)
								elif column in ['PLC_AO_HART_100_250', 'PLC_AO_HART_250_499', 'PLC_AO_HART_500']:
									plc_ao_hart = int_handler(attr_container[column]) if attr_container[column] else 0
									PLC_AO_HART = int_handler(PLC_AO_HART) + plc_ao_hart
									RGdic["PLC_AO_HART"] = str(PLC_AO_HART)
								elif column in ['PLC_Universal_Analog_Input8', 'PLC_Universal_Analog_Input8_TCRTDmVOhm']:
									plc_univer = int_handler(attr_container[column]) if attr_container[column] else 0
									PLC_Universal = int_handler(PLC_Universal) + plc_univer
									RGdic["PLC_Universal"] = str(PLC_Universal)
								elif column in ['PLC_DO_10_250', 'PLC_DO_250_500']:
									plc_do = int_handler(attr_container[column]) if attr_container[column] else 0
									PLC_DO = int_handler(PLC_DO) + plc_do
									RGdic["PLC_DO_Points"] = str(PLC_DO)
								elif column in ['PLC_Digital_Input16_125VDC', 'PLC_Digital_Input16_120240VAC']:
									plc_di = int_handler(attr_container[column]) if attr_container[column] else 0
									PLC_DI_Points_16 = int_handler(PLC_DI_Points_16) + plc_di
									RGdic["PLC_DI_Points_16"] = str(PLC_DI_Points_16)
								else:
									RGdic[column] = str(attr_container[column]) if attr_container[column] else '0'
						
						if attr == 'PLC_RG_UIO_Cont':
							rg_cabinet_rows = ChildItem.SelectedAttributes.GetContainerByName(attr)
							if rg_cabinet_rows:
								attr_container = rg_cabinet_rows.Rows[1]
								for column in rg_columns[attr]:
									if column == 'PLC_AI_Points':
										RGdic["PLC_AI_Points_R"] = str(attr_container[column]) if attr_container[column] else '0'
									elif column in ['PLC_AO_100_250', 'PLC_AO_250_499', 'PLC_AO_500']:
										plc_val = int_handler(attr_container[column]) if attr_container[column] else 0
										PLC_AO_R = int_handler(PLC_AO_R) + plc_val
										RGdic["PLC_AO_R"] = str(PLC_AO_R)
									elif column == 'PLC_DI_Points':
										RGdic["PLC_DI_Points_R"] = str(attr_container[column]) if (attr_container[column]) else '0'
									elif column in ['PLC_DO_10_250', 'PLC_DO_250_500']:
										plc_dval = int_handler(attr_container[column]) if attr_container[column] else 0
										PLC_DO_R = int_handler(PLC_DO_R) + plc_dval
										RGdic["PLC_DO_Points_R"] = str(PLC_DO_R)
									elif column in ['PLC_AO_HART_100_250', 'PLC_AO_HART_250_499', 'PLC_AO_HART_500']:
										PLC_AO_HART_R = int_handler(PLC_AO_HART_R) + int_handler(attr_container[column])
										RGdic["PLC_AO_HART_R"] = str(PLC_AO_HART_R)
										LIO_CNT += int_handler(attr_container[column])
									elif column == 'PLC_AI_HART_Points':
										PLC_AI_HART_Points_R = int_handler(PLC_AI_HART_Points_R) + int_handler(attr_container[column])
										RGdic["PLC_AI_HART_Points_R"] = str(PLC_AI_HART_Points_R)
										LIO_CNT += int_handler(attr_container[column])
					expectedResult = [RGdic[d] for d in rg_columns_seq if d in RGdic.keys()]
					Trace.Write("RG-Expected Result: "+str(expectedResult))
					newRow['RG'+str(n)] = "|".join(expectedResult)
					rg_list = [int_handler(i) for i in newRow['RG'+str(n)].split("|")]
					RIO_CNT += sum(rg_list)
					newRow['Remote_IO'] = RIO_CNT
					newRow['Remote_Qty'] = str(n)
					if n == 1:
						newRow['RGNames'] = ChildItem.PartNumber
					else:
						newRow['RGNames'] = newRow['RGNames'] + "|" + ChildItem.PartNumber	

	for row in QT_Table.Rows:
		Cabinet_cnt = 0
		Cabinet_dic = {}
		if row['System_Name'] == "ControlEdge PLC System" and row['CG_Name'] == '':
			for Item in Quote.Items:
				if Item.PartNumber in ('CC-CBDS01', 'CC-CBDD01') and str(Item.RolledUpQuoteItem).startswith(row['RolledUpQuoteItem']):
					Cabinet_cnt += Item.Quantity
					Cabinet_dic["Cabinet_cnt"] = str(Cabinet_cnt)
			expectedResult = [Cabinet_dic[d] for d in cabinet_columns_seq if d in Cabinet_dic.keys()]
			row["Cabinets"] = "|".join(expectedResult)

	QT_Table.Save()