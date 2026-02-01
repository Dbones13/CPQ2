from GS_R2Q_SafetyManagerContainerColumns import SafetyManagerContainerColumns as SMCC

Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
deletionRows = {'SM_IO_Count_Digital_Input_Cont':[], 'SM_IO_Count_Digital_Output_Cont':[], 'SM_IO_Count_Analog_Input_Cont':[]}
marCab = ''
if Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left') and Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows and Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows.Count > 0:
	marCab = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue

if Product.GetContainerByName('Number_SM_Remote_Groups_Cont') and Product.GetContainerByName('Number_SM_Remote_Groups_Cont').Rows and Product.GetContainerByName('Number_SM_Remote_Groups_Cont').Rows.Count > 0:
	label = Product.GetContainerByName('Number_SM_Remote_Groups_Cont').Rows[0]
	label.GetColumnByName('Number_SM_Remote_Groups').HeaderLabel = "Number of Remote Groups for SM Control Groups (0-10)"

if Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right') and Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows and Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows.Count > 0:
	label = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0]
	label.GetColumnByName('Percent_Installed_Spare_IOs').HeaderLabel = "Percent Installed Spare IOs (0-100%)"

def hideContainerColumns():
	for contColumn in SMCC.cgNonR2QContColumn:
		for col in SMCC.cgNonR2QContColumn[contColumn]:
			Product.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))

def deleteRows():
	for cont, col in deletionRows.items():
		for rowInd in sorted(col, reverse = True):
			Product.GetContainerByName(cont).DeleteRow(rowInd)

for cont, colName in SMCC.cgContainersAndRows.items():
	for row in Product.GetContainerByName(cont).Rows:
		if row[colName] in SMCC.cgContainersAndColumns.get(cont):
			deletionRows[cont].append(row.RowIndex)

hideContainerColumns()
deleteRows()

'''if marCab in ['Universal Marshalling', 'Universal_Marshalling']:
	pssmc = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('SM_CG_Percentage_SSM_Cabinet(0-100%)').Value
	umcpssc = Product.GetContainerByName('SM_CG_Universal_Marshalling_Cabinet_Details')
	umcpssc.Rows[0]['Percentage of Spare Space'] = pssmc
	Product.ParseString('<*CTX( Container(SM_CG_Cabinet_Details_Cont_Left).Column(SM_CG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(SM_CG_Cabinet_Details_Cont_Left).Column(SM_CG_RelayTypeForESD).SetPermission(Hidden) )*>')
elif marCab in ['Hardware Marshalling with Other', 'Hardware_Marshalling_with_Other']:
	Product.ParseString('<*CTX( Container(SM_CG_Cabinet_Details_Cont_Left).Column(SM_CG_RelayTypeForESD).SetPermission(Editable) )*>')'''

if marCab in ['Universal Marshalling','Universal_Marshalling']:
	Product.ParseString('<*CTX( Container(SM_CG_Cabinet_Details_Cont_Left).Column(SM_CG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(SM_CG_Cabinet_Details_Cont_Left).Column(SM_CG_RelayTypeForESD).SetPermission(Hidden) )*>')
elif marCab in ['Hardware Marshalling with Other', 'Hardware_Marshalling_with_Other']:
	Product.ParseString('<*CTX( Container(SM_CG_Cabinet_Details_Cont_Left).Column(SM_CG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(SM_CG_Cabinet_Details_Cont_Left).Column(SM_CG_RelayTypeForESD).SetPermission(Editable) )*>')
elif marCab != '':
	Product.ParseString('<*CTX( Container(SM_CG_Cabinet_Details_Cont_Left).Column(SM_CG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(SM_CG_Cabinet_Details_Cont_Left).Column(SM_CG_RelayTypeForESD).SetPermission(Hidden) )*>')

