def deleteRows():
    try:
        #Trace.Write("Deleted rows index="+str(rgDeletionRows.items(rgDeletionRows)))
        for cont, col in rgDeletionRows.items(rgDeletionRows):
            for rowInd in sorted(col, reverse = True):
                Product.GetContainerByName(cont).DeleteRow(rowInd)
    except:
        Trace.Write("Error")
'''if Product.Name == 'R2Q SM Remote Group':
	def deleteRows(dic):
		for cont, col in dic.items():
			for rowInd in sorted(col, reverse = True):
				Product.GetContainerByName(cont).DeleteRow(rowInd)

	def hideContainerColumns(contColumnList, access):
		for contColumn in contColumnList:
			for col in contColumnList[contColumn]:
				Product.ParseString('<*CTX( Container({0}).Column({1}).SetPermission({2}) )*>'.format(contColumn, col, access))

	hideShowConcol = [{"SM_RG_Universal_Safety_Cabinet_1.3M_Cont":['Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)'], "SM_SC_Universal_Safety_Cab_1_3M_Details_cont":['S300', 'PUIO_Count', 'PDIO_Count']},{"SM_RG_Cabinet_Details_Cont":['SM_Percent_Installed_Spare_IO'], "SM_RG_Cabinet_Details_Cont_Left":['Marshalling_Option', 'SM_RG_RelayTypeForESD', 'SM_RG_Percentage_SSM_Cabinet(0-100%)']}]

	access = ["Hidden", "Editable"]
	atex = True if Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue == 'Universal Safety Cab-1.3M' else False
	if atex:
		access[0] = "Editable"
		access[1] = "Hidden"

	for container, acs in zip(hideShowConcol, access):
		hideContainerColumns(container, acs)

	enclosure_type =  Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').Value
	Product.Attr('SM_RG_Enclosure_Type').AssignValue(enclosure_type)
	marCab = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
	if not atex:
		if marCab == 'Universal Marshalling':
			Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Editable) )*>')
			Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_RelayTypeForESD).SetPermission(Hidden) )*>')
		elif marCab == 'Hardware Marshalling with Other':
			Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('SM_RG_RelayTypeForESD').SetAttributeValue('Non SIL')
			Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Editable) )*>')
			Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_RelayTypeForESD).SetPermission(Editable) )*>')
		else:
			Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Hidden) )*>')
			Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_RelayTypeForESD).SetPermission(Hidden) )*>')

	# added for CXCPQ-94838 and CXCPQ-95051
	deletionRows = {'SM_RG_IO_Count_Digital_Input_Cont':[], 'SM_RG_IO_Count_Digital_Output_Cont':[], 'SM_RG_IO_Count_Analog_Input_Cont':[]}

	containersAndRows = {'SM_RG_IO_Count_Digital_Input_Cont':'Digital_Input_Type', 'SM_RG_IO_Count_Digital_Output_Cont':'Digital_Output_Type', 'SM_RG_IO_Count_Analog_Input_Cont':'Analog_Input_Type'}

	containersAndColumns = {'SM_RG_IO_Count_Digital_Input_Cont':("SDI(1) 24Vdc with 5K Resistor DIO  (0-5000)", "SDI(1) 24Vdc with 5K Resistor UIO  (0-5000)", "SDI(1) 24Vdc Line Mon DIO (0-5000)", "SDI(1) 24Vdc Line Mon UIO  (0-5000)"), 'SM_RG_IO_Count_Digital_Output_Cont':("SDO(16) SIL 2/3 250Vac/Vdc COM DIO  (0-5000)", "SDO(16) SIL 2/3 250Vac/Vdc DIO  (0-5000)", "SDO(16) SIL 2/3 250Vac/Vdc COM UIO  (0-5000)", "SDO(16) SIL 2/3 250Vac/Vdc UIO   (0-5000)", "SDO(7) 24Vdc Line Mon UIO  (0-5000)", "SDO(4)24Vdc 2A UIO  (0-5000)", "SDO(2)24Vdc 1A UIO  (0-5000)"), 'SM_RG_IO_Count_Analog_Input_Cont':("SAI(1)FIRE 3-4 wire current  Sink UIO  (0-5000)", "SAI(1) GAS current  UIO  (0-5000)", "SAI(1)FIRE 3-4 wire current  UIO  (0-5000)", "SAI(1)FIRE 2 wire current  UIO   (0-5000)", "SDI(1) 24Vdc DIO  (0-5000)", "SDI(1)  24Vdc SIL3 P+F UIO  (0-5000)", "SDI(1)  24Vdc SIL2 P+F UIO  (0-5000)", "SDI(1) 24Vdc UIO  (0-5000)")}

	for cont, colName in containersAndRows.items():
		for row in Product.GetContainerByName(cont).Rows:
			if row[colName] in containersAndColumns.get(cont):
				deletionRows[cont].append(row.RowIndex)

	deleteRows(deletionRows)

	Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('S300').SetAttributeValue('No S300')'''

