#51563
import math as m
import System.Decimal as D
import GS_C300_MCAR_calcs
def Turbo_cab_bays(Product):
    CBDS01,CBDD01,RF_4,RR_3,RFR_2,RF_6,RR_5,RFR_5,Std_5,Gray_200,Custom_100,Single_S1,Single_D1,Dual_S1,Dual_D1,Single_130,Single_180,Dual_130,Dual_180,X,Y,Z,L,C1,C2=GS_C300_MCAR_calcs.cab_51436(Product)
    A=B=C=F=D=E=0
    if Product.Name=="Series-C Control Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Trace.Write(family)
        cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        Trace.Write(cab_ac)
        if family=="Turbomachinery" and (cab_ac=="Dual Access" or cab_ac=="Single Access" ):
            A=CBDS01+CBDD01
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
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Trace.Write(family)
        cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        Trace.Write(cab_ac)
        if family=="Turbomachinery" and (cab_ac=="Dual Access" or cab_ac=="Single Access" ):
            A=CBDS01+CBDD01
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
#A,B,C,D,E,F=Turbo_cab_bays(Product)
#Trace.Write(A)
#Trace.Write(B)
#Trace.Write(C)
#Trace.Write(D)
#Trace.Write(E)
#Trace.Write(F)

#51571
def Turbo_Cab_qty1(Product):
    A,B,C,D,E,F=Turbo_cab_bays(Product)
    Turbo_Cab_qty1=Turbo_Cab_qty2=0
    if Product.Name=="Series-C Control Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Complexing=Product.Attr('SerC_CG_Complexing').GetValue()
        cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        if family=="Turbomachinery" and  Complexing== "Factory" and cab_ac=="Dual Access" :
            Turbo_Cab_qty1=3*B+1*D+2*E
        elif family=="Turbomachinery" and  Complexing== "Field" and cab_ac=="Dual Access" :
            Turbo_Cab_qty2=3*B+1*D+2*E
    elif Product.Name=="Series-C Remote Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Complexing=Product.Attr('SerC_RG_Complexing').GetValue()
        cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        if family=="Turbomachinery" and  Complexing== "Factory" and cab_ac=="Dual Access" :
            Turbo_Cab_qty1=3*B+1*D+2*E
        elif family=="Turbomachinery" and  Complexing== "Field" and cab_ac=="Dual Access" :
            Turbo_Cab_qty2=3*B+1*D+2*E
    return Turbo_Cab_qty1,Turbo_Cab_qty2
#Turbo_Cab_qty1,Turbo_Cab_qty2=Turbo_Cab_qty1(Product)
#Trace.Write(Turbo_Cab_qty1)
#Trace.Write(Turbo_Cab_qty2)

#51568
def Turbo_Cab_qty2(Product):
    A,B,C,D,E,F=Turbo_cab_bays(Product)
    Turbo_Cab_qty3=Turbo_Cab_qty4=0
    if Product.Name=="Series-C Control Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Complexing=Product.Attr('SerC_CG_Complexing').GetValue()
        cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        if family=="Turbomachinery" and  Complexing== "Factory" and cab_ac=="Single Access" :
            Turbo_Cab_qty3=3*B+1*D+2*E
        elif family=="Turbomachinery" and  Complexing== "Field" and cab_ac=="Single Access" :
            Turbo_Cab_qty4=3*B+1*D+2*E
    elif Product.Name=="Series-C Remote Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Complexing=Product.Attr('SerC_RG_Complexing').GetValue()
        cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        if family=="Turbomachinery" and  Complexing== "Factory" and cab_ac=="Single Access" :
            Turbo_Cab_qty3=3*B+1*D+2*E
        elif family=="Turbomachinery" and  Complexing== "Field" and cab_ac=="Single Access" :
            Turbo_Cab_qty4=3*B+1*D+2*E
    return Turbo_Cab_qty3,Turbo_Cab_qty4
#Turbo_Cab_qty3,Turbo_Cab_qty4=Turbo_Cab_qty2(Product)
#Trace.Write(Turbo_Cab_qty3)
#Trace.Write(Turbo_Cab_qty4)
#53770
def Turbo_cab_53770(Product):
    cg_part1=Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
    rg_part1=Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
    part1=['MU-C8SS01']
    part2=['MU-C8DS01']
    part3=['CC-CBDD01']
    part4=['CC-CBDS01']
    C8DS01=C8SS01=CBDD01=CBDS01=Qty=0
    if Product.Name=="Series-C Control Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Trace.Write(family)
        type_controller=Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
        PMIO_Req=Product.Attr('SerC_CG_PM_IO_Solution_required').GetValue()
        for row in cg_part1.Rows:
            if row.GetColumnByName("PartNumber").Value in part1:
                C8DS01 +=int(row.GetColumnByName("Part_Qty").Value)
                Trace.Write("Sum="+str(C8DS01))
        for row in cg_part1.Rows:
            if row.GetColumnByName("PartNumber").Value in part2:
                C8SS01 +=int(row.GetColumnByName("Part_Qty").Value)
                Trace.Write("Sum1="+str(C8SS01))
        for row in cg_part1.Rows:
            if row.GetColumnByName("PartNumber").Value in part3:
                CBDD01 +=int(row.GetColumnByName("Part_Qty").Value)
                Trace.Write("Sum="+str(CBDD01))
        for row in cg_part1.Rows:
            if row.GetColumnByName("PartNumber").Value in part4:
                CBDS01 +=int(row.GetColumnByName("Part_Qty").Value)
                Trace.Write("Sum="+str(CBDS01))
        if family=="Series C" and (type_controller=="C300 CEE" or type_controller=="") and PMIO_Req=="Yes" :
            Qty=C8DS01+C8SS01+CBDD01+CBDS01
    elif Product.Name=="Series-C Remote Group":
        family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Trace.Write(family)
        for row in rg_part1.Rows:
            if row.GetColumnByName("PartNumber").Value in part1:
                C8DS01 +=int(row.GetColumnByName("Part_Qty").Value)
                Trace.Write("Sum="+str(C8DS01))
        for row in rg_part1.Rows:
            if row.GetColumnByName("PartNumber").Value in part2:
                C8SS01 +=int(row.GetColumnByName("Part_Qty").Value)
                Trace.Write("Sum1="+str(C8SS01))
        for row in rg_part1.Rows:
            if row.GetColumnByName("PartNumber").Value in part3:
                CBDD01 +=int(row.GetColumnByName("Part_Qty").Value)
                Trace.Write("Sum="+str(CBDD01))
        for row in rg_part1.Rows:
            if row.GetColumnByName("PartNumber").Value in part4:
                CBDS01 +=int(row.GetColumnByName("Part_Qty").Value)
                Trace.Write("Sum="+str(CBDS01))
        if family=="Series C" :
            Qty=C8DS01+C8SS01+CBDD01+CBDS01
    return Qty
#Qty=Turbo_cab_53770(Product)
#Trace.Write(Qty)