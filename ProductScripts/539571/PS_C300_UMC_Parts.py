if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
    import math
    import GS_PS_Exp_Ent_BOM,GS_C300_UMC_Parts,GS_C300_RG_UPC_Calc3, GS_C300_UMC_MARK,GS_SerC_IOLink
    import GS_Get_Set_AtvQty
    CurrentTab=Product.Tabs.GetByName('Part Summary').IsSelected
    if CurrentTab==True:
        Product.Attr('CurrentTab_Is_partsummery').AssignValue('Part Summary')
        Trace.Write("correct")
    else:
        Product.Attr('CurrentTab_Is_partsummery').AssignValue('OtherTab')
        Trace.Write("Notcorrect")
    #Product.ExecuteRulesOnce = True
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UPTA01",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDIA01",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDOA01",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UAIA01",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UAOA02",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDOR01",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDIR01",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGAI01",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGAO02",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGDA01",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-ULLI01",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDXA01",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGAI03",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGDN02",0)
    mib=Product.Attr('MIB Configuration Required?').GetValue()
    io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    io_mounting=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
    ## UMC parts
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
        RG_GIIS_AI = Product.Attr('SerC_RG_GIIS_Analog_Inputs_Isolator_2Wire_Type').GetValue()
        RG_NAMUR = Product.Attr('SerC_RG_Is_NAMUR_isolator_type_Required').GetValue()
        #CXCPQ-46424
        qty_UPTA01 = GS_C300_UMC_Parts.get_UPTA01(Product)
        if qty_UPTA01>0 and io_mounting!='Universal Process Cab - 1.3M':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UPTA01",qty_UPTA01)
        #CXDEV-8782
        qty_UDIA01 = GS_C300_UMC_Parts.get_UDIA01(Product)
        if qty_UDIA01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDIA01",qty_UDIA01)
        #CXDEV-8783
        qty_UDOA01 = GS_C300_UMC_Parts.get_UDOA01(Product)
        if qty_UDOA01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDOA01",qty_UDOA01)
        #CXCPQ-46430,CXCPQ-46433
        qty_UAIA01, qty_UAOA02 = GS_C300_UMC_Parts.get_UAIA01(Product)
        if qty_UAIA01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UAIA01",qty_UAIA01)
        if qty_UAOA02>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UAOA02",qty_UAOA02)
        #CXCPQ-46091,CXCPQ-43585
        qty_UDOR01, qty_UDIR01 = GS_C300_UMC_Parts.get_RLY(Product)
        if qty_UDOR01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDOR01",qty_UDOR01)
        if qty_UDIR01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDIR01",qty_UDIR01)
        #CXCPQ-46429,CXCPQ-46431,CXCPQ-46800
        qty_UGAI01, qty_UGAO02,qty_UGDA01,qty_UGDN02 = GS_C300_UMC_Parts.get_IS(Product)
        qty_UGD = qty_UGDA01 + qty_UGDN02
        if qty_UGAI01>0:
            if RG_GIIS_AI == 'No':
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGAI01",qty_UGAI01)
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGAI03",qty_UGAI01)
        if qty_UGAO02>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGAO02",qty_UGAO02)
        if qty_UGD>0:
            if RG_NAMUR == 'No':
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGDA01",qty_UGD)
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGDA01",qty_UGDA01)
        if qty_UGDN02 > 0 and RG_NAMUR == 'Yes':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGDN02",qty_UGDN02)
        #CXCPQ-46436
        qty_ULLI01 = GS_C300_UMC_Parts.get_ULLI01(Product)
        if qty_ULLI01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-ULLI01",qty_ULLI01)
        #CXCPQ-46802
        qty_UDXA01 = GS_C300_UMC_Parts.get_UDXA01(Product)
        if qty_UDXA01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDXA01",qty_UDXA01)
    elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
        RG_GIIS_AI = Product.Attr('SerC_RG_GIIS_Analog_Inputs_Isolator_2Wire_Type').GetValue()
        RG_NAMUR = Product.Attr('SerC_RG_Is_NAMUR_isolator_type_Required').GetValue()
        #CXCPQ-51339,CXCPQ-52369
        mark_UDIR01, mark_UDOR01 = GS_C300_UMC_MARK.get_MARK_RLY(Product)
        if mark_UDIR01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDIR01",mark_UDIR01)
        if mark_UDOR01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDOR01",mark_UDOR01)
        #CXCPQ-50903,CXCPQ-51334,CXCPQ-51337
        mark_UGAI01, mark_UGAO02, mark_UGDA01,mark_UGDN02 = GS_C300_UMC_MARK.get_MARK_IS(Product)
        qty_UGD = mark_UGDA01+mark_UGDN02
        if mark_UGAI01>0:
            if RG_GIIS_AI == 'No':
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGAI01",mark_UGAI01)
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGAI03",mark_UGAI01)
        if mark_UGAO02>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGAO02",mark_UGAO02)
        if qty_UGD>0:
            if RG_NAMUR == 'No':
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGDA01",qty_UGD)
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGDA01",mark_UGDA01)
        if mark_UGDN02 > 0 and RG_NAMUR == 'Yes':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGDN02",mark_UGDN02)
        #CXCPQ-51338,CXCPQ-51336,CXCPQ-50912
        mark_UDXA01, mark_UAOA02, mark_UAIA01 = GS_C300_UMC_MARK.get_MARK_ISLTR(Product)
        if mark_UDXA01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDXA01",mark_UDXA01)
        if mark_UAOA02>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UAOA02",mark_UAOA02)
        if mark_UAIA01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UAIA01",mark_UAIA01)
        #CXCPQ-50900
        mark_UPTA01 = GS_C300_UMC_MARK.get_MARK_NIS(Product)
        if mark_UPTA01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UPTA01",mark_UPTA01)
        #CXDEV-8814 -Kaousalya Adala
        qty_UDIA01 = GS_C300_UMC_Parts.get_UDIA01(Product)
        if qty_UDIA01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDIA01",qty_UDIA01)
        #CXDEV-8815 - Kaousalya Adala
        qty_UDOA01 = GS_C300_UMC_Parts.get_UDOA01(Product)
        if qty_UDOA01>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDOA01",qty_UDOA01)

    if io_family=='Series C' and io_mounting=='Universal Process Cab - 1.3M':
        qty9=GS_C300_RG_UPC_Calc3.getpartCCUPTA01(Product)
        if qty9>0 and io_mounting=='Universal Process Cab - 1.3M':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UPTA01",qty9)

    #CXCPQ-53578,CXCPQ-45942,CXCPQ-45988
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-402",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-202",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-412",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-212",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-112",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-402",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-202",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-102",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-412",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-212",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-112",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-606",0)
    #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-302",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-726",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-736",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51153818-201",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51153818-202",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51153818-203",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51153818-204",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51153818-101",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51153818-102",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51153818-103",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51153818-104",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-102",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-716",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-706",0)
    #GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-302",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-312",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-722",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-732",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202341-102",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202341-112",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51195479-200",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51195479-400",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202330-200",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202330-300",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-802",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-812",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KFTA00",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KFTA05",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KFTA10",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KFTA15",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KFTA20",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KFTA25",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KFTA30",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KFTA35",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KFTA40",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KFTA45",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KFTA50",0)
    #Product.ApplyRules()

    PCNT = Product.Attr('PCNT_Val').GetValue() if Product.Attr('PCNT_Val').GetValue() != '' else 0
    PCNT02 = Product.Attr('PCNT02_Val').GetValue() if Product.Attr('PCNT_Val').GetValue() != '' else 0
    PCNT05 = Product.Attr('PCNT05_Val').GetValue() if Product.Attr('PCNT_Val').GetValue() != '' else 0
    IO_fam = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    Type_Controller = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
    Controller_type = Product.Attr('SerC_CG_Controller_Type').GetValue()
    PMIO_req = Product.Attr('SerC_CG_PM_IO_Solution_required').GetValue()
    A = int(float(Product.Attr('C300_RG_PMIO_Total_IO_Load').GetValue())) if Product.Attr('C300_RG_PMIO_Total_IO_Load').GetValue() != '' else 0
    ### TION need to inherit from COntrol grp
    #TION = Product.Attr('TION_Val').GetValue() if Product.Attr('TION_Val').GetValue() != '' else 0
    TION = GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_RG_Part_Summary', 'CC-TION11')
    CBDD = GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_RG_Part_Summary', 'CC-CBDD01')
    #CXCPQ-53578,CXCPQ-45942,CXCPQ-45988
    if IO_fam == "Series C" and Type_Controller == "C300 CEE":
        qty = GS_SerC_IOLink.SerC_IOLink(Product,PCNT)
        cab_access_qty,D_qty = GS_SerC_IOLink.SerC_Header(Product)
    #CXCPQ-46126,CXCPQ-46127
    elif IO_fam == "Series-C Mark II":
        qty = GS_SerC_IOLink.SMC_IOLink(Product,PCNT)
        ext_qty = GS_SerC_IOLink.SMC_extension(Product)
    #CXCPQ-46122,CXCPQ-46124
    elif IO_fam == "Turbomachinery":
        qty = GS_SerC_IOLink.Turbo_IOLink(Product,PCNT)
        cab_access_qty,D_qty = GS_SerC_IOLink.Turbo_Header(Product)
    if (IO_fam == "Series C" and Type_Controller == "C300 CEE") or IO_fam == "Turbomachinery":
        D = qty['D']
        Trace.Write(str(qty))
        #Log.Info("Mark2:"+str(qty))
        Product.Messages.Add("PCNT 'D' value is {}".format(D))
        rounded_D = math.ceil(D/10.0)
        round_parts = {1:["51153818-201"],2:["51153818-201","51153818-202"],3:["51153818-201","51153818-202","51153818-203"],4:["51153818-201","51153818-202","51153818-203","51153818-204"],5:["51153818-201","51153818-202","51153818-203","51153818-204","51153818-101"],6:["51153818-201","51153818-202","51153818-203","51153818-204","51153818-101","51153818-102"],7:["51153818-201","51153818-202","51153818-203","51153818-204","51153818-101","51153818-102","51153818-103"],8:["51153818-201","51153818-202","51153818-203","51153818-204","51153818-101","51153818-102","51153818-103","51153818-104"]}
        #if IO_fam == "Series C" and Type_Controller == "C300 CEE":
        Trace.Write("qnt F"+str(qty['F']))
        Trace.Write("qnt H"+str(qty['H']))
        if qty['H'] in range(1,4):
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-402",qty['F']*int(float(PCNT)))
        elif qty['H'] == 4:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-202",qty['F']*int(float(PCNT)))
        elif qty['H'] in range(5,7):
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-102",qty['F']*int(float(PCNT)))

        if qty['H1'] in range(1,4):
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-412",qty['G']*int(float(PCNT)))
        elif qty['H1'] == 4:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-212",qty['G']*int(float(PCNT)))
        elif qty['H1'] in range(5,7):
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-112",qty['G']*int(float(PCNT)))
    #CXCPQ-45942
    if IO_fam == "Series C" and Type_Controller == "C300 CEE":
        if cab_access_qty>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-606",cab_access_qty)
        '''if PCNT02: 
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-302",int(PCNT02))
        if PCNT05:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-302",int(PCNT05))'''
        #CXCPQ-45988
        if D > 0 and D < 41:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-726",D_qty)
            if rounded_D in round_parts:
                for part in round_parts[rounded_D]:
                    if int(PCNT02):
                        if Controller_type == "Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT02)/2)
                        elif Controller_type == "Non Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT02))
                    if int(PCNT05):
                        if Controller_type == "Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT05)/2)
                        elif Controller_type == "Non Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT05))
        elif D > 40 and D <= 80:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-736",D_qty)
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-726",D_qty)
            if rounded_D in round_parts:
                for part in round_parts[rounded_D]:
                    if int(PCNT02):
                        if Controller_type == "Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT02)/2)
                        elif Controller_type == "Non Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT02))
                    if int(PCNT05):
                        if Controller_type == "Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT05)/2)
                        elif Controller_type == "Non Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT05))
    #CXCPQ-46127,CXCPQ-52364
    elif IO_fam == "Series-C Mark II":
        '''if PCNT02: 
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-102",int(PCNT02))
        if PCNT05:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-102",int(PCNT05))'''
        D = qty['D']
        Trace.Write(str(qty))
        #Product.Messages.Add("PCNT 'D' value is {}".format(D))
        rounded_D = math.ceil(D/10.0)
        round_parts = {1:["51153818-201"],2:["51153818-201","51153818-202"],3:["51153818-201","51153818-202","51153818-203"],4:["51153818-201","51153818-202","51153818-203","51153818-204"],5:["51153818-201","51153818-202","51153818-203","51153818-204","51153818-101"],6:["51153818-201","51153818-202","51153818-203","51153818-204","51153818-101","51153818-102"],7:["51153818-201","51153818-202","51153818-203","51153818-204","51153818-101","51153818-102","51153818-103"],8:["51153818-201","51153818-202","51153818-203","51153818-204","51153818-101","51153818-102","51153818-103","51153818-104"]}
        #if IO_fam == "Series C" and Type_Controller == "C300 CEE":
        if qty['H'] in range(1,4):
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-402",qty['F']*int(float(PCNT)))
        elif qty['H'] == 4:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-202",qty['F']*int(float(PCNT)))
        elif qty['H'] in range(5,7):
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-102",qty['F']*int(float(PCNT)))

        if qty['H1'] in range(1,4):
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-412",qty['G']*int(float(PCNT)))
        elif qty['H1'] == 4:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-212",qty['G']*int(float(PCNT)))
        elif qty['H1'] in range(5,7):
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202971-112",qty['G']*int(float(PCNT)))
        if D > 0 and D < 41:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-706",ext_qty)
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-802",2*int(CBDD))
            if rounded_D in round_parts:
                for part in round_parts[rounded_D]:
                    if int(PCNT02):
                        if Controller_type == "Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT02)/2)
                        elif Controller_type == "Non Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT02))
                    if int(PCNT05):
                        if Controller_type == "Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT05)/2)
                        elif Controller_type == "Non Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT05))
        elif D > 40 and D <= 80:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-716",ext_qty)
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-706",ext_qty)
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-802",2*int(CBDD))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-812",2*int(CBDD))
            if rounded_D in round_parts:
                for part in round_parts[rounded_D]:
                    if int(PCNT02):
                        if Controller_type == "Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT02)/2)
                        elif Controller_type == "Non Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT02))
                    if int(PCNT05):
                        if Controller_type == "Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT05)/2)
                        elif Controller_type == "Non Redundant":
                            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(PCNT05))
    #CXCPQ-46124,CXCPQ-46125
    elif IO_fam == "Turbomachinery":
        if cab_access_qty>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-606",cab_access_qty)
        # if PCNT02:
        #     GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-302",int(PCNT02))
        if D > 0 and D < 7:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-726",D_qty)
            #jumper part
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51153818-201",int(float(PCNT)))
        elif D > 6 and D <= 12:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-736",D_qty)
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-726",D_qty)
            #jumper parts
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51153818-201",int(float(PCNT)))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51153818-101",int(float(PCNT)))
    #CXCPQ-55580,CXCPQ-55589 - Series C PM IO
    if IO_fam == "Series C" and (Type_Controller == "C300 CEE" or Type_Controller == "") and PMIO_req == "Yes":
        PMIO_PCNT = PMIO_B =0
        Length_FTA = Product.Attr('Length_of_IOP_FTA_Cable').GetValue()
        FTA_cables_len = ['InCab','10M','15M','20M','25M','30M','35M','40M','45M','50M']
        FTA_Parts = ['MU-KFTA00','MU-KFTA10','MU-KFTA15','MU-KFTA20','MU-KFTA25','MU-KFTA30','MU-KFTA35','MU-KFTA40','MU-KFTA45','MU-KFTA50']
        if Controller_type == "Redundant":
            if int(PCNT02):
                PMIO_B = math.ceil(int(PCNT02)/2)
            if int(PCNT05):
                PMIO_B = math.ceil(int(PCNT05)/2)
        elif Controller_type == "Non Redundant":
            if int(PCNT02):
                PMIO_B = int(PCNT02)
            if int(PCNT05):
                PMIO_B = int(PCNT05)
        B = 0
        if A and PMIO_B:
            B = math.ceil(A/int(PMIO_B))
        if int(PCNT02):
            PMIO_PCNT = int(PCNT02)
        if int(PCNT05):
            PMIO_PCNT = int(PCNT05)
        FTA_A = GS_SerC_IOLink.PMIO_RG_FTA(Product)
        if Length_FTA == '5M':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",'MU-KFTA05',FTA_A)
            Length_FTA = '05M'
        for length,part in zip(FTA_cables_len,FTA_Parts):
            if Length_FTA in length:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",part,FTA_A)
        '''GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51195479-200",PMIO_PCNT)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51195479-400",PMIO_PCNT)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202330-200",PMIO_PCNT)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202330-300",PMIO_PCNT)
        if B > 0 and B <= 40:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-302",PMIO_PCNT)
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-722",PMIO_PCNT)
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202341-102",PMIO_PCNT)
        elif B > 40 and B <= 80:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-302",PMIO_PCNT)
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-312",PMIO_PCNT)
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-722",PMIO_PCNT)
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-732",PMIO_PCNT)
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202341-102",PMIO_PCNT)
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202341-112",PMIO_PCNT)'''
    #CXCPQ-55123,CXCPQ-55119,CXCPQ-55125 --IOHIVE IO
    #CXCPQ-52363,CXCPQ-52362,CXCPQ-52361 --CN100 IO
    IOHIVE_controller = ['CN100 I/O HIVE - C300 CEE','Control HIVE - Physical','Control HIVE - Virtual','CN100 CEE']
    if IO_fam == "Series C" and Type_Controller in IOHIVE_controller:
        Trace.Write('inside--Series C--'+str(TION))
        qty = GS_SerC_IOLink.IOHIVE_drop(Product)
        cab_access_qty,IION,D_qty = GS_SerC_IOLink.IO_Header(Product)
        D = qty['D']
        Product.Messages.Add("CN100 'D' value is {}".format(D))
        rounded_D = math.ceil(D/10.0)
        round_parts = {1:["51153818-201"],2:["51153818-201","51153818-202"],3:["51153818-201","51153818-202","51153818-203"],4:["51153818-201","51153818-202","51153818-203","51153818-204"]}
        if qty['H'] in range(1,4):
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-402",qty['F']*int(float(TION)))
        elif qty['H'] == 4:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-202",qty['F']*int(float(TION)))
        elif qty['H'] in range(5,7):
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-102",qty['F']*int(float(TION)))

        if cab_access_qty>0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-606",cab_access_qty)
        # if IION:
        #     GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-302",int(IION))
        if D > 0 and D < 41:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202329-726",D_qty)
            if rounded_D in round_parts:
                for part in round_parts[rounded_D]:
                    #CCEECOMMBR-7120
                    #if int(IION):
                    #    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(IION))
                    Trace.Write('inside--Series C--part--'+str(part)+'--'+str(TION))
                    if int(TION):
                        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary",str(part),int(TION))

    Product.ApplyRules()
    #Product.ExecuteRulesOnce = False