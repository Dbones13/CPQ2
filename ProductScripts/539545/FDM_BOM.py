def setAtvQty(Product,AttrName,sv,qty):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        if av.Display == sv:
            av.IsSelected=False
            av.Quantity = 0
            if qty > 0:
                av.IsSelected=True
                av.Quantity=qty
                Trace.Write('Selected ' + sv + ' in attribute ' + AttrName + ' at Qty ' + str(qty))
                break

def qtyCalc(input):
    x=input+15
    i=0
    result=[]
    while(x>0):
        if(i==1 and x<16 or x<=15):break
        print(findLowerNearest(x))
        lowerNearest=findLowerNearest(x)
        result.append(lowerNearest)
        x=x-lowerNearest
        i=i+1
    return set(result)

def findLowerNearest(input):
    numList=[16,32,64,128,256,512,1024,2048,4096,8192,16000]
    i=0
    while(i<len(numList)):
        if(input>16000):
            return 16000
        if(input<numList[i]):
            if(i==0):
                return 16
            return numList[i-1] if i<=len(numList)-1 else 16000
        i=i+1

#Changes added by RP CXCPQ-107750
qty_HC_HIP000 = 0
qty_HC_HCM540_ESD = 0
qty_HC_HCM540 = 0
qty_HC_ALTMON = 0
qty_HC_OPCUSV = 0
qty_HC_OPCUDA = 0
qty_TP_FPW271 = 0
qty_TP_FPW241 = 0
#qty_MZ_PCWS94 = 0
qty_MZ_PCWS84 = 0
#qty_MZ_PCWS77 = 0
qty_MZ_PCWS14 = 0
qty_MZ_PCIS02 = 0
#qty_MZ_PCST82 = 0
qty_MZ_PCSV84 = 0
qty_MZ_PCSV65 = 0
qty_MZ_PCSR04 = 0
#qty_MZ_PCSR82 = 0
#qty_MZ_PCSR01 = 0
#qty_MZ_PCSR02 = 0
#qty_MZ_PCST02 = 0
#qty_MZ_PCST01 = 0
#qty_EP_COAW10 = 0
#qty_EP_COAW19 = 0
qty_EP_COAS19 = 0
qty_EP_COAS16 = 0
qty_FPD211_200 = 0
qty_FPD211_100 = 0
qty_MZ_PCWS15 = 0
#qty_MZ_PCWS93 = 0
qty_MZ_PCWS86 = 0
qty_MZ_PCWR01 = 0
qty_MZ_PCWT01 = 0
qty_MZ_PCSR03 = 0
qty_EP_COAS22 = 0
qty_EP_COAW21 = 0
qty_MZ_PCSV85 = 0
qty_MZ_SQLCL4 = 0
qty_MZ_PCWS85 = 0
qty_TP_FPW242 = 0
qty_TP_FPW272 = 0
qty_HC_OPCUAC = 0
qty_MZ_PCSR05 = 0
qty_MZ_PCSR06 = 0
qty_MZ_PCST03 = 0
qty_MZ_PCST04 = 0
qty_HC_OPCUHA = 0
qty_HC_FCI000 = 0
qty_HC_ICVR00 = 0
qty_HC_FCFVAL = 0
qty_MZ_PCWT02 = 0

