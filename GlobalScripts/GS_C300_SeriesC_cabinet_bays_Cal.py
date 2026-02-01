#45798
import GS_Get_Set_AtvQty
import math as m
import System.Decimal as D
import GS_C300_MCAR_calcs
import GS_C300_RG_UPC_Calc4
def cab_bays(Product):
    CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
    A=B=C=F=D=E=0
    CADS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS'))
    CASS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS'))
    if Product.Name=="Series-C Control Group":
        C8SS01=int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-C8SS01'))
        C8DS01=int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-C8DS01'))
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        marshling_cab=Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()
        cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
        if family=="Series C" and mounting_sol=="Cabinet" and marshling_cab in ("Yes","No") and cab_typ in ("Normal Cabinet","Alternate Cabinet") and cab_ac in ("Dual Access","Single Access" ):
            A=CBDS01+CBDD01+part100+part200+part300+part400+part500+part600+CADS+CASS+C8SS01+C8DS01
        elif family=="Series C" and mounting_sol=="Cabinet"and cab_typ=="Generic Cabinet" and ab_ac in ("Dual Access","Single Access" ):
            A=CASS12+CADS12
        if True:
            B=int(A/4)
            C=A%4
            if C==1:
                F=1 
                B=B
            if C==2:
                D=1
            if C==3:
                E=1
            
    elif Product.Name=="Series-C Remote Group":
        C8SS01=int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_RG_Part_Summary','CC-C8SS01'))
        C8DS01=int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_RG_Part_Summary','CC-C8DS01'))
        var4=GS_C300_RG_UPC_Calc4.getpartsUPC(Product)[4]
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        marshling_cab=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet').GetValue()
        cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
        if family=="Series C" and mounting_sol=="Cabinet" and marshling_cab in ("Yes","No") and cab_typ in ("Normal Cabinet","Alternate Cabinet") and cab_ac in ("Dual Access","Single Access" ):
            A=CBDS01+CBDD01+part100+part200+part300+part400+part500+part600+CADS+CASS+C8SS01+C8DS01
        elif family=="Series C" and mounting_sol=="Cabinet" and cab_typ=="Generic Cabinet" and cab_ac in ("Dual Access","Single Access" ):
            A=CASS12+CADS12
            Trace.Write("malfunc1-"+str(CASS12))
        if True:
            B=int(A/4)
            C=A%4
            if C==1:
                F=1 
                B=B
            if C==2:
                D=1
            if C==3:
                E=1
            
        elif family=="Series C" and mounting_sol=="Universal Process Cab - 1.3M":
            A=var4
            if True:
                B=int(A/4)
                C=A%4
                if C==1:
                    F=1 
                    B=B
                if C==2:
                    D=1
                if C==3:
                    E=1
    return A,B,C,D,E,F

#45769
def Cab_qty100(Product):
    CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
    A=B=C=D=E=F=Cab_qty100=0
    CADS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS'))
    CASS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS'))
    if Product.Name=="Series-C Control Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Trace.Write(family)
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        Trace.Write(mounting_sol)
        marshling_cab=Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()
        Trace.Write(marshling_cab)
        cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        Trace.Write(cab_ac)
        cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
        Trace.Write(cab_typ)
        if family=="Series C" and mounting_sol=="Cabinet" and (marshling_cab=="Yes") and (cab_typ=="Normal Cabinet" or cab_typ=="Alternate Cabinet")  and (cab_ac=="Dual Access" or cab_ac=="Single Access" ):
            A=part100+part200+part300+part400+part500+part600
            Trace.Write(A)
            if True:
                B=int(A/4)
                Trace.Write(B)
                C=A%4
                Trace.Write(C)
                if C==1:
                    F=1 
                    B=B
                if C==2:
                    D=1
                if C==3:
                    E=1
                Cab_qty100=(3*B+1*D+2*E)
    elif Product.Name=="Series-C Remote Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Trace.Write(family)
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        Trace.Write(mounting_sol)
        marshling_cab=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet').GetValue()
        Trace.Write(marshling_cab)
        cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        Trace.Write(cab_ac)
        cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
        Trace.Write(cab_typ)
        if family=="Series C" and mounting_sol=="Cabinet" and (marshling_cab=="Yes") and (cab_typ=="Normal Cabinet" or cab_typ=="Alternate Cabinet")  and (cab_ac=="Dual Access" or cab_ac=="Single Access" ):
            A=part100+part200+part300+part400+part500+part600
            Trace.Write(A)
            if True:
                B=int(A/4)
                Trace.Write(B)
                C=A%4
                Trace.Write(C)
                if C==1:
                    F=1 
                    B=B
                if C==2:
                    D=1
                if C==3:
                    E=1
                Cab_qty100=(3*B+1*D+2*E)
    return Cab_qty100
