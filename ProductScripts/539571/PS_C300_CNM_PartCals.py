if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
    import GS_PS_Exp_Ent_BOM
    import GS_Get_Set_AtvQty
    import GS_C300_RG_UPC_Calc,GS_C300_BOM_UIO,GS_C300_BOM_MARK
    import GS_Part_C300_CNM_Calc,GS_C300_RG_UPC_Calc3
    import GS_C300_RG_UPC_parts,GS_C300_RG_UPC_Calculations,GS_C300_RG_UPC_Calc4

    mib=Product.Attr('MIB Configuration Required?').GetValue()
    io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    io_mounting=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
    qty13=GS_C300_RG_UPC_Calc3.getpartPUIO31(Product)
    qty8=GS_C300_RG_UPC_Calc3.getpartTUIO31(Product)
    val_6=GS_C300_RG_UPC_Calc.getC300UPC_46087(Product)
    #CXCPQ-40104
    UIO = GS_C300_BOM_UIO.IOComponents(Product)
    CC_PUIO31,CC_TUIO41,CC_TUIO31,Amp_A = UIO.C300_Rail()
    qty20 = qty8 + val_6
    #commented these lines as it creates problem for CXCPQ-49228
    #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PUIO31",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PUIO31",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TUIO41",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TUIO31",0)
        if CC_PUIO31 > 0 and io_mounting=='Cabinet':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PUIO31",CC_PUIO31)
        elif qty13>0 and io_mounting=='Universal Process Cab - 1.3M':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PUIO31",qty13)
        if CC_TUIO41 > 0 and io_mounting=='Cabinet':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TUIO41",CC_TUIO41)
        elif val_6>0 and io_mounting=='Universal Process Cab - 1.3M':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TUIO41",val_6)
        if CC_TUIO31 > 0 and io_mounting=='Cabinet':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TUIO31",CC_TUIO31)
        elif qty8>0 and io_mounting=='Universal Process Cab - 1.3M':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TUIO31",qty8)
    else:
        #CXCPQ-44166
        MARK = GS_C300_BOM_MARK.IOComponents(Product)
        DC_PUIO31,DC_TUIO41,DC_TUIO31 = MARK.C300_Rail()
        #commented the below else condition as it creates problem for CXCPQ-49228
        if DC_PUIO31 > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PUIO31",DC_PUIO31)
        """else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PUIO31",0)"""
        if DC_TUIO41 > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TUIO41",DC_TUIO41)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TUIO41",0)
        if DC_TUIO31 > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TUIO31",DC_TUIO31)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TUIO31",0)

    CCTION13_qty=0
    '''if io_family=='Series C':
        if io_mounting=='Universal Process Cab - 1.3M':
            #CXCPQ-46123 by Ravika Pupneja
            CCTION13_qty=GS_C300_RG_UPC_Calc.getC300UpsCals_CCTION13(Product)'''

    #44627,44628,44630
    #44627,44628,44630
    Tion11_446=GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_RG_Part_Summary","CC-TION11")
    Tion13_446=GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_RG_Part_Summary","CC-TION13")
    Tion11=GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_RG_Part_Summary","CC-TION11")
    #Trace.Write('K....Tion11_446 = '+str(Tion11_446))
    #Trace.Write('K....Tion13_446 = '+str(Tion13_446))
    #Trace.Write('K....Tion11 = '+str(Tion11))
    M01,C01,E01,WM_WE = GS_Part_C300_CNM_Calc.part_qty_RG_CNM(Product,Tion13_446,Tion11_446)
    M011,C011,E011,WM_WE1 = GS_Part_C300_CNM_Calc.RG_CNM52426(Product,Tion11) #CXCPQ-52426
    M012,C012,E012,WM_WE2 = GS_Part_C300_CNM_Calc.RG_CNM52403(Product,Tion11) #CXCPQ-52403

    V10=GS_C300_RG_UPC_Calculations.getpart_CC_INWM01(Product)
    CCINWE01_qty=GS_C300_RG_UPC_Calc.getC300UpsCals_CCINWE01(Product)

    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-INWM01",int(M01)+int(M011)+int(M012)+int(V10))
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TNWC01",int(C01)+int(C011)+int(C012))
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-INWE01",int(E01)+int(E011)+int(E012)+int(CCINWE01_qty))
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50165649-001",int(WM_WE)+int(WM_WE1)+int(WM_WE2))
    #Trace.Write('M01 = '+str(M01))
    #Trace.Write('C01 = '+str(C01))
    #Trace.Write('E01 = '+str(E01))
    #Trace.Write('WM_WE = '+str(WM_WE))

    if io_family=='Series C' and io_mounting=='Universal Process Cab - 1.3M':
        #CXCPQ-43820,CXCPQ-43531,CXCPQ-43816,CXCPQ-45312,CXCPQ-45015
        qty,qty1,qty2,qty3,qty4,qty5,qty6,qty7=GS_C300_RG_UPC_Calc4.getpartsUPC(Product)
        #qty8=GS_C300_RG_UPC_Calc3.getpartTUIO31(Product)
        qty10=GS_C300_RG_UPC_Calc3.getpart51156387326(Product)
        #qty11=GS_C300_RG_UPC_Calc3.getpartCCINAM01(Product)
        #qty12=GS_C300_RG_UPC_Calc3.getpartCCIION01(Product)
        #qty13=GS_C300_RG_UPC_Calc3.getpartPUIO31(Product)
        qty14=GS_C300_RG_UPC_Calc3.getpartCCSICC1011LR10(Product)
        qty15=GS_C300_RG_UPC_Calc3.getpart51121566101(Product)
        V1=GS_C300_RG_UPC_parts.getpart_51202692_200(Product)
        V2=GS_C300_RG_UPC_parts.getpart_51121566_102(Product)
        V3=GS_C300_RG_UPC_Calculations.getpart_51202789_900(Product)
        V4=GS_C300_RG_UPC_Calculations.getpart_CC_SICC_1011(Product)
        V5=GS_C300_RG_UPC_Calculations.getpart_51156387_315(Product)
        V6=GS_C300_RG_UPC_Calculations.getpart_51202688_104(Product)
        V7=GS_C300_RG_UPC_Calculations.getpart_51156387_328(Product)
        V8=GS_C300_RG_UPC_Calculations.getpart_51156387_313(Product)
        V9=GS_C300_RG_UPC_Calculations.getpart_51156389_310(Product)
        #V10=GS_C300_RG_UPC_Calculations.getpart_CC_INWM01(Product)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50154548-008",qty)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-323",qty1)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50154548-002",qty2)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-306",qty3)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50154983-001",qty4)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-301",qty5)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-320",qty6)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-316",qty7)
        #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TUIO31",qty8)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-326",qty10)
        #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-INAM01",qty11)
        #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-IION01",qty12)
        #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PUIO31",qty13)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/LR10",qty14)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51121566-101",qty15)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202692-200",V1)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51121566-102",V2)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202789-900",V3)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/LR05",V4)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-315",V5)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202688-104",V6)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-328",V7)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-313",V8)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156389-310",V9)
        #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-INWM01",V10)

    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50154548-008",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-323",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50154548-002",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-306",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50154983-001",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-301",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-320",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-316",0)
        #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TUIO31",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-326",0)
        #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-INAM01",0)
        #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-IION01",0)
        #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PUIO31",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/LR10",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202692-200",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51121566-102",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202789-900",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/LR05",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51121566-101",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-315",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202688-104",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-328",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-313",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51156389-310",0)
        #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-INWM01",0)
        #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TNWC01",0)
        #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50165649-001",0)