setAtvQty(Product,"FDM_Part_Summary","HC-UA1024",0)
setAtvQty(Product,"FDM_Part_Summary","HC-UA2048",0)
setAtvQty(Product,"FDM_Part_Summary","HC-UA4096",0)
setAtvQty(Product,"FDM_Part_Summary","HC-UA8192",0)
setAtvQty(Product,"FDM_Part_Summary","HC-UA016K",0)
setAtvQty(Product,"FDM_Part_Summary","HC-UA0512",0)
setAtvQty(Product,"FDM_Part_Summary","HC-UA0256",0)
setAtvQty(Product,"FDM_Part_Summary","HC-UA0128",0)
setAtvQty(Product,"FDM_Part_Summary","HC-UA0064",0)
setAtvQty(Product,"FDM_Part_Summary","HC-UA0032",0)
setAtvQty(Product,"FDM_Part_Summary","HC-UA0016",0)
setAtvQty(Product,"FDM_Part_Summary","HC-FC0016",0)
setAtvQty(Product,"FDM_Part_Summary","HC-FC0032",0)
setAtvQty(Product,"FDM_Part_Summary","HC-FC0064",0)
setAtvQty(Product,"FDM_Part_Summary","HC-FC0128",0)
setAtvQty(Product,"FDM_Part_Summary","HC-FC0256",0)
setAtvQty(Product,"FDM_Part_Summary","HC-FC0512",0)
setAtvQty(Product,"FDM_Part_Summary","HC-NDM010",0)
setAtvQty(Product,"FDM_Part_Summary","HC-NDM020",0)
setAtvQty(Product,"FDM_Part_Summary","HC-NDM030",0)
setAtvQty(Product,"FDM_Part_Summary","HC-NDM040",0)
setAtvQty(Product,"FDM_Part_Summary","HC-NDM050",0)
setAtvQty(Product,"FDM_Part_Summary","HC-NDM060",0)
setAtvQty(Product,"FDM_Part_Summary","HC-NDM070",0)
setAtvQty(Product,"FDM_Part_Summary","HC-NDM080",0)
setAtvQty(Product,"FDM_Part_Summary","HC-NDM090",0)
setAtvQty(Product,"FDM_Part_Summary","HC-NDM100",0)


def addUAServerDeviceBlocks(input,map):
    qty=qtyCalc(input)
    for i in qty:
        setAtvQty(Product,"FDM_Part_Summary",map[str(i)],1)


sitevoltage = Product.Attr("CE_Site_Voltage").GetValue()
FDMRelease = Product.Attr("FDM_Release").GetValue()
ExpPKSRelease = Product.Attr('FDM_Experion_PKS_Release').GetValue()

