import math
def getContainer(prod, conName):
    return prod.GetContainerByName(conName)
def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def cal16k (value):
    list1 = ["16k","8k","4k","2k","1k","512","256","128","064","032","016"]
    partDict = {}
    for x in list1:
        partDict[x]=0

    if 15984 < value <= 16000:
        partDict["16k"] = 1
    else:
        if 8176<value <=8192:
            partDict["8k"] =1
        else:
            partDict["8k"] +=  math.floor(value/8192)
            if  4080<value <=4096 or 4080<(value-partDict["8k"]*8192) <=4096:
                partDict["4k"] =1
            else:
                partDict["4k"] =math.floor((value-partDict["8k"]*8192)/4096)
                if 2032<value<=2048 or 2032<(value-partDict["8k"]*8192 -partDict["4k"]*4096)<=2048:
                    partDict["2k"] =1
                else:
                    partDict["2k"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096)/2048)
                    if 1008< value<=1024 or 1008< (value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048)<=1024:
                        partDict["1k"] =1
                    else:
                        partDict["1k"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048)/1024)
                        if 496< value<=512 or 496<(value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024)<=512 :
                            partDict["512"] =1
                        else:
                            partDict["512"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024)/512)
                            if 240 <value<=256 or 240 <(value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512)<=256: 
                                partDict["256"] =1
                            else:
                                partDict["256"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512)/256)
                                if 112<value<=128 or 112<(value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256)<=128:
                                    partDict["128"] =1
                                else:
                                    partDict["128"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256)/128)
                                    if  48<value<=64 or 48<(value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256-partDict["128"]*128)<=64:
                                        partDict["064"] =1
                                    else:
                                        partDict["064"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256-partDict["128"]*128)/64)
                                        if 16< value<=32 or 16< (value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256-partDict["128"]*128-partDict["064"]*64)<=32:
                                            partDict["032"] =1
                                        else:
                                            partDict["032"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256-partDict["128"]*128-partDict["064"]*64)/32)
                                            partDict["016"] =math.ceil((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256-partDict["128"]*128-partDict["064"]*64-partDict["032"]*32)/16)
    return partDict
def cal10k(value):
    list1 = ["10k","5k","2k","1k","100"]
    partDict = {}
    for x in list1:
        partDict[x]=0
    if 9900<value<= 10000:
        partDict["10k"] = 1
    else:
        partDict["10k"] =  math.floor(value/10000)
        if 4900 < value<=5000 or 4900 < (value -partDict["10k"]*10000)<=5000:
            partDict["5k"] =1
        else:
            partDict["5k"] = math.floor((value -partDict["10k"]*10000)/5000)
            if 3900 < value<=4000 or 3900 < (value-partDict["10k"]*10000-partDict["5k"]*5000)<=4000:
                partDict["2k"] =2
            elif 1900 < value<=2000 or 1900 < (value-partDict["10k"]*10000-partDict["5k"]*5000)<=2000:
                partDict["2k"] =1
            else:
                partDict["2k"] =math.floor((value-partDict["10k"]*10000-partDict["5k"]*5000)/2000)
                if 900 < value<=1000 or 900 < (value-partDict["10k"]*10000-partDict["5k"]*5000-partDict["2k"]*2000)<=1000:
                    partDict["1k"] =1
                else:
                    partDict["1k"] =math.floor((value-partDict["10k"]*10000-partDict["5k"]*5000-partDict["2k"]*2000)/1000)
                    partDict["100"] =math.ceil((value-partDict["10k"]*10000-partDict["5k"]*5000-partDict["2k"]*2000-partDict["1k"]*1000)/100)
    return partDict

