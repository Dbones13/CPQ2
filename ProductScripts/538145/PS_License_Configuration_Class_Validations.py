SC_ESVT = eval(Product.Attr('SC_ESVT').GetValue())

Class_0 = SC_ESVT



SC_Experion_PKS = eval(Product.Attr('SC_Experion_PKS').GetValue())
SC_Honeywell_TPS = eval(Product.Attr('SC_Honeywell_TPS').GetValue())
SC_Experion_LX_Plantcruise = eval(Product.Attr('SC_Experion_LX_Plantcruise').GetValue())

Class_1 = SC_Experion_PKS + SC_Honeywell_TPS + SC_Experion_LX_Plantcruise

SC_Honeywell_Safety_Manager_S300 = eval(Product.Attr('SC_Honeywell_Safety_Manager_S300').GetValue())
SC_Triconex = eval(Product.Attr('SC_Triconex').GetValue())
SC_FSC = eval(Product.Attr('SC_FSC').GetValue())
SC_Experion_SCADA = eval(Product.Attr('SC_Experion_SCADA').GetValue())
SC_APC_Aspen_DMC_or_ProfitSuite = eval(Product.Attr('SC_APC_Aspen_DMC_or_ProfitSuite').GetValue())
SC_Honeywell_ControlEdge_PLC = eval(Product.Attr('SC_Honeywell_ControlEdge_PLC').GetValue())

Class_2 = SC_Honeywell_Safety_Manager_S300 + SC_Triconex + SC_FSC + SC_Experion_SCADA + SC_APC_Aspen_DMC_or_ProfitSuite + SC_Honeywell_ControlEdge_PLC

SC_Uniformance_PHD = eval(Product.Attr('SC_Uniformance_PHD').GetValue())
SC_OSI_PI = eval(Product.Attr('SC_OSI_PI').GetValue())
SC_SPI_Tools = eval(Product.Attr('SC_SPI_Tools').GetValue())
SC_RS_Logix = eval(Product.Attr('SC_RS_Logix').GetValue())
SC_Custom_User_Defined_System = eval(Product.Attr('SC_Custom_User_Defined_System').GetValue())

Class_3 = SC_Uniformance_PHD + SC_OSI_PI + SC_SPI_Tools + SC_RS_Logix + SC_Custom_User_Defined_System

err_msg_1 = ""
if (Class_0 + Class_1 + Class_2 + Class_3 == 0):
    err_msg_1 = 'Quantity of systems added should be > 0 for any of the classes.'
Product.Attr('ErrorMessage2').AssignValue(err_msg_1)