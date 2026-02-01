if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN' or Product.Tabs.GetByName('Part Summary').IsSelected:
    import System.Decimal as D
    import GS_Part_C300_FIM_Calc
    import GS_Part_C300_CNM_Calc
    import GS_PS_Exp_Ent_BOM as GS_EEB
    import GS_C300_Cal_Parts, GS_C300_Cal_Parts1, GS_C300_Cal_Parts2, GS_C300_Cal_Parts3, GS_C300_Cal_Parts4, GS_C300_Cal_Parts5, GS_C300_Cal_Parts6
    import GS_Get_Set_AtvQty, GS_C300_BOM_UIO, GS_C300_BOM_MARK, GS_C300_BOM_Enhance1, GS_C300_BOM_Enhance2, GS_C300_BOM_Enhance3
    import GS_C300_MCAR_calcs
    import GS_C300_Calc_Module, GS_SerC_parts, GS_C300_UMC_Parts, GS_SerC_C300_CableParts, GS_C300_IO_Calc, GS_SerC_Part_Calcs
    from math import ceil
    Product.ExecuteRulesOnce = True
    qty=0
    Product.Attr("CG_HN").AssignValue('0')
    Product.Attr("PCNT_Val").AssignValue('0')
    Product.Attr("Turbo_PCNT_Val").AssignValue('0')
    '''Product.Attr("PCNT02_Val").AssignValue('0')
    Product.Attr("PCNT05_Val").AssignValue('0')'''
    #39961,39298,39294,39843#44037#44050
    OK4 = GS_C300_Cal_Parts6.IOComponents(Product)
    PAIN01,PAIH51,TAIX61,TAIX51 = OK4.C300_Mark2()
    OK2 = GS_C300_Cal_Parts4.IOComponents(Product)
    PAON01,PAOH51,TAOX61,TAOX51 = OK2.C300_Mark2()
    CC_PAIN01,CC_TAIN11,CC_TAIN01,CC_PAIH51,CC_TAIX61,CC_TAIX51,CC_PAON01,CC_TAON11,CC_TAON01,CC_PAOH51,CC_TAOX61,CC_TAOX51=GS_C300_Cal_Parts.part_qty_IO(Product)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and  PAIN01 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIN01",PAIN01)
    elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_PAIN01 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIN01",CC_PAIN01)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIN01",0)
    if  Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and PAIH51 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIH51",PAIH51)
    elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_PAIH51 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIH51",CC_PAIH51)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIH51",0)
    if  Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and TAIX61 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAIX61",TAIX61)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAIX61",0)
    if  Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and TAIX51 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAIX51",TAIX51)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAIX51",0)
    #if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAIN11 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIN11",CC_TAIN11)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIN11",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAIN01 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIN01",CC_TAIN01)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIN01",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAIX61 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIX61",CC_TAIX61)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIX61",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAIX51 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIX51",CC_TAIX51)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIX51",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_PAON01 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAON01",CC_PAON01)
    elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and PAON01 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAON01",PAON01)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAON01",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAON11 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAON11",CC_TAON11)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAON11",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAON01 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAON01",CC_TAON01)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAON01",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_PAOH51 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAOH51",CC_PAOH51)
    elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and PAOH51 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAOH51",PAOH51)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAOH51",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAOX61 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAOX61",CC_TAOX61)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAOX61",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAOX51 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAOX51",CC_TAOX51)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAOX51",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and TAOX61 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAOX61",TAOX61)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAOX61",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and TAOX51 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAOX51",TAOX51)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAOX51",0)
    '''
    Commented - This portion of code has been removed to PS_SerC_C300_CG_Parts_2
    #CXCPQ-41510
    '''
    #44150
    #if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
    OK1 = GS_C300_Cal_Parts3.IOComponents(Product)
    PDOD51,TDOD61,TDOD51 = OK1.C300_Mark2()
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and PDOD51 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-PDOD51",PDOD51)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-PDOD51",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and TDOD61 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TDOD61",TDOD61)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TDOD61",0)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and TDOD51 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TDOD51",TDOD51)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TDOD51",0)

    #44049
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
        OK3 = GS_C300_Cal_Parts5.IOComponents(Product)
        CC_PAIL51,DC_TAIL51 = OK3.C300_Mark2()
        if CC_PAIL51 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIL51",CC_PAIL51)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIL51",0)
        if DC_TAIL51 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAIL51",DC_TAIL51)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAIL51",0)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIL51",0)

    #44051
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
        OK11 = GS_C300_Cal_Parts2.IOComponents(Product)
        DC_PDIL51,DC_PDIS51,DC_TDIL61,DC_TDIL51=OK11.C300_Mark2()
        if DC_PDIL51 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-PDIL51",DC_PDIL51)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-PDIL51",0)
        if DC_PDIS51 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-PDIS51",DC_PDIS51)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-PDIS51",0)
        if DC_TDIL61 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TDIL61",DC_TDIL61)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TDIL61",0)
        if DC_TDIL51 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TDIL51",DC_TDIL51)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TDIL51",0)

    #39951
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
        OK5 = GS_C300_Cal_Parts1.IOComponents(Product)
        CC_PAIL511,CC_TAIL511 = OK5.C300_Mark2()
        if CC_PAIL511 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIL51",CC_PAIL511)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIL51",0)
        if CC_TAIL511 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIL51",CC_TAIL511)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIL51",0)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAIL51",0)
    #CXCPQ-40869
    '''if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
        #MCTAMR04,MCTAMT04,MCTAMT14,MUKLAM03,MUTMCN01=GS_C300_Cal_Parts.getpartsseriesc(Product)
        #above one had error
        MCTAMR04,MCTAMT04,MCTAMT14,MUKLAM03=GS_C300_Cal_Parts.getpartsseriesc(Product)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAMR04",MCTAMR04)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAMT04",MCTAMT04)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAMT14",MCTAMT14)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KLAM03",MUKLAM03)
        #GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-TMCN01",MUTMCN01)'''

    #CXCPQ-40104
    UIO = GS_C300_BOM_UIO.IOComponents(Product)
    CC_PUIO31,CC_TUIO41,CC_TUIO31,Amp_A= UIO.C300_Rail()
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
        if CC_PUIO31 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PUIO31",CC_PUIO31)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PUIO31",0)
        if CC_TUIO41 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TUIO41",CC_TUIO41)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TUIO41",0)
        if CC_TUIO31 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TUIO31",CC_TUIO31)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TUIO31",0)

    ## Sprint-22 :- N
    #CXCPQ-44166
    MARK = GS_C300_BOM_MARK.IOComponents(Product)
    DC_PUIO31,DC_TUIO41,DC_TUIO31 = MARK.C300_Rail()
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
        if DC_PUIO31 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PUIO31",DC_PUIO31)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PUIO31",0)
        if DC_TUIO41 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TUIO41",DC_TUIO41)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TUIO41",0)
        if DC_TUIO31 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TUIO31",DC_TUIO31)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TUIO31",0)

    #CXCPQ-44457
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAOH01",0)
    MARK1 = GS_C300_BOM_Enhance1.IOComponents(Product)
    CC_PAOH01,DC_TAOX11,DC_TAOX01 = MARK1.C300_Mark()
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
        if CC_PAOH01 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAOH01",CC_PAOH01)
        """else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAOH01",0)"""
        if DC_TAOX11 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAOX11",DC_TAOX11)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAOX11",0)
        if DC_TAOX01 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAOX01",DC_TAOX01)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAOX01",0)

    #CXCPQ-44473
    MARK2 = GS_C300_BOM_Enhance2.IOComponents(Product)
    CC_PDIL01,DC_TDIL11,DC_TDIL01 = MARK2.C300_Mark2()
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
        if CC_PDIL01 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PDIL01",CC_PDIL01)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PDIL01",0)
        if DC_TDIL11 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TDIL11",DC_TDIL11)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TDIL11",0)
        if DC_TDIL01 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TDIL01",DC_TDIL01)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TDIL01",0)

    #CXCPQ-44340
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" or Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIH02",0)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIX02",0)
    MARK3 = GS_C300_BOM_Enhance3.IOComponents(Product)
    CC_PAIH02,CC_PAIX02,DC_TAID01,DC_TAID11 = MARK3.C300_Mark3()
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" or Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
        if CC_PAIH02 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIH02",CC_PAIH02)
        """else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIH02",0)"""
        if CC_PAIX02 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIX02",CC_PAIX02)
        """else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PAIX02",0)"""
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
        if DC_TAID01 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAID01",DC_TAID01)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAID01",0)
        if DC_TAID11 > 0:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAID11",DC_TAID11)
        else:
            GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAID11",0)

    family_type = Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue()
    #41843, 44565
    CC_PFB801, PQ2 = GS_Part_C300_FIM_Calc.part_qty_FIM8(Product)
    if family_type == 'Series C':
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PFB801",CC_PFB801)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TFB811",PQ2)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TFB813",0)
    elif family_type == 'Series-C Mark II':
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PFB801",CC_PFB801)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TFB813",PQ2)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TFB811",0)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PFB801",0)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TFB813",0)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TFB811",0)

    #41327, 44563
    CC_PFB402, PQ3, PQ4 = GS_Part_C300_FIM_Calc.part_qty_FIM4(Product)
    if family_type == 'Series C':
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PFB402",CC_PFB402)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TFB412",PQ3)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TFB402",PQ4)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TFB413",0)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TFB403",0)
    elif family_type == 'Series-C Mark II':
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PFB402",CC_PFB402)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TFB413",PQ3)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TFB403",PQ4)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TFB412",0)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TFB402",0)
    else:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PFB402",0)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TFB412",0)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TFB402",0)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TFB413",0)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TFB403",0)

    #CXCPQ-42768
    Power_Conditioner = Product.Attr('FIM_FF_IOs_with_Power_conditioner').GetValue()
    CC_PFB801, CC_TFB811 = GS_Part_C300_FIM_Calc.part_qty_FIM8(Product)
    CC_PFB402, CC_TFB412, CC_TFB402 = GS_Part_C300_FIM_Calc.part_qty_FIM4(Product)
    if Power_Conditioner == "Yes":
        Trace.Write("Power_Conditioner"+str (Power_Conditioner))
        F860 = CC_TFB811 + (CC_TFB412+CC_TFB402)/2
        FCAB_08 = CC_PFB801+CC_PFB402
        GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","F860",F860)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","FCAB-08",FCAB_08)
    else:
        Trace.Write("Power_Conditioner"+str (Power_Conditioner))
        GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","F860",0)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","FCAB-08",0)

    IO_Family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    Universal=Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue()
    #CXCPQ-41491
    V43= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V43')
    V83= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V83')
    V91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V91')
    V92= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V92')
    if IO_Family=="Series C" and Universal =='No':
        CC_SDXX01 = V43 + V83 + V91 + V92
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-SDXX01",CC_SDXX01)
    #CXCPQ-50470
    elif IO_Family=="Turbomachinery":
        CC_SDXX01 = V43 + V83 + V91 + V92
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-SDXX01",CC_SDXX01)
    else:
        CC_SDXX01 = 0
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-SDXX01",CC_SDXX01)

    #CXCPQ-41226
    Y21= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Y21')
    Y22= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Y22')
    Y31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Y31')
    Y32= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Y32')
    Y23= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Y23')
    Y33= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Y33')
    W11= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W11')
    W21= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W21')
    W31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W31')
    W12= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W12')
    W22= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W22')
    W32= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W32')
    W41= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W41')
    W51= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W51')
    W61= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W61')
    W42= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W42')
    W52= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W52')
    W62= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W62')
    W23= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W23')
    Z91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z91')
    if IO_Family=="Series C":
        CC_TAID11 = Y21 + Y22+ Y31 + Y32
        CC_TAID01 = Y23+ Y33
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAID11",CC_TAID11)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAID01",CC_TAID01)
    else:
        CC_TAID11 = CC_TAID01 = 0
    """
    #commented below two lines as they create problem for turbomachinery
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAID11",CC_TAID11)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAID01",CC_TAID01)"""
    if IO_Family=="Series C" and Universal =='No':
        CC_GAIX11 = (W11+W21+W31) + (W12+W22+W32) + (W41+W51+W61) + (W42+W52+W62)
        CC_GAIX21 = Z91 + W23
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GAIX11",CC_GAIX11)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GAIX21",CC_GAIX21)
    else:
        CC_GAIX11 = CC_GAIX21 =0
        """
        #commented below two lines as they create problem for turbomachinery
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GAIX11",CC_GAIX11)
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GAIX21",CC_GAIX21)"""
    #CXCPQ-39150
    totalLoadIO = GS_C300_Calc_Module.getTotalLoadIO(Product)
    totalIoPointLoad = GS_C300_Calc_Module.getTotalIoPointLoad(Product)

    Product.Attr("C300_CG_Total_IO_Load").AssignValue(str(totalLoadIO))
    Product.Attr("C300_CG_Total_IO_Point_Load").AssignValue(str(totalIoPointLoad))

    Product.Messages.Add("Total Load IO is {}.".format(totalLoadIO))
    Product.Messages.Add("Total IO Point Load is {}.".format(totalIoPointLoad))

    controllerType = Product.Attr("SerC_CG_Controller_Type").GetValue()
    #Changes done by Ravika--->CCEECOMMBR-7475
    Control_Firewall_Uplink_Fiber_Mod = Product.Attr("SerC_Control_Firewal_Uplink_FiberModule").GetValue()
    ioFamily = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    controllerTypeRequired = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-IION01", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-TION11", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-INAM01", 0)
    if ioFamily == "Series C" and controllerTypeRequired == "CN100 CEE":
        qty = ceil(totalLoadIO/40.0)
        qty = max(qty, ceil(totalIoPointLoad/800.0))
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-TION11", qty)
        if controllerType == "Redundant":
            qty *= 2
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-IION01", qty)
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-INAM01", qty)

    #CXCPQ-52347
    parts_dict = GS_SerC_Part_Calcs.getParts52347(Product, {})
    if len(parts_dict) > 0:
        GS_C300_IO_Calc.setIOCount(Product, 'Series_C_CG_Part_Summary', parts_dict)

    #CXCPQ-42498, CXCPQ-42551
    firewallCableLength = Product.Attr("SerC_CG_Control_Firewall").GetValue()
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-PCNT02", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-SCMB02", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-PCNT05", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-SCMB05", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51454475-100", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305980-836", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305980-224", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305980-124", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305980-236", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305980-136", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305980-248", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305980-148", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305980-260", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305980-160", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305980-284", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305980-184", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305482-202", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305482-102", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305482-205", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305482-105", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305482-210", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305482-110", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305482-220", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305482-120", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51202330-300", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51202330-200", 0)
    #code changes done by Ravika --->CCEECOMMBR-7473
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "DC-TCF902", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-TCF901", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-FMMX01", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-FSMX01", 0)
    #code chnages by Ravika --->CXDEV-7703
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "TC-SWCHC1", 0)
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "TC-SWCHV1", 0)

    pcntPart, memBlockPart, pcntQty = GS_C300_Cal_Parts.getPartCCPCNTQty(Product)
    pcntQty_52419= pcntQty
    Product.Attr("PCNT_Val").AssignValue(str(pcntQty))
    if pcntQty:
        if controllerTypeRequired != "Control HIVE - Virtual":
            GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", pcntPart, pcntQty)
        if controllerType == "Redundant":
            GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", pcntPart, pcntQty * 2)
            pcntQty = pcntQty * 2
        #Changes Done By RDT(Ravika Pupneja)CCEECOMMBR-6715
        if memBlockPart:
            GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", memBlockPart, ceil(pcntQty / 4.0))
        '''if memBlockPart and controllerType == "Redundant":
            GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", memBlockPart, ceil(pcntQty / 8.0))'''
        #Changes Done By RDT(Ravika Pupneja)CCEECOMMBR-6716
        if memBlockPart in ['CC-SCMB05','CC-SCMB02','51454475-100']:
            GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51202330-300", ceil(pcntQty / 4.0)*2)
            GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51202330-200", ceil(pcntQty / 4.0)*2)
    #CXCPQ-110808
    Product.Attr("Turbo_PCNT_Val").AssignValue(str(pcntQty))
    #CXCPQ-42552
    cableSetPartMap = {
        "24 Inch" : ["51305980-224", "51305980-124"],
        "36 Inch" : ["51305980-236", "51305980-136"],
        "48 Inch" : ["51305980-248", "51305980-148"],
        "60 Inch" : ["51305980-260", "51305980-160"],
        "84 Inch" : ["51305980-284", "51305980-184"],
        "2m" : ["51305482-202", "51305482-102"],
        "5m" : ["51305482-205", "51305482-105"],
        "10m" : ["51305482-210", "51305482-110"],
        "20m" : ["51305482-220", "51305482-120"]
    }
    if ioFamily == "Series-C Mark II" and pcntQty:
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "DC-TCNT01", pcntQty)
    else:
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "DC-TCNT01", 0)

    if ioFamily != "Series-C Mark II" and pcntQty and controllerTypeRequired != "Control HIVE - Virtual":
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-TCNT01", pcntQty)
    else:
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-TCNT01", 0)

    if controllerTypeRequired != "Control HIVE - Virtual":
        for part in cableSetPartMap.get(firewallCableLength, []):
            GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", part, pcntQty)
    crtlQty = 0
    pgmEimQty = GS_C300_Cal_Parts.getPgmEimQty(Product)
    Trace.Write(pcntQty)
    pcnt05 = GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PCNT05')
    pcnt02 = GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PCNT02')
    Trace.Write("PCNT05 Qty = {}".format(pcnt02))
    if controllerType == "Redundant":
        crtlQty = round(pcnt05/2) + round(pcnt02/2)

    crtlPgmEim = crtlQty + pgmEimQty
    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "51305980-836",crtlPgmEim)
    #CXCPQ-41230
    CC_PCNT02 = GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PCNT02')
    CC_PCNT05 = GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PCNT05')
    CC_PFB402 = GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PFB402')
    CC_PFB801 = GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PFB801')
    CC_IP0101 = GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-IP0101')
    CC_PEIM01 = GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PEIM01')

    '''Product.Attr("PCNT02_Val").AssignValue(str(CC_PCNT02))
    Product.Attr("PCNT05_Val").AssignValue(str(CC_PCNT05))'''
    if ioFamily == "Series-C Mark II":
        qty = 2 * (ceil((CC_PCNT02 + CC_PFB402 + CC_PFB801 + CC_IP0101 + CC_PEIM01) / 8.0))
    elif ioFamily == "Series C":
        qty = 2 * (ceil((CC_PCNT02 + CC_PFB402 + CC_PFB801 + CC_IP0101 + CC_PEIM01) / 8.0))
    else:
        qty = 2 * (ceil(CC_PCNT02 / 8.0))


    GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-PCF901", qty)
    if ioFamily == "Series-C Mark II":
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "DC-TCF902", qty)
    else:
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-TCF901", qty)

    #Changes made by Ravika---->CCEECOMMBR-7473
    if Control_Firewall_Uplink_Fiber_Mod == "Single Mode SFP":
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-FSMX01", qty)
    if Control_Firewall_Uplink_Fiber_Mod == "Multi Mode SFP":
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-FMMX01", qty)

    if ioFamily == "Turbomachinery":
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "TC-SWCS31", CC_PCNT02 + CC_PCNT05)
    else:
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "TC-SWCS30", CC_PCNT02 + CC_PCNT05)

    if ioFamily == "Turbomachinery" and controllerType == "Redundant":
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "TC-SWCS31", (CC_PCNT02/2) + (CC_PCNT05/2))
    if ioFamily != "Turbomachinery" and controllerType == "Redundant":
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "TC-SWCS30", (CC_PCNT02/2) + (CC_PCNT05/2))

    if ioFamily == "Series-C Mark II":
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "DC-TCF902", qty)
    else:
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-TCF901", qty)
    #CXDEV-7703
    ExpRelease = Product.Attr("Experion_PKS_Software_Release").GetValue()
    if ioFamily == "Series C" and controllerTypeRequired in ("Control HIVE - Physical", "Control HIVE - Virtual"):
        calc_hive_controller = GS_C300_Cal_Parts.getFloat(Product.Attr("SerC_CG_Number_of_HIVE_Control_Applications(HCA)").GetValue())
        addnl_hive_controller = GS_C300_Cal_Parts.getFloat(Product.Attr("SerC_CG_Number_of_Extra_HIVE_Control_Applications").GetValue())
    #CXDEV-7703
        if ExpRelease == 'R520' and controllerTypeRequired in ("Control HIVE - Virtual"):
            #Log.Info("RP")
            #Log.Info(str(pcntQty))
            GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "TC-SWCHC1", pcntQty)
        elif ExpRelease == 'R530' and controllerTypeRequired in ("Control HIVE - Virtual"):
            GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "TC-SWCHV1", pcntQty)
        elif controllerTypeRequired in ("Control HIVE - Physical") and (ExpRelease == 'R530' or ExpRelease == 'R520'):
            GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "TC-SWCHC1", pcntQty)
        GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "TC-SWCS30", calc_hive_controller + addnl_hive_controller)

        msg = "Control HIVE Controller Licenses are present. Please ensure sufficient quantities of C300 controllers and licenses are added in the configuration."
        if not Product.Messages.Contains(msg):
            Product.Messages.Add(msg)


    #CXCPQ-42026 ,42028,42032 and 52390, 52402, 52419
    pcntQty05=GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_CG_Part_Summary","CC-PCNT05")
    qty=GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_CG_Part_Summary","CC-PCF901")
    Tion11=GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_CG_Part_Summary","CC-TION11")
    CC_INWM01,CC_TNWC01,CC_INWE01,INWM_INWE = GS_Part_C300_CNM_Calc.part_qty_CNM(Product,pcntQty05,qty)
    CC_INWM011,CC_TNWC011,CC_INWE011,INWM_INWE1 = GS_Part_C300_CNM_Calc.CG_CNM52390(Product,Tion11)
    CC_INWM012,CC_TNWC012,CC_INWE012,INWM_INWE2 = GS_Part_C300_CNM_Calc.CG_CNM52402(Product, pcntQty05, qty,Tion11)
    CC_INWM013,CC_TNWC013,CC_INWE013,INWM_INWE3 = GS_Part_C300_CNM_Calc.CG_CNM52419(Product, pcntQty05, Tion11)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-INWM01",int(CC_INWM01)+int(CC_INWM011)+int(CC_INWM012)+int(CC_INWM013))
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TNWC01",int(CC_TNWC01)+int(CC_TNWC011)+int(CC_TNWC012)+int(CC_TNWC013))
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-INWE01",int(CC_INWE01)+int(CC_INWE011)+int(CC_INWE012)+int(CC_INWE013))
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","50165649-001",int(INWM_INWE)+int(INWM_INWE1)+int(INWM_INWE2)+int(INWM_INWE3))

    #CXCPQ-39151
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","8939-HN",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","8937-HN2",0)
    qty_8939_HN, qty_8937_HN2 = GS_SerC_parts.Get_CG_IOTA(Product)
    if qty_8939_HN > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","8939-HN",qty_8939_HN)
        Product.Attr("CG_HN").AssignValue(str(qty_8939_HN))
    if qty_8937_HN2 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","8937-HN2",qty_8937_HN2)
    #CXCPQ-39152
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KFSGR5",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KFSVR5",0)
    qty_CC_KFSGR5, qty_CC_KFSVR5 = GS_SerC_parts.Get_HN(Product)
    if qty_CC_KFSGR5>0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KFSGR5",qty_CC_KFSGR5)
    if qty_CC_KFSVR5>0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KFSVR5",qty_CC_KFSVR5)

    #CXCPQ-39268 #CXCPQ-39288
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-SDRX01",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-SDRX01",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","ICF1150I-SSCT-HPSC",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51155436-100",0)
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51156323-100",0)
    qty_SDRX, qty_HPSC, qty_100, qty_case3 = GS_SerC_parts.CG_iota(Product)
    if qty_SDRX > 0 and IO_Family != "Series-C Mark II":
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-SDRX01",qty_SDRX)
    elif qty_SDRX > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-SDRX01",qty_SDRX)
    if qty_HPSC > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","ICF1150I-SSCT-HPSC",qty_HPSC)
    if qty_100 > 0 and IO_Family != "Series-C Mark II":
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51155436-100",qty_100)
    elif qty_100 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51156323-100",qty_100)
    if qty_case3 > 0:
        GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","ICF1150I-MSTT-HPSC",qty_case3)

    #CXCPQ-41370
    CC_IP0101= GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-IP0101')
    CC_PEIM01= GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PEIM01')
    CC_PFB402= GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PFB402')
    CC_PFB802= GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PFB801')

    Parts=["51305980-224","51305980-124","51305980-236","51305980-136","51305980-248","51305980-148","51305980-260","51305980-160","51305980-284","51305980-184","51305482-202","51305482-102","51305482-205","51305482-105","51305482-210","51305482-110","51305482-220","51305482-120"]
    Partq=[]
    for i in Parts:
        x= GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary',i)
        Partq.append(int(x))

    C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,C14,C15,C16,C17,C18 = GS_SerC_C300_CableParts.returncableparts(Product,CC_IP0101,CC_PEIM01,CC_PFB402,CC_PFB802)

    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-224",C1 +int(Partq[0]))
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-124",C2 +int(Partq[1]))

    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-236",C3 +int(Partq[2]))
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-136",C4 +int(Partq[3]))

    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-248",C5 +int(Partq[4]))
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-148",C6 +int(Partq[5]))

    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-260",C7 +int(Partq[6]))
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-160",C8 +int(Partq[7]))

    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-284",C9 +int(Partq[8]))
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-184",C10+int(Partq[9]))

    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-202",C11+int(Partq[10]))
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-102",C12+int(Partq[11]))

    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-205",C13+int(Partq[12]))
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-105",C14+int(Partq[13]))

    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-210",C15+int(Partq[14]))
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-110",C16+int(Partq[15]))

    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-220",C17+int(Partq[16]))
    GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-120",C18+int(Partq[17]))

    Product.ApplyRules()
    Product.ExecuteRulesOnce = False