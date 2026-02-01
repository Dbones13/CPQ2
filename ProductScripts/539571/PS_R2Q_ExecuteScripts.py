import GS_C300_IO_Calc, GS_SerC_Container_Event, GS_C300_IO_Calc2
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
	Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
	IO_Family_Type = Product.Attr('SerC_CG_IO_Family_Type').GetValue()

	colMapping = dict()
	module = ''
	get_cont = Product.GetContainerByName('SerC_RG_Enhanced_Function_IO_Cont2')
	if get_cont.Rows.Count > 0:
		for row in get_cont.Rows:
			IO_Type = row['IO_Type']
			for col in row.Columns:
				if col.Value not in ["0", ""] and col.Name not in ['IO_Type', 'IO_Type_with_hint']:
					if IO_Family_Type == 'Series C':
						iOType = ['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)','Series-C: DI (32) 110 VAC (0-5000)','Series-C: DI (32) 110 VAC PROX (0-5000)','Series-C: DI (32) 220 VAC (0-5000)','Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)','Series-C: Pulse Input (8) Single Channel (0-5000)','Series-C: Pulse Input (4) Dual Channel (0-5000)','Series-C: Pulse Input (2) Fast Cut Off Channel (0-5000)']
						column = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR', 'Red_RLY', 'Future_Red_RLY', 'Non_Red_RLY', 'Red_HV_RLY', 'Future_Red_HV_RLY', 'Non_Red_HV_RLY']
						IO_Type = row['IO_Type']

						if IO_Type == 'Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)':
							module = '40887'
							colMapping = {'Red_IS': 'D81', 'Future_Red_IS': 'E81', 'Non_Red_IS': 'F81', 'Red_NIS': 'D82', 'Future_Red_NIS': 'E82', 'Non_Red_NIS': 'F82', 'Red_ISLTR': 'D83', 'Future_Red_ISLTR': 'E83',  'Non_Red_ISLTR': 'F83',  'Red_RLY': 'D84',  'Future_Red_RLY': 'E84',  'Non_Red_RLY': 'F84', 'Red_HV_RLY':'GG51', 'Future_Red_HV_RLY':'HH51', 'Non_Red_HV_RLY':'II51'}
						elif IO_Type == 'Series-C: DI (32) 24VDC SOE (0-5000)':
							module = '40887'
							colMapping = {'Red_IS': 'D91', 'Future_Red_IS': 'E91', 'Non_Red_IS': 'F91', 'Red_NIS': 'D92', 'Future_Red_NIS': 'E92', 'Non_Red_NIS': 'F92', 'Red_ISLTR': 'D93', 'Future_Red_ISLTR': 'E93',  'Non_Red_ISLTR': 'F93',  'Red_RLY': 'D94',  'Future_Red_RLY': 'E94',  'Non_Red_RLY': 'F94', 'Red_HV_RLY':'GG81', 'Future_Red_HV_RLY':'HH81', 'Non_Red_HV_RLY':'II81'}
						elif IO_Type == 'Series-C: DI (32) 110 VAC (0-5000)':
							module = '40972'
							colMapping = {'Red_NIS': 'G12', 'Future_Red_NIS': 'H12', 'Non_Red_NIS': 'I12'}
						elif IO_Type == 'Series-C: DI (32) 110 VAC PROX (0-5000)':
							module = '40972'
							colMapping = {'Non_Red_NIS': 'I22'}
						elif IO_Type == 'Series-C: DI (32) 220 VAC (0-5000)':
							module = '40972'
							colMapping = {'Red_NIS': 'G32', 'Future_Red_NIS': 'H32', 'Non_Red_NIS': 'I32'}
						elif IO_Type == 'Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)':
							module = '41229'
							colMapping = {'Red_IS': 'G41', 'Future_Red_IS': 'H41', 'Non_Red_IS': 'I41', 'Red_NIS': 'G42', 'Future_Red_NIS': 'H42', 'Non_Red_NIS': 'I42', 'Red_ISLTR': 'G43', 'Future_Red_ISLTR': 'H43',  'Non_Red_ISLTR': 'I43',  'Red_RLY': 'G44',  'Future_Red_RLY': 'H44',  'Non_Red_RLY': 'I44',  'Red_HV_RLY':'GG61', 'Future_Red_HV_RLY':'HH61', 'Non_Red_HV_RLY':'II61'}
						elif IO_Type == 'Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)':
							module = '41229'
							colMapping = {'Red_IS': 'G51', 'Future_Red_IS': 'H51', 'Non_Red_IS': 'I51', 'Red_NIS': 'G52', 'Future_Red_NIS': 'H52', 'Non_Red_NIS': 'I52', 'Red_ISLTR': 'G53', 'Future_Red_ISLTR': 'H53',  'Non_Red_ISLTR': 'I53',  'Red_RLY': 'G54',  'Future_Red_RLY': 'H54',  'Non_Red_RLY': 'I54', 'Red_HV_RLY':'GG71', 'Future_Red_HV_RLY':'HH71', 'Non_Red_HV_RLY':'II71'}
						elif IO_Type == 'Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)':
							module = '41229'
							column = ['Red_RLY', 'Future_Red_RLY', 'Non_Red_RLY']
							colMapping = {'Red_RLY': 'G64',  'Future_Red_RLY': 'H64',  'Non_Red_RLY': 'I64'}
						elif IO_Type == 'Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)':
							module = '41229'
							column = ['Red_RLY', 'Future_Red_RLY', 'Non_Red_RLY']
							colMapping = {'Red_RLY': 'G74',  'Future_Red_RLY': 'H74',  'Non_Red_RLY': 'I74'}
						elif IO_Type == 'Series-C: Pulse Input (8) Single Channel (0-5000)':
							module = '41449'
							column = ['Red_IS', 'Future_Red_IS', 'Red_NIS','Future_Red_NIS','Red_ISLTR','Future_Red_ISLTR']
							colMapping = {'Red_IS': 'G81', 'Future_Red_IS': 'H81', 'Red_NIS': 'G82', 'Future_Red_NIS': 'H82', 'Red_ISLTR': 'G83', 'Future_Red_ISLTR': 'H83'}
						elif IO_Type == 'Series-C: Pulse Input (4) Dual Channel (0-5000)':
							module = '41449'
							column = ['Red_IS', 'Future_Red_IS', 'Red_NIS','Future_Red_NIS','Red_ISLTR','Future_Red_ISLTR']
							colMapping = {'Red_IS': 'G91', 'Future_Red_IS': 'H91', 'Red_NIS': 'G92', 'Future_Red_NIS': 'H92', 'Red_ISLTR': 'G93', 'Future_Red_ISLTR': 'H93'}
						elif IO_Type == 'Series-C: Pulse Input (2) Fast Cut Off Channel (0-5000)':
							module = '41449'
							column = ['Red_IS', 'Future_Red_IS', 'Red_NIS','Future_Red_NIS','Red_ISLTR','Future_Red_ISLTR']
							colMapping = {'Red_IS': 'J11', 'Future_Red_IS': 'K11', 'Red_NIS': 'J12', 'Future_Red_NIS': 'K12', 'Red_ISLTR': 'J13', 'Future_Red_ISLTR': 'K13'}

						if len(colMapping) > 0 and col.Name in column:
							changedColumn = col.Name
							newValue = col.Value
							if newValue > 0:
								if module == '40887':
									GS_C300_IO_Calc.calcIOModule40887(Product, IO_Type, changedColumn, GS_C300_IO_Calc.getFloat(newValue))
								elif module == '40972':
									GS_C300_IO_Calc.calcIOModule40972(Product, IO_Type, changedColumn, GS_C300_IO_Calc.getFloat(newValue))
								elif module == '41229':
									GS_C300_IO_Calc.calcIOModule41229(Product, IO_Type, changedColumn, GS_C300_IO_Calc.getFloat(newValue))
								elif module == '41449':
									GS_C300_IO_Calc.calcIOModule41449(Product, IO_Type, changedColumn, GS_C300_IO_Calc.getFloat(newValue))
							else:
								GS_C300_IO_Calc.setIOCount(Product, 'SerC_IO_Params', {colMapping[changedColumn]:0})
							if module == '40887':
								parts_dict = GS_C300_IO_Calc.getParts40887(Product, {})
							elif module == '40972':
								parts_dict = GS_C300_IO_Calc.getParts40972(Product, {})
							elif module == '41229':
								parts_dict = GS_C300_IO_Calc.getParts41229(Product, {})
							elif module == '41449':
								parts_dict = GS_C300_IO_Calc.getParts41449(Product, {})
							GS_C300_IO_Calc.setIOCount(Product, 'Series_C_RG_Part_Summary', parts_dict)
							#Product.Messages.Add("Total Load IO is {}".format(GS_C300_Calc_Module.getTotalLoadIO(Product)))
					elif IO_Family_Type == 'Turbomachinery':
						changedColumn = col.Name
						newValue = col.Value
						ioTypes50461 = ['Series-C: DI (32) 110 VAC (0-5000)', 'Series-C: DI (32) 110 VAC PROX (0-5000)', 'Series-C: DI (32) 220 VAC (0-5000)']
						ioTypes50463 = ['Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)', 'Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)', 'Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)', 'Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)']
						if IO_Type in ioTypes50461:
							module = '50461'
						elif IO_Type in ioTypes50463:
							module = '50463'
						if IO_Type == 'Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)':
							module = '49225'
							colMapping = {'Red_IS': 'D81', 'Future_Red_IS': 'E81', 'Non_Red_IS': 'F81', 'Red_NIS': 'D82', 'Future_Red_NIS': 'E82', 'Non_Red_NIS': 'F82', 'Red_ISLTR': 'D83', 'Future_Red_ISLTR': 'E83',  'Non_Red_ISLTR': 'F83',  'Red_RLY': 'D84',  'Future_Red_RLY': 'E84',  'Non_Red_RLY': 'F84'}
						elif IO_Type == 'Series-C: DI (32) 24VDC SOE (0-5000)':
							module = '49225'
							colMapping = {'Red_IS': 'D91', 'Future_Red_IS': 'E91', 'Non_Red_IS': 'F91', 'Red_NIS': 'D92', 'Future_Red_NIS': 'E92', 'Non_Red_NIS': 'F92', 'Red_ISLTR': 'D93', 'Future_Red_ISLTR': 'E93',  'Non_Red_ISLTR': 'F93',  'Red_RLY': 'D94',  'Future_Red_RLY': 'E94',  'Non_Red_RLY': 'F94'}
						elif IO_Type == 'Series-C: DI (32) 110 VAC (0-5000)':
							colMapping = {'Red_NIS': 'G12', 'Future_Red_NIS': 'H12', 'Non_Red_NIS': 'I12'}
						elif IO_Type == 'Series-C: DI (32) 110 VAC PROX (0-5000)':
							colMapping = {'Non_Red_NIS': 'I22'}
						elif IO_Type == 'Series-C: DI (32) 220 VAC (0-5000)':
							colMapping = {'Red_NIS': 'G32', 'Future_Red_NIS': 'H32', 'Non_Red_NIS': 'I32'}
						elif IO_Type == 'Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)':
							colMapping = {'Red_IS': 'G41', 'Future_Red_IS': 'H41', 'Non_Red_IS': 'I41', 'Red_NIS': 'G42', 'Future_Red_NIS': 'H42', 'Non_Red_NIS': 'I42', 'Red_ISLTR': 'G43', 'Future_Red_ISLTR': 'H43',  'Non_Red_ISLTR': 'I43', 'Red_RLY': 'G44', 'Future_Red_RLY': 'H44', 'Non_Red_RLY': 'I44'}
						elif IO_Type == 'Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)':
							colMapping = {'Red_IS': 'G51', 'Future_Red_IS': 'H51', 'Non_Red_IS': 'I51', 'Red_NIS': 'G52', 'Future_Red_NIS': 'H52', 'Non_Red_NIS': 'I52', 'Red_ISLTR': 'G53', 'Future_Red_ISLTR': 'H53',  'Non_Red_ISLTR': 'I53', 'Red_RLY': 'G54', 'Future_Red_RLY': 'H54', 'Non_Red_RLY': 'I54'}
						elif IO_Type == 'Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)':
							colMapping = {'Red_RLY': 'G64', 'Future_Red_RLY': 'H64', 'Non_Red_RLY': 'I64'}
						elif IO_Type == 'Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)':
							colMapping = {'Red_RLY': 'G74', 'Future_Red_RLY': 'H74', 'Non_Red_RLY': 'I74'}
						if changedColumn in colMapping.keys():
							GS_SerC_Container_Event.changeCellEvent(Product, IO_Family_Type, IO_Type, changedColumn, GS_C300_IO_Calc.getFloat(newValue), module, colMapping)

	get_cont2 = Product.GetContainerByName('SerC_RG_Enhanced_Function_IO_Cont')
	if get_cont2.Rows.Count > 0:
		for row in get_cont2.Rows:
			IO_Type = row['IO_Type']
			for col in row.Columns:
				if col.Value not in ["0", ""] and col.Name not in ['IO_Type', 'IO_Type_with_hint']:
					if IO_Family_Type == 'Series C':
						iOType = ['Series-C: HLAI (16) with HART with differential inputs (0-5000)','Series-C: HLAI (16) without HART with differential inputs (0-5000)']
						column = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR',  'Non_Red_ISLTR']
						if IO_Type == 'Series-C: HLAI (16) with HART with differential inputs (0-5000)':
							module = '40833'
							colMapping = {'Red_IS': 'D21', 'Future_Red_IS': 'E21', 'Non_Red_IS': 'F21', 'Red_NIS': 'D22', 'Future_Red_NIS': 'E22', 'Non_Red_NIS': 'F22', 'Red_ISLTR': 'D23', 'Future_Red_ISLTR': 'E23',  'Non_Red_ISLTR': 'F23'}
						elif IO_Type == 'Series-C: HLAI (16) without HART with differential inputs (0-5000)':
							module = '40833'
							colMapping = {'Red_IS': 'D31', 'Future_Red_IS': 'E31', 'Non_Red_IS': 'F31', 'Red_NIS': 'D32', 'Future_Red_NIS': 'E32', 'Non_Red_NIS': 'F32', 'Red_ISLTR': 'D33', 'Future_Red_ISLTR': 'E33',  'Non_Red_ISLTR': 'F33'}
						elif IO_Type == 'Series-C: LLAI (1) Mux RTD (0-5000)':
							module = '40859'
							column = ['Non_Red_IS', 'Non_Red_NIS', 'Non_Red_ISLTR']
							colMapping = {'Non_Red_IS': 'F41', 'Non_Red_NIS': 'F42', 'Non_Red_ISLTR': 'F43'}
						elif IO_Type == 'Series-C: LLAI (1) Mux TC (0-5000)':
							module = '40859'
							column = ['Non_Red_IS', 'Non_Red_NIS', 'Non_Red_ISLTR']
							colMapping = {'Non_Red_IS': 'F51', 'Non_Red_NIS': 'F52', 'Non_Red_ISLTR': 'F53'}
						elif IO_Type == 'Series-C: LLAI (1) Mux TC Remote CJR (0-5000)':
							module = '40859'
							column = ['Non_Red_IS', 'Non_Red_NIS', 'Non_Red_ISLTR']
							colMapping = {'Non_Red_IS': 'F61', 'Non_Red_NIS': 'F62', 'Non_Red_ISLTR': 'F63'}
						elif IO_Type == 'Series-C: AO (16) HART (0-5000)':
							module = '40872'
							colMapping = {'Red_IS': 'D71', 'Future_Red_IS': 'E71', 'Non_Red_IS': 'F71', 'Red_NIS': 'D72', 'Future_Red_NIS': 'E72', 'Non_Red_NIS': 'F72', 'Red_ISLTR': 'D73', 'Future_Red_ISLTR': 'E73',  'Non_Red_ISLTR': 'F73'}
						if len(colMapping) > 0 and col.Name in column:
							changedColumn = col.Name
							newValue = col.Value
							if newValue > 0:
								if module == '40833':
									GS_C300_IO_Calc.calcIOModule40833(Product, IO_Type, changedColumn, GS_C300_IO_Calc.getFloat(newValue))
								elif module == '40859':
									GS_C300_IO_Calc.calcIOModule40859(Product, IO_Type, changedColumn, GS_C300_IO_Calc.getFloat(newValue))
								elif module == '40872':
									GS_C300_IO_Calc.calcIOModule40872(Product, IO_Type, changedColumn, GS_C300_IO_Calc.getFloat(newValue))
							else:
								GS_C300_IO_Calc.setIOCount(Product, 'SerC_IO_Params', {colMapping[changedColumn]:0})
							if module == '40833':
								parts_dict = GS_C300_IO_Calc.getParts40833(Product, {})
							elif module == '40859':
								parts_dict = GS_C300_IO_Calc.getParts40859(Product, {})
							elif module == '40872':
								parts_dict = GS_C300_IO_Calc.getParts40872(Product, {})
							GS_C300_IO_Calc.setIOCount(Product, 'Series_C_RG_Part_Summary', parts_dict)
							#Product.Messages.Add("Total Load IO is {}".format(GS_C300_Calc_Module.getTotalLoadIO(Product)))
							#ScriptExecutor.Execute('PS_Series_C_RG_Part_Summary_Cont_update_parts')
							#Product.GetContainerByName('Series_C_RG_Part_Summary_Cont').Calculate()
					elif IO_Family_Type == 'Turbomachinery':
						changedColumn = col.Name
						newValue = col.Value
						iOType49229 = ['Series-C: HLAI (16) with HART with differential inputs (0-5000)','Series-C: HLAI (16) without HART with differential inputs (0-5000)']
						iOType49231 = ['Series-C: LLAI (1) Mux RTD (0-5000)', 'Series-C: LLAI (1) Mux TC (0-5000)', 'Series-C: LLAI (1) Mux TC Remote CJR (0-5000)']
						if IO_Type in iOType49229:
							module = '49229'
						elif IO_Type in iOType49231:
							module = '49231'

						if IO_Type == 'Series-C: HLAI (16) with HART with differential inputs (0-5000)':
							colMapping = {'Red_IS': 'D21', 'Future_Red_IS': 'E21', 'Non_Red_IS': 'F21', 'Red_NIS': 'D22', 'Future_Red_NIS': 'E22', 'Non_Red_NIS': 'F22', 'Red_ISLTR': 'D23', 'Future_Red_ISLTR': 'E23',  'Non_Red_ISLTR': 'F23'}
						elif IO_Type == 'Series-C: HLAI (16) without HART with differential inputs (0-5000)':
							colMapping = {'Red_IS': 'D31', 'Future_Red_IS': 'E31', 'Non_Red_IS': 'F31', 'Red_NIS': 'D32', 'Future_Red_NIS': 'E32', 'Non_Red_NIS': 'F32', 'Red_ISLTR': 'D33', 'Future_Red_ISLTR': 'E33',  'Non_Red_ISLTR': 'F33'}

						elif IO_Type == iOType49231[0]:
							colMapping = {'Non_Red_IS': 'F41', 'Non_Red_NIS': 'F42', 'Non_Red_ISLTR': 'F43'}
						elif IO_Type == iOType49231[1]:
							colMapping = {'Non_Red_IS': 'F51', 'Non_Red_NIS': 'F52', 'Non_Red_ISLTR': 'F53'}
						elif IO_Type == iOType49231[2]:
							colMapping = {'Non_Red_IS': 'F61', 'Non_Red_NIS': 'F62', 'Non_Red_ISLTR': 'F63'}
						elif IO_Type == 'Series-C: AO (16) HART (0-5000)':
							module = '49233'
							colMapping = {'Red_IS': 'D71', 'Future_Red_IS': 'E71', 'Non_Red_IS': 'F71', 'Red_NIS': 'D72', 'Future_Red_NIS': 'E72', 'Non_Red_NIS': 'F72', 'Red_ISLTR': 'D73', 'Future_Red_ISLTR': 'E73',  'Non_Red_ISLTR': 'F73'}
						if changedColumn in colMapping.keys():
							GS_SerC_Container_Event.changeCellEvent(Product, IO_Family_Type, IO_Type, changedColumn, GS_C300_IO_Calc.getFloat(newValue), module, colMapping)
	#Product.ParseString('<* ExecuteScript(PS_Series_C_RG_Part_Summary_Cont_update_parts) *>')
	#Product.GetContainerByName('Series_C_RG_Part_Summary_Cont').Calculate()

	if IO_Family_Type == 'Series-C Mark II':
		#container = EventArgs.Container
		#changedCell = EventArgs.ChangedCell
		#oldValue = changedCell.OldValue
		#newValue = changedCell.NewValue
		#changedColumn = changedCell.ColumnName
		#rowIndex = changedCell.RowIndex
		#row = container.Rows[rowIndex]
		iOType = ['SCM: DI (32) 110 VAC (0-5000)', 'SCM: DI (32) 220 VAC (0-5000)']
		iOType2 = ['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)', 'SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)', 'SCM: DO (32) 24VDC Relay Bus above 30V (0-5000)', 'SCM: DO (32) 24VDC Relay Bus up to 30V (0-5000)']
		iOType3 = ['SCM: Pulse Input (8) Single Channel (0-5000)', 'SCM: Pulse Input (4) Dual Channel (0-5000)', 'SCM: Pulse Input (2) Fast Cut Off Channel (0-5000)']

		get_cont = Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1')
		for row in get_cont.Rows:
			for col in row.Columns:
				if col.Value not in ["0", ""] and col.Name not in ['IO_Type', 'IO_Type_with_hint']:
					IO_Type = row['IO_Type']
					if IO_Type in iOType:
						module = '44474'
					elif IO_Type in iOType2:
						module = '44488'
					elif IO_Type in iOType3:
						module = '44490'
					if IO_Type == 'SCM: DI (32) 110 VAC (0-5000)':
						colMapping = {'Non_Red_NIS': 'I12'}
					elif IO_Type == 'SCM: DI (32) 220 VAC (0-5000)':
						colMapping = {'Non_Red_NIS': 'I32'}
					elif IO_Type == 'SCM: DO (32) 24VDC Bus External Power Supply (0-5000)':
						colMapping = {'Red_IS': 'G41', 'Future_Red_IS': 'H41', 'Non_Red_IS': 'I41', 'Red_NIS': 'G42', 'Future_Red_NIS': 'H42', 'Non_Red_NIS': 'I42', 'Red_ISLTR': 'G43', 'Future_Red_ISLTR': 'H43',  'Non_Red_ISLTR': 'I43', 'Red_RLY': 'G44', 'Future_Red_RLY': 'H44', 'Non_Red_RLY': 'I44'}
					elif IO_Type == 'SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)':
						colMapping = {'Red_IS': 'G51', 'Future_Red_IS': 'H51', 'Non_Red_IS': 'I51', 'Red_NIS': 'G52', 'Future_Red_NIS': 'H52', 'Non_Red_NIS': 'I52', 'Red_ISLTR': 'G53', 'Future_Red_ISLTR': 'H53',  'Non_Red_ISLTR': 'I53', 'Red_RLY': 'G54', 'Future_Red_RLY': 'H54', 'Non_Red_RLY': 'I54'}
					elif IO_Type == 'SCM: DO (32) 24VDC Relay Bus above 30V (0-5000)':
						colMapping = {'Red_RLY': 'G64', 'Future_Red_RLY': 'H64', 'Non_Red_RLY': 'I64'}
					elif IO_Type == 'SCM: DO (32) 24VDC Relay Bus up to 30V (0-5000)':
						colMapping = {'Red_RLY': 'G74', 'Future_Red_RLY': 'H74', 'Non_Red_RLY': 'I74'}
					elif IO_Type == 'SCM: Pulse Input (8) Single Channel (0-5000)':
						colMapping = {'Red_IS': 'G81', 'Future_Red_IS': 'H81', 'Red_NIS': 'G82', 'Future_Red_NIS': 'H82', 'Red_ISLTR': 'G83', 'Future_Red_ISLTR': 'H83'}
					elif IO_Type == 'SCM: Pulse Input (4) Dual Channel (0-5000)':
						colMapping = {'Red_IS': 'G91', 'Future_Red_IS': 'H91', 'Red_NIS': 'G92', 'Future_Red_NIS': 'H92', 'Red_ISLTR': 'G93', 'Future_Red_ISLTR': 'H93'}
					elif IO_Type == 'SCM: Pulse Input (2) Fast Cut Off Channel (0-5000)':
						colMapping = {'Red_IS': 'J11', 'Future_Red_IS': 'K11', 'Red_NIS': 'J12', 'Future_Red_NIS': 'K12', 'Red_ISLTR': 'J13', 'Future_Red_ISLTR': 'K13'}
					#Log.Info("colMapping " +str(len(colMapping))) 
					parts_dict = dict()
					if len(colMapping) > 0 and col.Name in colMapping.keys():
						changedcolumns = col.Name
						newValue = col.Value
						if newValue > 0:
							if module == '44474':
								GS_C300_IO_Calc.calcIOModule44474(Product, IO_Type, changedcolumns, GS_C300_IO_Calc.getFloat(newValue))
								parts_dict = GS_C300_IO_Calc.getParts44474(Product, parts_dict)
							elif module == '44488':
								GS_C300_IO_Calc2.calcIOModule44488(Product, IO_Type, changedcolumns, GS_C300_IO_Calc.getFloat(newValue))
								parts_dict = GS_C300_IO_Calc2.getParts44488(Product, parts_dict)
							elif module == '44490':
								GS_C300_IO_Calc2.calcIOModule44490(Product, IO_Type, changedcolumns, GS_C300_IO_Calc.getFloat(newValue))
								parts_dict = GS_C300_IO_Calc2.getParts44490(Product, parts_dict)
								Log.Info("parts_dict cell edit 4490=> "+str(parts_dict))
							Log.Info("parts_dict cell edit 88 REMOTE=> "+str(parts_dict))
					if len(parts_dict) > 0:
						Log.Info("parts_dict cell edit REMOTE=> "+str(parts_dict))
						GS_C300_IO_Calc.setIOCount(Product, 'Series_C_RG_Part_Summary', parts_dict)
						#Product.ParseString('<* ExecuteScript(PS_Series_C_RG_Part_Summary_Cont_update_parts) *>')
						#ScriptExecutor.Execute('PS_Series_C_RG_Part_Summary_Cont_update_parts')
						Product.GetContainerByName('Series_C_RG_Part_Summary_Cont').Calculate()
					# if IO_Type == 'SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)' and changedcolumns == 'Non_Red_ISLTR':
					# 	Log.Info('Internal Power Supply = '+str(col.Value)+' row value = '+str(row[changedcolumns]))'''

	get_Turbo_RM_cont = Product.GetContainerByName('C300_TurboM_IOM_RG_Cont')
	if get_Turbo_RM_cont.Rows.Count > 0:
		for row in get_Turbo_RM_cont.Rows:
			for col in row.Columns:
				if col.Value not in ["0", ""] and col.Name not in ['IO_Type']:
					IO_Type = row['IO_Type']
					module = '49227'
					IO_Family_Type = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
					part_list = []
					param_list = []
					changedcolumns = col.Name
					newValue = col.Value
					if IO_Type == 'Number of Servo Position Modules (0-480)':
						part_list = ['CC-PSV201', 'CC-TSV211']
						colMapping = {'Red_IOM': 'A11'}
					elif IO_Type == 'Number of Speed Protection Modules (0-480)':
						part_list = ['CC-PSP401','CC-TSP411']
						colMapping = {'Red_IOM': 'A21'}
					if len(part_list) > 0 and changedcolumns in colMapping.keys():
						GS_SerC_Container_Event.changeCellEvent(Product, IO_Family_Type, IO_Type, changedcolumns, newValue, module, colMapping)

	# get_UIO_RM_cont = Product.GetContainerByName('C300_RG_Universal_IO_cont_1')
	# if get_UIO_RM_cont.Rows.Count > 0:
	# 	for row in get_UIO_RM_cont.Rows:
	# 		for col in row.Columns:
	# 			if col.Value not in ["0", ""] and col.Name not in ['IO_Type','IO_Type_with_hint']:
	# 				IO_Type = row['IO_Type']
	# 				colMapping = dict()
	# 				module = ''
	# 				changedcolumns = col.Name
	# 				newValue = col.Value
	# 				if IO_Family_Type == 'Series C':
	# 					pass
	# 				elif IO_Family_Type == 'Turbomachinery':
	# 					ioTypes49228 = ['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)', 'Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)']
	# 					ioTypes49228.extend(['Series-C: UIO (32) Analog Output (0-5000)'])
	# 					if IO_Type in ioTypes49228:
	# 						module = '49228'
	# 					if IO_Type == 'Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)':
	# 						colMapping = {'Red_IS': 'A61', 'Future_Red_IS': 'B61', 'Non_Red_IS': 'C61', 'Red_NIS': 'A62', 'Future_Red_NIS': 'B62', 'Non_Red_NIS': 'C62', 'Red_ISLTR': 'A63', 'Future_Red_ISLTR': 'B63',  'Non_Red_ISLTR': 'C63'}
	# 					elif IO_Type == 'Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)':
	# 						colMapping = {'Red_ISLTR': 'A73', 'Future_Red_ISLTR': 'B73',  'Non_Red_ISLTR': 'C73'}
	# 					elif IO_Type == 'Series-C: UIO (32) Analog Output (0-5000)':
	# 						colMapping = {'Red_IS': 'A81', 'Future_Red_IS': 'B81', 'Non_Red_IS': 'C81', 'Red_NIS': 'A82', 'Future_Red_NIS': 'B82', 'Non_Red_NIS': 'C82', 'Red_ISLTR': 'A83', 'Future_Red_ISLTR': 'B83',  'Non_Red_ISLTR': 'C83'}
	# 					if changedcolumns in colMapping.keys():
	# 						GS_SerC_Container_Event.changeCellEvent(Product, IO_Family_Type, IO_Type, changedcolumns, GS_C300_IO_Calc.getFloat(newValue), module, colMapping)

	get_UIO2_RM_cont = Product.GetContainerByName('C300_RG_Universal_IO_cont_2')
	if get_UIO2_RM_cont.Rows.Count > 0:
		for row in get_UIO2_RM_cont.Rows:
			for col in row.Columns:
				if col.Value not in ["0", ""] and col.Name not in ['IO_Type','IO_Type_with_hint']:
					IO_Type = row['IO_Type']
					colMapping = dict()
					module = ''
					changedcolumns = col.Name
					newValue = col.Value
					if IO_Family_Type == 'Series C':
						pass
					elif IO_Family_Type == 'Turbomachinery':
						ioTypes49228 = ['Series-C: UIO (32) Digital Input (0-5000)', 'Series-C: UIO (32) Digital Output (0-5000)']
						if IO_Type in ioTypes49228:
							module = '49228'
						if IO_Type == 'Series-C: UIO (32) Digital Input (0-5000)':
							colMapping = {'Red_IS': 'A91', 'Future_Red_IS': 'B91', 'Non_Red_IS': 'C91', 'Red_NIS': 'A92', 'Future_Red_NIS': 'B92', 'Non_Red_NIS': 'C92', 'Red_ISLTR': 'A93', 'Future_Red_ISLTR': 'B93',  'Non_Red_ISLTR': 'C93', 'Red_RLY': 'A94', 'Future_Red_RLY': 'B94', 'Non_Red_RLY': 'C94'}
						elif IO_Type == 'Series-C: UIO (32) Digital Output (0-5000)':
							colMapping = {'Red_IS': 'D11', 'Future_Red_IS': 'E11', 'Non_Red_IS': 'F11', 'Red_NIS': 'D12', 'Future_Red_NIS': 'E12', 'Non_Red_NIS': 'F12', 'Red_ISLTR': 'D13', 'Future_Red_ISLTR': 'E13',  'Non_Red_ISLTR': 'F13', 'Red_RLY': 'D14', 'Future_Red_RLY': 'E14', 'Non_Red_RLY': 'F14'}
						if changedcolumns in colMapping.keys():
							GS_SerC_Container_Event.changeCellEvent(Product, IO_Family_Type, IO_Type, changedcolumns, GS_C300_IO_Calc.getFloat(newValue), module, colMapping)
	#C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont,C300_CG_Universal_IO_Mark_1,C300_CG_Universal_IO_Mark_2 - not needed