#Final=Cab_qty100(Product)
#Trace.Write(Final) 
#45776----Start----
def Cab_qty1(Product):
    A,B,C,D,E,F=cab_bays(Product)
    Cab_qty1=0
    if Product.Name=="Series-C Control Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Complexing=Product.Attr('SerC_CG_Complexing').GetValue()
        if family=="Series C" and  Complexing== "Factory" :
            Cab_qty1=1*D
    elif Product.Name=="Series-C Remote Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Complx=Product.Attr('SerC_RG_Complexing').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        if family=="Series C" and Complx =="Factory":
            Cab_qty1=1*D
        elif family=="Series C" and mounting_sol=="Universal Process Cab - 1.3M":
            Cab_qty1=1*D
    return Cab_qty1
def Cab_qty2(Product):
    A,B,C,D,E,F=cab_bays(Product)
    Cab_qty2=0
    if Product.Name=="Series-C Control Group" :
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Complexing=Product.Attr('SerC_CG_Complexing').GetValue()
        if family=="Series C" and Complexing == "Factory":
            Cab_qty2=1*E
    elif Product.Name=="Series-C Remote Group" :
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Complx=Product.Attr('SerC_RG_Complexing').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        if family=="Series C" and Complx =="Factory":
            Cab_qty2=1*E
        elif family=="Series C" and mounting_sol=="Universal Process Cab - 1.3M":
            Cab_qty2=1*E
    return Cab_qty2
def Cab_qty3(Product):
    A,B,C,D,E,F=cab_bays(Product)
    Cab_qty3=0
    if Product.Name=="Series-C Control Group" :
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Complexing=Product.Attr('SerC_CG_Complexing').GetValue()
        if family=="Series C" and Complexing== "Factory":
            Cab_qty3=1*B
    elif Product.Name=="Series-C Remote Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Complx=Product.Attr('SerC_RG_Complexing').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        if family=="Series C" and Complx =="Factory":
            Cab_qty3=1*B
        elif family=="Series C" and mounting_sol=="Universal Process Cab - 1.3M":
            Cab_qty3=1*B
    return Cab_qty3
