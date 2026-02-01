def hideContainerColumns(contColumnList):
	for contColumn in contColumnList:
		for col in contColumnList[contColumn]:
			TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))


nonR2QContColumn = {"UOC_RG_Cabinet_Cont":["UOC_Cabinet_Type","UOC_Cabinet_Door_Type","UOC_Cabinet_Base_Size","UOC_Cabinet_Door_Keylock","UOC_Cabinet_Power_Entry","UOC_Cabinet_Thermostat","UOC_Cabinet_Light"],"UOC_RG_Controller_Rack_Cont":["UOC_Power_Supply","UOC_Power_Input","UOC_Power_Status_Mod_Redundant_Supply","UOC_Field_Wiring_DIDOAOAI_Channel_Mod","UOC_Field_Wiring_Other_Mod","UOC_Remote_Terminal_Cable_Length","UOC_IO_Rack_Type"],"UOC_RG_UIO_Cont":["UOC_AO_100_250","UOC_AO_250_499","UOC_AO_HART_100_250","UOC_AO_HART_250_499","UOC_DO_250_500"],"UOC_RG_Other_IO_Cont":["UOC_Digital_Input_Contact_Type16","UOC_Digital_Input16_125VDC","UOC_Pulse_Input_Frequency_point4"],"UOC_RG_PF_IO_Cont":["UOC_AI_Points","UOC_AI_Hart","UOC_AO_Points","UOC_AO_Hart","UOC_DI_Contact","UOC_DO_Points"]}
#ScriptExecutor.ExecuteGlobal('CQSHOWHIDE',{'product_name':'R2Q UOC Remote Group','func_call':'Hidden'})
hideContainerColumns(nonR2QContColumn)

for row in Product.GetContainerByName("UOC_RG_Controller_Rack_Cont").Rows:
	row.Product.Attr("UOC_IO_Rack_Type").SelectDisplayValue('Optimum Mixed I/O Rack')