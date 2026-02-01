import System.Decimal as D
#import GS_C300_PMIO_Calcs_One,GS_C300_PMIO_Calcs_Two,GS_C300_PMIO_Calcs_Three,GS_PMIO_Variable
import GS_PMIO_Variable
from math import ceil
def PMIO_Parts(Product):
    MC_PHAO01=MC_PAIH03=BC_THAI11=MC_PSTX03=MC_PDOY22=BU_TDOC02=MC_PDIY22=MC_TAOY25=MC_GHAO21=MC_TAIH22=MC_TDOY22=MC_TDOY23=MC_TAIH12=MC_TAIH02=MC_TDIY22=MC_TAOY55=MC_TDOY62=MC_TDOY63=MC_TAIH52=MC_TAIH62=MC_TDIY62=BC_GHAI11=MC_GAIH13=MC_GAIH14=MC_PAIH01=MC_TAIH04=MC_TAIH14=MC_TAIH54=MC_PAIL02=MC_TAIL02=MC_PAOY22=MC_THAO11=MC_GHAO11=MC_TAOY22=MC_TAOY52=MC_PRHM01=MC_TRPA01=MC_GRMT01=MU_CMSC03=0
    MC_PLAM02=MC_TAMT14=MC_TAMR04=MC_TAMT04=MC_TLPA02=MU_KLAM03=MC_GPRD02=MU_KDPRYY=MU_KGPRXX=MU_KDPR05=MU_KDPR10=MU_KDPRInCab=0
    FTA_Connection=Product.Attr('FTA_Connection_Type').GetValue()
    Length_of_GI_IS_FTA_PDP_Cable=Product.Attr('Length_of_GI_IS_FTA_PDP_Cable').GetValue()
    Length_of_PS_PDP_Cable=Product.Attr('Length_of_PS_PDP_Cable').GetValue()
    Trace.Write(FTA_Connection)
    if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
        Trace.Write("AAAA ")
        #commented on 27/07/23
        """First = GS_C300_PMIO_Calcs_One.IOComponents(Product)
        Second = GS_C300_PMIO_Calcs_Two.IOComponents(Product)
        Third = GS_C300_PMIO_Calcs_Three.IOComponents(Product)
        JA11,JB11,JC11,KB11,JA12,JB12,JC12,KB12,NA11,NB11,NA12,NB12,AA11,AB11,AC11,AA12,AB12,AC12,DA11,DB11,DA12,DB12,BA11,BB11,BA12,BB12,X11,X12,X13,X21,X22,Y51,Y52,X41,X42,Y11,Y12,Y13,Y22,CA11,CB11,CC11,CA12,CB12,CC12,X31,X32,X33,EC11,EC12,X53,Y31,Y32,Y41,Y42,LA11,LB11,LA12,LB12,MA11,MB11,MA12,MB12,IC11,IC12,X93,X931,FC11,FC12,GC11,GC12,HC11,HC12,X63,X73,X83=First.c300_PIMO()
        PA11,PB11,PA12,PB12,Y71,Y72,WA11,WB11,WA12,WB12,A111,B111,A112,B112,Z51,Z52,Z91,Z92=Second.c300_PIMO_RLY()
        A1811,C1811,A2011,C2011,A1911,B1911,A511,B511,QX81,QX83,RX81,RX82,SX81,SX83,DX82,DX81,A1311,C1311,A1411,C1411,A1511,C1511,NX83,LX81,LX83,MX81,MX83,NX81,C1211,KX83,KX82,A1611,C1611,A1711,C1711,OX81,OX83,PX81,PX83,A411,B411,CX81,CX82=Third.SerC_PMIO_CG()
        result=GS_PMIO_Variable.partCalc(Product)
        FX81 = result["FX81"]
        EX83 = result["EX83"]
        FX83 = result["FX83"]
        GX83 = result["GX83"]
        HX83 = result["HX83"]
        IX83 = result["IX83"]
        JX83 = result["JX83"]"""
        JA11 = JB11 = JC11 = KB11 = JA12 = JB12 = JC12 = 0
        KB12 = NA11 = NB11 = NA12 = NB12 = AA11 = AB11 = 0
        AC11 = AA12 = AB12 = AC12 = DA11 = DB11 = 0
        DA12 = DB12 = BA11 = BB11 = BA12 = BB12 = X11 = 0
        X12 = X13 = X21 = X22 = Y51 = Y52 = X41 = X42 = Y11 = 0
        Y12 = Y13 = Y22 = CA11 = CB11 = CC11 = CA12 = CB12 = 0
        CC12 = X31 = X32 = X33 = EC11 = EC12 = X53 = Y31 = Y32 = 0
        Y41 = Y42 = LA11 = LB11 = LA12 = LB12 = MA11 = 0
        MB11 = MA12 = MB12 = IC11 = IC12 = X93 = X931 = 0
        FC11 = FC12 = GC11 = GC12 = HC11 = HC12 = X63 = X73 = X83 = 0
        PA11 = PB11 = PA12 = PB12 = Y71 = Y72 = WA11 = WB11 = WA12 = 0
        WB12 = A111 = B111 = A112 = B112 = Z51 = Z52 = Z91 = Z92 = 0
        A1811 = C1811 = A2011 = C2011 = A1911 = B1911 = A511 = 0
        B511 = QX81 = QX83 = RX81 = RX82 = SX81 = SX83 = DX82 = DX81 = 0
        A1311 = C1311 = A1411 = C1411 = A1511 = C1511 = NX83 = 0
        LX81 = LX83 = MX81 = MX83 = NX81 = C1211 = KX83 = KX82 = 0
        A1611 = C1611 = A1711 = C1711 = OX81 = OX83 = 0
        PX81 = PX83 = A411 = B411 = CX81 = CX82 = 0
        FX81 = EX83 = FX83 = GX83 = HX83 = IX83 = JX83 = 0
        result = GS_PMIO_Variable.partCalc(Product)
        for key in result.keys():
            locals()[key] = int(result[key])
        MC_PHAO01=(2*Y51) + Y52 + (2*DX81) + DX82
        MC_PAIH03=(2*X11) + X12 + X13 + (2*X41) + X42 + (2*X21) + X22 + (2*LX81) + LX83 + (2*MX81) + MX83 + (2*NX81) + NX83
        BC_THAI11=X21 + X22
        MC_PSTX03 = 2*(Y11) + Y12 + Y13 + Y22 + (2*QX81) + QX83 + (2*RX81) + RX82 + (2*SX81) + SX83
        MC_PDOY22 = (2*Z51) + Z52 + (2*Z91) + Z92 + KX83
        BU_TDOC02 = KX83
        MC_PDIY22 = (2*Y71) + Y72
        BC_GHAI11 = MX81 + RX81 + RX82 + MX83
        MC_GAIH13 = LX81 + LX83 + OX81 + OX83 + QX81 + QX83
        MC_GAIH14 = NX81 + NX83 + PX81 + PX83 + SX81 + SX83
        MC_PAIH01 = (2*X31) + X32 + X33 + (2*OX81) + OX83 + (2*PX81) + PX83
        MC_TAIH04 = X33
        MC_PAIL02 = X53
        MC_TAIL02 = X53
        MC_PAOY22 = (2*Y31) + Y32 + (2*Y41) + Y42 + (2*CX81) + CX82
        MC_THAO11 = Y41 + Y42
        MC_GHAO11 = CX81 + CX82
        MC_PRHM01 = X93
        MC_TRPA01 = X93
        MC_GRMT01 = X931
        MU_CMSC03 = X931
        MC_PLAM02 = X63 + X73 + X83
        MC_TAMT14 = X63
        MC_TAMR04 = X73
        MC_TAMT04 = X83
        MC_GHAO21= DX81 + DX82
        MC_TLPA02 = D.Ceiling((MC_TAMT14 + MC_TAMR04 + MC_TAMT04) / 2.0)
        MU_KLAM03 = MC_TAMT14 + MC_TAMR04 + MC_TAMT04
        MC_GPRD02 = D.Ceiling((CX81 + CX82 + DX81 + DX82 + FX81 + LX81 + MX81+ NX81+ OX81+ PX81+ QX81+ RX81 + RX82+ SX81+ EX83+ FX83+ GX83+ HX83+ IX83+ JX83+ KX83+ LX83+ MX83+ NX83+ OX83+ PX83+ QX83+ SX83)/4.0)
        MU_KDPRYY = MC_GPRD02 * 2
        MU_KGPRXX = (CX81 + CX82 + DX81 + DX82 + FX81 + LX81 + MX81+ NX81+ OX81+ PX81+ QX81+ RX81 + RX82+ SX81+ EX83+ FX83+ GX83+ HX83+ IX83+ JX83+ KX83+ LX83+ MX83+ NX83+ OX83+ PX83+ QX83+ SX83) * 2
        Trace.Write("Y11  "+str(Y11))
        Trace.Write("Y12  "+str(Y12))
        Trace.Write("Y13  "+str(Y13))
        Trace.Write("MC_PSTX03  "+str(MC_PSTX03))
        Trace.Write("MC_PAIH03 "+str(MC_PAIH03))
        Trace.Write("BC_THAI11 "+str(BC_THAI11))
        '''if Length_of_PS_PDP_Cable == "5M" and Length_of_GI_IS_FTA_PDP_Cable == "5M":
            MU_KDPR05= MU_KDPRYY+MU_KGPRXX
            #MU_KDPR051= MU_KGPRXX+MU_KDPRYY
            Trace.Write("MU_KDPR05 "+str(MU_KDPR05))
            #Trace.Write("MU_KDPR051 "+str(MU_KDPR051))
        else:
            if Length_of_PS_PDP_Cable == "5M":
                MU_KDPR05= MU_KDPRYY
                Trace.Write("MU_KDPR05 "+str(MU_KDPR05))
            if Length_of_GI_IS_FTA_PDP_Cable == "5M":
                MU_KDPR05= MU_KGPRXX
                Trace.Write("MU_KDPR051 "+str(MU_KDPR05))
        if Length_of_PS_PDP_Cable == "10M" and Length_of_GI_IS_FTA_PDP_Cable == "10M":
            MU_KDPR10= MU_KDPRYY+MU_KGPRXX
            #MU_KDPR101= MU_KGPRXX+MU_KDPRYY
            Trace.Write("MU_KDPR10 "+str(MU_KDPR10))
            #Trace.Write("MU_KDPR101 "+str(MU_KDPR101))
        else:
            if Length_of_PS_PDP_Cable == "10M":
                MU_KDPR10= MU_KDPRYY
                Trace.Write("MU_KDPR10 "+str(MU_KDPR10))
            if Length_of_GI_IS_FTA_PDP_Cable == "10M":
                MU_KDPR10= MU_KGPRXX
                Trace.Write("MU_KDPR101 "+str(MU_KDPR10))
        if Length_of_PS_PDP_Cable == "InCab" and Length_of_GI_IS_FTA_PDP_Cable == "InCab":
            MU_KDPRInCab= MU_KDPRYY+MU_KGPRXX
            #MU_KDPRInCab1= MU_KGPRXX+MU_KDPRYY
            Trace.Write("MU_KDPRInCab "+str(MU_KDPRInCab))
            #Trace.Write("MU_KDPRInCab1 "+str(MU_KDPRInCab1))
        else:
            if Length_of_PS_PDP_Cable == "InCab":
                MU_KDPRInCab= MU_KDPRYY
                Trace.Write("MU_KDPRInCab "+str(MU_KDPRInCab))
            if Length_of_GI_IS_FTA_PDP_Cable == "InCab":
                MU_KDPRInCab= MU_KGPRXX
                Trace.Write("MU_KDPRInCab1 "+str(MU_KDPRInCab))'''
        if FTA_Connection == "Compression":
            MC_TAOY25= Y51 + Y52
            MC_TAIH22= Y22
            MC_TDOY22 = Z51 + Z52
            MC_TDOY23 = (Z91 + Z92) * 2
            MC_TAIH12 = X11 + X12 + X41 + X42 + Y11 + Y12
            MC_TAIH02 = X13 + Y13
            MC_TDIY22= Y71 + Y72
            MC_TAIH14 = X31 + X32
            MC_TAOY22 =Y31 + Y32
        elif FTA_Connection == "Screw":
            MC_TAOY55= Y51 + Y52
            MC_TDOY62= Z51 + Z52
            MC_TDOY63= (Z91 + Z92) * 2
            MC_TAIH52= X11 + X12 + X13 + Y11 + Y12 + Y13
            MC_TAIH62= X41 + X42 + Y22
            MC_TDIY62= Y71 + Y72
            MC_TAIH54= X31 + X32
            MC_TAOY52= Y31 + Y32
        Trace.Write("MC_TAOY25 "+str(MC_TAOY25))
        Trace.Write("MC_GHAO21 "+str(MC_GHAO21))
        Trace.Write("MC_TAOY55 "+str(MC_TAOY55))
    return int(MC_PHAO01),int(MC_PAIH03),int(BC_THAI11),int(MC_PSTX03),int(MC_PDOY22),int(BU_TDOC02),int(MC_PDIY22),int(MC_TAOY25),int(MC_GHAO21),int(MC_TAIH22),int(MC_TDOY22),int(MC_TDOY23),int(MC_TAIH12),int(MC_TAIH02),int(MC_TDIY22),int(MC_TAOY55),int(MC_TDOY62),int(MC_TDOY63),int(MC_TAIH52),int(MC_TAIH62),int(MC_TDIY62),int(BC_GHAI11),int(MC_GAIH13),int(MC_GAIH14),int(MC_PAIH01),int(MC_TAIH04),int(MC_TAIH14),int(MC_TAIH54),int(MC_PAIL02),int(MC_TAIL02),int(MC_PAOY22),int(MC_THAO11),int(MC_GHAO11),int(MC_TAOY22),int(MC_TAOY52),int(MC_PRHM01),int(MC_TRPA01),int(MC_GRMT01),int(MU_CMSC03),int(MC_PLAM02),int(MC_TAMT14),int(MC_TAMR04),int(MC_TAMT04),int(MC_TLPA02),int(MU_KLAM03),int(MC_GPRD02),int(MU_KDPRYY),int(MU_KGPRXX)
#val = PMIO_Parts(Product)
#Trace.Write(val)