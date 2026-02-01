'''Product.Attr('SC_License_type_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Central_Managed_SQL_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Select_desired_Release_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Standard_User_CALs_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Business_Level_Access_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_L4_Trace_Server_Option_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Number_of_Concurrent_Users_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Years_of_Support_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_ESVT_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Experion_PKS_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Honeywell_TPS_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Experion_LX_Plantcruise_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Honeywell_Safety_Manager_S300_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Triconex_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_FSC_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Experion_SCADA_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_APC_Aspen_DMC_or_ProfitSuite_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Honeywell_ControlEdge_PLC_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Uniformance_PHD_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_OSI_PI_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_SPI_Tools_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_RS_Logix_PY').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Custom_User_Defined_System_PY').Access = AttributeAccess.ReadOnly'''
if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    Product.AttrValue('SC_License_type', 'Term').Allowed = False