def updateAttrDictWithCustomFDMUpgrade(product, attrValDict):
    l = 0
    con = getContainer(product, "FDM_Upgrade_Configuration")
    for row in con.Rows:
        l = getFloat(row["FDM_Upgrade_Total_FDM_Clients"])
    attrValDict["FDM_Upgrade_Total_FDM_Client_Count"] = float(l)
    if float(attrValDict["FDM_Upgrade_Total_FDM_Client_Count"]) > 0:
        attrValDict["FDM_Upgrade_Total_FDM_Client_Count_grt_0"] = 'True'
    con1 = getContainer(product, 'FDM_Upgrade_Additional_Configuration')
    HC_SM0000= 0
    HC_OC0000= 0
    HC_HM0000= 0
    HC_HM0MX1= 0
    HC_MM0000= 0
    HC_MM0MX1= 0
    HC_RI0000= 0
    HC_RI0MX1= 0
    HC_IS0000= 0
    HC_CLNT00 = 0
    #server device
    HC_SV0016=0
    HC_SV0032=0
    HC_SV0064=0
    HC_SV0128=0
    HC_SV0256=0
    HC_SV0512=0
    HC_SV1024=0
    HC_SV2048=0
    HC_SV4096=0
    HC_SV8192=0
    HC_SV016K=0
    #Audit trail
    HC_AT0016=0
    HC_AT0032=0
    HC_AT0064=0
    HC_AT0128=0
    HC_AT0256=0
    HC_AT0512=0
    HC_AT1024=0
    HC_AT2048=0
    HC_AT4096=0
    HC_AT8192=0
    HC_AT016K=0
    #FDM HART Multiplexer
    HC_FH0016=0
    HC_FH0032=0
    HC_FH0064=0
    HC_FH0128=0
    HC_FH0256=0
    HC_FH0512=0
    HC_FH1024=0
    HC_FH2048=0
    #Experion Server process I/O point licenses
    EP_DPR100=0
    EP_DPR01K=0
    EP_DPR02K=0
    EP_DPR05K=0
    EP_DPR10K=0
    #Experion Server process I/O point Redundancy adder licenses
    EP_RPR100=0
    EP_RPR01K=0
    EP_RPR02K=0
    EP_RPR05K=0
    EP_RPR10K=0
    #PVST Planner Licenses
    HC_PV0032=0
    HC_PV0064=0
    HC_PV0128=0
    HC_PV0256=0
    HC_PV0512=0
    HC_PV1024=0
    #Downlink Liscene
    HC_HIP000=0
    for row in con1.Rows:
        FH0016=0
        FH0032=0
        FH0064=0
        FH0128=0
        FH0256=0
        FH0512=0
        FH1024=0
        FH2048=0
        PV0032=0
        PV0064=0
        PV0128=0
        PV0256=0
        PV0512=0
        PV1024=0
        serDevice = getFloat(row['FDM_Upgrade_How_many_devices_will_be_managed'])
        auditTrail = getFloat(row['FDM_Upgrade_Number_of_Audit_Trail_Devices'])
        FDMHartMulti = getFloat(row['FDM_Upgrade_Number_of_HART_devices_from_device_vendors'])
        EXserIOLic = getFloat(row['FDM_Upgrade_Number_of_Experion_Server_process_IO_point_licenses'])  
        PVSTLic = getFloat(row['FDM_Upgrade_Number_of_PVST_Planner_Licenses_for_supported_HART_ESD_Devices'])
        noOfExpTPSserver = getFloat(row['FDM_Upgrade_Number_of_Experion_TPS_Servers_for_FDM_Integration'])
        noOfserNetLic = getFloat(row['FDM_Upgrade_Number_of_Server_Network_Interface_Licenses_Add'])
        noOfHartLic = getFloat(row['FDM_Upgrade_Number_of_HART_Hardware_MUX_Network_Monitoring_Licenses'])
        noOfRemoPC = getFloat(row['FDM_Upgrade_Number_of_remote_PCs_connecting_to_FDM_Serve_ via_LAN'])
        fdmClients = getFloat(row['FDM_Upgrade_Number_of_FDM_Clients'])
        if (row["FDM_Upgrade_HART_Devices_Offline_Configuration_required"] == "Yes"):
            HC_OC0000 +=1
        if (row["FDM_Upgrade_Asset_Sentinel_integration_required"]=="Yes"):
            HC_IS0000 +=1
        HC_SM0000 +=noOfExpTPSserver
        if noOfserNetLic <25:
            HC_HM0000 +=noOfserNetLic
        else:
            HC_HM0MX1 +=1
        if noOfHartLic <25:
            HC_MM0000 +=noOfHartLic 
        else:
            HC_MM0MX1 +=1
        
        if noOfRemoPC <25:
            HC_RI0000 +=noOfRemoPC 
        else:
            HC_RI0MX1 +=1
        HC_CLNT00 += fdmClients
        #FDM_Upgrade_Total_number_of_Server_Device_Points
        serRes = cal16k(serDevice)
        HC_SV0016+=serRes["016"]
        HC_SV0032+=serRes["032"]
        HC_SV0064+=serRes["064"]
        HC_SV0128+=serRes["128"]
        HC_SV0256+=serRes["256"]
        HC_SV0512+=serRes["512"]
        HC_SV1024+=serRes["1k"]
        HC_SV2048+=serRes["2k"]
        HC_SV4096+=serRes["4k"]
        HC_SV8192+=serRes["8k"]
        HC_SV016K+=serRes["16k"]
        #Audit trail
        if(row["FDM_Upgrade_Audit_trail_file_required"] not in(" ",None, "No")):
            auditRes = cal16k(auditTrail)
            HC_AT0016+=auditRes["016"]
            HC_AT0032+=auditRes["032"]
            HC_AT0064+=auditRes["064"]
            HC_AT0128+=auditRes["128"]
            HC_AT0256+=auditRes["256"]
            HC_AT0512+=auditRes["512"]
            HC_AT1024+=auditRes["1k"]
            HC_AT2048+=auditRes["2k"]
            HC_AT4096+=auditRes["4k"]
            HC_AT8192+=auditRes["8k"]
            HC_AT016K+=auditRes["16k"]
        #Fdm Hart
        if 2032<FDMHartMulti<= 2048:
            FH2048 =1
        else:
            if 1008< FDMHartMulti<= 1024:
                FH1024 = 1
            else:
                FH1024 = math.floor(FDMHartMulti/1024)
                if 496 <FDMHartMulti<=512 or 496 <(FDMHartMulti -FH1024*1024)<=512:
                    FH0512 =1
                else:
                    FH0512 = math.floor((FDMHartMulti -FH1024*1024)/512)
                    if 240< FDMHartMulti<=256 or 240< (FDMHartMulti-FH1024*1024-FH0512*512)<=256:
                        FH0256 =1
                    else:
                        FH0256 =math.floor((FDMHartMulti-FH1024*1024-FH0512*512)/256)
                        if 112<FDMHartMulti<=128 or 112<(FDMHartMulti-FH1024*1024-FH0512*512 -FH0256*256)<=128:
                            FH0128 =1
                        else:
                            FH0128 =math.floor((FDMHartMulti-FH1024*1024-FH0512*512 -FH0256*256)/128)
                            if 48<FDMHartMulti<=64 or 48<(FDMHartMulti-FH1024*1024-FH0512*512 -FH0256*256- FH0128*128)<=64:
                                FH0064 =1
                            else:
                                FH0064 =math.floor((FDMHartMulti-FH1024*1024-FH0512*512 -FH0256*256- FH0128*128)/64)
                                if 16 < FDMHartMulti<=32 or 16 < (FDMHartMulti-FH1024*1024-FH0512*512 -FH0256*256- FH0128*128 - FH0064*64)<=32:
                                    FH0032 =1
                                else:
                                    FH0032 =math.floor((FDMHartMulti-FH1024*1024-FH0512*512 -FH0256*256- FH0128*128 - FH0064*64)/32)
                                    FH0016 =math.ceil((FDMHartMulti-FH1024*1024-FH0512*512 -FH0256*256- FH0128*128 - FH0064*64 - FH0032*32)/16)
        HC_FH0016+=FH0016
        HC_FH0032+=FH0032
        HC_FH0064+=FH0064
        HC_FH0128+=FH0128
        HC_FH0256+=FH0256
        HC_FH0512+=FH0512
        HC_FH1024+=FH1024
        HC_FH2048+=FH2048

        if(row["FDM_Upgrade_Is_Experion_Server_redundant_for_FDM_Multiplexer_Monitoring"] not in(" ",None, "No")):
            #Experion Server process I/O point Redundancy adder licenses
            RedRes =cal10k(EXserIOLic)
            EP_RPR100+=RedRes["100"]
            EP_RPR01K+=RedRes["1k"]
            EP_RPR02K+=RedRes["2k"]
            EP_RPR05K+=RedRes["5k"]
            EP_RPR10K+=RedRes["10k"]
        #Experion Server process I/O point licenses
        IORes= cal10k(EXserIOLic)
        EP_DPR100+=IORes["100"]
        EP_DPR01K+=IORes["1k"]
        EP_DPR02K+=IORes["2k"]
        EP_DPR05K+=IORes["5k"]
        EP_DPR10K+=IORes["10k"]
        #PVST Planner Licenses
        if 992<PVSTLic<= 1024:
            PV1024 = 1
        else:
            if 480< PVSTLic<=512:
                PV0512 =1
            else:
                PV0512 =  math.floor(PVSTLic/512)
                if 224< PVSTLic<=256 or 224< (PVSTLic-PV0512*512)<=256:
                    PV0256 =1
                else:
                    PV0256 =math.floor((PVSTLic-PV0512*512)/256)
                    if 96<PVSTLic<=128 or 96<(PVSTLic-PV0512*512 -PV0256*256)<=128:
                        PV0128 +=1
                    else:
                        PV0128 =math.floor((PVSTLic-PV0512*512 -PV0256*256)/128)
                        if 32< PVSTLic<=64 or 32< (PVSTLic-PV0512*512 -PV0256*256- PV0128*128)<=64:
                            PV0064 =1
                        else:
                            PV0064 =math.floor((PVSTLic-PV0512*512 -PV0256*256- PV0128*128)/64)
                            PV0032 =math.ceil((PVSTLic-PV0512*512 -PV0256*256- PV0128*128 - PV0064*64)/32)
        HC_PV0032+=PV0032
        HC_PV0064+=PV0064
        HC_PV0128+=PV0128
        HC_PV0256+=PV0256
        HC_PV0512+=PV0512
        HC_PV1024+=PV1024
        if(row["FDM HART IP DOWNLINK LICENSE"] == "Yes"):
            HC_HIP000+=1
    #FMD Upgrade Configuration-----------------------------------
    UPANR_FDM = 0
    q0=q1=q2=q3= 0
    for row in con.Rows:
        Trace.Write(row["FDM_Upgrade_Do_you_want_to_upgrade_this_FDM"])
        if row["FDM_Upgrade_Do_you_want_to_upgrade_this_FDM"] == "Yes":
            q0 += 50
            #Trace.Write(row["FDM_Upgrade_Total_number_of_Server_Device_Points"])
            q1 += int(getFloat(row["FDM_Upgrade_Total_number_of_Server_Device_Points"]) * 0.22 + getFloat(row["FDM_Upgrade_Total_number_of_Audit_Trail_Devices"]) * 0.22)
            q2 += int(getFloat(row["FDM_Upgrade_Total_RCIs_excluding_Experion_PKS_Server_Interfaces"])*31) + int(getFloat(row["FDM_Upgrade_Total_FDM_Clients"])*17)
            q3 += int(getFloat(row["FDM_Upgrade_Total_Server_Hardware_Multiplexer_Licenses"]) *14) + int(getFloat(row["FDM_Upgrade_Total_Multiplexer_Monitoring_Network_Licenses"]) *14)

    UPANR_FDM += (q0 + q1 + q2 + q3)  

    attrValDict["UPANR_FDM"]=UPANR_FDM
    #-----------------------------------------------
    attrValDict["HC_SM0000"]=HC_SM0000
    attrValDict["HC_OC0000"]=HC_OC0000
    attrValDict["HC_HM0000"]=HC_HM0000
    attrValDict["HC_HM0MX1"]=HC_HM0MX1
    attrValDict["HC_MM0000"]=HC_MM0000
    attrValDict["HC_MM0MX1"]=HC_MM0MX1
    attrValDict["HC_RI0000"]=HC_RI0000
    attrValDict["HC_RI0MX1"]=HC_RI0MX1
    attrValDict["HC_IS0000"]=HC_IS0000
    attrValDict["HC_CLNT00"]=HC_CLNT00
    #server device
    attrValDict["HC_SV0016"]=HC_SV0016
    attrValDict["HC_SV0032"]=HC_SV0032
    attrValDict["HC_SV0064"]=HC_SV0064
    attrValDict["HC_SV0128"]=HC_SV0128
    attrValDict["HC_SV0256"]=HC_SV0256
    attrValDict["HC_SV0512"]=HC_SV0512
    attrValDict["HC_SV1024"]=HC_SV1024
    attrValDict["HC_SV2048"]=HC_SV2048
    attrValDict["HC_SV4096"]=HC_SV4096
    attrValDict["HC_SV8192"]=HC_SV8192
    attrValDict["HC_SV016K"]=HC_SV016K
    #Audit trail
    attrValDict["HC_AT0016"]=HC_AT0016
    attrValDict["HC_AT0032"]=HC_AT0032
    attrValDict["HC_AT0064"]=HC_AT0064
    attrValDict["HC_AT0128"]=HC_AT0128
    attrValDict["HC_AT0256"]=HC_AT0256
    attrValDict["HC_AT0512"]=HC_AT0512
    attrValDict["HC_AT1024"]=HC_AT1024
    attrValDict["HC_AT2048"]=HC_AT2048
    attrValDict["HC_AT4096"]=HC_AT4096
    attrValDict["HC_AT8192"]=HC_AT8192
    attrValDict["HC_AT016K"]=HC_AT016K
    #FDM HART Mutiplexer
    attrValDict["HC_FH0016"]=HC_FH0016
    attrValDict["HC_FH0032"]=HC_FH0032
    attrValDict["HC_FH0064"]=HC_FH0064
    attrValDict["HC_FH0128"]=HC_FH0128
    attrValDict["HC_FH0256"]=HC_FH0256
    attrValDict["HC_FH0512"]=HC_FH0512
    attrValDict["HC_FH1024"]=HC_FH1024
    attrValDict["HC_FH2048"]=HC_FH2048
    #Experion Server process I/O point licenses
    attrValDict["EP_DPR100"]=EP_DPR100
    attrValDict["EP_DPR01K"]=EP_DPR01K
    attrValDict["EP_DPR02K"]=EP_DPR02K
    attrValDict["EP_DPR05K"]=EP_DPR05K
    attrValDict["EP_DPR10K"]=EP_DPR10K
    #Experion Server process I/O point Redundancy adder licenses
    attrValDict["EP_RPR100"]=EP_RPR100
    attrValDict["EP_RPR01K"]=EP_RPR01K
    attrValDict["EP_RPR02K"]=EP_RPR02K
    attrValDict["EP_RPR05K"]=EP_RPR05K
    attrValDict["EP_RPR10K"]=EP_RPR10K
    #PVST Planner Licenses
    attrValDict["HC_PV0032"]=HC_PV0032
    attrValDict["HC_PV0064"]=HC_PV0064
    attrValDict["HC_PV0128"]=HC_PV0128
    attrValDict["HC_PV0256"]=HC_PV0256
    attrValDict["HC_PV0512"]=HC_PV0512
    attrValDict["HC_PV1024"]=HC_PV1024
    #Downlink Liscene
    attrValDict["HC_HIP000"]=HC_HIP000
    