atex = True if Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont') and Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows and Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows.Count > 0 and Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0] and Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type') and Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue == 'Universal Safety Cab-1.3M' else False

enclosure_type =  Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').Value if Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont') and Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows and Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows.Count > 0 and Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0] and Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type') else ''

Product.Attr('SM_RG_Enclosure_Type').AssignValue(enclosure_type)

if atex:
	from GS_R2Q_SafetyManagerContainerColumns import SafetyManagerContainerColumns as SMCC

	rgDeletionRows = {'SM_RG_IO_Count_Digital_Input_Cont': [], 'SM_RG_IO_Count_Digital_Output_Cont': [], 'SM_RG_IO_Count_Analog_Input_Cont': []}

	'''if not atex:
		marCab = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue if Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left') and Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows and Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows.Count > 0 and Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0] and Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option') else ''
		if marCab in ['Universal Marshalling', 'Universal_Marshalling']:
			Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Editable) )*>')
			Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_RelayTypeForESD).SetPermission(Hidden) )*>')
		elif marCab in ['Hardware Marshalling with Other', 'Hardware_Marshalling_with_Other']:
			Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Editable) )*>')
			Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_RelayTypeForESD).SetPermission(Editable) )*>')
		elif marCab != '':
			Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Hidden) )*>')
			Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_RelayTypeForESD).SetPermission(Hidden) )*>')'''

	def hideContainerColumns():
		for contColumn in SMCC.rgNonR2QContColumn:
			for col in SMCC.rgNonR2QContColumn[contColumn]:
				Product.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))

	'''def deleteRows():
		for cont, col in rgDeletionRows.items():
			for rowInd in sorted(col, reverse = True):
				Product.GetContainerByName(cont).DeleteRow(rowInd)'''

	for cont, colName in SMCC.rgContainersAndRows.items():
		if Product.GetContainerByName(cont) and Product.GetContainerByName(cont).Rows and Product.GetContainerByName(cont).Rows.Count > 0:
			for row in Product.GetContainerByName(cont).Rows:
				if row[colName] in SMCC.rgContainersAndColumns.get(cont):
					rgDeletionRows[cont].append(row.RowIndex)

	hideContainerColumns()
	deleteRows()

if Product.GetContainerByName('SM_RG_Cabinet_Details_Cont') and Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows and Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows.Count > 0:
	label = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0]
	label.GetColumnByName('SM_Percent_Installed_Spare_IO').HeaderLabel = "Percent Installed Spare IOs (0-100%)"

if Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont') and Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows and Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows.Count > 0:
	label = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0]
	label.GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').HeaderLabel = "Number of SMSC Universal Safety Cabinets 1.3M (0-63)"
try:
    mar_opt = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').Value
    if not mar_opt:
        Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').Value="Universal_Marshalling"
except:
      mar_opt=''
Marshalling_option = mar_opt 
sm_rg_digital_ip =Product.GetContainerByName("SM_RG_IO_Count_Digital_Input_Cont").Rows
total_row =Product.GetContainerByName("SM_RG_IO_Count_Digital_Input_Cont").Rows.Count
delete_rows_column={"columns":("SDI(1) 24Vdc with 5K Resistor UIO  (0-5000)", "SDI(1) 24Vdc with 5K Resistor DIO  (0-5000)"), "indexes":[]}
if total_row:
    for i in sm_rg_digital_ip:
        if i["Digital_Input_Type"] in delete_rows_column["columns"]:
            delete_rows_column["indexes"].append(i.RowIndex)


    for rowInd in sorted(delete_rows_column["indexes"], reverse=True):
        Product.GetContainerByName("SM_RG_IO_Count_Digital_Input_Cont").DeleteRow(rowInd)
marCab = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue if (Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left') and Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows.Count >0) else ''
if marCab in ['Universal Marshalling', 'Universal_Marshalling']:
    Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Editable) )*>')
elif marCab in ("Hardware Marshalling with P+F", "Hardware_Marshalling_with_P+F"):
    Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Hidden) )*>')