#45776----end----
#45766
def cab_bays_kit(Product):
    CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
    A=B=C=F=D=E=cab_bays_kit1=cab_bays_kit2=cab_bays_kit3=cab_bays_kit4=cab_bays_kit5=cab_bays_kit6=cab_bays_kit7=cab_bays_kit8=0
    if Product.Name=="Series-C Control Group":
        C8SS01=int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-C8SS01'))
        C8DS01=int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-C8DS01'))
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        marshling_cab=Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()

        cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()

        Complexing=Product.Attr('SerC_CG_Complexing').GetValue()

        cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()

        Type_cntr=Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
        if family=="Series C" and cab_ac=="Single Access" and Complexing=="Factory" and (Type_cntr=="C300 CEE" or Type_cntr=="CN100 CEE" or Type_cntr=="CN100 I/O HIVE - C300 CEE" or Type_cntr=="Control HIVE - Physical" or Type_cntr=="Control HIVE - Virtual"):
            A=CBDS01+CBDD01+CASS12
            if True:
                B=int(A/4)
                C=A%4
                if C==1:
                    F=1 
                    B=B
                if C==2:
                    D=1
                if C==3:
                    E=1
            if marshling_cab=="No" and cab_typ=="Normal Cabinet":
                cab_bays_kit1=3*B+1*D+2*E
            elif cab_typ=="Generic Cabinet":
                cab_bays_kit5=3*B+1*D+2*E
        if family=="Series C" and cab_ac=="Single Access" and Complexing=="Field" and (Type_cntr=="C300 CEE" or Type_cntr=="CN100 CEE" or Type_cntr=="CN100 I/O HIVE - C300 CEE" or Type_cntr=="Control HIVE - Physical" or Type_cntr=="Control HIVE - Virtual") :
            A=CBDS01+CBDD01+CASS12+C8SS01+C8DS01
            if True:
                B=int(A/4)
                C=A%4
                if C==1:
                    F=1 
                    B=B
                if C==2:
                    D=1
                if C==3:
                    E=1
            if marshling_cab=="No" and cab_typ=="Normal Cabinet":
                cab_bays_kit2=3*B+1*D+2*E
            elif cab_typ=="Generic Cabinet":
                cab_bays_kit6=3*B+1*D+2*E

        if family=="Series C" and cab_ac=="Dual Access" and Complexing=="Factory" and (Type_cntr=="C300 CEE" or Type_cntr=="CN100 CEE" or Type_cntr=="CN100 I/O HIVE - C300 CEE" or Type_cntr=="Control HIVE - Physical" or Type_cntr=="Control HIVE - Virtual"):
            A=CBDS01+CBDD01+CADS12+C8SS01+C8DS01
            if True:
                B=int(A/4)
                C=A%4
                if C==1:
                    F=1 
                    B=B
                if C==2:
                    D=1
                if C==3:
                    E=1
                
            if marshling_cab=="No" and cab_typ=="Normal Cabinet":
                cab_bays_kit3=3*B+1*D+2*E
            elif cab_typ=="Generic Cabinet":
                cab_bays_kit7=3*B+1*D+2*E
        if family=="Series C" and cab_ac=="Dual Access" and Complexing=="Field" and (Type_cntr=="C300 CEE" or Type_cntr=="CN100 CEE" or Type_cntr=="CN100 I/O HIVE - C300 CEE" or Type_cntr=="Control HIVE - Physical" or Type_cntr=="Control HIVE - Virtual"):
            A=CBDS01+CBDD01+CADS12+C8SS01+C8DS01
            if True:
                B=int(A/4)
                C=A%4
                if C==1:
                    F=1 
                    B=B
                if C==2:
                    D=1
                if C==3:
                    E=1
                
            if marshling_cab=="No" and cab_typ=="Normal Cabinet":
                cab_bays_kit4=3*B+1*D+2*E
            elif cab_typ=="Generic Cabinet":
                cab_bays_kit8=3*B+1*D+2*E
    elif Product.Name=="Series-C Remote Group":
        C8SS01=int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_RG_Part_Summary','CC-C8SS01'))
        C8DS01=int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_RG_Part_Summary','CC-C8DS01'))
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()

        marshling_cab=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet').GetValue()

        Complx=Product.Attr('SerC_RG_Complexing').GetValue()
        cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()

        cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()

        Type_cntr=Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
        if family=="Series C" and cab_ac=="Single Access" and Complx=="Factory" and (Type_cntr=="C300 CEE" or Type_cntr=="CN100 CEE" or Type_cntr=="CN100 I/O HIVE - C300 CEE" or Type_cntr=="Control HIVE - Physical" or Type_cntr=="Control HIVE - Virtual") :
            A=CBDS01+CBDD01+CASS12+C8SS01+C8DS01
            Trace.Write(A)
            if True:
                B=int(A/4)
                Trace.Write(B)
                C=A%4
                Trace.Write(C)
                if C==1:
                    F=1 
                    B=B
                if C==2:
                    D=1
                if C==3:
                    E=1
            if marshling_cab=="No" and cab_typ=="Normal Cabinet":
                cab_bays_kit1=3*B+1*D+2*E
            elif cab_typ=="Generic Cabinet":
                cab_bays_kit5=3*B+1*D+2*E
        if family=="Series C" and cab_ac=="Single Access" and Complx=="Field" and (Type_cntr=="C300 CEE" or Type_cntr=="CN100 CEE" or Type_cntr=="CN100 I/O HIVE - C300 CEE" or Type_cntr=="Control HIVE - Physical" or Type_cntr=="Control HIVE - Virtual") :
            A=CBDS01+CBDD01+CASS12+C8SS01+C8DS01
            if True:
                B=int(A/4)
                C=A%4
                if C==1:
                    F=1 
                    B=B
                if C==2:
                    D=1
                if C==3:
                    E=1
            if marshling_cab=="No" and cab_typ=="Normal Cabinet":
                cab_bays_kit2=3*B+1*D+2*E
            elif cab_typ=="Generic Cabinet":
                cab_bays_kit6=3*B+1*D+2*E
        if family=="Series C" and cab_ac=="Dual Access" and Complx=="Factory" and (Type_cntr=="C300 CEE" or Type_cntr=="CN100 CEE" or Type_cntr=="CN100 I/O HIVE - C300 CEE" or Type_cntr=="Control HIVE - Physical" or Type_cntr=="Control HIVE - Virtual"):
            A=CBDS01+CBDD01+CADS12+C8SS01+C8DS01
            if True:
                B=int(A/4)
                C=A%4
                if C==1:
                    F=1 
                    B=B
                if C==2:
                    D=1
                if C==3:
                    E=1
            if marshling_cab=="No" and cab_typ=="Normal Cabinet":
                cab_bays_kit3=3*B+1*D+2*E
            elif cab_typ=="Generic Cabinet":
                cab_bays_kit7=3*B+1*D+2*E
        if family=="Series C" and cab_ac=="Dual Access" and Complx=="Field" and (Type_cntr=="C300 CEE" or Type_cntr=="CN100 CEE" or Type_cntr=="CN100 I/O HIVE - C300 CEE" or Type_cntr=="Control HIVE - Physical" or Type_cntr=="Control HIVE - Virtual") :
            A=CBDS01+CBDD01+CADS12+C8SS01+C8DS01
            if True:
                B=int(A/4)
                C=A%4
                if C==1:
                    F=1 
                    B=B
                if C==2:
                    D=1
                if C==3:
                    E=1
            if marshling_cab=="No" and cab_typ=="Normal Cabinet":
                cab_bays_kit4=3*B+1*D+2*E
            elif cab_typ=="Generic Cabinet":
                cab_bays_kit8=3*B+1*D+2*E
    return cab_bays_kit1,cab_bays_kit2,cab_bays_kit3,cab_bays_kit4,cab_bays_kit5,cab_bays_kit6,cab_bays_kit7,cab_bays_kit8