def populateWriteInsLM(product):
    writeInData = dict()
    msid= product.Attr('Migration_MSID_Choices').GetValue()
    sysNumber= product.Attr('Migration_MSID_System_Number').GetValue()
    area = msid +" - "+ sysNumber
    if product.GetContainerByName("LM_to_ELMM_3rd_Party_Items"):
        con = getContainer(product, "LM_to_ELMM_3rd_Party_Items")
        if con.Rows.Count == 3:
            rowWIPrice = con.Rows[0]
            rowWICost = con.Rows[1]
            rowWIExDesc = con.Rows[2]
            writeInData["LM_to_ELMM_3rd_Party_Hardware_Weidmuller"] = [rowWIPrice["LM_to_ELMM_3rd_Party_Hardware_Weidmuller"] if rowWIPrice["LM_to_ELMM_3rd_Party_Hardware_Weidmuller"] else "0",rowWICost["LM_to_ELMM_3rd_Party_Hardware_Weidmuller"] if rowWICost["LM_to_ELMM_3rd_Party_Hardware_Weidmuller"] else "0",rowWIExDesc["LM_to_ELMM_3rd_Party_Hardware_Weidmuller"] if rowWIExDesc["LM_to_ELMM_3rd_Party_Hardware_Weidmuller"] else "0", area]
            writeInData["LM_to_ELMM_3rd_Party_Hardware_Interposing_Relays"] = [rowWIPrice["LM_to_ELMM_3rd_Party_Hardware_Interposing_Relays"] if rowWIPrice["LM_to_ELMM_3rd_Party_Hardware_Interposing_Relays"] else "0",rowWICost["LM_to_ELMM_3rd_Party_Hardware_Interposing_Relays"] if rowWICost["LM_to_ELMM_3rd_Party_Hardware_Interposing_Relays"] else "0",rowWIExDesc["LM_to_ELMM_3rd_Party_Hardware_Interposing_Relays"] if rowWIExDesc["LM_to_ELMM_3rd_Party_Hardware_Interposing_Relays"] else "0", area]
            writeInData["LM_to_ELMM_3rd_Party_Hardware_Others"] = [rowWIPrice["LM_to_ELMM_3rd_Party_Hardware_Others"] if rowWIPrice["LM_to_ELMM_3rd_Party_Hardware_Others"] else "0",rowWICost["LM_to_ELMM_3rd_Party_Hardware_Others"] if rowWICost["LM_to_ELMM_3rd_Party_Hardware_Others"] else "0",rowWIExDesc["LM_to_ELMM_3rd_Party_Hardware_Others"] if rowWIExDesc["LM_to_ELMM_3rd_Party_Hardware_Others"] else "0", area]
            writeInData["LM_to_ELMM_3rd_Party_Hardware_Cabinet"] = [rowWIPrice["LM_to_ELMM_3rd_Party_Hardware_Cabinet"] if rowWIPrice["LM_to_ELMM_3rd_Party_Hardware_Cabinet"] else "0",rowWICost["LM_to_ELMM_3rd_Party_Hardware_Cabinet"] if rowWICost["LM_to_ELMM_3rd_Party_Hardware_Cabinet"] else "0",rowWIExDesc["LM_to_ELMM_3rd_Party_Hardware_Cabinet"] if rowWIExDesc["LM_to_ELMM_3rd_Party_Hardware_Cabinet"] else "0", area]

    productContainer = product.GetContainerByName("MSID_Product_Container")
    productRow = productContainer.Rows.GetByColumnName("Product Name", "LM to ELMM ControlEdge PLC")
    prod = productRow.Product
    conWriteIn = prod.GetContainerByName("WriteInProduct")
    if conWriteIn.Rows.Count > 0:
        conWriteIn.Rows.Clear()
    for wi, wiData in writeInData.items():
        if (getFloat(wiData[0]) > 0) and (getFloat(wiData[1]) > 0):
            row = conWriteIn.AddNewRow()
            row.Product.Attr("Selected_WriteIn").AssignValue("Write-in Third Party Hardware Misc")
            row.Product.Attr("Price").AssignValue(wiData[0])
            row.Product.Attr("Cost").AssignValue(wiData[1])
            row.Product.Attr("QI_Area").AssignValue(wiData[3])
            row.Product.Attr("ItemQuantity").AssignValue("1")
            row.Product.Attr("Extended Description").AssignValue(wiData[2])
            row.Product.ApplyRules()
            row.ApplyProductChanges()
            row.Calculate()
    conWriteIn.Calculate()

