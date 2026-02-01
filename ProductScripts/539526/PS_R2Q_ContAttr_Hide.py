isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
Trace.Write("rg_check_before_isR2Qquote33="+str(isR2Qquote)+" Checkproduct="+str(Checkproduct))
if isR2Qquote and Checkproduct == "PRJT R2Q":
    for attr_name in ('PLC_Field_Wiring_DIDOAOAI_Channel_Mod','PLC_Field_Wiring_PIFII_Channel_Mod','PLC_Field_Wiring_Other_Mod','PLC_Remote_Terminal_Cable_Length'):
        Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('PLC_RG_Controller_Rack_Cont', attr_name))
        Trace.Write("rg_check_after_isR2Qquote34="+str(isR2Qquote)+" Checkproduct="+str(Checkproduct)+str(Product.ParseString('<*CTX( Container({}).Column({}).GetPermission)*>'.format('PLC_RG_Controller_Rack_Cont', attr_name))))