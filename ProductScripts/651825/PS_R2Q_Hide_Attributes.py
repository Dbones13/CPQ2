def hideAttr(attrList):
	for attr in attrList:
		Product.Attr(attr).Access = AttributeAccess.Hidden

def hideContainerColumns(contColumnList):
	for contColumn in contColumnList:
		for col in contColumnList[contColumn]:
			Product.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))


def deleteRowsByCondition(container_name, io_types):
	cont = Product.GetContainerByName(container_name)
	rows_to_delete = [row.RowIndex for row in cont.Rows if row['IO_Type'] in io_types]
	for row_index in sorted(rows_to_delete, reverse=True):
		cont.DeleteRow(row_index)

def resetContainerColumns(contName, colList):
	for contRow in contName.Rows:
		for col in colList:
			contRow.GetColumnByName(col).SetAttributeValue('0')
			contRow.Product.Attr(col).AssignValue('0')
			contRow[col] = '0'
		contRow.Calculate()
		contRow.ApplyProductChanges()
	contName.Calculate()

nonR2QContColumn = {
	"SerC_CG_Enhanced_Function_IO_Cont": ["Future_Red_IS", "Future_Red_NIS", "Future_Red_ISLTR"],
	"SerC_CG_Enhanced_Function_IO_Cont2": ["Future_Red_IS", "Future_Red_NIS", "Future_Red_ISLTR", "future_red_rly", "Future_Red_HV_RLY"],
	"C300_CG_Universal_IO_cont_1": ["Future_Red_IS", "Future_Red_NIS", "Future_Red_ISLTR"],
	"C300_CG_Universal_IO_cont_2": ["Future_Red_IS", "Future_Red_NIS", "Future_Red_ISLTR", "future_red_rly", "Future_Red_HV_RLY"],
	"SerC_CG_FIM_FF_IO_Cont": ["Future_Red_wo_C300", "Future_Red_C300"]
}

nonR2QContColumn2 = {
	"C300_CG_Universal_IO_Mark_1": ["Future_Red_IS", "Future_Red_NIS", "Future_Red_ISLTR"],
	"C300_CG_Universal_IO_Mark_2": ["Future_Red_IS", "Future_Red_NIS", "Future_Red_ISLTR", "future_red_rly", "Future_HV_Rly"],
	"C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont": ["Future_Red_IS", "Future_Red_NIS", "Future_Red_ISLTR"],
	"C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1": ["Future_Red_IS", "Future_Red_NIS", "Future_Red_ISLTR", "future_red_rly", "Future_HV_Rly"],
	"SerC_CG_FIM_FF_IO_Cont": ["Future_Red_wo_C300", "Future_Red_C300"]
}

if Product.Attr('SerC_CG_Marshalling_Cabinet_Type').GetValue() == "3rd Party Marshalling":
	Product.ParseString('<*CTX( Container(SerC_CG_Enhanced_Function_IO_Cont2).Column(Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(SerC_CG_Enhanced_Function_IO_Cont2).Column(Non_Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_Mark_2).Column(Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_Mark_2).Column(Non_Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_cont_2).Column(Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_cont_2).Column(Non_Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1).Column(Red_HV_Rly).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1).Column(Non_Red_HV_Rly).SetPermission(Hidden) )*>')
	resetContainerColumns(Product.GetContainerByName("SerC_CG_Enhanced_Function_IO_Cont2"), ['Red_HV_RLY', 'Non_Red_HV_RLY'])
	resetContainerColumns(Product.GetContainerByName("C300_CG_Universal_IO_Mark_2"), ['Red_HV_RLY', 'Non_Red_HV_RLY'])
	resetContainerColumns(Product.GetContainerByName("C300_CG_Universal_IO_cont_2"), ['Red_HV_RLY', 'Non_Red_HV_RLY'])
	resetContainerColumns(Product.GetContainerByName("C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1"), ['Red_HV_RLY', 'Non_Red_HV_RLY'])
else:
	Product.ParseString('<*CTX( Container(SerC_CG_Enhanced_Function_IO_Cont2).Column(Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(SerC_CG_Enhanced_Function_IO_Cont2).Column(Non_Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_Mark_2).Column(Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_Mark_2).Column(Non_Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_cont_2).Column(Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_CG_Universal_IO_cont_2).Column(Non_Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1).Column(Red_HV_Rly).SetPermission(Editable) )*>')
	Product.ParseString('<*CTX( Container(C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1).Column(Non_Red_HV_Rly).SetPermission(Editable) )*>')
familyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
if familyType in ('Series C','Turbomachinery'):
	hideContainerColumns(nonR2QContColumn)
	deleteRowsByCondition('C300_CG_Universal_IO_cont_1', ["Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)"])
	deleteRowsByCondition('SerC_CG_Enhanced_Function_IO_Cont', ["Series-C: HLAI (16) without HART with differential inputs (0-5000)","Series-C: HLAI (13-16) with HART with differential inputs (0-5000)","Series-C: HLAI (13-16) without HART with differential inputs (0-5000)"])
	deleteRowsByCondition('SerC_CG_Enhanced_Function_IO_Cont2', [
		"Series-C: DI (32) 110 VAC (0-5000)", "Series-C: DI (32) 110 VAC PROX (0-5000)", 
		"Series-C: DI (32) 220 VAC (0-5000)", "Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)", 
		"Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)"
	])
elif familyType == 'Series-C Mark II':
	hideContainerColumns(nonR2QContColumn2)
	deleteRowsByCondition('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont', ["SCM: HLAI (16) without HART with differential inputs (0-5000)","SCM: HLAI (13-16) with HART with differential inputs (0-5000)","SCM: HLAI (13-16) without HART with differential inputs (0-5000)","SCM: HLAI (13-16) differential inputs (0-5000)"])
	deleteRowsByCondition('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1', [
		"SCM: DI (32) 110 VAC (0-5000)", "SCM: DI (32) 220 VAC (0-5000)", 
		"SCM: DO (32) 24VDC Relay Bus above 30V (0-5000)", "SCM: DO (32) 24VDC Relay Bus up to 30V (0-5000)"
	])

attributes_defaults = {
	'SerC_CG_Universal_Marshalling_Cabinet': 'Yes',
	'SerC_GC_Profibus_Gateway_Interface': 'No',
	'SerC_CG_Foundation_Fieldbus_Interface_required': 'No',
	'SerC_CG_Ethernet_Interface': 'No',
	'SerC_CG_Controller_Memory_Backup': 'No',
	'SerC_CG_Type_of_Controller_Required': 'CN100 I/O HIVE - C300 CEE',
	'SerC_CG_R2Q_Power_System_Vendor': 'Phoenix Contact'
}

for attr, default_value in attributes_defaults.items():
	if Product.Attr(attr).GetValue() == '':
		Product.Attr(attr).SelectDisplayValue(default_value)

Product.Attr("SerC_CG_C300_Controller_Module_Type").SelectDisplayValue("C300(PCNT05)")
Product.Attr('SerC_CG_C300_Controller_Module_Type').Access = AttributeAccess.Hidden
if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == 'Turbomachinery':
	Product.DisallowAttr('SerC_CG_Universal_Marshalling_Cabinet')