displayquery = SqlHelper.GetList("Select AttributeName,Supplier,Quantity,TPM from FDM_BOM")
server_spec = Product.Attr("FDM_Server_Specification").GetValue()
if displayquery is not None:
    for row in displayquery:
        displaysize = Product.Attr(row.AttributeName).GetValue()
        displaysupplier = Product.Attr(row.Supplier).GetValue()
        quantity = int(Product.Attr(row.Quantity).GetValue()) if Product.Attr(row.Quantity).GetValue()!="" else 0
        tpm_value = Product.Attr(row.TPM).GetValue()

        if displaysupplier == "Honeywell":
            if displaysize == "27 inch NTS NEC":
                qty_TP_FPW271 += quantity
            if displaysize == "24 inch NTS NEC":
                qty_TP_FPW241 += quantity
            if displaysize == "24 inch NTS DELL":
                qty_TP_FPW242 += quantity
            if displaysize == "27 inch NTS DELL":
                qty_TP_FPW272 += quantity
            if displaysize == "21.33 inch NTS" and sitevoltage == "240V":
                qty_FPD211_200 += quantity
            if displaysize == "21.33 inch NTS" and sitevoltage == "120V":
                qty_FPD211_100 += quantity
            if displaysize == "STN_PER_HP_Tower_RAID1":
                qty_MZ_PCWS84 += quantity
            '''if displaysize == "STN_PER_DELL_Rack_RAID1":
                qty_MZ_PCWS77 += quantity'''
            # Commented because CXCPQ-86035 story- Saurabh
            """# for 7987 story 
            if displaysize == "STN_PER_DELL_Tower_RAID1":
                if ExpPKSRelease == "R511":
                    qty_MZ_PCWS93 += quantity"""
                    

            if tpm_value == "Yes":
                if displaysize == "SVR_PER_DELL_Rack_RAID1_RUG":
                    qty_MZ_PCIS02 += quantity
                if displaysize == "SVR_PER_HP_Rack_RAID5":
                    qty_MZ_PCSV84 += quantity
                if displaysize == "SVR_PER_DELL_Rack_RAID5":
                    qty_MZ_PCSR04 += quantity
                '''#if displaysize == "SVR_STD_DELL_Rack_RAID1":
                    #qty_MZ_PCSR01 += quantity
                #if displaysize == "SVR_PER_DELL_Rack_RAID1":
                    #qty_MZ_PCSR02 += quantity
                #if displaysize == "SVR_PER_DELL_Tower_RAID1":
                    #qty_MZ_PCST02 += quantity
                #if displaysize == "SVR_STD_DELL_Tower_RAID1":
                    #qty_MZ_PCST01 += quantity

            if tpm_value == "No":
                if displaysize == "SVR_PER_DELL_Tower_RAID1":
                    qty_MZ_PCST82 += quantity
                if displaysize == "SVR_PER_DELL_Rack_RAID1":
                    qty_MZ_PCSR82 += quantity'''


            """if FDMRelease == "R520":
                if displaysize == "SVR_PER_HP_Rack_RAID5" or displaysize == "SVR_PER_DELL_Rack_RAID1_RUG" or displaysize == "SVR_PER_DELL_Tower_RAID1" or displaysize == "SVR_PER_DELL_Rack_RAID1" or displaysize == "SVR_STD_DELL_Tower_RAID1" or displaysize == "SVR_STD_DELL_Rack_RAID1" or displaysize == "SVR_PER_DELL_Rack_RAID5":
                    qty_EP_COAS19 += quantity"""
                # for 7988 story
            #if ExpPKSRelease != "R520":
                #if displaysize == "STN_STD_DELL_Tower_NonRAID":
                    #qty_MZ_PCWS14 += quantity
                # Commented for 7986 story. 
                #if displaysize == "STN_PER_DELL_Tower_RAID1":
                    #qty_MZ_PCWS94 += quantity
                #if displaysize == "STN_PER_DELL_Tower_RAID1" or displaysize == "STN_PER_DELL_Rack_RAID1" or displaysize == "STN_PER_HP_Tower_RAID1":
                    #qty_EP_COAW19 += quantity

            """if FDMRelease == "R501" or FDMRelease == "R511":
                if displaysize == "SVR_PER_HP_Rack_RAID5" or displaysize == "SVR_PER_DELL_Rack_RAID1_RUG" or displaysize == "SVR_PER_DELL_Tower_RAID1" or displaysize == "SVR_PER_DELL_Rack_RAID1" or displaysize == "SVR_STD_DELL_Tower_RAID1" or displaysize == "SVR_STD_DELL_Rack_RAID1" or displaysize == "SVR_PER_DELL_Rack_RAID5":
                    qty_EP_COAS16 += quantity
                if displaysize == "STN_PER_DELL_Tower_RAID1" or displaysize == "STN_PER_DELL_Rack_RAID1" or displaysize == "STN_PER_HP_Tower_RAID1":
                    qty_EP_COAW10 += quantity"""
            # for 7986 story
            #Commented because CXCPQ-86035 Story- Saurabh
            '''if ExpPKSRelease == "R520":
                if displaysize == "STN_PER_DELL_Tower_RAID1":
                    qty_MZ_PCWS94 += quantity'''
            if ExpPKSRelease in ("R520","R530"):
                # for 7995 story
                if displaysize == "SVR_PER_DELL_Rack_RAID1_XE":
                    qty_MZ_PCSR03 += quantity
            if ExpPKSRelease in ("R520","R530") and tpm_value:
                # for 103993 story
                if displaysize == "SVR_STD_DELL_Rack_RAID1":
                    qty_MZ_PCSR05 += quantity
                elif displaysize == "SVR_PER_DELL_Rack_RAID1":
                    qty_MZ_PCSR06 += quantity
                elif displaysize == "SVR_STD_DELL_Tower_RAID1":
                    qty_MZ_PCST03 += quantity
                elif displaysize == "SVR_PER_DELL_Tower_RAID1":
                    qty_MZ_PCST04 += quantity
            # for 7994 story
            if ExpPKSRelease == "R530":
                if displaysize == "STN_STD_DELL_Tower_NonRAID":
                    qty_MZ_PCWS15 += quantity
                # For 7993 Story
                if displaysize == "STN_PER_HP_Tower_RAID1":
                    qty_MZ_PCWS86 += quantity  
                # for 7992 story
                if displaysize == "STN_PER_DELL_Rack_RAID1":
                    qty_MZ_PCWR01 += quantity
                # for 7991 story
                if displaysize == "STN_PER_DELL_Tower_RAID1":
                    qty_MZ_PCWT01 += quantity 
                # for 7989 story
                if FDMRelease in ('R530','R540'):
                    if displaysize in ('SVR_PER_HP_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_RUG','SVR_PER_DELL_Tower_RAID1','SVR_PER_DELL_Rack_RAID1','SVR_STD_DELL_Tower_RAID1','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_XE'):
                        qty_EP_COAS22 += quantity
                        #Trace.Write('qty_EP_COAS22')
                    # for 7990 story
                    if displaysize in ('STN_PER_DELL_Tower_RAID1','STN_PER_DELL_Rack_RAID1','STN_PER_HP_Tower_RAID1'):
                        qty_EP_COAW21 += quantity
                        #Trace.Write('qty_EP_COAW21')
    #CXDEV-7978-79-82-83
    if server_spec == "Server":
        node_supp = Product.Attr("FDM_Node Supplier (Server)").GetValue()
        node_type = Product.Attr("FDM_Server Node Type").GetValue()
        node_tpm = Product.Attr('FDM_Trusted Platform Module (TPM)').GetValue()
        if node_supp == "Honeywell" and ExpPKSRelease == "R520" :
            qty_EP_COAS19+=1
        if node_supp == "Honeywell" and ExpPKSRelease == "R511":
            qty_EP_COAS16+=1
        if node_supp == "Honeywell" and ExpPKSRelease in ['R520','R530'] and node_type == "SVR_PER_HP_Rack_RAID5" and node_tpm == "Yes":
            qty_MZ_PCSV85 +=1
        qty_MZ_SQLCL4 += 1
    fdm_gateway = Product.Attr("FDM_ FDM_Gateway_required").GetValue()
    if fdm_gateway == "Yes":
        pc_qty = Product.Attr("FDM_FDM_Gateway_PC_Qty(0-6)").GetValue()
        pc_nodeSupp = Product.Attr("FDM_Node_Supplier(Server)").GetValue()
        nodeGtway = Product.Attr("FDM_Server_Node_Type").GetValue()
        tpm_value_GT = Product.Attr('FDM_Trusted_Platform_Module(TPM)').GetValue()
        if pc_qty > 0 and pc_nodeSupp == "Honeywell" and ExpPKSRelease == "R520":
            qty_EP_COAS19 +=int(pc_qty)
        if pc_qty > 0 and pc_nodeSupp == "Honeywell" and ExpPKSRelease == "R511":
            qty_EP_COAS16 += int(pc_qty)
        if pc_qty > 0 and pc_nodeSupp == "Honeywell" and ExpPKSRelease in ['R520','R530'] and nodeGtway == "SVR_PER_HP_Rack_RAID5" and tpm_value_GT == 'Yes':
            qty_MZ_PCSV85 += int(pc_qty)
        if pc_qty > 0:
            qty_MZ_SQLCL4 += int(pc_qty)
    #CXDEV-7980-81-84
    if server_spec == "Workstation":
        nodeSuppStation = Product.Attr("FDM_Node Supplier").GetValue()
        stationNodeType = Product.Attr("FDM_Station Node Type").GetValue()
        #Commented because CXCPQ-86035 Story- Saurabh
        '''if nodeSuppStation == "Honeywell" and ExpPKSRelease == "R520":
            qty_EP_COAW19 +=1
        if nodeSuppStation == "Honeywell" and ExpPKSRelease == "R511":
            qty_EP_COAW10 +=1
        if nodeSuppStation == "Honeywell" and ExpPKSRelease in ['R520','R511'] and stationNodeType == 'STN_PER_DELL_Rack_RAID1':
            qty_MZ_PCWS77 +=1'''
        if nodeSuppStation == "Honeywell" and ExpPKSRelease == "R520"and stationNodeType == 'STN_PER_HP_Tower_RAID1':
            qty_MZ_PCWS85+=1
        qty_MZ_SQLCL4 += 1
    FDMCS = Product.Attr("FDM Client Stations required").GetValue()
    FDM_RCIPC = Product.Attr("FDM_RCI_PC_required").GetValue()
    rciQty = int(Product.Attr("FDM_RCI_PC_Qty(0-25)").GetValue()) if Product.Attr("FDM_RCI_PC_Qty(0-25)").GetValue() else 0
    FDMCSQty = int(Product.Attr("FDM Client Station Qty (0-10)").GetValue()) if Product.Attr("FDM Client Station Qty (0-10)").GetValue() else 0
    rciNode = Product.Attr("FDM_RCI_PC_Node_Supplier").GetValue()
    rciNodeType = Product.Attr("FDM_RCI_PC_Station_Node_Type").GetValue()
    FDMCS_Node = Product.Attr("FDM_Node Supplier(Client Station)").GetValue()
    FDMCS_NodeType = Product.Attr("FDM_Client_Station Node Type").GetValue()
    if FDMCS == "Yes":
        #Commented because CXCPQ-86035 Story- Saurabh
        '''if FDMCSQty > 0 and FDMCS_Node =="Honeywell" and ExpPKSRelease == "R520":
            qty_EP_COAW19 += int(FDMCSQty)
        if FDMCSQty > 0 and FDMCS_Node =="Honeywell" and ExpPKSRelease == "R511":
            qty_EP_COAW10 += int(FDMCSQty)
        if FDMCSQty > 0 and FDMCS_Node =="Honeywell" and ExpPKSRelease in ['R520','R511'] and FDMCS_NodeType == 'STN_PER_DELL_Rack_RAID1':
            qty_MZ_PCWS77 += int(FDMCSQty)'''
        
        if FDMCSQty > 0 and FDMCS_Node =="Honeywell" and ExpPKSRelease == 'R520' and FDMCS_NodeType == 'STN_PER_HP_Tower_RAID1':
            qty_MZ_PCWS85 += int(FDMCSQty)
        if FDMCSQty > 0:
            qty_MZ_SQLCL4 += int(FDMCSQty)
                
    
    if FDM_RCIPC == "Yes":
        #Commented because CXCPQ-86035 Story- Saurabh
        '''if rciQty > 0 and rciNode =="Honeywell" and ExpPKSRelease == "R520":
            qty_EP_COAW19 += int(rciQty)
        if rciQty > 0 and rciNode =="Honeywell" and ExpPKSRelease == "R511":
            qty_EP_COAW10 += int(rciQty)
        if rciQty > 0 and rciNode =="Honeywell" and ExpPKSRelease in ['R520','R511'] and rciNodeType == 'STN_PER_DELL_Rack_RAID1' :
            qty_MZ_PCWS77  += int(rciQty)'''
        if rciQty > 0 and rciNode =="Honeywell" and ExpPKSRelease == 'R520' and rciNodeType == 'STN_PER_HP_Tower_RAID1': 
            qty_MZ_PCWS85 += int(rciQty)
        if rciQty > 0:
            qty_MZ_SQLCL4 += int(rciQty)

    if ExpPKSRelease == 'R520':
        if FDMCS == "Yes" and FDMCS_Node =="Honeywell" and FDMCS_NodeType == 'STN_PER_DELL_Tower_RAID2':
            qty_MZ_PCWT02 += FDMCSQty
            qty_EP_COAS19 += FDMCSQty

        if FDM_RCIPC == "Yes" and rciNode =="Honeywell" and rciNodeType == 'STN_PER_DELL_Tower_RAID2':
            qty_MZ_PCWT02 += rciQty
            qty_EP_COAS19 += rciQty
    
    #Changes added by RP CXCPQ-107750

    FDM_Base_Delivery=Product.Attr("FDM_Base_Media_Delivery").GetValue()
    New_Expansion=Product.Attr("New_Expansion").GetValue()
    FDM_Alert_Monitoring=(Product.Attr("FDM_Alert_Monitoring_License").GetValue())
    Trace.Write("FDM_Alert_Monitoring:{}".format(FDM_Alert_Monitoring))
    FDM_AM=int(FDM_Alert_Monitoring) if FDM_Alert_Monitoring else  0
    FDM_OPC_Server_Enabler_License =(Product.Attr("FDM_OPC_UA_Server_Enabler_License").GetValue())
    FDM_OPC=int(FDM_OPC_Server_Enabler_License) if FDM_OPC_Server_Enabler_License else  0
    fdmda=Product.Attr("FDM_OPC_UA_DA_Profile_Enabler_License").GetValue()
    FDM_DA=int(fdmda) if fdmda else  0
    fdmac=Product.Attr("FDM_OPC_UA_AC_Profile_Enabler_License").GetValue()
    FDM_AC=int(fdmac) if fdmac else  0
    fdmhda=Product.Attr("FDM_OPC_UA_HDA_Profile_Enabler_License").GetValue()
    FDM_HDA=int(fdmhda) if fdmhda else  0
    FDM_Connector_Interface=(Product.Attr("FDM_FF_Connector_Interface_License").GetValue())
    FDM_INT=int(FDM_Connector_Interface) if FDM_Connector_Interface else  0
    FDM_Device = (Product.Attr("FDM_FF_Custom_Connector").GetValue())
    FDM_DEVICE_BLOCK=int(FDM_Device) if FDM_Device else  0
    FDM_HART=Product.Attr("FDM HART-IP Downlink license (0-10)").GetValue()
    FDM_HART_Downlink_license=int(FDM_HART) if FDM_HART else  0
    FMD_Report=Product.Attr("FDM Report license (0-1)").GetValue()
    FMD_Report_License = int(FMD_Report) if FMD_Report else  0
    FDM_Diag=Product.Attr("FDM Diagnostic Custom Model (0-100)").GetValue()
    FDM_Diagnostic_Custom_Model=int(FDM_Diag) if FDM_Diag else  0
    FDM_OPC_Sv_blk=(Product.Attr("FDM_OPC_UA_Server_Device_Blocks").GetValue())
    FDM_OPC_UA_Server_Device_Blocks=int(FDM_OPC_Sv_blk) if FDM_OPC_Sv_blk else  0
    fdm_fisher=(Product.Attr("FDM_FF_Connector_Interface_Licence_Fisher").GetValue())
    FDM_FISHER=int(fdm_fisher) if fdm_fisher else  0

    if FDM_HART_Downlink_license > 0 :
        Trace.Write("HERE")
        qty_HC_HIP000 = FDM_HART_Downlink_license
    if (FDMRelease == "R530" or FDMRelease == "R540"):
        if FMD_Report_License==1:
            qty_HC_ICVR00=1
        if FDM_Diagnostic_Custom_Model>0:
            if FDM_Diagnostic_Custom_Model<=10:
                setAtvQty(Product,"FDM_Part_Summary","HC-NDM010",1)
            elif FDM_Diagnostic_Custom_Model >=91:
                setAtvQty(Product,"FDM_Part_Summary","HC-NDM100",1)
            else:
                fdmRem=(int(FDM_Diagnostic_Custom_Model) % 10)
                fdmMod=int(int(FDM_Diagnostic_Custom_Model)/10)
                if(fdmRem==0):
                    Log.Info("HC_NDM0{}0".format(fdmMod))
                    setAtvQty(Product,"FDM_Part_Summary","HC-NDM0{}0".format(fdmMod),1)
                else:
                    setAtvQty(Product,"FDM_Part_Summary","HC-NDM0{}0".format(fdmMod+1),1)


   #Changes added by RP CXCPQ-107750
    if FDMRelease == 'R540':
        if FDM_Base_Delivery == 'Electronic Download':
            qty_HC_HCM540_ESD += 1
        elif FDM_Base_Delivery == "Physical Delivery":
            qty_HC_HCM540 += 1

        if New_Expansion == 'New':
            if FDM_FISHER == 1:
                qty_HC_FCFVAL +=1

            if FDM_AM == 1:
                Trace.Write("also here")
                qty_HC_ALTMON +=1

            if FDM_OPC == 1:
                qty_HC_OPCUSV +=1
                if FDM_DA == 1:
                    Trace.Write("DA")
                    qty_HC_OPCUDA +=1
                if FDM_HDA==1:
                    Trace.Write("HDA")
                    qty_HC_OPCUHA +=1
                if FDM_AC==1:
                    Trace.Write("Ac")
                    qty_HC_OPCUAC +=1
            
            if FDM_INT==1:
                qty_HC_FCI000 +=1

            if FDM_OPC_UA_Server_Device_Blocks > 0 :
                Trace.Write("here")
                partNumMap={'16000':'HC-UA016K','16':'HC-UA0016','32':'HC-UA0032','64':'HC-UA0064','128':'HC-UA0128','256':'HC-UA0256','512':'HC-UA0512','1024':'HC-UA1024','2048':'HC-UA2048','4096':'HC-UA4096','8192':'HC-UA8192'}
                addUAServerDeviceBlocks(FDM_OPC_UA_Server_Device_Blocks,partNumMap)
            if FDM_DEVICE_BLOCK > 0 :

                partNumMap_CC={'16':'HC-FC0016','32':'HC-FC0032','64':'HC-FC0064','128':'HC-FC0128','256':'HC-FC0256','512':'HC-FC0512'}
                addUAServerDeviceBlocks(FDM_DEVICE_BLOCK,partNumMap_CC)
    #Changes added by RP CXCPQ-107750
    setAtvQty(Product,"FDM_Part_Summary","HC-ICVR00",qty_HC_ICVR00)
    setAtvQty(Product,"FDM_Part_Summary","HC-FCFVAL",qty_HC_FCFVAL)
    setAtvQty(Product,"FDM_Part_Summary","HC-HIP000",qty_HC_HIP000)
    setAtvQty(Product,"FDM_Part_Summary","HC-FCI000",qty_HC_FCI000)
    setAtvQty(Product,"FDM_Part_Summary","HC-OPCUAC",qty_HC_OPCUAC)
    setAtvQty(Product,"FDM_Part_Summary","HC-OPCUHA",qty_HC_OPCUHA)
    setAtvQty(Product,"FDM_Part_Summary","HC-HCM540",qty_HC_HCM540)
    setAtvQty(Product,"FDM_Part_Summary","HC-HCM540-ESD",qty_HC_HCM540_ESD)
    setAtvQty(Product,"FDM_Part_Summary","HC-ALTMON",qty_HC_ALTMON)
    setAtvQty(Product,"FDM_Part_Summary","HC-OPCUSV",qty_HC_OPCUSV)
    setAtvQty(Product,"FDM_Part_Summary","HC-OPCUDA",qty_HC_OPCUDA)
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCIS02",qty_MZ_PCIS02)
    #setAtvQty(Product,"FDM_Part_Summary","MZ-PCST82",qty_MZ_PCST82)
    #setAtvQty(Product,"FDM_Part_Summary","MZ-PCSV84",qty_MZ_PCSV84)
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCSR04",qty_MZ_PCSR04)
    #setAtvQty(Product,"FDM_Part_Summary","MZ-PCSR82",qty_MZ_PCSR82)
    #setAtvQty(Product,"FDM_Part_Summary","MZ-PCSR01",qty_MZ_PCSR01)
    #setAtvQty(Product,"FDM_Part_Summary","MZ-PCSR02",qty_MZ_PCSR02)
    #setAtvQty(Product,"FDM_Part_Summary","MZ-PCST02",qty_MZ_PCST02)
    #setAtvQty(Product,"FDM_Part_Summary","MZ-PCST01",qty_MZ_PCST01)
    setAtvQty(Product,"FDM_Part_Summary","EP-COAS19",qty_EP_COAS19)
    setAtvQty(Product,"FDM_Part_Summary","EP-COAS16",qty_EP_COAS16)
    setAtvQty(Product,"FDM_Part_Summary","TP-FPW271",qty_TP_FPW271)
    setAtvQty(Product,"FDM_Part_Summary","TP-FPW272",qty_TP_FPW272)
    setAtvQty(Product,"FDM_Part_Summary","TP-FPW241",qty_TP_FPW241)
    setAtvQty(Product,"FDM_Part_Summary","TP-FPW242",qty_TP_FPW242)
    #setAtvQty(Product,"FDM_Part_Summary","MZ-PCWS94",qty_MZ_PCWS94) #Commented because CXCPQ-86035 Story- Saurabh
    #setAtvQty(Product,"FDM_Part_Summary","MZ-PCWS84",qty_MZ_PCWS84)
    #setAtvQty(Product,"FDM_Part_Summary","MZ-PCWS77",qty_MZ_PCWS77) #Commented because CXCPQ-86035 Story- Saurabh
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCWS14",qty_MZ_PCWS14)
    #setAtvQty(Product,"FDM_Part_Summary","EP-COAW10",qty_EP_COAW10) #Commented because CXCPQ-86035 Story- Saurabh
    #setAtvQty(Product,"FDM_Part_Summary","EP-COAW19",qty_EP_COAW19) #Commented because CXCPQ-86035 Story- Saurabh
    setAtvQty(Product,"FDM_Part_Summary","TP-FPD211-200",qty_FPD211_200)
    setAtvQty(Product,"FDM_Part_Summary","TP-FPD211-100",qty_FPD211_100)
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCWS15",qty_MZ_PCWS15)
    #setAtvQty(Product,"FDM_Part_Summary","MZ-PCWS93",qty_MZ_PCWS93) #Commented because CXCPQ-86035 Story- Saurabh
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCWS86",qty_MZ_PCWS86)
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCWR01",qty_MZ_PCWR01)
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCWT01",qty_MZ_PCWT01)
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCSR03",qty_MZ_PCSR03)
    setAtvQty(Product,"FDM_Part_Summary","EP-COAS22",qty_EP_COAS22)
    setAtvQty(Product,"FDM_Part_Summary","EP-COAW21",qty_EP_COAW21)
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCSV85",qty_MZ_PCSV85)
    setAtvQty(Product,"FDM_Part_Summary","MZ-SQLCL4",qty_MZ_SQLCL4)
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCWS85",qty_MZ_PCWS85)
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCSR05",qty_MZ_PCSR05)
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCSR06",qty_MZ_PCSR06)
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCST03",qty_MZ_PCST03)
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCST04",qty_MZ_PCST04)
    setAtvQty(Product,"FDM_Part_Summary","MZ-PCWT02",qty_MZ_PCWT02)