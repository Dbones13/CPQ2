if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
    import GS_PS_Exp_Ent_BOM, GS_Get_Set_AtvQty
    import GS_C300_SeriesC_cabinet_bays_Cal,GS_C300_Series_C_Turbomachinery_cabinet_bays
    Product.ExecuteRulesOnce = True
    #46369,51572 Shivani
    A1,B1,C1,D1,E1,F1=GS_C300_Series_C_Turbomachinery_cabinet_bays.Turbo_cab_bays(Product)
    A,B,C,D,E,F=GS_C300_SeriesC_cabinet_bays_Cal.cab_bays(Product)
    Crate_Type=Product.Attr('Crate Type').GetValue()
    Trace.Write(Crate_Type)
    Crate_Design=Product.Attr('Crate Design').GetValue()
    Trace.Write(Crate_Design)
    Cabinet_Base_Size=Product.Attr('SerC_RG_Cabinet_Base_Size').GetValue()
    Trace.Write(Crate_Design)
    Complexing=Product.Attr('SerC_RG_Complexing').GetValue()
    Trace.Write(Crate_Design)
    #GS_Get_Set_AtvQty.resetParamQty(Product, "Series_C_RG_Part_Summary", ["CF-SP0000","CF-SP0001","CF-PP0000","CF-PP0001","CF-CT4A00","CF-CT4A02","CF-CT4A01","CF-CT4A03","CF-CT4000","CF-CT4002","CF-CT4001","CF-CT4003"])
    #GS_Get_Set_AtvQty.resetParamQty(Product, "Series_C_RG_Part_Summary", ["CF-SC0000","CF-SC0001","CF-SC0002","CF-SC0003","CF-SC0004","CF-SC0005","CF-PC0000","CF-PC0001","CF-PC0002","CF-PC0003","CF-PC0004","CF-PC0005","CF-CT7A00","CF-CT7A02","CF-CT8A00","CF-CT8A02","CF-CT9A00","CF-CT9A02","CF-CT7A01","CF-CT7A03","CF-CT8A01","CF-CT8A03","CF-CT9A01","CF-CT9A03","CF-CT7000","CF-CT7002","CF-CT8000","CF-CT8002","CF-CT9000","CF-CT9002","CF-CT7001","CF-CT7003","CF-CT8001","CF-CT8003","CF-CT9001","CF-CT9003"])
    family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    if family=="Series C" or family=="Turbomachinery":
        GS_Get_Set_AtvQty.resetParamQty(Product, "Series_C_RG_Part_Summary", ["CF-SC0000","CF-SC0001","CF-SC0002","CF-SC0003","CF-SC0004","CF-SC0005","CF-PC0000","CF-PC0001","CF-PC0002","CF-PC0003","CF-PC0004","CF-PC0005","CF-CT7A00","CF-CT7A02","CF-CT8A00","CF-CT8A02","CF-CT9A00","CF-CT9A02","CF-CT7A01","CF-CT7A03","CF-CT8A01","CF-CT8A03","CF-CT9A01","CF-CT9A03","CF-CT7000","CF-CT7002","CF-CT8000","CF-CT8002","CF-CT9000","CF-CT9002","CF-CT7001","CF-CT7003","CF-CT8001","CF-CT8003","CF-CT9001","CF-CT9003"])
        if Complexing=="Factory":
            if B>0 or C>0 or B1>0 or C1>0:
                if Crate_Type=="Domestic/Truck" and Crate_Design=="Standard" and Cabinet_Base_Size=="100mm" :
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SC0000",int(D)+int(D1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SC0002",int(E)+int(E1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SC0004",int(B)+int(B1))
                else:
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SC0000",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SC0002",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SC0004",0)
                if Crate_Type=="Domestic/Truck" and Crate_Design=="Standard" and Cabinet_Base_Size=="200mm" :
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SC0001",int(D)+int(D1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SC0003",int(E)+int(E1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SC0005",int(B)+int(B1))
                else:
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SC0001",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SC0003",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SC0005",0)

                if Crate_Type=="Domestic/Truck" and Crate_Design=="Premium" and Cabinet_Base_Size=="100mm" :
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PC0000",int(D)+int(D1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PC0002",int(E)+int(E1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PC0004",int(B)+int(B1))
                else:
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PC0000",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PC0002",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PC0004",0)
                if Crate_Type=="Domestic/Truck" and Crate_Design=="Premium" and Cabinet_Base_Size=="200mm" :
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PC0001",int(D)+int(D1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PC0003",int(E)+int(E1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PC0005",int(B)+int(B1))
                else:
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PC0001",0)     
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PC0003",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PC0005",0)

                if Crate_Type=="Air" and Crate_Design=="Standard" and Cabinet_Base_Size=="100mm" :
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7A00",int(D)+int(D1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8A00",int(E)+int(E1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9A00",int(B)+int(B1))
                else:
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A00",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8A00",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9A00",0)
                if Crate_Type=="Air" and Crate_Design=="Standard" and Cabinet_Base_Size=="200mm" :
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7A02",int(D)+int(D1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8A02",int(E)+int(E1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9A02",int(B)+int(B1))
                else:
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7A02",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8A02",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9A02",0)
                if Crate_Type=="Air" and Crate_Design=="Premium" and Cabinet_Base_Size=="100mm" :
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7A01",int(D)+int(D1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8A01",int(E)+int(E1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9A01",int(B)+int(B1))
                else:
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7A01",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8A01",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9A01",0)
                if Crate_Type=="Air" and Crate_Design=="Premium" and Cabinet_Base_Size=="200mm" :
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7A03",int(D)+int(D1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8A03",int(E)+int(E1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9A03",int(B)+int(B1))
                else:
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7A03",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8A03",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9A03",0)

                if Crate_Type=="Ocean" and Crate_Design=="Standard" and Cabinet_Base_Size=="100mm" :
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7000",int(D)+int(D1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8000",int(E)+int(E1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9000",int(B)+int(B1))
                else:
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7000",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8000",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9000",0)
                if Crate_Type=="Ocean" and Crate_Design=="Standard" and Cabinet_Base_Size=="200mm" :
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7002",int(D)+int(D1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8002",int(E)+int(E1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9002",int(B)+int(B1))
                else:
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7002",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8002",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9002",0)

                if Crate_Type=="Ocean" and Crate_Design=="Premium" and Cabinet_Base_Size=="100mm" :
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7001",int(D)+int(D1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8001",int(E)+int(E1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9001",int(B)+int(B1))
                else:
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7001",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8001",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9001",0)
                if Crate_Type=="Ocean" and Crate_Design=="Premium" and Cabinet_Base_Size=="200mm" :
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7003",int(D)+int(D1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8003",int(E)+int(E1))
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9003",int(B)+int(B1))
                else:
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT7003",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT8003",0)
                    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT9003",0)
    #45776 ,51576 Added by Shivani
    Complexing=Product.Attr('SerC_RG_Complexing').GetValue()
    family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    if family=="Series C" or family=="Turbomachinery":
        qty1=GS_C300_SeriesC_cabinet_bays_Cal.Cab_qty1(Product)
        A1,B1,C1,D1,E1,F1=GS_C300_Series_C_Turbomachinery_cabinet_bays.Turbo_cab_bays(Product)
        if qty1>0 or (D1>0 and Complexing=="Factory"):
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51196958-401",int(qty1)+int(D1))
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51196958-401",0)
        qty2=GS_C300_SeriesC_cabinet_bays_Cal.Cab_qty2(Product)
        Trace.Write("Cab2- "+str(qty2))
        if qty2>0 or (E1>0 and Complexing=="Factory"):
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51196958-402",int(qty2)+int(E1))
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51196958-402",0)
        qty3=GS_C300_SeriesC_cabinet_bays_Cal.Cab_qty3(Product)
        Trace.Write("Cab3- "+str(qty3))
        if qty3>0 or (B1>0 and Complexing=="Factory"):
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51196958-403",int(qty3)+int(B1))
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51196958-403",0)
    #49226,51576(Remaining else) Shivani
    Complexing=Product.Attr('SerC_RG_Complexing').GetValue()
    A=GS_C300_SeriesC_cabinet_bays_Cal.cab_bays400(Product)
    A,B,C,D,E,F=GS_C300_SeriesC_cabinet_bays_Cal.cab_bays(Product)
    A1,B1,C1,D1,E1,F1=GS_C300_Series_C_Turbomachinery_cabinet_bays.Turbo_cab_bays(Product)
    GS_Get_Set_AtvQty.resetParamQty(Product, "Series_C_RG_Part_Summary", ["51196958-400"])
    if (A>0 or A1>0) and Complexing=="Field":
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51196958-400",int(A)+int(A1))
    elif (F1>0 or F>0) and Complexing=="Factory":
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51196958-400",int(F1)+int(F))
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51196958-400",0)


    #46143,53770 Shivani
    if family=="Series C" or family=="Turbomachinery" :
        GS_Get_Set_AtvQty.resetParamQty(Product, "Series_C_RG_Part_Summary", ["CF-SP0000","CF-SP0001","CF-PP0000","CF-PP0001","CF-CT4A00","CF-CT4A02","CF-CT4A01","CF-CT4A03","CF-CT4000","CF-CT4002","CF-CT4001","CF-CT4003"])
        A1,B1,C1,D1,E1,F1=GS_C300_Series_C_Turbomachinery_cabinet_bays.Turbo_cab_bays(Product)
        A,B,C,D,E,F=GS_C300_SeriesC_cabinet_bays_Cal.cab_bays(Product)
        part=GS_C300_Series_C_Turbomachinery_cabinet_bays.Turbo_cab_53770(Product)
        Crate_Type=Product.Attr('Crate Type').GetValue()
        Trace.Write(Crate_Type)
        Crate_Design=Product.Attr('Crate Design').GetValue()
        Trace.Write(Crate_Design)
        Cabinet_Base_Size=Product.Attr('SerC_RG_Cabinet_Base_Size').GetValue()
        Trace.Write(Crate_Design)
        Complexing=Product.Attr('SerC_RG_Complexing').GetValue()
        Trace.Write(Crate_Design)
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        type_controller=Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
        PMIO_Req=Product.Attr('SerC_CG_PM_IO_Solution_required').GetValue()
        if (mounting_sol=="Cabinet" and Complexing=="Field") or ((type_controller=="C300 CEE" or type_controller=="") and PMIO_Req=="Yes")  :
            if (A>0 or part>0 or A1>0) and Crate_Type=="Domestic/Truck" and Crate_Design=="Standard" and Cabinet_Base_Size=="100mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SP0000",int(A)+int(part)+int(A1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SP0000",0)
            if (A>0 or part>0 or A1>0) and Crate_Type=="Domestic/Truck" and Crate_Design=="Standard" and Cabinet_Base_Size=="200mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SP0001",int(A)+int(part)+int(A1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SP0001",0)
            if (A>0 or part>0 or A1>0) and Crate_Type=="Domestic/Truck" and Crate_Design=="Premium" and Cabinet_Base_Size=="100mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PP0000",int(A)+int(part)+int(A1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PP0000",0)
            if (A>0 or part>0 or A1>0) and Crate_Type=="Domestic/Truck" and Crate_Design=="Premium" and Cabinet_Base_Size=="200mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PP0001",int(A)+int(part)+int(A1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PP0001",0)

            if (A>0 or part>0 or A1>0) and Crate_Type=="Air" and Crate_Design=="Standard" and Cabinet_Base_Size=="100mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A00",int(A)+int(part)+int(A1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A00",0)
            if (A>0 or part>0 or A1>0) and Crate_Type=="Air" and Crate_Design=="Standard" and Cabinet_Base_Size=="200mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A02",int(A)+int(part)+int(A1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A02",0)
            if (A>0 or part>0 or A1>0) and Crate_Type=="Air" and Crate_Design=="Premium" and Cabinet_Base_Size=="100mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A01",int(A)+int(part)+int(A1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A01",0)
            if (A>0 or part>0 or A1>0) and Crate_Type=="Air" and Crate_Design=="Premium" and Cabinet_Base_Size=="200mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A03",int(A)+int(part)+int(A1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A03",0)

            if (A>0 or part>0 or A1>0) and Crate_Type=="Ocean" and Crate_Design=="Standard" and Cabinet_Base_Size=="100mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4000",int(A)+int(part)+int(A1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4000",0)
            if (A>0 or part>0 or A1>0) and Crate_Type=="Ocean" and Crate_Design=="Standard" and Cabinet_Base_Size=="200mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4002",int(A)+int(part)+int(A1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4002",0)
            if (A>0 or part>0 or A1>0) and Crate_Type=="Ocean" and Crate_Design=="Premium" and Cabinet_Base_Size=="100mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4001",int(A)+int(part)+int(A1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4001",0)
            if (A>0 or part>0 or A1>0) and Crate_Type=="Ocean" and Crate_Design=="Premium" and Cabinet_Base_Size=="200mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4003",int(A)+int(part)+int(A1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4003",0)
        elif mounting_sol=="Cabinet" and Complexing=="Factory":
            if (F>0 or F1>0 ) and Crate_Type=="Domestic/Truck" and Crate_Design=="Standard" and Cabinet_Base_Size=="100mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SP0000",int(F)+int(F1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SP0000",0)
            if (F>0 or F1>0 ) and Crate_Type=="Domestic/Truck" and Crate_Design=="Standard" and Cabinet_Base_Size=="200mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SP0001",int(F)+int(F1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SP0001",0)
            if (F>0 or F1>0 ) and Crate_Type=="Domestic/Truck" and Crate_Design=="Premium" and Cabinet_Base_Size=="100mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PP0000",int(F)+int(F1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PP0000",0)
            if (F>0 or F1>0 ) and Crate_Type=="Domestic/Truck" and Crate_Design=="Premium" and Cabinet_Base_Size=="200mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PP0001",int(F)+int(F1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PP0001",0)

            if (F>0 or F1>0 ) and Crate_Type=="Air" and Crate_Design=="Standard" and Cabinet_Base_Size=="100mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A00",int(F)+int(F1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A00",0)
            if (F>0 or F1>0 ) and Crate_Type=="Air" and Crate_Design=="Standard" and Cabinet_Base_Size=="200mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A02",int(F)+int(F1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A02",0)
            if (F>0 or F1>0 ) and Crate_Type=="Air" and Crate_Design=="Premium" and Cabinet_Base_Size=="100mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A01",int(F)+int(F1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A01",0)
            if (F>0 or F1>0 ) and Crate_Type=="Air" and Crate_Design=="Premium" and Cabinet_Base_Size=="200mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A03",int(F)+int(F1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A03",0)

            if (F>0 or F1>0 ) and Crate_Type=="Ocean" and Crate_Design=="Standard" and Cabinet_Base_Size=="100mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4000",int(F)+int(F1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4000",0)
            if (F>0 or F1>0 ) and Crate_Type=="Ocean" and Crate_Design=="Standard" and Cabinet_Base_Size=="200mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4002",int(F)+int(F1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4002",0)
            if (F>0 or F1>0 ) and Crate_Type=="Ocean" and Crate_Design=="Premium" and Cabinet_Base_Size=="100mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4001",int(F)+int(F1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4001",0)
            if (F>0 or F1>0 ) and Crate_Type=="Ocean" and Crate_Design=="Premium" and Cabinet_Base_Size=="200mm" :
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4003",int(F)+int(F1))
            else:
                GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4003",0)
    Product.ApplyRules()
    Product.ExecuteRulesOnce = False