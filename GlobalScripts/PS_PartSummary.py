import System.Decimal as d
import GS_PS_Exp_Ent_BOM
import GS_Exp_Ent_Grp_BomCal
import GS_Part_Exp_Ent_Grp_UOC_Calc as UOC_Parts

def Roundup(n):
    Trace.Write(n)
    res= int(n)
    return res if res == n else res+1

def partsummary(Product):
    Product.ExecuteRulesOnce = True
    
    #44029
    CMS=Product.Attr("CMS Cabinet Station Mounting Type").GetValue()
    #Trace.Write("CMS:"+str(CMS))
    C_S_V=Product.Attr("CE_Site_Voltage").GetValue()
    #Trace.Write("C_S_V:"+str(C_S_V)
    Add_Scenario1=int((Product.Attr("Add_Scenario1").GetValue())) if Product.Attr("Add_Scenario1").GetValue()!='' else 0
    #Trace.Write("Add_Scenario1:"+str(Add_Scenario1))
    Add_Scenario2=int((Product.Attr("Add_Scenario2").GetValue())) if Product.Attr("Add_Scenario2").GetValue()!='' else 0
    #Trace.Write("Add_Scenario2:"+str(Add_Scenario2))
    Additional_Station_Cabinet_Mounting_Type=Product.Attr("Additional_Station_Cabinet_Mounting_Type").GetValue()
    #Trace.Write("Additional_Station_Cabinet_Mounting_Type:"+str(Additional_Station_Cabinet_Mounting_Type))
    TS=int((Product.Attr("TotalSum").GetValue()))
    #for TP-WPCMS1-101 part
    if CMS == "Slide Mount" and Additional_Station_Cabinet_Mounting_Type=="Slide Mount" and C_S_V== "120V" :
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMS1-101",TS)
    elif CMS == "Slide Mount" and Additional_Station_Cabinet_Mounting_Type !="Slide Mount" and C_S_V== "120V" :
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMS1-101",Add_Scenario1)
    elif Additional_Station_Cabinet_Mounting_Type=="Slide Mount" and CMS != "Slide Mount" and C_S_V== "120V" :
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMS1-101",Add_Scenario2)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMS1-101",0)
    # for TP-WPCMS1-301 part
    if CMS == "Slide Mount" and Additional_Station_Cabinet_Mounting_Type=="Slide Mount" and C_S_V== "240V" :
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMS1-301",TS)
    elif CMS != "Slide Mount" and Additional_Station_Cabinet_Mounting_Type =="Slide Mount" and C_S_V== "240V" :
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMS1-301",Add_Scenario2)
    elif CMS == "Slide Mount"and Additional_Station_Cabinet_Mounting_Type !="Slide Mount" and C_S_V== "240V" :
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMS1-301",Add_Scenario1)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMS1-301",0)
    #for TP-WPCMF1-301 part
    if CMS == "Fixed Mount" and Additional_Station_Cabinet_Mounting_Type=="Fixed Mount" and C_S_V== "240V" :
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMF1-301",TS)
    elif Additional_Station_Cabinet_Mounting_Type=="Fixed Mount" and CMS != "Fixed Mount" and C_S_V== "240V" :
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMF1-301",Add_Scenario2)
    elif CMS == "Fixed Mount" and Additional_Station_Cabinet_Mounting_Type !="Fixed Mount" and C_S_V== "240V" :
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMF1-301",Add_Scenario1)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMF1-301",0)
    # TP-WPCMF1-101 part
    if CMS == "Fixed Mount" and Additional_Station_Cabinet_Mounting_Type=="Fixed Mount" and C_S_V== "120V" :
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMF1-101",TS)
    elif CMS == "Fixed Mount" and Additional_Station_Cabinet_Mounting_Type !="Fixed Mount" and C_S_V== "120V" :
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMF1-101",Add_Scenario1)
    elif Additional_Station_Cabinet_Mounting_Type=="Fixed Mount" and CMS != "Fixed Mount" and C_S_V== "120V" :
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMF1-101",Add_Scenario2)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-WPCMF1-101",0)
    #44032
    TPSPCMF1,TPSPCMS1=GS_Exp_Ent_Grp_BomCal.MountingType(Product)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-SPCMF1-101",TPSPCMF1)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-SPCMS1-101",TPSPCMS1)
    #CXCPQ-45547
    New_Expansion=Product.Attr('New_Expansion').GetValue()
    TPS_Required =Product.Attr('Interface with TPS Required?').GetValue()
    Experion_server =Product.Attr('Experion Server Type').GetValue()
    ELCN= Product.Attr('ELCN Solution Required').GetValue()
    MIB=Product.Attr('MIB Configuration Required?').GetValue()
    Desk=Product.Attr('DMS Desk Mounting Stations required').GetValue()
    Cabinet=Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
    DMS_TPS_Station=Product.Attr('DMS TPS Station Qty 0_20').GetValue()
    CMS_TPS_Station=Product.Attr('CMS TPS Station Qty 0_20').GetValue()
    Server_redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
    app_node_tower=Product.Attr('Experion APP Node - Tower Mount').GetValue()
    app_node_rack=Product.Attr('Experion APP Node - Rack Mount').GetValue()
    server_mounting=Product.Attr('Server Mounting').GetValue()
    Total=Total1=count_desk1=Count_cab1=Tot=Tot1=count_desk2=Count_cab2=Count_desk=Count_cab=0
    if New_Expansion=='Expansion' and TPS_Required == 'Yes':
        if Experion_server =='Server TPS' and ELCN =='No':
            if Server_redundancy=='Redundant':
                if server_mounting=='Desk':
                    count_desk1 =2
                if server_mounting=='Cabinet':
                    Count_cab1 =2
                if Desk =='Yes' and DMS_TPS_Station>0:
                    count_desk2  =int(DMS_TPS_Station)
                if Cabinet =='Yes' and CMS_TPS_Station>0:
                    Count_cab2 =int(CMS_TPS_Station)
                Count_desk=count_desk1+count_desk2
                Count_cab=Count_cab1+Count_cab2
                Trace.Write('Count_desk'+str(Count_desk))
            if Server_redundancy =='Non Redundant':
                if server_mounting=='Desk':
                    count_desk1 =1
                if server_mounting=='Cabinet':
                    Count_cab1 =1
                if Desk=='Yes' and DMS_TPS_Station>0:
                    count_desk2 =int(DMS_TPS_Station)
                if Cabinet =='Yes' and CMS_TPS_Station>0:
                    Count_cab2=int(CMS_TPS_Station)
                Count_desk=count_desk1+count_desk2
                Count_cab=Count_cab1+Count_cab2
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-LCNP05-100",int(Count_desk))
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-LCNP05-101",int(Count_cab))

    if New_Expansion=='Expansion' and TPS_Required== 'Yes':
        if Desk == 'Yes' and DMS_TPS_Station>0:
            Tot+=int(DMS_TPS_Station)
        if Cabinet == 'Yes' and CMS_TPS_Station>0:
            Tot1+= int(CMS_TPS_Station)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-CONTPS",int(Tot)+int(Tot1))
    if New_Expansion== 'Expansion' and TPS_Required== 'Yes':
        if app_node_tower>0:
            Total+= int(app_node_tower)
        if app_node_rack>0:
            Total1 += int(app_node_rack)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-ABV000",int(Total)+int(Total1))
    #CXCPQ-45606
    DMS_Flex_Station = int((Product.Attr("DMS Flex Station Qty 0_60").GetValue())) if Product.Attr("DMS Flex Station Qty 0_60").GetValue()!='' else 0
    #DMS_Flex_Station=Product.Attr('DMS Flex Station Qty 0_60').GetValue()
    CMS_Flex_Station = int((Product.Attr("CMS Flex Station Qty 0_60").GetValue())) if Product.Attr("CMS Flex Station Qty 0_60").GetValue()!='' else 0
    #CMS_Flex_Station=Product.Attr('CMS Flex Station Qty 0_60').GetValue()
    CMS_Console = int((Product.Attr("CMS Console Station Qty 0_20").GetValue())) if Product.Attr("CMS Console Station Qty 0_20").GetValue()!='' else 0
    #CMS_Console=Product.Attr('CMS Console Station Qty 0_20').GetValue()
    DMS_Console = int((Product.Attr("DMS Console Station Qty 0_20").GetValue())) if Product.Attr("DMS Console Station Qty 0_20").GetValue()!='' else 0
    #DMS_Console=Product.Attr('DMS Console Station Qty 0_20').GetValue()
    Mobile_Server_Node = int((Product.Attr("Mobile Server Nodes").GetValue())) if Product.Attr("Mobile Server Nodes").GetValue()!='' else 0
    #Mobile_Server_Node=Product.Attr('Mobile Server Nodes').GetValue()
    CMS_Console_Extension = int((Product.Attr("CMS Console Station Extension Qty 0_15").GetValue())) if Product.Attr("CMS Console Station Extension Qty 0_15").GetValue()!='' else 0
    #CMS_Console_Extension=Product.Attr('CMS Console Station Extension Qty 0_15').GetValue()
    DMS_Console_Extension = int((Product.Attr("DMS Console Station Extension Qty 0_15").GetValue())) if Product.Attr("DMS Console Station Extension Qty 0_15").GetValue()!='' else 0
    #DMS_Console_Extension=Product.Attr('DMS Console Station Extension Qty 0_15').GetValue()
    Q1=Q2=Q3=Q4=Q5=Q6=Q7=Q8=Q9=0
    if Desk=='Yes':
        if DMS_Flex_Station>0:
            Q1 =int(DMS_Flex_Station)
        if TPS_Required!= 'Yes':
            if DMS_Console>0:
                Q2 =int(DMS_Console)
        if DMS_Console_Extension>0:
            Q4 =int(DMS_Console_Extension)
    if New_Expansion=='Expansion' and TPS_Required=='Yes' and Desk=='Yes':
        if DMS_TPS_Station>0:
            Q3 =int(DMS_TPS_Station)
    if Cabinet =='Yes':
        if  MIB=='No':
            if CMS_Console_Extension>0:
                Q5 =int(CMS_Console_Extension)
        if CMS_Flex_Station>0:
            Q6 =int(CMS_Flex_Station)
        if TPS_Required!= 'Yes' and MIB=='No':
            if CMS_Console>0:
                Q7 =int(CMS_Console)
    if New_Expansion=='Expansion' and TPS_Required=='Yes'and Cabinet =='Yes':
        if CMS_TPS_Station>0:
            Q8 =int(CMS_TPS_Station)
    if Mobile_Server_Node>0:
        Q9 =int(Mobile_Server_Node)
    Sum1=Q1+Q2+Q3+Q6+Q7+Q8+Q9
    Sum2=Q1+Q2+Q3+Q4+Q5+Q6+Q7+Q8+Q9
    Qnt=Roundup((Sum2-5)/5.0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-EPKY01",int(Sum1))
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-S04CAL",int(Qnt))

    #CXCPQ-45551
    Qty_of_100 = Qty_of_50 = 0
    Is_TPS = Product.Attr('Interface with TPS Required?').GetValue() if Product.Attr('Interface with TPS Required?').GetValue() !='' else 'No'
    Exp_UOC_AP = int((Product.Attr("Experion UOC Analog Points (0-61440)").GetValue())) if Product.Attr("Experion UOC Analog Points (0-61440)").GetValue()!='' else 0
    if Exp_UOC_AP > 200:
        Qty_of_100, Qty_of_50 = UOC_Parts.part_qty_100_50(Exp_UOC_AP - 200)
        if Is_TPS == 'No':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-AIO100",int(Qty_of_100))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-ANLG50",int(Qty_of_50))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","ES-ANLG50",0)
        elif Is_TPS == 'Yes':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-AIO100",int(Qty_of_100))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","ES-ANLG50",int(Qty_of_50))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-ANLG50",0)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-AIO100",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-ANLG50",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","ES-ANLG50",0)

    Qty_of_100 = Qty_of_50 = 0
    Exp_UOC_DP = int((Product.Attr("Experion UOC Digital Points (0-61440)").GetValue())) if Product.Attr("Experion UOC Digital Points (0-61440)").GetValue()!='' else 0
    if Exp_UOC_DP > 600:
        Qty_of_100, Qty_of_50 = UOC_Parts.part_qty_100_50(Exp_UOC_DP - 600)
        if Is_TPS == 'No':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-DIO100",int(Qty_of_100))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-DISC50",int(Qty_of_50))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","ES-DISC50",0)
        elif Is_TPS == 'Yes':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-DIO100",int(Qty_of_100))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","ES-DISC50",int(Qty_of_50))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-DISC50",0)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-DIO100",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-DISC50",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","ES-DISC50",0)

    Qty_of_100 = Qty_of_50 = 0
    Exp_UOC_RCP = int((Product.Attr("Experion UOC Regulatory Compliance Points (0-61440)").GetValue())) if Product.Attr("Experion UOC Regulatory Compliance Points (0-61440)").GetValue()!='' else 0
    if Exp_UOC_RCP > 0:
        Qty_of_100, Qty_of_50 = UOC_Parts.part_qty_100_50(Exp_UOC_RCP)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-REG100",int(Qty_of_100))
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-RCMP01",int(Qty_of_50))
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-REG100",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-RCMP01",0)

    Qty_of_100 = Qty_of_50 = 0
    Exp_UOC_BP = int((Product.Attr("Experion UOC Batch Points (0-61440)").GetValue())) if Product.Attr("Experion UOC Batch Points (0-61440)").GetValue()!='' else 0
    if Exp_UOC_BP > 0:
        Qty_of_100, Qty_of_50 = UOC_Parts.part_qty_100_50(Exp_UOC_BP)
        if Is_TPS == 'No':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-1BP100",int(Qty_of_100))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-1UOS50",int(Qty_of_50))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","ES-1UOS50",0)
        elif Is_TPS == 'Yes':
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-1BP100",int(Qty_of_100))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","ES-1UOS50",int(Qty_of_50))
            GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-1UOS50",0)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-1BP100",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-1UOS50",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","ES-1UOS50",0)

    Qty_of_100 = 0
    Exp_UOC_ABP = int((Product.Attr("Experion UOC Advanced Batch Points (0-61440)").GetValue())) if Product.Attr("Experion UOC Advanced Batch Points (0-61440)").GetValue()!='' else 0
    if Exp_UOC_ABP > 0:
        Qty_of_100 = UOC_Parts.part_qty_100(Exp_UOC_ABP)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-2BP100",int(Qty_of_100))
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-2BP100",0)

    Qty_of_100 = Qty_of_10 = 0
    Exp_UOC_CDL = int((Product.Attr("Experion UOC Composite Device License (0-61440)").GetValue())) if Product.Attr("Experion UOC Composite Device License (0-61440)").GetValue()!='' else 0
    if Exp_UOC_CDL > 0:
        Qty_of_100, Qty_of_10 = UOC_Parts.part_qty_100_10(Exp_UOC_CDL)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-DEV100",int(Qty_of_100))
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-DEV010",int(Qty_of_10))
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-DEV100",0)
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-DEV010",0)

    Exp_UOC_PUL = int((Product.Attr("Experion UOC PROFINET Usage License (0-30)").GetValue())) if Product.Attr("Experion UOC PROFINET Usage License (0-30)").GetValue()!='' else 0
    if Exp_UOC_PUL > 0:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-PROF01",int(Exp_UOC_PUL))
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-PROF01",0)

    Product.ApplyRules()
    Product.ExecuteRulesOnce = False