#49226 Shivani
def cab_bays400(Product):
    CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
    A=0
    CADS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS'))
    CASS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS'))
    if Product.Name=="Series-C Control Group":
        C8SS01=int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-C8SS01'))
        C8DS01=int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-C8DS01'))
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        marshling_cab=Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()
        cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
        if family=="Series C" and mounting_sol=="Cabinet" and (marshling_cab=="Yes" or marshling_cab=="No" ) and (cab_typ=="Normal Cabinet" or cab_typ=="Alternate Cabinet" or cab_typ=="Generic Cabinet")  and (cab_ac=="Dual Access" or cab_ac=="Single Access"):
            A=CBDS01+CBDD01+part100+part200+part300+part400+part500+part600+CADS+CASS+C8SS01+C8DS01
        elif family=="Series C" and mounting_sol=="Cabinet" and cab_typ=="Generic Cabinet" and (cab_ac=="Dual Access" or cab_ac=="Single Access"):
            A=CASS12+CADS12
    elif Product.Name=="Series-C Remote Group":
        C8SS01=int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_RG_Part_Summary','CC-C8SS01'))
        C8DS01=int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_RG_Part_Summary','CC-C8DS01'))        
        var4=GS_C300_RG_UPC_Calc4.getpartsUPC(Product)[4]
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        marshling_cab=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet').GetValue()
        cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
        if family=="Series C" and mounting_sol=="Cabinet" and (marshling_cab=="Yes" or marshling_cab=="No") and (cab_typ=="Normal Cabinet" or cab_typ=="Alternate Cabinet" or cab_typ=="Generic Cabinet")  and (cab_ac=="Dual Access" or cab_ac=="Single Access" ):
            A=CBDS01+CBDD01+part100+part200+part300+part400+part500+part600+CADS+CASS+C8SS01+C8DS01
        elif family=="Series C" and mounting_sol=="Cabinet" and cab_typ=="Generic Cabinet" and (cab_ac=="Dual Access" or cab_ac=="Single Access" ):
            A=CASS12+CADS12
        elif family=="Series C" and mounting_sol=="Universal Process Cab - 1.3M":
            A=var4
    return A