def updateAttrDictWithXP10Actuator(product, attrValDict):
    con = getContainer(product, 'XP10_Actuator_General_Information')
    conrow = con.Rows[0]
    numActuator = getFloat(conrow['XP10_Actuator_Number_of_actuators_to_be_upgraded'])
    p6530230006 = 0
    if numActuator>0:
        p6530230006 =1
    attrValDict['p6530230006'] 	= p6530230006

def updateAttrDictWithCWSRAE(Product, attrValDict):
    
    phyconfig = Product.Attr('CWS_Mig_Physical_configuration').GetValue()
    virtconfig = Product.Attr('CWS_Mig_Virtualization_Configuration').GetValue()
    tsMonitor = Product.Attr('CWS_Mig_Customer_require_a_Touch_Screen_monitor').GetValue()
    curRelease = Product.Attr('CWS_Mig_Current_Release_on_System').GetValue()
    typeComm3 = Product.Attr('CWS_Mig_Type_of_Communication_Links_with_3rd_party').GetValue()
    serialComm = Product.Attr('CWS_Mig_system_contain_Serial_Communication_links').GetValue()
    MXProLine = Product.Attr('CWS_Mig_MXProLine_desktop_server').GetValue()
    uScenario = Product.Attr('CWS_Mig_Upgrade_Scenario').GetValue()
    operStation = Product.Attr('CWS_Mig_Touch_Screen_monitor_for_the_Operator_Station').GetValue()
    QCSstandardEd = Product.Attr('CWS_Mig_Will_customer_provide_HW_for_QCS_Standard').GetValue()

    V346279N =V346279T =V35700RAE7 =V35700MIGSVR7 =V3587002 =V3587602 =V346279ON =V346279OT =V35700MIGOPS7 =V35700OPS7 =V3HCI =V3HCIPT =V3587401 =V3587401PT =V3587601 =V3587601PT =V3587101 =V3587101PT =VEPIRSL36=0
    if phyconfig == "MX Proline":
        if tsMonitor =="No":
            V346279N =1
        else:
            V346279T = 1
        if curRelease =="RAE 2 or Less":
            V35700RAE7 =1
        else:
            V35700MIGSVR7 =1
        if MXProLine > 0 and uScenario == 'Physical hardware only': 
            if operStation == 'No':
                V346279ON = MXProLine
            else:
                V346279OT = MXProLine
        if MXProLine > 0 and uScenario == 'Physical hardware only':
            if curRelease == 'RAE 3 or Later':
                V35700MIGOPS7 = MXProLine
            else:
                V35700OPS7 = MXProLine
    QCSSE110SYS=QCSSE110ESD=MZSQLCL4=Q590460=MZPCWS14=EPCOAW10 =0
    if phyconfig == "QCS Standard Edition":
        QCSSE110SYS=QCSSE110ESD=MZSQLCL4=Q590460 =1
        if QCSstandardEd == "No":
            MZPCWS14 = EPCOAW10 = 1


    if uScenario =="Physical hardware only":
        if curRelease =="RAE 2 or Less":
            
            if typeComm3 =='Honeywell OPC Client':
                V3HCI =1
                V3HCIPT = 1
            elif typeComm3 == 'Modbus Ethernet':
                V3587401 =1
                V3587401PT = 1
            elif typeComm3 == 'Modbus RTU':
                V3587601 =1
                V3587601PT =1
            elif typeComm3 == "Allen Bradley Serial":
                V3587101 =1
                V3587101PT =1  
        if typeComm3 in ['Allen Bradley Ethernet','Allen Bradley Serial']:
            V3587002 =1
            VEPIRSL36 =1
        if serialComm == "Yes":
            V3587602 = 1

    MZPCVM22=MZPCVMM5=MZPCWS13=MZNWSTR6 =NESW224P=Q509580=TPTHNCL6100=QCSEXPMXVMS=EPVESPB6=V3509664=EPCOADC4=EPT09CAL= 0
    MZPCVM20=V3509662 = 0
    SH2620R4=MZPCEM39 =EPVWKB16=EPCOAS16 = 0
    
    
    if virtconfig == "ESXi Virtualization with Management host and four VMs and four thin clients":
        MZPCVM22 =EPCOADC4= 2
        MZPCVMM5 = MZPCWS13 = MZNWSTR6 =EPVESPB6=V3509664= EPCOAW10 =1
        NESW224P = 3
        Q509580 = 5
        TPTHNCL6100 = V35700RAE7 = QCSEXPMXVMS =EPT09CAL = MZSQLCL4=4
        #Write -ins
    elif virtconfig == "Virtualization on a Server with One VM and 2 Thin Clients":
        MZPCVM20 = MZPCWS13 =V35700RAE7=QCSEXPMXVMS=EPVESPB6=V3509662=EPCOAW10=EPCOADC4 =1
        NESW224P =Q509580 = 3
        TPTHNCL6100 = EPT09CAL =MZSQLCL4 = 2
        #writeins
    elif virtconfig == "Workstation Virtualization":
        V346279N=SH2620R4=MZPCEM39 =V35700RAE7=QCSEXPMXVMS=EPVWKB16=EPCOAS16 = 1
        #writeins
    elif virtconfig == "QCS Standard Edition":
        QCSSE110SYS=QCSSE110ESD=MZSQLCL4=Q590460=1
        if QCSstandardEd == "No":
            MZPCWS14 = EPCOAW10 =1

    V3878500 =V3878600 =V3878700 =V3878800 =V3878900 =V3879000 =V3879100 =V3879200 =V3879300 =V3879500 =V3879600 =V3879700 =V3879800 = 0
    if Product.Attr('CWS_Mig_Machine_Cross_Direction_controls_upgraded_peripheral_hardware_licensing').GetValue() == "Yes":
        V3878500 = getFloat(Product.Attr('CWS_Mig_System_Chassis_with_C50_Controller').GetValue())
        V3878600 = getFloat(Product.Attr('CWS_Mig_Analog_Input_Modules_8_point').GetValue())
        V3878700 = getFloat(Product.Attr('CWS_Mig_Analog_Output_Modules_4_point').GetValue())
        V3878800 = getFloat(Product.Attr('CWS_Mig_Digital_Input_Contact_type_Modules_16_point').GetValue())
        V3878900 = getFloat(Product.Attr('CWS_Mig_Digital_Input_24VDC_Modules_16_point').GetValue())
        V3879000 = getFloat(Product.Attr('CWS_Mig_Digital_Input_120_240_VAC_Modules_16_point').GetValue())
        V3879100 = getFloat(Product.Attr('CWS_Mig_Digital_Output_Relays_Modules_8_point').GetValue())
        V3879200 = getFloat(Product.Attr('CWS_Mig_Digital_Output_24VDC_Modules_16_point').GetValue())
        V3879300 = getFloat(Product.Attr('CWS_Mig_Digital_Output_120_240_VAC_Modules_8_point').GetValue())
        V3879500 = getFloat(Product.Attr('CWS_Mig_Digital_Output_24VDC_Modules_32_point').GetValue())
        V3879600 = getFloat(Product.Attr('CWS_Mig_Digital_Input_24VDC_Modules_32_point').GetValue())
        V3879700 = getFloat(Product.Attr('CWS_Mig_Hi_level_Analog_Input_Modules_16_point').GetValue())
        V3879800 = getFloat(Product.Attr('CWS_Mig_Pulse_Frequency_Quadrature_Input_Modules_4_point').GetValue())
    
    V3879404 = V3879404BO = V3879405 = V3879405BO = V3879406 = V3879406BO = V3879407 = V3879407BO = 0
    if Product.Attr('CWS_Mig_Cross_Direction_controls_upgraded_peripheral_hardware_licensing').GetValue() == "Yes":
        singlePhase = Product.Attr('CWS_Mig_Single_phase_or_Three_phase_power').GetValue()
        dieBolts = getFloat(Product.Attr('CWS_Mig_Number_of_die_bolts').GetValue())
        if singlePhase == "Single phase":
            if dieBolts < 97:
                V3879404 = 1
                V3879404BO = dieBolts
            else:
                V3879406 =1
                V3879406BO = dieBolts
        elif singlePhase == "Three phase":
            if dieBolts < 97:
                V3879405 = 1
                V3879405BO = dieBolts
            else:
                V3879407 =1
                V3879407BO = dieBolts
    attrValDict["V346279N"]=V346279N
    attrValDict["V346279T"]=V346279T
    attrValDict["V35700RAE7"]=V35700RAE7
    attrValDict["V35700MIGSVR7"]=V35700MIGSVR7
    attrValDict["V3587002"]=V3587002
    attrValDict["V3587602"]=V3587602
    attrValDict["V346279ON"]=V346279ON
    attrValDict["V346279OT"]=V346279OT
    attrValDict["V35700MIGOPS7"]=V35700MIGOPS7
    attrValDict["V35700OPS7"]=V35700OPS7
    attrValDict["V3HCI"]=V3HCI
    attrValDict["V3HCIPT"]=V3HCIPT
    attrValDict["V3587401"]=V3587401
    attrValDict["V3587401PT"]=V3587401PT
    attrValDict["V3587601"]=V3587601
    attrValDict["V3587601PT"]=V3587601PT
    attrValDict["V3587101"]=V3587101
    attrValDict["V3587101PT"]=V3587101PT
    attrValDict["VEPIRSL36"]=VEPIRSL36
    attrValDict["V3878500"]=V3878500
    attrValDict["V3878600"]=V3878600
    attrValDict["V3878700"]=V3878700
    attrValDict["V3878800"]=V3878800
    attrValDict["V3878900"]=V3878900
    attrValDict["V3879000"]=V3879000
    attrValDict["V3879100"]=V3879100
    attrValDict["V3879200"]=V3879200
    attrValDict["V3879300"]=V3879300
    attrValDict["V3879500"]=V3879500
    attrValDict["V3879600"]=V3879600
    attrValDict["V3879700"]=V3879700
    attrValDict["V3879800"]=V3879800
    attrValDict["V3879404"]=V3879404
    attrValDict["V3879404BO"]=V3879404BO
    attrValDict["V3879405"]=V3879405
    attrValDict["V3879405BO"]=V3879405BO
    attrValDict["V3879406"]=V3879406
    attrValDict["V3879406BO"]=V3879406BO
    attrValDict["V3879407"]=V3879407
    attrValDict["V3879407BO"]=V3879407BO
    attrValDict["VQCSSE110SYS"]=QCSSE110SYS
    attrValDict["VQCSSE110ESD"]=QCSSE110ESD
    attrValDict["VMZSQLCL4"]=MZSQLCL4
    attrValDict["VQ590460"]=Q590460
    attrValDict["VMZPCWS14"]=MZPCWS14
    attrValDict["VEPCOAW10"]=EPCOAW10
    attrValDict["VMZPCVM22"]=MZPCVM22
    attrValDict["VMZPCVMM5"]=MZPCVMM5
    attrValDict["VMZPCWS13"]=MZPCWS13
    attrValDict["VMZNWSTR6"]=MZNWSTR6
    attrValDict["VNESW224P"]=NESW224P
    attrValDict["VQ509580"]=Q509580
    attrValDict["VTPTHNCL6100"]=TPTHNCL6100
    attrValDict["VQCSEXPMXVMS"]=QCSEXPMXVMS
    attrValDict["VEPVESPB6"]=EPVESPB6
    attrValDict["V3509664"]=V3509664
    attrValDict["VEPCOADC4"]=EPCOADC4
    attrValDict["VEPT09CAL"]=EPT09CAL
    attrValDict["VMZPCVM20"]=MZPCVM20
    attrValDict["V3509662"]=V3509662
    attrValDict["VSH2620R4"]=SH2620R4
    attrValDict["VMZPCEM39"]=MZPCEM39
    attrValDict["VEPVWKB16"]=EPVWKB16
    attrValDict["VEPCOAS16"]=EPCOAS16

