def populateUOCData(Quote):
	#["System_Group","System_Grp_GUID"   "System_Name"   "System_Item_GUID"  "CG_Name"   "CG_Item_GUID"  "CG"]
	hierarchy = {'Level0': "Migration_new", 'Level1': "Msid_new", "Level2": "3rd Party PLC to ControlEdge PLC/UOC", "Level3":"UOC Control Group"}
	contrl_guid_uoc=[]
	lst = ["CE_Site_Voltage", "PLC_IO_Filler_Module", "PLC_IO_Spare", "PLC_IO_Slot_Spare", "PLC_Shielded_Terminal_Strip", "CE_Selected_Products", "CE_Add_System_Rows", "CE_Apply_System_Number", "CE_Scope_Choices", "New_Expansion", "Sys_Group_Name", "PLC_Software_Release","PLC_CG_Name","PLC_RG_Name", "CE PLC Engineering Execution Year"]
	# UOC_Common_Questions_Cont
	sys_columns = ['UOC_IO_Spare', 'UOC_IO_Slot_Spare','UOC_Marshalling_Cabinet_Cont_Labour']
	sys_columns_seq = ['UOC_IO_Spare', 'UOC_IO_Slot_Spare','UOC_Marshalling_Cabinet_Cont_Labour']
	cg_columns = ['UOC_AI_Points', 'UOC_AI_HART_Points', 'UOC_AO_100_250', 'UOC_AO_250_499', 'UOC_AO_500', 'UOC_AO_HART_100_250', 'UOC_AO_HART_250_499', 'UOC_AO_HART_500', 'UOC_DI_Points', 'UOC_DO_10_250', 'UOC_DO_250_500', 'UOC_Universal_Analog_Input8', 'UOC_Universal_Analog_Input8_TCRTDmVOhm', 'UOC_Analog_Input16', 'UOC_Analog_Output4', 'UOC_Analog_Output8_Internal', 'UOC_Analog_Output8_External', 'UOC_Digital_Input32', 'UOC_Digital_Input16_120240VAC', 'UOC_Digital_Input_Contact_Type16', 'UOC_Digital_Input16_125VDC', 'UOC_Digital_Output32', 'UOC_Digital_Output8', 'UOC_Digital_Output_Relay8', 'UOC_AI_Hart', 'UOC_AO_Points','UOC_AO_Hart','UOC_DI_Contact', 'UOC_DO_Points','UOC_Cabinet_Spare_Space', 'UOC_Integrated_Marshalling_Cabinet']
	cg_columns_seq = ['UOC_Cabinet_Spare_Space', 'UOC_Integrated_Marshalling_Cabinet', 'UOC_AI_Points', 'UOC_AI', 'UOC_AI_HART_Points', 'UOC_AI_Hart', 'UOC_AO', 'UOC_AO_Points', 'UOC_AO_HART_Points', 'UOC_AO_Hart', 'UOC_Universal', 'UOC_Analog_Input16', 'UOC_Analog_Output4', 'UOC_Analog_Output8_Internal', 'UOC_Analog_Output8_External', 'UOC_DI_Points', 'UOC_DI_Contact', 'UOC_DO' ,'UOC_DO_Points', 'UOC_Digital_Input32', 'UOC_DI', 'UOC_Digital_Input_Contact_Type16', 'UOC_Digital_Output32', 'UOC_Digital_Output8', 'UOC_Digital_Output_Relay8' ]
	rg_columns = ['UOC_AI_Points', 'UOC_AI_HART_Points', 'UOC_AO_100_250', 'UOC_AO_250_499', 'UOC_AO_500', 'UOC_AO_HART_100_250', 'UOC_AO_HART_250_499', 'UOC_AO_HART_500', 'UOC_DI_Points', 'UOC_DO_10_250', 'UOC_DO_250_500', 'UOC_Universal_Analog_Input8', 'UOC_Universal_Analog_Input8_TCRTDmVOhm', 'UOC_Analog_Input16', 'UOC_Analog_Output4', 'UOC_Analog_Output8_Internal', 'UOC_Analog_Output8_External', 'UOC_Digital_Input32', 'UOC_Digital_Input16_120240VAC', 'UOC_Digital_Input_Contact_Type16', 'UOC_Digital_Input16_125VDC', 'UOC_Digital_Output32', 'UOC_Digital_Output8', 'UOC_Digital_Output_Relay8', 'UOC_AI_Hart', 'UOC_AO_Points','UOC_AO_Hart','UOC_DI_Contact', 'UOC_DO_Points', 'UOC_Cabinet_Spare_Space', 'UOC_Integrated_Marshalling_Cabinet']
	rg_columns_seq = ['UOC_Cabinet_Spare_Space', 'UOC_Integrated_Marshalling_Cabinet', 'UOC_AI_Points', 'UOC_AI', 'UOC_AI_HART_Points', 'UOC_AI_Hart', 'UOC_AO', 'UOC_AO_Points', 'UOC_AO_HART_Points', 'UOC_AO_Hart', 'UOC_Universal', 'UOC_Analog_Input16', 'UOC_Analog_Output4', 'UOC_Analog_Output8_Internal', 'UOC_Analog_Output8_External', 'UOC_DI_Points', 'UOC_DI_Contact', 'UOC_DO' ,'UOC_DO_Points', 'UOC_Digital_Input32', 'UOC_DI', 'UOC_Digital_Input_Contact_Type16', 'UOC_Digital_Output32', 'UOC_Digital_Output8', 'UOC_Digital_Output_Relay8' ]
	cabinets_columns = ['Cabinet_cnt']
	cabinet_columns_seq = ['Cabinet_cnt']
	cg_system_col_seq = ['IMC_Yes','IMC_No','cab_count_yes', 'cab_count_no']
	QT_Table = Quote.QuoteTables["PAS_Document_Data"]
	#QT_Table.Rows.Clear()
	UOC = ''
	#for level 2
	for Item in Quote.MainItems:
		if hierarchy["Level2"] == Item.ProductName:
			UOC ='Yes'
			newRow = QT_Table.AddNewRow()
			newRow["System_Name"] = Item.ProductName
			newRow["System_Item_GUID"] = Item.QuoteItemGuid
			newRow["System_Grp_GUID"] = Item.ParentItemGuid
			newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem
		if hierarchy["Level3"] == Item.ProductName:
			newRow = QT_Table.AddNewRow()
			newRow["CG_Name"] = Item.PartNumber
			newRow["CG_Item_GUID"] = Item.QuoteItemGuid
			newRow["System_Item_GUID"] = Item.ParentItemGuid
			newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem
	if UOC != 'Yes':
		for row in QT_Table.Rows:
			if row["System_Name"] == 'ControlEdge UOC System':
				rowId = row.Id
				QT_Table.DeleteRow(int(rowId))
	LST_CG_GUID = 1
	CGn = 0
	for row in QT_Table.Rows:
		for Item in Quote.MainItems:
			if hierarchy["Level1"] == Item.ProductName and row["System_Item_GUID"] == Item.QuoteItemGuid:
				row["System_Group"] = Item.PartNumber
			if hierarchy["Level2"] == Item.ProductName and row["System_Item_GUID"] == Item.QuoteItemGuid:
				row["System_Name"] = Item.ProductName
				row["System_Item_GUID"] = Item.QuoteItemGuid
				row["System_Grp_GUID"] = Item.ParentItemGuid
				if LST_CG_GUID == Item.ParentItemGuid and row["CG_Name"] != '':
					CGn += int(1)
					row["CG_No"] = str(CGn)
				elif row["CG_Name"] != '':
					CGn = 1
					row["CG_No"] = str(CGn)
					LST_CG_GUID = Item.ParentItemGuid
	IMC_Yes = False
	IMC_No = False
	cab_count_yes = 0
	cab_count_no = 0
	for row in QT_Table.Rows:
		n = 0
		RIO_CNT = 0
		LIO_CNT = 0
		for Item in Quote.Items:
			if row['CG_ITEM_GUID'] == Item.QuoteItemGuid and Item.ProductName == "UOC Control Group" and (Item.QuoteItemGuid  not in contrl_guid_uoc):
				contrl_guid_uoc.append(Item.QuoteItemGuid)
				CGdic = {}
				for attr in Item.SelectedAttributes:
					error_flag=False
					if attr.Name not in lst and "PLC" not in attr.Name:
						try:
							attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
						except:
							error_flag = True
						if error_flag:
							continue
						UOC_AO = 0
						UOC_AO_HART = 0
						UOC_Universal = 0
						UOC_DO = 0
						UOC_DI = 0
						for column in attr_containers:
							if column.Name in cg_columns:
								if column.Name == 'UOC_Integrated_Marshalling_Cabinet':
									try:
										if column.Value == 'Yes':
											parts = Item.SelectedAttributes.GetContainerByName('UOC_CG_PartSummary_Cont').Rows
											for part in parts:
												if part['CE_Part_Number'] in ('CC-CBDS01', 'CC-CBDD01'):
													cab_count_yes += int(part['CE_Part_Qty'])
											IMC_Yes = True
										elif column.Value == 'No':
											IMC_No = True
											parts = Item.SelectedAttributes.GetContainerByName('UOC_CG_PartSummary_Cont').Rows
											for part in parts:
												if part['CE_Part_Number'] in ('CC-CBDS01', 'CC-CBDD01'):
													cab_count_no += int(part['CE_Part_Qty'])
									except:
										Trace.Write('Error while reading Part Summary')
									CGdic[column.Name] = column.Value
								elif column.Name == 'UOC_Cabinet_Spare_Space':
									CGdic[column.Name] = column.Value
								elif column.Name in ['UOC_AO_500']:
									LIO_CNT += int(column.Value or 0)
									UOC_AO += int(column.Value or 0)
									CGdic['UOC_AO'] = UOC_AO
								elif column.Name in ['UOC_AO_HART_100_250']:
									LIO_CNT += int(column.Value or 0)
									UOC_AO_HART += int(column.Value or 0)
									CGdic['UOC_AO_HART_Points'] = UOC_AO_HART
								elif column.Name in ['UOC_Universal_Analog_Input8', 'UOC_Universal_Analog_Input8_TCRTDmVOhm']:
									LIO_CNT += int(column.Value or 0)
									UOC_Universal += int(column.Value or 0)
									CGdic['UOC_Universal'] = UOC_Universal
								elif column.Name in ['UOC_DO_10_250']:
									LIO_CNT += int(column.Value or 0)
									UOC_DO += int(column.Value or 0)
									CGdic['UOC_DO'] = UOC_DO
								elif column.Name in ['UOC_Digital_Input16_120240VAC']:
									LIO_CNT += int(column.Value or 0)
									UOC_DI += int(column.Value or 0)
									CGdic['UOC_DI'] = UOC_DI
								elif attr.Name == 'UOC_CG_PF_IO_Cont' and column.Name == 'UOC_AI_Points':
									LIO_CNT += int(column.Value or 0)
									CGdic['UOC_AI'] = column.Value
								else:
									Trace.Write(column.Value)
									LIO_CNT += int(column.Value or 0)
									CGdic[column.Name] = column.Value
				expectedResult = [str(CGdic[d]) for d in cg_columns_seq if d in CGdic.keys()]
				Trace.Write("Expected Result: "+str(expectedResult))
				row['CG'] = "|".join(expectedResult)
				CGn += int(1)
				row["CG_No"] = str(CGn)
				row['Local_IO'] = LIO_CNT

			elif Item.ProductName == "UOC Remote Group" and Item.ParentItemGuid == row['CG_ITEM_GUID']:
				RGdic = {}
				n = n + 1
				for attr in Item.SelectedAttributes:
					error_flag=False
					if attr.Name not in lst and "PLC" not in attr.Name:
						try:
							attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
						except:
							error_flag = True
						if error_flag:
							continue
						UOC_AO = 0
						UOC_AO_HART = 0
						UOC_Universal = 0
						UOC_DO = 0
						UOC_DI = 0
						for column in attr_containers:
							Trace.Write("{} : {}".format(column.Name, column.Value))
							if column.Name in cg_columns:
								if column.Name == 'UOC_Integrated_Marshalling_Cabinet':
									try:
										if column.Value == 'Yes':
											parts = Item.SelectedAttributes.GetContainerByName('UOC_RG_PartSummary_Cont').Rows
											for part in parts:
												if part['CE_Part_Number'] in ('CC-CBDS01', 'CC-CBDD01'):
													cab_count_yes += int(part['CE_Part_Qty'])
											IMC_Yes = True
										elif column.Value == 'No':
											IMC_No = True
											parts = Item.SelectedAttributes.GetContainerByName('UOC_RG_PartSummary_Cont').Rows
											for part in parts:
												if part['CE_Part_Number'] in ('CC-CBDS01', 'CC-CBDD01'):
													cab_count_no += int(part['CE_Part_Qty'])
										RGdic[column.Name] = column.Value 
									except:
										Trace.Write('Error while reading Part Summary RG UOC')
								elif column.Name == 'UOC_Cabinet_Spare_Space':
									RGdic[column.Name] = column.Value
								elif column.Name in ['UOC_AO_500']:
									RIO_CNT += int(column.Value or 0)
									UOC_AO += int(column.Value or 0)
									RGdic['UOC_AO'] = UOC_AO
								elif column.Name in ['UOC_AO_HART_100_250']:
									RIO_CNT += int(column.Value or 0)
									UOC_AO_HART += int(column.Value or 0)
									RGdic['UOC_AO_HART_Points'] = UOC_AO_HART
								elif column.Name in ['UOC_Universal_Analog_Input8', 'UOC_Universal_Analog_Input8_TCRTDmVOhm']:
									RIO_CNT += int(column.Value or 0)
									UOC_Universal += int(column.Value or 0)
									RGdic['UOC_Universal'] = UOC_Universal
								elif column.Name in ['UOC_DO_10_250']:
									RIO_CNT += int(column.Value or 0)
									UOC_DO += int(column.Value or 0)
									RGdic['UOC_DO'] = UOC_DO
								elif column.Name in ['UOC_Digital_Input16_120240VAC']:
									RIO_CNT += int(column.Value or 0)
									UOC_DI += int(column.Value or 0)
									RGdic['UOC_DI'] = UOC_DI
								elif attr.Name == 'UOC_RG_PF_IO_Cont' and column.Name == 'UOC_AI_Points':
									RIO_CNT += int(column.Value or 0)
									RGdic['UOC_AI'] = column.Value
								else:
									RIO_CNT += int(column.Value or 0)
									RGdic[column.Name] = column.Value
				expectedResult = [str(RGdic[d]) for d in rg_columns_seq if d in RGdic.keys()]
				Trace.Write("RG-Expected Result: "+str(expectedResult))
				row['RG'+str(n)] = "|".join(expectedResult)
				row['Remote_IO'] = RIO_CNT
				row['Remote_Qty'] = str(n)
				if n == 1:
					row['RGNames'] = Item.PartNumber
				else:
					row['RGNames'] = row['RGNames'] + "|" + Item.PartNumber
	for row in QT_Table.Rows:
		Cabinet_cnt = 0
		Cabinet_dic = {}
		CG_dic = {}
		if row['System_Name'] == "ControlEdge UOC System" and row['CG_Name'] == '':
			CG_dic['IMC_No'] = '1' if IMC_No else '0'
			CG_dic['IMC_Yes'] = '1' if IMC_Yes else '0'
			CG_dic['cab_count_yes'] = str(cab_count_yes)
			CG_dic['cab_count_no'] = str(cab_count_no)
			for Item in Quote.Items:
				if Item.PartNumber in ('CC-CBDS01', 'CC-CBDD01') and Item.RolledUpQuoteItem[:3] == row['RolledUpQuoteItem'][:3]:
					Cabinet_cnt += Item.Quantity
					Cabinet_dic["Cabinet_cnt"] = str(Cabinet_cnt)
			expectedResult = [Cabinet_dic[d] for d in cabinet_columns_seq if d in Cabinet_dic.keys()]
			row["Cabinets"] = "|".join(expectedResult)
			expectedResultCG = [CG_dic[d] for d in cg_system_col_seq if d in CG_dic.keys()]
			row["CG"] = "|".join(expectedResultCG)
		if row['System_Name'] == "ControlEdge UOC System" and row['CG_Name'] != '':
			if row['Remote_IO'] == '':
				row['Remote_IO'] = '0'
				row['Remote_Qty'] = '0'
	QT_Table.Save()

	if UOC != 'Yes':
		return False
	else:
		return True
#populateUOCData(Quote)