'''get_cont_avail = True if Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left') else False

if get_cont_avail:
	#cabinet_Q_Visibility,Cabinet_Q_Visibility2
	get_cont = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows
	for row in get_cont:
		if row['Marshalling_Option'] =='Hardware Marshalling with P+F':
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Left', 'Fault_Contact_GIIS_Integration_Boards'))
		elif row['Marshalling_Option'] =='Universal Marshalling':
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI_SIL1_Relay_5K_resistor_Adapter_UMC'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI/DO_SIL2/3_Relay_Adapter_UMC'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI_NAMUR_proximity_Switches_Adapter_UMC'))
		else:
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Left', 'Fault_Contact_GIIS_Integration_Boards'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI_SIL1_Relay_5K_resistor_Adapter_UMC'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI/DO_SIL2/3_Relay_Adapter_UMC'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'DI_NAMUR_proximity_Switches_Adapter_UMC'))

	get_cont_2 = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows
	for row in get_cont_2:
		if row['SM_Switch_Safety_IO'] =='Control Network Module (CNM)':
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Common_Questions_Cont', 'SM_CNM_Switch_Network_IOTA'))
		if row['SM_Universal_IOTA'] =='RUSIO':
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'SDO_2_24Vdc1A_UIO_Unit_Load_501mA_1000mA'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'SDO_4_24Vdc2A_UIO_Unit_Load_1001mA_2000mA'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Input_UIO_Redundant'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Inpu_UIO'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Input_DIO_Redundant'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Editable) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Input_DIO'))
		else:
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Common_Questions_Cont', 'SM_CNM_Switch_Network_IOTA'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'SDO_2_24Vdc1A_UIO_Unit_Load_501mA_1000mA'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'SDO_4_24Vdc2A_UIO_Unit_Load_1001mA_2000mA'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Input_UIO_Redundant'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Inpu_UIO'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Input_DIO_Redundant'))
			Product.ParseString('<CTX( Container({}).Column({}).SetPermission(Hidden) )>'.format('SM_CG_Cabinet_Details_Cont_Right', 'Shutdown_Input_DIO'))

	container_columns_1 = {"SM_CG_DI_RLY_NMR_Cont":["Red_SIL2_RLY","Non_Red_SIL2_RLY","Red_SIL3_RLY","Non_Red_SIL3_RLY","Red_NMR","Non_Red_NMR","Red_NMR_Safety","Non_Red_NMR_Safety"],"SM_CG_DO_RLY_NMR_Cont":["Red_SIL2_RLY","Non_Red_SIL2_RLY","Red_SIL3_RLY","Non_Red_SIL3_RLY","Red_NMR","Non_Red_NMR","Red_NMR_Safety","Non_Red_NMR_Safety"]}
	container_columns_2_1 = {"SM_CG_DI_RLY_NMR_Cont":["Red_SIL2_RLY","Non_Red_SIL2_RLY","Red_SIL3_RLY","Non_Red_SIL3_RLY"],"SM_CG_DO_RLY_NMR_Cont":["Red_SIL2_RLY","Non_Red_SIL2_RLY","Red_SIL3_RLY","Non_Red_SIL3_RLY"]}
	container_columns_2_2 = {"SM_CG_DI_RLY_NMR_Cont":["Red_NMR","Non_Red_NMR","Red_NMR_Safety","Non_Red_NMR_Safety"],"SM_CG_DO_RLY_NMR_Cont":["Red_NMR","Non_Red_NMR","Red_NMR_Safety","Non_Red_NMR_Safety"]}
	get_cont_avail_2 = True if Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right') else False
	
	if get_cont_avail_2:
		get_cont_value_1 = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Right").Rows[0].GetColumnByName("DI/DO_SIL2/3_Relay_Adapter_UMC").Value
		get_cont_value_2 = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Right").Rows[0].GetColumnByName("DI_NAMUR_proximity_Switches_Adapter_UMC").Value
		#DIDO_RLY_NMR_Case1
		if get_cont_value_1 == 'Yes' and get_cont_value_2 == 'Yes':
			Product.Attr('SM_CG_DI_RLY_NMR_Case').AssignValue('1|DI / DO for SIL 2/ 3 Relay and NAMUR')
			editenableContainerColumns(container_columns_1)
			hideContainerColumns(container_columns_1, 'Editable')
		#DIDO_RLY_NMR_Case2   
		elif get_cont_value_1 == 'Yes' and get_cont_value_2 in ['NO','']:
			Product.Attr('SM_CG_DI_RLY_NMR_Case').AssignValue('2|DI / DO for SIL 2/ 3 Relay')
			hideContainerColumns(container_columns_1, 'Editable')
			hideContainerColumns(container_columns_1, 'Hidden')
		#DIDO_RLY_NMR_Case3
		elif get_cont_value_1 in ['NO',''] and get_cont_value_2 == 'Yes':
			Product.Attr('SM_CG_DI_RLY_NMR_Case').AssignValue('3|DI / DO for SIL 2/ 3 NAMUR')
			hideContainerColumns(container_columns_2_1, 'Hidden')
			hideContainerColumns(container_columns_2_2, 'Editable')
		#DIDO_RLY_NMR_Case4
		elif get_cont_value_1 in ['NO',''] and get_cont_value_2 in ['NO','']:
			Product.Attr('SM_CG_DI_RLY_NMR_Case').AssignValue('4')
			hideContainerColumns(container_columns_1, 'Hidden')'''


#ScriptExecutor.ExecuteGlobal('CQSHOWHIDE',{'product_name':'R2Q SM Control Group','func_call':'Hidden'})
# added for CXCPQ-95051 and CXCPQ-94838