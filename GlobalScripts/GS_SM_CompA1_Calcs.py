import math as m
import System.Decimal as D
#parts_dict={}
def get_int(val):
    if val!="":
        return int(val)
    return 0

def get_thing(n):
    if n != "":
        n = int(float(n))
    else:
        n = 0
    return n

def get_CompA1(Product):
    if Product.Name == "SM Control Group":
        if Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Switch_Safety_IO').DisplayValue in ["Control Network Module (CNM)" , "Third Party MOXA"]:
            A=B=C=D=E=F=G=H=I=J=K=L=m1=0
            IOTAR=int(get_thing(Product.Attr('Rusio_IotaR').GetValue()))
            IOTANR=int(get_thing(Product.Attr('Rusio_IotaNR').GetValue()))
            FC_TUIO11=int(get_thing(Product.Attr('FC_TUIO').GetValue()))
            FC_TDIO11 = int(get_thing(Product.Attr('FC_TDIO').GetValue()))
            SM_Control_Group = Product.GetContainerByName('SM_RemoteGroup_Cont').Rows.Count
            A = int(IOTAR)+int(IOTANR)+int(FC_TUIO11)+int(FC_TDIO11)
            Trace.Write("A:"+str(A))
            if A>0:
                B = int(SM_Control_Group)
            Trace.Write("B:"+str(B))
            C=A+B
            Trace.Write("C:"+str(C))
            D=C/11
            Trace.Write("D:"+str(D))
            if C<=0:
                E=0
            else:
                E=((C-1)//11)
            Trace.Write("E:"+str(E))
            if C>12:
                F= C-((E*11) +1)
            else:
                F=C-(E*12)
            Trace.Write("F:"+str(F))
            if F<=0:
                G=0
            elif C<=4 or F<=3:
                G=0.5
            else:
                G=1
            Trace.Write("G:"+str(G))
            H=B//8
            Trace.Write("H:"+str(H))
            I=B-((H*8))
            Trace.Write("I:"+str(I))
            if I<=0:
                J=0
            elif I<=3 or C<=4:
                J=0.5
            else:
                J=1
            Trace.Write("J:"+str(J))
            K=(E+G)
            Trace.Write("K:"+str(K))
            L=(H+J)
            Trace.Write("L:"+str(L))
            m1=(max(K,L))
            Trace.Write("M1:"+str(m1))
            A_Comp={'A1':A,'A2':B,'M':m1}
            return A_Comp
    elif Product.Name == "SM Remote Group":
        if Product.Attr('SM_CG_Safety_IO_Link').GetValue() in ["Control Network Module (CNM)" , "Third Party MOXA"]:
            A=B=C=D=E=F=G=H=I=J=K=L=m1=0
            IOTAR=get_thing(Product.Attr('RUSIO_RG_IOTAR').GetValue())
            IOTANR=get_thing(Product.Attr('RUSIO_RG_IOTANR').GetValue())
            FC_TUIO11=get_thing(Product.Attr('FC_RG_TUIO').GetValue())
            FC_TDIO11 = get_thing(Product.Attr('FC_RG_TDIO').GetValue())
            A = int(IOTAR)+int(IOTANR)+int(FC_TUIO11)+int(FC_TDIO11)
            Trace.Write("A:"+str(A))
            B = 0
            Trace.Write("B:"+str(B))
            C=A+B
            Trace.Write("C:"+str(C))
            D=C/11
            Trace.Write("D:"+str(D))
            if C<=0:
                E=0
            else:
                E=((C-1)//11)
            Trace.Write("E:"+str(E))
            if C>12:
                F= C-((E*11) +1)
            else:
                F=C-(E*12)
            Trace.Write("F:"+str(F))
            if F<=0:
                G=0
            elif C<=4 or F<=3:
                G=0.5
            else:
                G=1
            Trace.Write("G:"+str(G))
            H=B//8
            Trace.Write("H:"+str(H))
            I=B-((H*8))
            Trace.Write("I:"+str(I))
            if I<=0:
                J=0
            elif I<=3 or C<=4:
                J=0.5
            else:
                J=1
            Trace.Write("J:"+str(J))
            K=(E+G)
            Trace.Write("K:"+str(K))
            L=(H+J)
            Trace.Write("L:"+str(L))
            m1=(max(K,L))
            Trace.Write("M1:"+str(m1))
            A_Comp={'A1':A,'A2':B,'M':m1}
            return A_Comp
#Trace.Write(str(get_CompA1(Product)))
#CXCPQ-33621
#A_Comp=get_CompA1(Product)
def CCI_HSE(A_Comp, Product, parts_dict):
    Qty=0
    if Product.Name=="SM Control Group":
        if A_Comp['A1']>0:
            if Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_SCController_Architecture').DisplayValue=="Redundant" and Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Switch_Safety_IO').DisplayValue=="Control Network Module (CNM)":
                Qty = 1 + A_Comp['A1']
                parts_dict["FS-CCI-HSE-30"] = {'Quantity' : Qty, 'Description': 'SM RIO Ethernet Cable Set'}
            elif Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_SCController_Architecture').DisplayValue=="Redundant A.R.T+" and Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Switch_Safety_IO').DisplayValue=="Control Network Module (CNM)":
                Qty = 2 + A_Comp['A1']
                parts_dict["FS-CCI-HSE-30"] = {'Quantity' : Qty, 'Description': 'SM RIO Ethernet Cable Set'}
    elif Product.Name=="SM Remote Group":
        if Product.Attr('Controller_Architecture').GetValue()=="Redundant" and Product.Attr('SM_CG_Safety_IO_Link').GetValue()=="Control Network Module (CNM)" and A_Comp['A1']>0 :
            Qty= 1 + A_Comp['A1']
            parts_dict["FS-CCI-HSE-30"] = {'Quantity' : Qty, 'Description': 'SM RIO Ethernet Cable Set'}
        elif Product.Attr('Controller_Architecture').GetValue()=="Redundant A.R.T+" and Product.Attr('SM_CG_Safety_IO_Link').GetValue()=="Control Network Module (CNM)" and A_Comp['A1']>0:
            Qty= 2 + A_Comp['A1']
            parts_dict["FS-CCI-HSE-30"] = {'Quantity' : Qty, 'Description': 'SM RIO Ethernet Cable Set'}
    return parts_dict
