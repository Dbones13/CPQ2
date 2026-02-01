isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
    script_list = ['PS_UOC_RG_LI_Part_Summary', 'PS_UOC_remote_Sys_Cabinets_Qty', 'GS_R2Q_ContAttr_Hide']
    Trace.Write("REMOTE-GROUP-START")
    Trace.Write("REMOTE-GROUP-START-COUNT-"+str(Product.GetContainerByName("UOC_RG_PartSummary_Cont").Rows.Count))
    for script_name in script_list:
        Product.ParseString('<*ExecuteScript({})*>'.format(script_name))
        Trace.Write("REMOTE-GROUP-EXECUTED")
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if isR2Qquote and Checkproduct == "Migration":
    for attr_name in ('UOC_Field_Wiring_DIDOAOAI_Channel_Mod','UOC_Field_Wiring_Other_Mod','UOC_Remote_Terminal_Cable_Length'):
        Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('UOC_RG_Controller_Rack_Cont', attr_name))