isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
    PLC_controlgrpRows = Product.GetContainerByName('Number_PLC_Remote_Groups').Rows
    if PLC_controlgrpRows.Count > 0:
    	PLC_controlgrp = PLC_controlgrpRows[0]
    	PLC_controlgrp.GetColumnByName('Number_PLC_Remote_Groups').HeaderLabel = "Number of Remote Group for ControlEdge PLC Control Groups (0-10)"
    Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
    if Checkproduct == 'Migration':
        for attr_name in ("PLC_Ethernet_Switch_Type", "PLC_Power_Status_Mod_Redudant_Supply"):
            TagParserProduct.ParseString('<*CTX( Container(PLC_CG_Controller_Rack_Cont).Column({}).SetPermission(Editable) )*>'.format(attr_name))
if isR2Qquote == False:
    plc_remoteGroup_cont= Product.GetContainerByName('PLC_RemoteGroup_Cont').Rows
    for row in plc_remoteGroup_cont:
        row.Product.Attr('PLC_Cabinet_Required_Racks_Mounting').AssignValue(Product.Attr("PLC_Cabinet_Required_Racks_Mounting").GetValue())
        #row.Product.Attr("PLC_Cabinet_Required_Racks_Mounting").GetValue()