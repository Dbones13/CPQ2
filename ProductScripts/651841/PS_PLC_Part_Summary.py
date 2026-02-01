Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if Checkproduct != "PRJT R2Q":
    import GS_PLC_UOC_Software_Calcs
    import GS_PLC_UOC_PartUpdate
    import GS_PLC_ReadAttrs

    try:
        attrs = GS_PLC_ReadAttrs.AttrStorage(Product)
        Log.Write("CE-PLC-ATTR-LIST=" + str(attrs.__dict__))
    except Exception,e:
        attrs = None
        Product.Messages.Add("Error when Reading PLC System Attributes: " + str(e))
        Trace.Write("Error when Reading PLC System Attributes: " + str(e))
        Log.Error("Error when Reading PLC System Attributes: " + str(e) + " -- " + str(Checkproduct))

    parts_dict = {}

    if attrs:
        try:
            parts_dict = GS_PLC_UOC_Software_Calcs.calc_software_plc_system(attrs, parts_dict, Checkproduct)
        except Exception,e:
            Product.Messages.Add("Error in GS_PLC_UOC_Software_Calcs: " + str(e))

        Trace.Write("debugging: " + str(parts_dict))
        if Product.Attr('MIgration_Scope_Choices').GetValue() == 'LABOR':
            for k in parts_dict.keys():
                if not k.startswith('HPS_SYS'):
                    parts_dict.pop(k)
        Log.Write("Parts Dict CE-PLC-CG: {0}".format(parts_dict))
        GS_PLC_UOC_PartUpdate.execute(Product, 'PLC_PartSummary_Cont', parts_dict)