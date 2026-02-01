from GS_R2Q_SafetyManagerContainerColumns import SafetyManagerContainerColumns as SMCC

Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
rgDeletionRows = {'SM_RG_IO_Count_Digital_Input_Cont': [], 'SM_RG_IO_Count_Digital_Output_Cont': [], 'SM_RG_IO_Count_Analog_Input_Cont': []}

if Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont') and Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows and Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows.Count > 0:
	label = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0]
	label.GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').HeaderLabel = "Number of SMSC Universal Safety Cabinets 1.3M (0-63)"

def hideContainerColumns():
	for contColumn in SMCC.rgNonR2QContColumn:
		for col in SMCC.rgNonR2QContColumn[contColumn]:
			Product.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))

def deleteRows():
	for cont, col in rgDeletionRows.items():
		for rowInd in sorted(col, reverse = True):
			Product.GetContainerByName(cont).DeleteRow(rowInd)

for cont, colName in SMCC.rgContainersAndRows.items():
	if Product.GetContainerByName(cont) and Product.GetContainerByName(cont).Rows and Product.GetContainerByName(cont).Rows.Count > 0:
		for row in Product.GetContainerByName(cont).Rows:
			if row[colName] in SMCC.rgContainersAndColumns.get(cont):
				rgDeletionRows[cont].append(row.RowIndex)

hideContainerColumns()
deleteRows()

if Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left') and Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows.Count > 0:
	marCab = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
	'''if marCab in ['Hardware Marshalling with Other', 'Hardware_Marshalling_with_Other']:
		Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Editable) )*>')
		Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_RelayTypeForESD).SetPermission(Editable) )*>')
	else:
		Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('SM_RG_RelayTypeForESD').SetAttributeValue('Non SIL')'''
	
	if marCab in ['Universal Marshalling', 'Universal_Marshalling']:
		Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Editable) )*>')
		Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_Percent_Installed_Spare_IO).SetPermission(Editable) )*>')
		Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_RelayTypeForESD).SetPermission(Hidden) )*>')
		Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('SM_RG_RelayTypeForESD').SetAttributeValue('Non SIL')
	elif marCab in ['Hardware Marshalling with Other', 'Hardware_Marshalling_with_Other']:
		Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Editable) )*>')
		Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_RelayTypeForESD).SetPermission(Editable) )*>')
	else:
		Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Hidden) )*>')
		Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_Percent_Installed_Spare_IO).SetPermission(Hidden) )*>')
		Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_RelayTypeForESD).SetPermission(Hidden) )*>')
		Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('SM_RG_RelayTypeForESD').SetAttributeValue('Non SIL')
'''
Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))

if Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont') and Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows.Count > 0:
	Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('S300').SetAttributeValue('No S300')

if Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left') and Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows.Count > 0:
	Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('SM_RG_RelayTypeForESD').SetAttributeValue('Non SIL')

if Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont') and Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows.Count > 0:
	label = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0]
	label.GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').HeaderLabel = "Number of SMSC  Universal Safety Cabinets 1.3M (0-63)"

marCab = ''
if Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left') and Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows.Count > 0:
	marCab = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
if marCab in ['Hardware Marshalling with Other', 'Hardware_Marshalling_with_Other']:
	Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_RelayTypeForESD).SetPermission(Editable) )*>')
else:
	if Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows.Count > 0:
		Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('SM_RG_RelayTypeForESD').SetAttributeValue('Non SIL')
'''

#hideContainerColumns()
#deleteRows()
def setDisplayType():
    di_cont = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_1.3_Cabinet_Cont')
    ai_cont = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_1.3_Cabinet_Cont')
    if di_cont.Rows.Count == 0 and ai_cont.Rows.Count == 0:
        uio_row = di_cont.AddNewRow(); dio_row = di_cont.AddNewRow()
        uio_row['Digital_Input/Output_Type'] = "SDI(1) 24Vdc UIO (0-5000)"
        dio_row['Digital_Input/Output_Type'] = "SDO(1) 24Vdc 500mA UIO (0-5000)"
        #di_cont.Calculate()
        # Add Two Rows DO
        uio_row = ai_cont.AddNewRow(); dio_row = ai_cont.AddNewRow()
        uio_row['Analog_Input/Output_Type'] = "SAI(1)mA type Current UIO (0-5000)"
        dio_row['Analog_Input/Output_Type'] = "SAO(1)mA Type UIO (0-5000)"

Enclosure_Type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').Value
if Enclosure_Type == "Universal Safety Cab-1.3M":
    setDisplayType()