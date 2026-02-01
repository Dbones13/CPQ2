def int_handler(val):
	return int(val or 0)

def populateUOCproposal(Quote, UOCItem, guid):
	sys_columns = {'UOC_Common_Questions_Cont':['UOC_IO_Spare', 'UOC_IO_Slot_Spare'], 'UOC_Labor_Details':['UOC_Marshalling_Cabinet_Cont_Labour']}
	sys_columns_seq = ['UOC_IO_Spare', 'UOC_IO_Slot_Spare','UOC_Marshalling_Cabinet_Cont_Labour']

	cg_columns = {'UOC_CG_PF_IO_Cont':['UOC_AI_Hart','UOC_AO_Hart','UOC_DI_Contact','UOC_AI_Points','UOC_DO_Points','UOC_AO_Points'], 'UOC_CG_UIO_Cont':['UOC_AI_Points','UOC_AI_HART_Points','UOC_AO_100_250','UOC_AO_250_499','UOC_AO_500','UOC_AO_HART_100_250','UOC_AO_HART_250_499','UOC_AO_HART_500','UOC_DI_Points','UOC_DO_10_250','UOC_DO_250_500'], 'UOC_CG_Cabinet_Cont':['UOC_Cabinet_Spare_Space','UOC_Integrated_Marshalling_Cabinet'], 'UOC_CG_Other_IO_Cont':['UOC_Universal_Analog_Input8','UOC_Universal_Analog_Input8_TCRTDmVOhm','UOC_Analog_Input16','UOC_Analog_Output4','UOC_Analog_Output8_Internal','UOC_Analog_Output8_External','UOC_Digital_Input32','UOC_Digital_Input16_120240VAC','UOC_Digital_Input_Contact_Type16','UOC_Digital_Input16_125VDC','UOC_Digital_Output32','UOC_Digital_Output8','UOC_Digital_Output_Relay8']}

	cg_columns_seq = ['UOC_Cabinet_Spare_Space', 'UOC_Integrated_Marshalling_Cabinet', 'UOC_AI_Points', 'UOC_AI', 'UOC_AI_HART_Points', 'UOC_AI_Hart', 'UOC_AO', 'UOC_AO_Points', 'UOC_AO_HART_Points', 'UOC_AO_Hart', 'UOC_Universal', 'UOC_Analog_Input16', 'UOC_Analog_Output4', 'UOC_Analog_Output8_Internal', 'UOC_Analog_Output8_External', 'UOC_DI_Points', 'UOC_DI_Contact', 'UOC_DO' ,'UOC_DO_Points', 'UOC_Digital_Input32', 'UOC_DI', 'UOC_Digital_Input_Contact_Type16', 'UOC_Digital_Output32', 'UOC_Digital_Output8', 'UOC_Digital_Output_Relay8' ]

	rg_columns = {'UOC_RG_Cabinet_Cont':['UOC_Cabinet_Spare_Space','UOC_Integrated_Marshalling_Cabinet'], 'UOC_RG_UIO_Cont':['UOC_AI_Points','UOC_AI_HART_Points','UOC_AO_100_250','UOC_AO_250_499','UOC_AO_500','UOC_AO_HART_100_250','UOC_AO_HART_250_499','UOC_AO_HART_500','UOC_DI_Points','UOC_DO_10_250','UOC_DO_250_500'], 'UOC_RG_Other_IO_Cont':['UOC_Universal_Analog_Input8','UOC_Universal_Analog_Input8_TCRTDmVOhm','UOC_Analog_Input16','UOC_Analog_Output4','UOC_Analog_Output8_Internal','UOC_Analog_Output8_External','UOC_Digital_Input32','UOC_Digital_Input16_120240VAC','UOC_Digital_Input_Contact_Type16','UOC_Digital_Input16_125VDC','UOC_Digital_Output32','UOC_Digital_Output8','UOC_Digital_Output_Relay8'], 'UOC_RG_PF_IO_Cont':['UOC_AI_Hart','UOC_AO_Hart','UOC_DI_Contact','UOC_AI_Points','UOC_AO_Points','UOC_DO_Points']}

	rg_columns_seq = ['UOC_Cabinet_Spare_Space', 'UOC_Integrated_Marshalling_Cabinet', 'UOC_AI_Points', 'UOC_AI', 'UOC_AI_HART_Points', 'UOC_AI_Hart', 'UOC_AO', 'UOC_AO_Points', 'UOC_AO_HART_Points', 'UOC_AO_Hart', 'UOC_Universal', 'UOC_Analog_Input16', 'UOC_Analog_Output4', 'UOC_Analog_Output8_Internal', 'UOC_Analog_Output8_External', 'UOC_DI_Points', 'UOC_DI_Contact', 'UOC_DO' ,'UOC_DO_Points', 'UOC_Digital_Input32', 'UOC_DI', 'UOC_Digital_Input_Contact_Type16', 'UOC_Digital_Output32', 'UOC_Digital_Output8', 'UOC_Digital_Output_Relay8' ]

	cabinets_columns = ['Cabinet_cnt']
	cabinet_columns_seq = ['Cabinet_cnt']

	cg_system_col_seq = ['IMC_Yes','IMC_No','cab_count_yes', 'cab_count_no']

	QT_Table = Quote.QuoteTables["PAS_Document_Data"]
	CGn = 0
	LST_CG_GUID = None
	IMC_Yes = False
	IMC_No = False
	cab_count_yes = 0
	cab_count_no = 0

	#for level 2
	newRow = QT_Table.AddNewRow()
	sys_name = UOCItem.ProductName
	newRow["System_Name"] = sys_name
	sys_name_guid = UOCItem.QuoteItemGuid
	newRow["System_Item_GUID"] = sys_name_guid
	sys_grp = guid[UOCItem.ParentItemGuid]
	newRow["System_Group"] = sys_grp
	sys_grp_guid = UOCItem.ParentItemGuid
	newRow["System_Grp_GUID"] = sys_grp_guid
	newRow["RolledUpQuoteItem"] = UOCItem.RolledUpQuoteItem
	Sysdic = {}
	for attr in sys_columns:
		cabinet_rows = UOCItem.SelectedAttributes.GetContainerByName(attr)
		if cabinet_rows:
			attr_container = cabinet_rows.Rows[0]
			for column in sys_columns[attr]:
				Sysdic[column] = attr_container[column] if attr_container[column] else '0'
	expectedResult = [Sysdic[d] for d in sys_columns_seq if d in Sysdic.keys()]
	newRow['System'] = "|".join(expectedResult)

	for Item in UOCItem.Children:
		#for level 3
		if Item.ProductName == "UOC Control Group":
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
			for attr in cg_columns:
				UOC_AO = 0
				UOC_AO_HART = 0
				UOC_Universal = 0
				UOC_DO = 0
				UOC_DI = 0
				cabinet_rows = Item.SelectedAttributes.GetContainerByName(attr)
				if cabinet_rows:
					attr_container = cabinet_rows.Rows[0]
					for column in cg_columns[attr]:
						if column == 'UOC_Integrated_Marshalling_Cabinet':
							try:
								if attr_container[column] == 'Yes':
									parts = Item.SelectedAttributes.GetContainerByName('UOC_CG_PartSummary_Cont').Rows
									for part in parts:
										if part['CE_Part_Number'] in ('CC-CBDS01', 'CC-CBDD01'):
											cab_count_yes += int(part['CE_Part_Qty'])
									IMC_Yes = True
								elif attr_container[column] == 'No':
									IMC_No = True
									parts = Item.SelectedAttributes.GetContainerByName('UOC_CG_PartSummary_Cont').Rows
									for part in parts:
										if part['CE_Part_Number'] in ('CC-CBDS01', 'CC-CBDD01'):
											cab_count_no += int(part['CE_Part_Qty'])
							except:
								Trace.Write('Error while reading Part Summary')
							CGdic[column] = attr_container[column]
						elif column == 'UOC_Cabinet_Spare_Space':
							CGdic[column] = attr_container[column]
						elif column in ['UOC_AO_100_250', 'UOC_AO_250_499', 'UOC_AO_500']:
							LIO_CNT += int_handler(attr_container[column])
							UOC_AO += int_handler(attr_container[column])
							CGdic['UOC_AO'] = UOC_AO
						elif column in ['UOC_AO_HART_100_250', 'UOC_AO_HART_250_499', 'UOC_AO_HART_500']:
							LIO_CNT += int_handler(attr_container[column])
							UOC_AO_HART += int_handler(attr_container[column])
							CGdic['UOC_AO_HART_Points'] = UOC_AO_HART
						elif column in ['UOC_Universal_Analog_Input8', 'UOC_Universal_Analog_Input8_TCRTDmVOhm']:
							LIO_CNT += int_handler(attr_container[column])
							UOC_Universal += int_handler(attr_container[column])
							CGdic['UOC_Universal'] = UOC_Universal
						elif column in ['UOC_DO_10_250', 'UOC_DO_250_500']:
							LIO_CNT += int_handler(attr_container[column])
							UOC_DO += int_handler(attr_container[column])
							CGdic['UOC_DO'] = UOC_DO
						elif column in ['UOC_Digital_Input16_120240VAC', 'UOC_Digital_Input16_125VDC']:
							LIO_CNT += int_handler(attr_container[column])
							UOC_DI += int_handler(attr_container[column])
							CGdic['UOC_DI'] = UOC_DI
						elif attr == 'UOC_CG_PF_IO_Cont' and column == 'UOC_AI_Points':
							LIO_CNT += int_handler(attr_container[column])
							CGdic['UOC_AI'] = int_handler(attr_container[column])
						else:
							LIO_CNT += int_handler(attr_container[column])
							CGdic[column] = int_handler(attr_container[column])
			cg_dict = {key: 0 for key in cg_columns_seq if key not in CGdic}
			cg_merged_dict = cg_dict.copy()
			cg_merged_dict.update(CGdic)
			expectedResult = [str(cg_merged_dict[d]) for d in cg_columns_seq]
			Trace.Write("Expected Result CG: "+str(expectedResult))
			newRow['CG'] = "|".join(expectedResult)
			newRow['Local_IO'] = LIO_CNT
			newRow['Remote_IO'] = '0'
			newRow['Remote_Qty'] = '0'

			#for level 4
			n = 0 
			RIO_CNT = 0
			for ChildItem in Item.Children:
				if ChildItem.ProductName == "UOC Remote Group":
					RGdic = {}
					n = n + 1
					for attr in rg_columns:
						UOC_AO = 0
						UOC_AO_HART = 0
						UOC_Universal = 0
						UOC_DO = 0
						UOC_DI = 0
						cabinet_rows = ChildItem.SelectedAttributes.GetContainerByName(attr)
						if cabinet_rows:
							attr_container = cabinet_rows.Rows[0]
							for column in rg_columns[attr]:
								if column == 'UOC_Integrated_Marshalling_Cabinet':
									try:
										if attr_container[column] == 'Yes':
											parts = ChildItem.SelectedAttributes.GetContainerByName('UOC_RG_PartSummary_Cont').Rows
											for part in parts:
												if part['CE_Part_Number'] in ('CC-CBDS01', 'CC-CBDD01'):
													cab_count_yes += int(part['CE_Part_Qty'])
											IMC_Yes = True
										elif attr_container[column] == 'No':
											IMC_No = True
											parts = ChildItem.SelectedAttributes.GetContainerByName('UOC_RG_PartSummary_Cont').Rows
											for part in parts:
												if part['CE_Part_Number'] in ('CC-CBDS01', 'CC-CBDD01'):
													cab_count_no += int(part['CE_Part_Qty'])
										RGdic[column] = attr_container[column] 
									except:
										Trace.Write('Error while reading Part Summary RG UOC')
								elif column == 'UOC_Cabinet_Spare_Space':
									RGdic[column] = attr_container[column]
								elif column in ['UOC_AO_100_250', 'UOC_AO_250_499', 'UOC_AO_500']:
									RIO_CNT += int_handler(attr_container[column])
									UOC_AO += int_handler(attr_container[column])
									RGdic['UOC_AO'] = UOC_AO
								elif column in ['UOC_AO_HART_100_250', 'UOC_AO_HART_250_499', 'UOC_AO_HART_500']:
									RIO_CNT += int_handler(attr_container[column])
									UOC_AO_HART += int_handler(attr_container[column])
									RGdic['UOC_AO_HART_Points'] = UOC_AO_HART
								elif column in ['UOC_Universal_Analog_Input8', 'UOC_Universal_Analog_Input8_TCRTDmVOhm']:
									RIO_CNT += int_handler(attr_container[column])
									UOC_Universal += int_handler(attr_container[column])
									RGdic['UOC_Universal'] = UOC_Universal
								elif column in ['UOC_DO_10_250', 'UOC_DO_250_500']:
									RIO_CNT += int_handler(attr_container[column])
									UOC_DO += int_handler(attr_container[column])
									RGdic['UOC_DO'] = UOC_DO
								elif column in ['UOC_Digital_Input16_120240VAC', 'UOC_Digital_Input16_125VDC']:
									RIO_CNT += int_handler(attr_container[column])
									UOC_DI += int_handler(attr_container[column])
									RGdic['UOC_DI'] = UOC_DI
								elif attr == 'UOC_RG_PF_IO_Cont' and column == 'UOC_AI_Points':
									RIO_CNT += int_handler(attr_container[column])
									RGdic['UOC_AI'] = int_handler(attr_container[column])
								else:
									RIO_CNT += int_handler(attr_container[column])
									RGdic[column] = int_handler(attr_container[column])
					rg_dict = {key: 0 for key in rg_columns_seq if key not in RGdic}
					rg_merged_dict = rg_dict.copy()
					rg_merged_dict.update(RGdic)
					expectedResult = [str(rg_merged_dict[d]) for d in rg_columns_seq]
					Trace.Write("RG-Expected Result: "+str(expectedResult))
					newRow['RG'+str(n)] = "|".join(expectedResult)
					newRow['Remote_IO'] = RIO_CNT
					newRow['Remote_Qty'] = str(n)
					if n == 1:
						newRow['RGNames'] = ChildItem.PartNumber
					else:
						newRow['RGNames'] = newRow['RGNames'] + "|" + ChildItem.PartNumber

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
				if Item.PartNumber in ('CC-CBDS01', 'CC-CBDD01') and str(Item.RolledUpQuoteItem).startswith(row['RolledUpQuoteItem']):
					Cabinet_cnt += Item.Quantity
					Cabinet_dic["Cabinet_cnt"] = str(Cabinet_cnt)
			expectedResult = [Cabinet_dic[d] for d in cabinet_columns_seq if d in Cabinet_dic.keys()]
			row["Cabinets"] = "|".join(expectedResult)
			expectedResultCG = [CG_dic[d] for d in cg_system_col_seq if d in CG_dic.keys()]
			row["CG"] = "|".join(expectedResultCG)

	QT_Table.Save()