#45771 Shivani
def cab_bays66(Product):
    cg_part1=Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
    rg_part1=Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
    Part=['51454345-100', '51454345-200', '51454345-300', '51454345-400']
    Quantity=0
    if Product.Name=="Series-C Control Group" :
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        Trace.Write(mounting_sol)
        SUM=0
        for row in cg_part1.Rows:
            if row.GetColumnByName("PartNumber").Value in Part:
                SUM +=int(row.GetColumnByName("Part_Qty").Value)
                Trace.Write("SUM="+str(SUM))
        if family=="Series C" and mounting_sol=='Mounting Panel':
            Quantity=SUM
    elif Product.Name=="Series-C Remote Group" :
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        Trace.Write(mounting_sol)
        SUM=0
        for row in rg_part1.Rows:
            if row.GetColumnByName("PartNumber").Value in Part:
                SUM +=int(row.GetColumnByName("Part_Qty").Value)
                Trace.Write("SUM="+str(SUM))
        if family=="Series C" and mounting_sol=='Mounting Panel':
            Quantity=SUM
    return Quantity
#45767 Shivani
def shipping_bays(Product):
    cg_part1=Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
    rg_part1=Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
    Part=['50154983-001','51454345-100', '51454345-200', '51454345-300', '51454345-400']
    Quantity=0
    if Product.Name=="Series-C Control Group" :
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        Trace.Write(mounting_sol)
        SUM=0
        for row in cg_part1.Rows:
            if row.GetColumnByName("PartNumber").Value in Part:
                SUM +=int(row.GetColumnByName("Part_Qty").Value)
                Trace.Write("SUM="+str(SUM))
        if family=="Series C" and mounting_sol=='Mounting Panel':
            Quantity=SUM
        else:
            Quantity=0
    elif Product.Name=="Series-C Remote Group" :
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        var4=GS_C300_RG_UPC_Calc4.getpartsUPC(Product)[4]
        Trace.Write(mounting_sol)
        SUM=0
        for row in rg_part1.Rows:
            if row.GetColumnByName("PartNumber").Value in Part:
                SUM +=int(row.GetColumnByName("Part_Qty").Value)
                Trace.Write("SUM="+str(SUM))
        if family=="Series C" and mounting_sol=='Mounting Panel':
            Quantity=SUM
        elif family=="Series C" and mounting_sol=="Universal Process Cab - 1.3M":
            Quantity=var4
    return Quantity
#CXCPQ-47465
def Cab_Bay234(Product):
    CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
    A=B=C=D=E=F=Qty_47465_bay2=Qty_47465_bay3=Qty_47465_bay4=0
    CASS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS'))
    Trace.Write(CASS)
    if Product.Name=="Series-C Control Group" :
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
        Integrated_marshalling=Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()

        if family=="Series C":
            if mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Alternate Cabinet' and Integrated_marshalling=='No':
                A=CASS
                Trace.Write(A)
                if True:
                    B=int(A/4)
                    Trace.Write('B :'+str(B))
                    C=A%4
                    Trace.Write('C :'+str(C))
                    if C==1:
                        F=1
                    if C==0:
                        B=B
                    if C==2:
                        D=1
                    if C==3:
                        E=1
                    Qty_47465_bay2= D
                    Qty_47465_bay3= E
                    Qty_47465_bay4= B
                    Trace.Write('Qty_47465_bay4 :'+str(Qty_47465_bay4))
    elif Product.Name=="Series-C Remote Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
        Integrated_marshalling=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet').GetValue()

        if family=="Series C":
            if mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Alternate Cabinet' and Integrated_marshalling=='No':
                A=CASS
                Trace.Write(A)
                if True:
                    B=int(A/4)
                    C=A%4
                    if C==1:
                        F=1
                    if C==0:
                        B=B
                    if C==2:
                        D=1
                    if C==3:
                        E=1
                    Qty_47465_bay2= D
                    Qty_47465_bay3= E
                    Qty_47465_bay4= B
                    Trace.Write('Qty_47465_bay4 :'+str(Qty_47465_bay4))
    return Qty_47465_bay2,Qty_47465_bay3,Qty_47465_bay4
