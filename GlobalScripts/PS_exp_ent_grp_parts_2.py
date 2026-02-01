import GS_BOM_exp_ent_grp, GS_BOM_exp_ent_grp_2, GS_Exp_grp_parts, GS_Exp_grp_parts2
import GS_PS_Exp_Ent_BOM
import GS_BOM_Multi_Window_Sup
import GS_Exp_ENT_BOM_Calcs
import Gs_EXpEnt_Grp_BOM_calcs
import GS_EXP_NetworkStorage

def PartsummanryEntGrp2(Product,Quote):
    Product.Attr('qty_405').AssignValue('0')
    Product.Attr('qty_407').AssignValue('0')
    Product.Attr('qty_579').AssignValue('0')
    Product.Attr('qty_581').AssignValue('0')

    ESR = Product.Attr('Experion Software Release').GetValue()
    DMSR = Product.Attr('DMS Desk Mounting Stations required').GetValue()
    OSR = Product.Attr('Orion Stations required').GetValue()
    CMSR = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
    EST = Product.Attr('Experion Server Type').GetValue()
    LOB = Quote.GetCustomField('Booking Lob').Content
    TPS_required=Product.Attr("Interface with TPS Required?").GetValue()
    SM  = Product.Attr('Server Mounting').GetValue()
    FSNT = Product.Attr("Flex Server Node Type").GetValue()
    servers=["SVR_PER_HP_Rack_RAID5", "SVR_PER_DELL_Rack_RAID1_RUG", "SVR_PER_DELL_Tower_RAID1", "SVR_PER_DELL_Rack_RAID1", "SVR_STD_DELL_Tower_RAID1", "SVR_STD_DELL_Rack_RAID1", "SVR_PER_DELL_Rack_RAID5", "SVR_PER_DELL_Rack_RAID1_XE"]
    additional_stations_R530 = ["STN_PER_DELL_Tower_RAID1","STN_PER_DELL_Rack_RAID1", "STN_PER_HP_Tower_RAID1"]
    #Ravika-->CCEECOMMBR-7729
    try:
        SNTD= Product.Attr("Server Node Type_desk").GetValue()
    except:
        SNTD = ""
    try:
        SNTC= Product.Attr("Server_NodeType").GetValue()
    except:
        SNTC = ""
    Tower_station_qty=GS_BOM_exp_ent_grp.station_qnt1(Product,'SVR_F_PER_DELL_Tower_RAID1','STN_PER_DELL_Tower_RAID1')
    Rack_station_qty =GS_BOM_exp_ent_grp.station_qnt1(Product,'SVR_F_PER_DELL_Rack_RAID1','STN_PER_DELL_Rack_RAID1')
    HP_Tower_station_qty=GS_BOM_exp_ent_grp.station_qnt1(Product,'SVR_F_PER_HP_Tower_RAID1','STN_PER_HP_Tower_RAID1')
    CMS_DMS_Rack_station_qty=GS_BOM_exp_ent_grp.station_qnt3(Product,'SVR_F_PER_DELL_Rack_RAID1','STN_PER_DELL_Rack_RAID1')

    serever_qnt_T,serever_qntnode_T,station_37200=GS_Exp_ENT_BOM_Calcs.server_qnt1(Product)

    #CXCPQ-44532
    qt10k,qt5k,qt2k,qt1k,qt100 = GS_Exp_grp_parts.get_QVCS(Product)
    if qt10k > 0:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC10K",qt10k)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC10K",0)
    if qt5k > 0:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC05K",qt5k)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC05K",0)
    if qt2k > 0:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC02K",qt2k)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC02K",0)
    if qt1k > 0:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC01K",qt1k)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC01K",0)
    if qt100 > 0:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC100",qt100)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC100",0)

    #CXCPQ-43659
    try:
        SNT=Product.Attributes.GetByName("Server Node Type EBR").GetValue()
        TPM=Product.Attributes.GetByName("Trusted Platform Module TPM EBR").GetValue()
        NS=Product.Attributes.GetByName("Node Supplier Server EBR").GetValue()
        DSS=Product.Attributes.GetByName("Display Size server EBR").GetValue()
        #CXDEV-7720--RP
        Node_Sup_Desk=Product.Attributes.GetByName("Node Supplier_server").GetValue()
        Node_Sup_Cab=Product.Attributes.GetByName("Node_Supplier_Server").GetValue()
        DSP=Product.Attributes.GetByName("Display Supplier EBR").GetValue()
    except:
        SNT=""
        TPM=""
        NS=""
        DSS=""
        DSP=""

    SRR=Product.Attributes.GetByName("Server Redundancy Requirement?").GetValue()
    BackRelease=Product.Attr('Experion Backup Restore Software Release').GetValue()

    MZ_PCSR03SR=0
    EP_COAS22SR=0
    MZ_PCSV84SR=0
    MZ_PCSR01SR=0
    MZ_PCSR02SR=0
    MZ_PCSR82SR=0
    MZ_PCSV65SR=0
    MZ_PCIS02SR=0
    MZ_PCST01SR=0
    MZ_PCST02SR=0
    MZ_PCST82SR=0

    TP_FPD211_100SR=0
    TP_FPD211_200SR=0
    TP_FPW271SR=0
    TP_FPW241SR=0
    TP_FPW242SR=0
    TP_FPW272SR=0

    EP_COAS16SR=0
    MZ_SQLCL4SR=0
    EP_COAS19SR=0

    serever_qntnode_Final=0
    serever_qntnode_FinalR520=0

    SR16=1
    SR19=1
    #CXCPQ-45056
    SR=1
    #CXCPQ-45056
    if Product.Attributes.GetByName("EBR_Server_Check").GetValue()=="No":
        SR=0

    if DSS=="21.33 inch NTS" and DSP=="Honeywell":
        TP_FPD211_100SR=SR
        TP_FPD211_200SR=SR
    if DSS=="27 inch NTS NEC" and DSP=="Honeywell":
        TP_FPW271SR=SR
    if DSS=="24 inch NTS NEC" and DSP=="Honeywell":
        TP_FPW241SR=SR
    if DSS=="24 inch NTS DELL" and DSP=="Honeywell":
        TP_FPW242SR=SR
    if DSS=="27 inch NTS DELL" and DSP=="Honeywell":
        TP_FPW272SR=SR

    if SNT=="SVR_PER_DELL_Rack_RAID1_XE" and TPM=="Yes" and NS=="Honeywell":
        MZ_PCSR03SR=SR

    if SNT=="SVR_PER_HP_Rack_RAID5" and TPM=="Yes" and NS=="Honeywell":
        MZ_PCSV84SR=SR

    if SNT=="SVR_STD_DELL_Rack_RAID1" and TPM=="Yes" and NS=="Honeywell":
        MZ_PCSR01SR=SR

    if SNT=="SVR_PER_DELL_Rack_RAID1" and TPM=="Yes" and NS=="Honeywell":
        MZ_PCSR02SR=SR

    if SNT=="SVR_PER_DELL_Rack_RAID1" and TPM=="No" and NS=="Honeywell":
        MZ_PCSR82SR=SR

    if SNT=="SVR_PER_DELL_Rack_RAID5" and TPM=="Yes" and NS=="Honeywell":
        MZ_PCSV65SR=SR

    if SNT=="SVR_PER_DELL_Rack_RAID1_RUG" and TPM=="Yes" and NS=="Honeywell":
        MZ_PCIS02SR=SR

    if SNT=="SVR_STD_DELL_Tower_RAID1" and TPM=="Yes" and NS=="Honeywell":
        MZ_PCST01SR=SR

    if SNT=="SVR_PER_DELL_Tower_RAID1" and TPM=="Yes" and NS=="Honeywell":
        MZ_PCST02SR=SR
    if SNT=="SVR_PER_DELL_Tower_RAID1" and TPM=="No" and NS=="Honeywell":
        MZ_PCST82SR=SR

    if NS=="Honeywell" and BackRelease=="R501":
        EP_COAS16SR=SR16
    if NS=="Honeywell" and BackRelease=="R520":
        EP_COAS19SR=SR19

    if SNT!="" and TPM=="Yes" and NS=="Honeywell":
        MZ_SQLCL4SR=SR
        EP_COAS22SR=SR

    if ESR == 'R530':
        MZ_PCWS15_qty = GS_BOM_exp_ent_grp.station_qnt1(Product,'','STN_STD_DELL_Tower_NonRAID')
        if MZ_PCWS15_qty > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS15",MZ_PCWS15_qty)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS15",0)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS15",0)

    if ESR == 'R530':
        MZ_PCWR01_qty = GS_BOM_exp_ent_grp.station_qnt1(Product,'','STN_PER_DELL_Rack_RAID1')
        if MZ_PCWR01_qty > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWR01",MZ_PCWR01_qty)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWR01",0)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWR01",0)

    if ESR == 'R530':
        MZ_PCWT01_qty = GS_BOM_exp_ent_grp.station_qnt1(Product,'','STN_PER_DELL_Tower_RAID1')
        if MZ_PCWT01_qty > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWT01",MZ_PCWT01_qty)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWT01",0)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWT01",0)

    #CCEECOMMBR-7728--RP and CXDEV-8016--kaousalya Adala
    if (ESR=='R530'or ESR=='R520'): 
        MZ_PCSR03_qty = GS_BOM_exp_ent_grp_2.Node_server(Product,["SVR_PER_DELL_Rack_RAID1_XE"],'Yes')
        if MZ_PCSR03_qty+MZ_PCSR03SR > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCSR03",MZ_PCSR03_qty+MZ_PCSR03SR)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCSR03",0)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCSR03",0)

    if ESR=='R530':
        NE_NICS04_qty1 = GS_BOM_exp_ent_grp_2.Node_server(Product,servers,'No')
        NE_NICS04_qty = GS_BOM_exp_ent_grp.station_qnt1(Product,'','STN_STD_DELL_Tower_NonRAID')
        if NE_NICS04_qty > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","NE-NICS04",NE_NICS04_qty + NE_NICS04_qty1)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","NE-NICS04",0)

    if (ESR == 'R520' or ESR == 'R510' or ESR == 'R511'):
        NE_NICS04_qty = GS_BOM_exp_ent_grp.station_qnt1(Product,'','STN_PER_DELL_Tower_RAID1')
        NE_NICS04_qty1 = GS_BOM_exp_ent_grp_2.Node_server(Product,servers,'No')
        if NE_NICS04_qty > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","NE-NICS04",NE_NICS04_qty + NE_NICS04_qty1)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","NE-NICS04",0)

    #CCEECOMMBR-7729--RP and CXDEV-8017-kaousalya Adala
    if  ESR=='R530':
        serever_qntnode_FinalR530=serever_qntnode_T
        if serever_qntnode_FinalR530+EP_COAS22SR > 0:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAS22",serever_qntnode_FinalR530+EP_COAS22SR)
        else:
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAS22",0)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAS22",0)

    #CXDEV-8352
    qty_TP_FPW242, qty_TP_FPD211_200, qty_TP_FPT211_100 = GS_Exp_grp_parts2.get_parts(Product,"24 inch NTS DELL")
    if qty_TP_FPW242+TP_FPW242SR >0:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPW242",qty_TP_FPW242+TP_FPW242SR)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPW242",0)

    #CXDEV-8354    
    qty_TP_FPW272, qty_TP_FPD211_200, qty_TP_FPT211_100 = GS_Exp_grp_parts2.get_parts(Product,"27 inch NTS DELL")
    if qty_TP_FPW272 +TP_FPW272SR>0:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPW272",qty_TP_FPW272+TP_FPW272SR)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPW272",0)

    #CXDEV-8357   
    qty_TP_FPT242,qty_TP_FPW231 = GS_Exp_grp_parts2.get_23(Product,"24 inch Touch Dell")
    if qty_TP_FPT242>0:
        Trace.Write("38883")
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPT242",qty_TP_FPT242)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPT242",0)

    Product.ApplyRules()