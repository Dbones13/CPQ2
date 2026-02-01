if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
    import GS_PS_Exp_Ent_BOM
    import GS_C300_RG_Label
    import GS_C300_Cal_Parts5
    import GS_C300_Cal_Parts1,GS_C300_Cal_Parts2
    import GS_C300_RG_UPC_parts
    CCC_PAIL51=0
    CC_PAIL511=0
    #Added to top for CXCPQ-46098
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","ICF1150I-SSCT-HPSC",0)
    #44049
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
        OK3 = GS_C300_Cal_Parts5.IOComponents(Product)
        CCC_PAIL51,DC_TAIL51 = OK3.C300_Mark2()
        if CCC_PAIL51 > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIL51",CCC_PAIL51)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIL51",0)
        if DC_TAIL51 > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIL51",DC_TAIL51)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIL51",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIL51",0)
    mounting=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
    #39951
    '''if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
        OK5 = GS_C300_Cal_Parts1.IOComponents(Product)
        CC_PAIL511,CC_TAIL511 = OK5.C300_Mark2()
        if CC_PAIL511 > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIL51",CC_PAIL511)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIL51",0)
        if CC_TAIL511 > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIL51",CC_TAIL511)
        #CXCPQ-45898
        var16=GS_C300_RG_UPC_parts.get_CC_TAIL51(Product)
        Trace.Write("var16"+str(var16))
        if var16>0 and mounting=='Universal Process Cab - 1.3M':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIL51",var16)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIL51",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIL51",0)'''
    #44051
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
        OK11 = GS_C300_Cal_Parts2.IOComponents(Product)
        DC_PDIL51,DC_PDIS51,DC_TDIL61,DC_TDIL51=OK11.C300_Mark2()
        if DC_PDIL51 > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-PDIL51",DC_PDIL51)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-PDIL51",0)
        if DC_PDIS51 > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-PDIS51",DC_PDIS51)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-PDIS51",0)
        if DC_TDIL61 > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TDIL61",DC_TDIL61)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TDIL61",0)
        if DC_TDIL51 > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TDIL51",DC_TDIL51)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TDIL51",0)



    #CXCPQ-45357,CXCPQ-45311,CXCPQ-45889
    mounting=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
    P51156387_325,P51156387_304,CC_PAIL51,P51156387_330,ICF1150I_SSCT_HPSC,P51156387_312,P51156387_322,P50154762_002,P51454248_100,P50171803_001 = GS_C300_RG_Label.getpartSYSTEMLABEL(Product)
    #CXCPQ-45357
    if P51156387_325>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-325",P51156387_325)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-325",0)
    #CXCPQ-45311
    if P51156387_304>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-304",P51156387_304)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-304",0)
    #CXCPQ-45889
    if CC_PAIL51 + CCC_PAIL51 + CC_PAIL511>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIL51",CC_PAIL51 + CCC_PAIL51 + CC_PAIL511)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIL51",0)
    #CXCPQ-45374
    if P51156387_330>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-330",P51156387_330)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-330",0)
    #CXCPQ-46098
    if ICF1150I_SSCT_HPSC>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","ICF1150I-SSCT-HPSC",ICF1150I_SSCT_HPSC)
    #CXCPQ-45323
    if P51156387_312>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-312",P51156387_312)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-312",0)
    #CXCPQ-45334
    if P51156387_322>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-322",P51156387_322)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-322",0)
    #CXCPQ-45014
    if P50154762_002>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50154762-002",P50154762_002)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50154762-002",0)
    #CXCPQ-45807
    if P51454248_100>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454248-100",P51454248_100)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454248-100",0)
    #CXCPQ-45052
    if P50171803_001>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50171803-001",P50171803_001)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50171803-001",0)

    #CXCPQ-45360
    var13=GS_C300_RG_UPC_parts.getpart_51156387_327(Product)
    if var13>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-327",var13)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-327",0)
    #CXCPQ-46095
    var14=GS_C300_RG_UPC_parts.getpart_FS_CCI_HSE_03(Product)
    if var14>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","FS-CCI-HSE-03",var14)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","FS-CCI-HSE-03",0)
    #CXCPQ-45321
    var15=GS_C300_RG_UPC_parts.getpart_51156387_311(Product)
    if var15>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-311",var15)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-311",0)
    #CXCPQ-45320
    var17=GS_C300_RG_UPC_parts.getpart_51156387_309(Product)
    if var17>0 and mounting=='Universal Process Cab - 1.3M':
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-309",var17)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-309",0)