Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))

def hideContainerColumns(contColumnList):
	for contColumn in contColumnList:
		for col in contColumnList[contColumn]:
			TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))

nonR2QContColumn = {"UOC_CG_Cabinet_Cont":["UOC_Cabinet_Type","UOC_Cabinet_Door_Type","UOC_Cabinet_Base_Size","UOC_Cabinet_Door_Keylock","UOC_Cabinet_Power_Entry","UOC_Cabinet_Thermostat","UOC_Cabinet_Light"],"UOC_CG_Controller_Rack_Cont":["UOC_Power_Supply","UOC_Power_Input","UOC_Power_Status_Mod_Redundant_Supply","UOC_Field_Wiring_DIDOAOAI_Channel_Mod","UOC_Field_Wiring_Other_Mod","UOC_Remote_Terminal_Panel_Cable_Type","UOC_Remote_Terminal_Cable_Length","UOC_Network_Topology","UOC_Ethernet_Switch_Supplier","UOC_Ethernet_Switch_Type","UOC_IO_Rack_Type"],"UOC_CG_UIO_Cont":["UOC_AO_100_250","UOC_AO_250_499","UOC_AO_HART_100_250","UOC_AO_HART_250_499","UOC_DO_250_500"],"UOC_CG_Other_IO_Cont":["UOC_Digital_Input_Contact_Type16","UOC_Digital_Input16_125VDC","UOC_Pulse_Input_Frequency_point4"],"UOC_CG_PF_IO_Cont":["UOC_AI_Points","UOC_AI_Hart","UOC_AO_Points","UOC_AO_Hart","UOC_DI_Contact","UOC_DO_Points"],"UOC_CG_Additional_Controller_Cont":["UOC_Two_Pos_Terminal_Board_Jumpers","UOC_Ten_Pos_Terminal_Board_Jumpers","UOC_MIMP_250Ohm_Resistor_Kit","UOC_IO_Mod_Label_Kit","UOC_Fiber_Optic_Converter_Single","UOC_Additonal_Controller"]}

hideContainerColumns(nonR2QContColumn)
#ScriptExecutor.ExecuteGlobal('CQSHOWHIDE',{'product_name':'R2Q UOC Control Group','func_call':'Hidden'})
control_cont = Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows
if control_cont.Count > 0:
	control_cont[0].Product.Attr('UOC_IO_Rack_Type').SelectDisplayValue('Optimum Mixed I/O Rack')

UOC_CG_cont = Product.GetContainerByName('Number_UOC_Remote_Groups').Rows
if UOC_CG_cont.Count > 0:
	UOC_CG_cont[0].GetColumnByName('Number_UOC_Remote_Groups').HeaderLabel = "Number of  Remote Group for ControlEdge UOC Control Groups (0-10)"
if Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows.Count > 0:
    UOC_CG_PS = Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('UOC_Power_Supply')
    if not UOC_CG_PS.Value:
        UOC_CG_PS.Value = 'Non Redundant'