#b=CCI_HSE(A_Comp, Product, parts_dict)
#Trace.Write(str(b))
#a_comp=get_CompA1(Product)
def get_CompC(parts_dict, Product,a_comp):
    C1 = C2 = C3 = C4 = 0
    if Product.Name == "SM Control Group":
        Trace.Write("MM:"+str(a_comp['M']))
        safenet=Product.Attr('SM_CG_Safety_IO_Link').GetValue()
        Trace.Write(safenet)
        if safenet=="Control Network Module (CNM)" and a_comp['A1']>0:
            Trace.Write("aaaaaa")
            C1=2*(D.Ceiling(a_comp['M']))
            Trace.Write("C1:"+str(C1))
            C2=2*(int(a_comp['M']))
            Trace.Write("C2:"+str(C2))
            C3=C1-C2
            parts_dict["CC-TNWD01"]={'Quantity':C1,'Description':'Total Network Module DIN Rail IOTA'}
            parts_dict["CC-INWM01"]={'Quantity':C1,'Description':'Total Main Module'}
            parts_dict["CC-INWE01"]={'Quantity':C2,'Description':'Total Expansion Module'}
            parts_dict["50165649-001"]={'Quantity':C3,'Description':'Total Filler Plate Assembly'}
    if Product.Name=="SM Remote Group":
        if Product.Attr('SM_CG_Safety_IO_Link').GetValue()=="Control Network Module (CNM)" and a_comp['A1']>0:
            Trace.Write("aaaaaa")
            C1=2*(D.Ceiling(a_comp['M']))
            Trace.Write("C1:"+str(C1))
            C2=2*(int(a_comp['M']))
            Trace.Write("C2:"+str(C2))
            C3=C1-C2
            parts_dict["CC-TNWD01"]={'Quantity':C1,'Description':'Total Network Module DIN Rail IOTA'}
            parts_dict["CC-INWM01"]={'Quantity':C1,'Description':'Total Main Module'}
            parts_dict["CC-INWE01"]={'Quantity':C2,'Description':'Total Expansion Module'}
            parts_dict["50165649-001"]={'Quantity':C3,'Description':'Total Filler Plate Assembly'}
    return parts_dict
#Trace.Write(str(get_CompC(parts_dict, Product,a_comp)))
#Trace.Write(str(get_CompC(parts_dict, Product,a_comp)))