def updateAttrDictWithQCSRAE(Product, attrDict):

    Q3878500 =Q3878600 =Q3878700 =Q3878800 =Q3878900 =Q3879000 =Q3879100 =Q3879200 =Q3879300 =Q3879500 =Q3879600 =Q3879700 =Q3879800 = 0
    if Product.Attr('QCS_Mig_What_type_of_Machine_Direction_Controls').GetValue() == "MDMV":
        Q3878500 = getFloat(Product.Attr('QCS_Mig_System_Chassis_with_C50_Controller_power').GetValue())
        Q3878600 = getFloat(Product.Attr('QCS_Mig_Analog_Input_Modules_8_point').GetValue())
        Q3878700 = getFloat(Product.Attr('QCS_Mig_Analog_Output_Modules_4_point').GetValue())
        Q3878800 = getFloat(Product.Attr('QCS_Mig_Digital_Input_Contact_type_Modules_16_poin').GetValue())
        Q3878900 = getFloat(Product.Attr('QCS_Mig_Digital_Input_24VDC_Modules_16_point').GetValue())
        Q3879000 = getFloat(Product.Attr('QCS_Mig_Digital_Input_120_240_VAC_Modules_16_point').GetValue())
        Q3879100 = getFloat(Product.Attr('QCS_Mig_Digital_Output_Relays_Modules_8_point').GetValue())
        Q3879200 = getFloat(Product.Attr('QCS_Mig_Digital_Output_24VDC_Modules_16_point').GetValue())
        Q3879300 = getFloat(Product.Attr('QCS_Mig_Digital_Output_120_240_VAC_Modules_8_point').GetValue())
        Q3879500 = getFloat(Product.Attr('QCS_Mig_Digital_Output_24VDC_Modules_32_point').GetValue())
        Q3879600 = getFloat(Product.Attr('QCS_Mig_Digital_Input_24VDC_Modules_32_point').GetValue())
        Q3879700 = getFloat(Product.Attr('QCS_Mig_Hi_level_Analog_Input_Modules_16_point').GetValue())
        Q3879800 = getFloat(Product.Attr('QCS_Mig_Pulse_Frequency_Quadrature_Input_Modules_4').GetValue())

    Q3879404 = Q3879404BO = Q3879405 = Q3879405BO = Q3879406 = Q3879406BO = Q3879407 = Q3879407BO = 0
    if Product.Attr('QCS_Mig_CD_Controls').GetValue() in ["CDMV","CD Traditional with Intellimap"]:
        singlePhase = Product.Attr('QCS_Mig_Single_phase_or_Three_phase_power').GetValue()
        dieBolts = getFloat(Product.Attr('QCS_Mig_Number_of_die_bolts').GetValue())
        if singlePhase == "Single phase":
            if dieBolts < 97:
                Q3879404 = 1
                Q3879404BO = dieBolts
            else:
                Q3879406 =1
                Q3879406BO = dieBolts
        elif singlePhase == "Three phase":
            if dieBolts < 97:
                Q3879405 = 1
                Q3879405BO = dieBolts
            else:
                Q3879407 =1
                Q3879407BO = dieBolts
    attrDict["Q3878500"]=Q3878500
    attrDict["Q3878600"]=Q3878600
    attrDict["Q3878700"]=Q3878700
    attrDict["Q3878800"]=Q3878800
    attrDict["Q3878900"]=Q3878900
    attrDict["Q3879000"]=Q3879000
    attrDict["Q3879100"]=Q3879100
    attrDict["Q3879200"]=Q3879200
    attrDict["Q3879300"]=Q3879300
    attrDict["Q3879500"]=Q3879500
    attrDict["Q3879600"]=Q3879600
    attrDict["Q3879700"]=Q3879700
    attrDict["Q3879800"]=Q3879800
    attrDict["Q3879404"]=Q3879404
    attrDict["Q3879404BO"]=Q3879404BO
    attrDict["Q3879405"]=Q3879405
    attrDict["Q3879405BO"]=Q3879405BO
    attrDict["Q3879406"]=Q3879406
    attrDict["Q3879406BO"]=Q3879406BO
    attrDict["Q3879407"]=Q3879407
    attrDict["Q3879407BO"]=Q3879407BO