import math as m
import GS_Get_Set_AtvQty
def getFloat(x):
    if x:
        return float(x)
    return 0
#53160
def partCalc(product):
    #Trace.Write(product.Name)
    result = {}
    if product.Name == "Series-C Control Group":
        percent = 1.00 + getFloat(product.Attr('SerC_CG_Percent_Installed_Spare').GetValue())/100
        pmioCont1 = product.GetContainerByName("C300_SerC_PointCount_PMIO_CG_RlyCont")
        pmioCont2 = product.GetContainerByName("C300_SerC_GIIS_PMIO_CG_Cont")
        FTA = product.Attr('FTA_Connection_Type').GetValue()
        Trace.Write(FTA)

    if product.Name == "Series-C Remote Group":
        percent = 1.00 + getFloat(product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue())/100
        pmioCont1 = product.GetContainerByName("C300_SerC_PointCount_PMIO_RG_RlyCont")
        pmioCont2 = product.GetContainerByName("SerC_PMIO_CG_Group")
        FTA = product.Attr('FTA_Connection_Type').GetValue()

    Y81 = 0
    Y83 = 0
    Z11 = 0
    Z13 = 0
    Z31 = 0
    Z33 = 0
    Z43 = 0
    Z63 = 0
    Z73 = 0
    Z83 = 0
    Y63 = 0
    Y93 = 0
    Z23 = 0
    EX83 = 0
    HX83 = 0
    FX81 = 0
    FX83 = 0
    GX81 = 0
    GX83 = 0
    AX83 = 0
    BX83 = 0
    IX83 = 0
    JX83 = 0
    KX82 = 0
    TDON12=0
    TDOD13=0
    TDOD23 =0
    TDOA13 = 0
    TDOR12 = 0
    TDOR22 = 0
    TDON52=0
    TDOD53=0
    TDOD63 = 0
    TDOA53 = 0
    TDOR52 = 0
    TDOR62 = 0
    MCTDID12 = 0
    MCTDIA12= 0
    MCTDIA22= 0
    MCTDID52 = 0
    MCTDIA52= 0
    MCTDIA62= 0
    

    if pmioCont1:
        for row in pmioCont1.Rows:
            if row["IO_Type"] == "PMIO DI SOE 24 VDC (32) (0-5000)":
                Y81 = m.ceil((getFloat(row["Red_IS"])*percent)/32) + m.ceil((getFloat(row["Red_NIS"])*percent)/32)
                Y83 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/32) + m.ceil((getFloat(row["Non_Red_NIS"])*percent)/32)
            if row["IO_Type"] == "PMIO DI SOE 120 VAC (32) (0-5000)":
                Z11 = m.ceil((getFloat(row["Red_IS"])*percent)/32) + m.ceil((getFloat(row["Red_NIS"])*percent)/32)
                Z13 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/32) + m.ceil((getFloat(row["Non_Red_NIS"])*percent)/32)
            if row["IO_Type"] == "PMIO DI SOE 240 VAC (32) (0-5000)":
                Z31 = m.ceil((getFloat(row["Red_IS"])*percent)/32) + m.ceil((getFloat(row["Red_NIS"])*percent)/32)
                Z33 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/32) + m.ceil((getFloat(row["Non_Red_NIS"])*percent)/32)
            if row["IO_Type"] == "PMIO DO 24 VDC (16) (0-5000)":
                Z43 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/16) + m.ceil((getFloat(row["Non_Red_NIS"])*percent)/16)
            if row["IO_Type"] == "PMIO DO 3 to 30 VDC (16) (0-5000)":
                Z63 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/16) + m.ceil((getFloat(row["Non_Red_NIS"])*percent)/16)
            if row["IO_Type"] == "PMIO DO 31 to 200 VDC (16) (0-5000)":
                Z73 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/16) + m.ceil((getFloat(row["Non_Red_NIS"])*percent)/16)
            if row["IO_Type"] == "PMIO DO 120/240 VAC SS (16) (0-5000)":
                Z83 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/16) + m.ceil((getFloat(row["Non_Red_NIS"])*percent)/16)
            if row["IO_Type"] == "PMIO DO 120 VAC Relay (16) (0-5000)":
                AX83 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/16) + m.ceil((getFloat(row["Non_Red_NIS"])*percent)/16)
            if row["IO_Type"] == "PMIO DO 240 VAC Relay (16) (0-5000)":
                BX83 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/16) + m.ceil((getFloat(row["Non_Red_NIS"])*percent)/16)
            if row["IO_Type"] == "PMIO DI 24 VDC (32) (0-5000)":
                Y63 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/32) + m.ceil((getFloat(row["Non_Red_NIS"])*percent)/32)
            if row["IO_Type"] == "PMIO DI 120 VAC (32) (0-5000)":
                Y93 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/32) + m.ceil((getFloat(row["Non_Red_NIS"])*percent)/32)
            if row["IO_Type"] == "PMIO DI 240 VAC (32) (0-5000)":
                Z23 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/32) + m.ceil((getFloat(row["Non_Red_NIS"])*percent)/32)
                

    if pmioCont2:
        for row in pmioCont2.Rows:
            if row["IO_Type"] == "PMIO GI/IS DI SOE (32)  (0-5000)":
                FX81 = m.ceil((getFloat(row["Red_IS"])*percent)/32)
                FX83 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/32)
            if row["IO_Type"] == "PMIO GI/IS DI Solid State SOE (32)  (0-5000)":
                GX81 = m.ceil((getFloat(row["Red_IS"])*percent)/32)
                GX83 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/32)
            if row["IO_Type"] == "PMIO GI/IS DO LFD (16)  (0-5000)":
                IX83 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/16)
            if row["IO_Type"] == "PMIO GI/IS DO (16)  (0-5000)":
                JX83 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/16)
            if row["IO_Type"] == "PMIO GI/IS DI (32)  (0-5000)":
                EX83 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/32)
            if row["IO_Type"] == "PMIO GI/IS DI Solid State (32)  (0-5000)":
                HX83 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/32)
            if row["IO_Type"] == "PMIO GI/IS DO (32) Via non red combine panel  (0-5000)":
                KX82 = m.ceil((getFloat(row["Non_Red_IS"])*percent)/16)
                
                
    Trace.Write(str(Y81)+" "+str(Y83)+" "+str(Z11)+" "+str(Z13)+" "+str(Z31)+" "+str(Z33)+" "+str(FX81)+" "+str(FX83)+" "+str(GX81)+" "+str(GX83)+" "+str(Z43)+" "+str(Z63)+" "+str(Z73)+" "+str(Z83)+" "+str(AX83)+" "+str(BX83)+" "+str(IX83)+" "+str(JX83)+" ")

    qtyMCPDIS12 = 2*(Y81) + Y83+2*(Z11) + Z13+2*(Z31) + Z33+ 2*(FX81) + FX83+ 2*(GX81) + GX83
    qtyMCPDOX02 = Z43+ Z63+ Z73+ Z83+ AX83+ BX83+IX83 + JX83
    qtyMCGDOL12 = IX83
    qtyMCGLFD02 = m.ceil(IX83/2)
    qtyMCGDID12= FX81 + EX83 + FX83
    qtyMCGDID13= GX81 + GX83 + HX83
    qtyMCGDOD13 = JX83 + KX82
    qtyMCPDIX02 = Y63+ Y93+ Z23 + EX83 + HX83 + qtyMCGLFD02
    
    if FTA=="Compression":
        TDON12=Z43
        TDOD13=Z63
        TDOD23 = Z73
        TDOA13 = Z83
        TDOR12 = AX83
        TDOR22 = BX83
        MCTDID12 = Y81 + Y63 + Y83
        MCTDIA12= Z11 + Y93 + Z13
        MCTDIA22= Z31 + Z23 + Z33
    if FTA=="Screw":
        TDON52=Z43
        TDOD53=Z63
        TDOD63 = Z73
        TDOA53 = Z83
        TDOR52 = AX83
        TDOR62 = BX83
        MCTDID52 = Y81 + Y63 + Y83
        MCTDIA52= Z11 + Y93 + Z13
        MCTDIA62= Z31 + Z23 + Z33
    
    result["MC-PDIS12"] = qtyMCPDIS12
    result["MC-PDOX02"] = qtyMCPDOX02
    result["MC-GDOL12"] = qtyMCGDOL12
    result["MC-GLFD02"] = qtyMCGLFD02
    
    result["MC-TDON12"] = TDON12
    result["MC-TDOD13"] = TDOD13
    result["MC-TDOD23"] = TDOD23
    result["MC-TDOA13"] = TDOA13
    result["MC-TDOR12"] = TDOR12
    result["MC-TDOR22"] = TDOR22
    
    result["MC-TDON52"] = TDON52
    result["MC-TDOD53"] = TDOD53
    result["MC-TDOD63"] = TDOD63
    result["MC-TDOA53"] = TDOA53
    result["MC-TDOR52"] = TDOR52
    result["MC-TDOR62"] = TDOR62
    
    result["MC-TDID12"] = MCTDID12
    result["MC-TDIA12"] = MCTDIA12
    result["MC-TDIA22"] = MCTDIA22
    result["MC-TDID52"] = MCTDID52
    result["MC-TDIA52"] = MCTDIA52
    result["MC-TDIA62"] = MCTDIA62
    
    result["MC-GDID12"] = qtyMCGDID12
    result["MC-GDID13"] = qtyMCGDID13
    result["MC-GDOD13"] = qtyMCGDOD13
    
    result["MC-PDIX02"] = qtyMCPDIX02
    return result
#K=partCalc(Product)
#Trace.Write(str(K))