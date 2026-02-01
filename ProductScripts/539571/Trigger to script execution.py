import GS_C300_IO_Calc, GS_SerC_Container_Event, GS_C300_IO_Calc2
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
	IO_Family_Type = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	get_cont = Product.GetContainerByName('C300_RG_Universal_IO_cont_1')
	changedcolumns = ['Red_IS', 'Future_Red_IS', 'Non_Red_IS', 'Red_NIS', 'Future_Red_NIS', 'Non_Red_NIS', 'Red_ISLTR', 'Future_Red_ISLTR','Non_Red_ISLTR'] 
	module = ''
	colMapping = dict()
	def valueassign(changedColumns,newValue,colMapping,IO_Type):
		if changedColumns in colMapping.keys():
			#Log.Info("CC===>>>  "+str(changedColumns)+"     VAL===>>> "+str(newValue)+"     colMapping===>>> "+str(colMapping))
			GS_SerC_Container_Event.changeCellEvent(Product, IO_Family_Type, IO_Type, changedColumns, GS_C300_IO_Calc.getFloat(newValue), module, colMapping)

	for row in get_cont.Rows:
		Io_Type = row['IO_Type']
		for col in row.Columns:
			if col.Value not in  ["0", ""] and col.Name not in ['IO_Type', 'IO_Type_with_hint']:
				ioTypes49228 = ['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)', 'Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)']
				ioTypes49228.extend(['Series-C: UIO (32) Analog Output (0-5000)'])
				if Io_Type in ioTypes49228:
					module = '49228'
				if Io_Type == 'Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)':
					colMapping = {'Red_IS': 'A61', 'Future_Red_IS': 'B61', 'Non_Red_IS': 'C61', 'Red_NIS': 'A62', 'Future_Red_NIS': 'B62', 'Non_Red_NIS': 'C62', 'Red_ISLTR': 'A63', 'Future_Red_ISLTR': 'B63',  'Non_Red_ISLTR': 'C63'}
					#Trace.Write(str(Io_Type)+'---Io_Type---'+str(col.Name)+"--col----"+str(col.Value))
					valueassign(col.Name,col.Value,colMapping,Io_Type)
				elif Io_Type == 'Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)':
					colMapping = {'Red_ISLTR': 'A73', 'Future_Red_ISLTR': 'B73',  'Non_Red_ISLTR': 'C73'}
					valueassign(col.Name,col.Value,colMapping,Io_Type)
				elif Io_Type == 'Series-C: UIO (32) Analog Output (0-5000)':
					colMapping = {'Red_IS': 'A81', 'Future_Red_IS': 'B81', 'Non_Red_IS': 'C81', 'Red_NIS': 'A82', 'Future_Red_NIS': 'B82', 'Non_Red_NIS': 'C82', 'Red_ISLTR': 'A83', 'Future_Red_ISLTR': 'B83',  'Non_Red_ISLTR': 'C83'}
					valueassign(col.Name,col.Value,colMapping,Io_Type)
	Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
	#Log.Write('---product script -PERF_ExecuteScripts-' + str(Product.Attr('PERF_ExecuteScripts').GetValue()))
					

	"""IO_Family_Type = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	if IO_Family_Type == 'Series-C Mark II':
		container = EventArgs.Container
		changedCell = EventArgs.ChangedCell
		oldValue = changedCell.OldValue
		newValue = changedCell.NewValue
		changedColumn = changedCell.ColumnName
		rowIndex = changedCell.RowIndex
		row = container.Rows[rowIndex]
		iOType = ['SCM: DI (32) 110 VAC (0-5000)', 'SCM: DI (32) 220 VAC (0-5000)']
		iOType2 = ['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)', 'SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)', 'SCM: DO (32) 24VDC Relay Bus above 30V (0-5000)', 'SCM: DO (32) 24VDC Relay Bus up to 30V (0-5000)']
		iOType3 = ['SCM: Pulse Input (8) Single Channel (0-5000)', 'SCM: Pulse Input (4) Dual Channel (0-5000)', 'SCM: Pulse Input (2) Fast Cut Off Channel (0-5000)']
		
		get_cont = Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1')
		for row in get_cont.Rows:
			for col in row.Columns:
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
				parts_dict = dict()
				if len(colMapping) > 0 and changedcolumns in colMapping.keys():
					if col.Value > 0:
						if module == '44474':
							GS_C300_IO_Calc.calcIOModule44474(Product, IO_Type, changedcolumns, GS_C300_IO_Calc.getFloat(col.Value))
							parts_dict = GS_C300_IO_Calc.getParts44474(Product, parts_dict)
						elif module == '44488':
							GS_C300_IO_Calc2.calcIOModule44488(Product, IO_Type, changedcolumns, GS_C300_IO_Calc.getFloat(col.Value))
							parts_dict = GS_C300_IO_Calc2.getParts44488(Product, parts_dict)
						elif module == '44490':
							GS_C300_IO_Calc2.calcIOModule44490(Product, IO_Type, changedcolumns, GS_C300_IO_Calc.getFloat(col.Value))
							parts_dict = GS_C300_IO_Calc2.getParts44490(Product, parts_dict)
				if len(parts_dict) > 0:
					GS_C300_IO_Calc.setIOCount(Product, 'Series_C_RG_Part_Summary', parts_dict)
					ScriptExecutor.Execute('PS_Series_C_RG_Part_Summary_Cont_update_parts')
					Product.GetContainerByName('Series_C_RG_Part_Summary_Cont').Calculate()
				if IO_Type == 'SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)' and changedcolumns == 'Non_Red_ISLTR':
					Log.Info('Internal Power Supply = '+str(col.Value)+' row value = '+str(row[changedcolumns]))"""
		