#CXCPQ-34705
def Cab_Bay_34705(Product):
    CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
    A=B=C=D=E=F=Qty_34705=0
    if Product.Name=="Series-C Control Group" :
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
        if family!='Series C' and mounting_sol!='Cabinet' and cab_ac!='Single Access' and (cab_typ!='Normal Cabinet' or cab_typ!='Alternate Cabinet'):
            return 0
        if family=="Series C":
            if mounting_sol=='Cabinet' and cab_ac=='Single Access' and (cab_typ=='Normal Cabinet' or cab_typ=='Alternate Cabinet'):
                A=part300+part600+CBDS01
                Trace.Write(A)
                if True:
                    B=int(A/4)
                    Trace.Write('B :'+str(B))
                    C=A%4
                    Trace.Write('C :'+str(C))
                    if C==0:
                        B=B
                    if C==1:
                        F=1
                    if C==2:
                        D=1
                    if C==3:
                        E=1
                    Qty_34705= 2*(B+D+E+F)
                    Trace.Write('Qty_34705 :'+str(Qty_34705))
    elif Product.Name=="Series-C Remote Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
        if family!='Series C' and mounting_sol!='Cabinet' and cab_ac!='Single Access' and (cab_typ!='Normal Cabinet' or cab_typ!='Alternate Cabinet'):
            return 0
        if family=="Series C":
            if mounting_sol=='Cabinet' and cab_ac=='Single Access' and (cab_typ=='Normal Cabinet' or cab_typ=='Alternate Cabinet'):
                A=part300+part600+CBDS01
                Trace.Write(A)
                if True:
                    B=int(A/4)
                    C=A%4
                    if C==0:
                        B=B
                    if C==1:
                        F=1
                    if C==2:
                        D=1
                    if C==3:
                        E=1
                    Qty_34705= 2*(B+D+E+F)
    return Qty_34705
#CXCPQ-83002
def Cab_Bay_83002(Product):
    CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
    A=B=C=D=E=F=Qty_83002=Qty_83003=0
    CADS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS'))
    CASS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS'))
    if Product.Name=="Series-C Control Group" :
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
        if family!='Series C' and mounting_sol!='Cabinet' and (cab_ac!='Single Access' or cab_ac!='Dual Access') and cab_typ!='Generic Cabinet':
            return 0
        if family=="Series C":
            if mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Generic Cabinet':
                A=part300+part600+CASS12
                Trace.Write(A)
                if True:
                    B=int(A/4)
                    Trace.Write('B :'+str(B))
                    C=A%4
                    Trace.Write('C :'+str(C))
                    if C==0:
                        B=B
                    if C==1:
                        F=1
                    if C==2:
                        D=1
                    if C==3:
                        E=1
                    Qty_83002= 2*(B+D+E+F)
                    Trace.Write('Qty_83002 :'+str(Qty_83002))
            elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Generic Cabinet':
                A=part300+part600+CADS12+CBDS01+CBDD01+part100+part200+part400+part500+CADS+CASS
                Trace.Write(A)
                if True:
                    B=int(A/4)
                    Trace.Write('B :'+str(B))
                    C=A%4
                    Trace.Write('C :'+str(C))
                    if C==0:
                        B=B
                    if C==1:
                        F=1
                    if C==2:
                        D=1
                    if C==3:
                        E=1
                    Qty_83003= 2*(B+D+E+F)
                    Trace.Write('Qty_83003 :'+str(Qty_83003))
    elif Product.Name=="Series-C Remote Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
        if family!='Series C' and mounting_sol!='Cabinet' and (cab_ac!='Single Access' or cab_ac!='Dual Access') and cab_typ!='Generic Cabinet':
            return 0
        if family=="Series C":
            if mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Generic Cabinet':
                A=part300+part600+CASS12
                Trace.Write(A)
                if True:
                    B=int(A/4)
                    C=A%4
                    if C==0:
                        B=B
                    if C==1:
                        F=1
                    if C==2:
                        D=1
                    if C==3:
                        E=1
                    Qty_83002= 2*(B+D+E+F)
            elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Generic Cabinet':
                A=part300+part600+CADS12+CBDS01+CBDD01+part100+part200+part400+part500+CADS+CASS
                Trace.Write(A)
                if True:
                    B=int(A/4)
                    Trace.Write('B :'+str(B))
                    C=A%4
                    Trace.Write('C :'+str(C))
                    if C==0:
                        B=B
                    if C==1:
                        F=1
                    if C==2:
                        D=1
                    if C==3:
                        E=1
                    Qty_83003= 2*(B+D+E+F)
                    Trace.Write('Qty_83003 :'+str(Qty_83003))
    return Qty_83002,Qty_83003