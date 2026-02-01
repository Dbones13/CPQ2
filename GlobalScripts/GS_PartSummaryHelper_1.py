import math
from GS_PartSummaryHelper import cal16k, cal10k

def getFloat(Var):
	if Var:
		return float(Var)
	return 0

def FDM_HartIP_License(product):
	HS4096=HS2048=HS1024=HS0512=HS0256=HS0128=HS0064=HS0032=HS0016=0
	partdict={}
	if product.Attr('FDM_HART_IP_Server_DevicePoint_License').Allowed:
		serLc = getFloat(product.Attr('FDM_HART_IP_Server_DevicePoint_License').GetValue())
		if serLc>4080 and serLc<=4096:
			HS4096=1
		Pcal=HS4096*4096
		Cal=(serLc-Pcal)
		if Cal >2032 and Cal<=2048:
			HS2048=1
		else:
			HS2048=math.floor(Cal/2048)
		Pcal=Pcal+(HS2048*2048)
		Cal=(serLc-Pcal)
		if Cal >1008 and Cal<=1024:
			HS1024=1
		else:
			HS1024=math.floor(Cal/1024)
		Pcal=Pcal+(HS1024*1024)
		Cal=(serLc-Pcal)
		if Cal >496 and Cal<=512:
			HS0512=1
		else:
			HS0512=math.floor(Cal/512)
		Pcal=Pcal+(HS0512*512)
		Cal=(serLc-Pcal)
		if Cal >240 and Cal<=256:
			HS0256=1
		else:
			HS0256=math.floor(Cal/256)
		Pcal=Pcal+(HS0256*256)
		Cal=(serLc-Pcal)
		if Cal >112 and Cal<=128:
			HS0128=1
		else:
			HS0128=math.floor(Cal/128)
		Pcal=Pcal+(HS0128*128)
		Cal=(serLc-Pcal)
		if Cal >48 and Cal<=64:
			HS0064=1
		else:
			HS0064=math.floor(Cal/64)
		Pcal=Pcal+(HS0064*64)
		Cal=(serLc-Pcal)
		if Cal >16 and Cal<=32:
			HS0032=1
		else:
			HS0032=math.floor(Cal/32)
		Pcal=Pcal+(HS0032*32)
		Cal=(serLc-Pcal)
		HS0016=math.ceil(Cal/16)
	partdict['HC-HS4096']=HS4096
	partdict['HC-HS2048']=HS2048
	partdict['HC-HS1024']=HS1024
	partdict['HC-HS0512']=HS0512
	partdict['HC-HS0256']=HS0256
	partdict['HC-HS0128']=HS0128
	partdict['HC-HS0064']=HS0064
	partdict['HC-HS0032']=HS0032
	partdict['HC-HS0016']=HS0016
	return partdict

def FDM_Namur_Licence(product):
	NDM010=NDM020=NDM030=NDM040=NDM050=NDM060=NDM070=NDM080=NDM090=NDM100=0
	partdict={}
	if product.Attr('FDM_NAMUR_Diagnostic_Custom_Model_Licenses').Allowed:
		NrLicense = getFloat(product.Attr('FDM_NAMUR_Diagnostic_Custom_Model_Licenses').GetValue())
		if NrLicense >0 and NrLicense<=10:
			NDM010=1
		elif NrLicense >10 and NrLicense<=20:
			NDM020=1
		elif NrLicense >20 and NrLicense<=30:
			NDM030=1
		elif NrLicense >30 and NrLicense<=40:
			NDM040=1
		elif NrLicense >40 and NrLicense<=50:
			NDM050=1
		elif NrLicense >50 and NrLicense<=60:
			NDM060=1
		elif NrLicense >60 and NrLicense<=70:
			NDM070=1
		elif NrLicense >70 and NrLicense<=80:
			NDM080=1
		elif NrLicense >80 and NrLicense<=90:
			NDM090=1
		elif NrLicense >90 and NrLicense<=100:
			NDM100=1
	partdict['HC-NDM010']=NDM010
	partdict['HC-NDM020']=NDM020
	partdict['HC-NDM030']=NDM030
	partdict['HC-NDM040']=NDM040
	partdict['HC-NDM050']=NDM050
	partdict['HC-NDM060']=NDM060
	partdict['HC-NDM070']=NDM070
	partdict['HC-NDM080']=NDM080
	partdict['HC-NDM090']=NDM090
	partdict['HC-NDM100']=NDM100
	return partdict

def FDM_OPC_UA_License(product):
	UA016K=UA8192=UA4096=UA2048=UA1024=UA0512=UA0256=UA0128=UA0064=UA0032=UA0016=0
	partdict={}
	if product.Attr('FDM_OPC_UA_Server_Tag_read-only_Licenses').Allowed:
		OPCLicense = getFloat(product.Attr('FDM_OPC_UA_Server_Tag_read-only_Licenses').GetValue())
		if OPCLicense >15984 and OPCLicense<=16000:
			UA016K=1
		Pcal=UA016K*16000
		Cal=(OPCLicense-Pcal)
		if Cal >8176 and Cal<=8192:
			UA8192=1
		else:
			UA8192=math.floor(Cal/8192)
		Pcal=Pcal+(UA8192*8192)
		Cal=(OPCLicense-Pcal)
		if Cal >4080 and Cal<=4096:
			UA4096=1
		else:
			UA4096=math.floor(Cal/4096)
		Pcal=Pcal+(UA4096*4096)
		Cal=(OPCLicense-Pcal)
		if Cal >2032 and Cal<=2048:
			UA2048=1
		else:
			UA2048=math.floor(Cal/2048)
		Pcal=Pcal+(UA2048*2048)
		Cal=(OPCLicense-Pcal)
		if Cal >1008 and Cal<=1024:
			UA1024=1
		else:
			UA1024=math.floor(Cal/1024)
		Pcal=Pcal+(UA1024*1024)
		Cal=(OPCLicense-Pcal)
		if Cal >496 and Cal<=512:
			UA0512=1
		else:
			UA0512=math.floor(Cal/512)
		Pcal=Pcal+(UA0512*512)
		Cal=(OPCLicense-Pcal)
		if Cal >240 and Cal<=256:
			UA0256=1
		else:
			UA0256=math.floor(Cal/256)
		Pcal=Pcal+(UA0256*256)
		Cal=(OPCLicense-Pcal)
		if Cal >112 and Cal<=128:
			UA0128=1
		else:
			UA0128=math.floor(Cal/128)
		Pcal=Pcal+(UA0128*128)
		Cal=(OPCLicense-Pcal)
		if Cal >48 and Cal<=64:
			UA0064=1
		else:
			UA0064=math.floor(Cal/64)
		Pcal=Pcal+(UA0064*64)
		Cal=(OPCLicense-Pcal)
		if Cal >16 and Cal<=32:
			UA0032=1
		else:
			UA0032=math.floor(Cal/32)
		Pcal=Pcal+(UA0032*32)
		Cal=(OPCLicense-Pcal)
		UA0016=math.ceil(Cal/16)
	partdict['HC-UA016K']=UA016K
	partdict['HC-UA8192']=UA8192
	partdict['HC-UA4096']=UA4096
	partdict['HC-UA2048']=UA2048
	partdict['HC-UA1024']=UA1024
	partdict['HC-UA0512']=UA0512
	partdict['HC-UA0256']=UA0256
	partdict['HC-UA0128']=UA0128
	partdict['HC-UA0064']=UA0064
	partdict['HC-UA0032']=UA0032
	partdict['HC-UA0016']=UA0016
	return partdict

def FDM_FF_License(product):
	FC0512=FC0256=FC0128=FC0064=FC0032=FC0016=0
	partdict={}
	if product.Attr('FDM_Devices_for_FF_Connector_Interface_License').Allowed:
		FFLicense = getFloat(product.Attr('FDM_Devices_for_FF_Connector_Interface_License').GetValue())
		if FFLicense >496 and FFLicense<=512:
			FC0512=1
		Pcal=FC0512*512
		Cal=(FFLicense-Pcal)
		if Cal >240 and Cal<=256:
			FC0256=1
		else:
			FC0256=math.floor(Cal/256)
		Pcal=Pcal+(FC0256*256)
		Cal=(FFLicense-Pcal)
		if Cal >112 and Cal<=128:
			FC0128=1
		else:
			FC0128=math.floor(Cal/128)
		Pcal=Pcal+(FC0128*128)
		Cal=(FFLicense-Pcal)
		if Cal >48 and Cal<=64:
			FC0064=1
		else:
			FC0064=math.floor(Cal/64)
		Pcal=Pcal+(FC0064*64)
		Cal=(FFLicense-Pcal)
		if Cal >16 and Cal<=32:
			FC0032=1
		else:
			FC0032=math.floor(Cal/32)
		Pcal=Pcal+(FC0032*32)
		Cal=(FFLicense-Pcal)
		FC0016=math.ceil(Cal/16)
	partdict['HC-FC0512']=FC0512
	partdict['HC-FC0256']=FC0256
	partdict['HC-FC0128']=FC0128
	partdict['HC-FC0064']=FC0064
	partdict['HC-FC0032']=FC0032
	partdict['HC-FC0016']=FC0016
	return partdict

def updateAttrDictWithCustomFDMUpgrade(product, attrValDict):
	l = getFloat(product.Attr("Attr_FDM_Upg1_TotalFDMClients").GetValue())
	attrValDict["FDM_Upgrade_Total_FDM_Client_Count"] = l
	if float(attrValDict["FDM_Upgrade_Total_FDM_Client_Count"]) > 0:
		attrValDict["FDM_Upgrade_Total_FDM_Client_Count_grt_0"] = 'True'
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
	if 1:
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
		serDevice = getFloat(product.Attr('Attr_FDM_Upg_devmanaged').GetValue())
		auditTrail = getFloat(product.Attr('Attr_FDM_Upg_AuditTrailDev').GetValue())
		FDMHartMulti = getFloat(product.Attr('Attr_FDM_Upg_HARTdevvendors').GetValue())
		EXserIOLic = getFloat(product.Attr('Attr_ExpServer_processI/Opoint').GetValue())
		PVSTLic = getFloat(product.Attr('Attr_PVST_HARTESD').GetValue())
		noOfExpTPSserver = getFloat(product.Attr('Attr_Experion/TPS_Servers_FDMInt').GetValue())
		noOfserNetLic = getFloat(product.Attr('Attr_ServerNetInterfaceLic').GetValue())
		noOfHartLic = getFloat(product.Attr('Attr_HWMUX_Net_MonitoringLic').GetValue())
		noOfRemoPC = getFloat(product.Attr('Attr_remPCs_FDMServerviaLAN').GetValue())
		fdmClients = getFloat(product.Attr('Attr_FDMUpg_FDMClients').GetValue())
		if (product.Attr("FDM_Upgrade_HART_Devices_Offline_Configuration_req").GetValue() == "Yes"):
			HC_OC0000 +=1
		if (product.Attr("FDM_Upgrade_Asset_Sentinel_integration_required").GetValue()=="Yes"):
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
		if(product.Attr("FDM_Upgrade_Audit_trail_file_required").GetValue() not in(" ",None, "No")):
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

		if(product.Attr("FDM_Upgrade_Is_Experion_Server_redundant_for_FDM").GetValue() not in(" ",None, "No")):
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
		if(product.Attr("FDM HART IP DOWNLINK LICENSE").GetValue() == "Yes"):
			HC_HIP000+=1
	d1=FDM_HartIP_License(product)
	attrValDict.update(d1)
	d2=FDM_Namur_Licence(product)
	attrValDict.update(d2)
	d3=FDM_OPC_UA_License(product)
	attrValDict.update(d3)
	d4=FDM_FF_License(product)
	attrValDict.update(d4)
	#FMD Upgrade Configuration-----------------------------------
	UPANR_FDM = 0
	q0=q1=q2=q3= 0
	if 1:
		if product.Attr("FDM_Upgrade_Do_you_want_to_upgrade_this_FDM").GetValue() == "Yes":
			q0 += 50
			#Trace.Write(row["FDM_Upgrade_Total_number_of_Server_Device_Points"])
			q1 += int(getFloat(product.Attr("Attr_FDM_Upg1ServerDevicePoints").GetValue()) * 0.22 + getFloat(product.Attr("Attr_FDMUpg1_AuditTrailDev").GetValue()) * 0.22)
			q2 += int(getFloat(product.Attr("Attr_FDMUpg1_RCIs_excExperion").GetValue())*31) + int(getFloat(product.Attr("Attr_FDM_Upg1_TotalFDMClients").GetValue())*17)
			q3 += int(getFloat(product.Attr("Attr_FDM_Upg_HdwareMultiplexer").GetValue()) *14) + int(getFloat(product.Attr("Attr_FDM_Upg_Multiplexer").GetValue()) *14)

	UPANR_FDM += (q0 + q1 + q2 + q3)  

	attrValDict["UPANR_FDM"]=UPANR_FDM
	if UPANR_FDM >0:
		attrValDict["UPGCLN_FDM"]=1
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

def updateAttrDictWithCustomFDMUpgrade2(product, attrValDict):
	l = getFloat(product.Attr("Attr_FDM_Upg1_TotalFDMClients").GetValue())
	attrValDict["FDM_Upgrade_2_Total_FDM_Client_Count"] = l
	if float(attrValDict["FDM_Upgrade_2_Total_FDM_Client_Count"]) > 0:
		attrValDict["FDM_Upgrade_2_Total_FDM_Client_Count_grt_0"] = 'True'
	HC_SM0000 = 0
	HC_OC0000 = 0
	HC_HM0000 = 0
	HC_HM0MX1 = 0
	HC_MM0000 = 0
	HC_MM0MX1 = 0
	HC_RI0000 = 0
	HC_RI0MX1 = 0
	HC_IS0000 = 0
	HC_CLNT00 = 0
	#server device
	HC_SV0016 = 0
	HC_SV0032 = 0
	HC_SV0064 = 0
	HC_SV0128 = 0
	HC_SV0256 = 0
	HC_SV0512 = 0
	HC_SV1024 = 0
	HC_SV2048 = 0
	HC_SV4096 = 0
	HC_SV8192 = 0
	HC_SV016K = 0
	#Audit trail
	HC_AT0016 = 0
	HC_AT0032 = 0
	HC_AT0064 = 0
	HC_AT0128 = 0
	HC_AT0256 = 0
	HC_AT0512 = 0
	HC_AT1024 = 0
	HC_AT2048 = 0
	HC_AT4096 = 0
	HC_AT8192 = 0
	HC_AT016K = 0
	#FDM HART Multiplexer
	HC_FH0016 = 0
	HC_FH0032 = 0
	HC_FH0064 = 0
	HC_FH0128 = 0
	HC_FH0256 = 0
	HC_FH0512 = 0
	HC_FH1024 = 0
	HC_FH2048 = 0
	#Experion Server process I/O point licenses
	EP_DPR100 = 0
	EP_DPR01K = 0
	EP_DPR02K = 0
	EP_DPR05K = 0
	EP_DPR10K = 0
	#Experion Server process I/O point Redundancy adder licenses
	EP_RPR100 = 0
	EP_RPR01K = 0
	EP_RPR02K = 0
	EP_RPR05K = 0
	EP_RPR10K = 0
	#PVST Planner Licenses
	HC_PV0032 = 0
	HC_PV0064 = 0
	HC_PV0128 = 0
	HC_PV0256 = 0
	HC_PV0512 = 0
	HC_PV1024 = 0
	#Downlink Liscene
	HC_HIP000 = 0
	if 1:
		FH0016 = 0
		FH0032 = 0
		FH0064 = 0
		FH0128 = 0
		FH0256 = 0
		FH0512 = 0
		FH1024 = 0
		FH2048 = 0
		PV0032 = 0
		PV0064 = 0
		PV0128 = 0
		PV0256 = 0
		PV0512 = 0
		PV1024 = 0
		serDevice = getFloat(product.Attr('Attr_FDM_Upg_devmanaged').GetValue())
		auditTrail = getFloat(product.Attr('Attr_FDM_Upg_AuditTrailDev').GetValue())
		FDMHartMulti = getFloat(product.Attr('Attr_FDM_Upg_HARTdevvendors').GetValue())
		EXserIOLic = getFloat(product.Attr('Attr_ExpServer_processI/Opoint').GetValue())
		PVSTLic = getFloat(product.Attr('Attr_PVST_HARTESD').GetValue())
		noOfExpTPSserver = getFloat(product.Attr('Attr_Experion/TPS_Servers_FDMInt').GetValue())
		noOfserNetLic = getFloat(product.Attr('Attr_ServerNetInterfaceLic').GetValue())
		noOfHartLic = getFloat(product.Attr('Attr_HWMUX_Net_MonitoringLic').GetValue())
		noOfRemoPC = getFloat(product.Attr('Attr_remPCs_FDMServerviaLAN').GetValue())
		fdmClients = getFloat(product.Attr('Attr_FDMUpg_FDMClients').GetValue())
		if (product.Attr("FDM_Upgrade_HART_Devices_Offline_Configuration_req").GetValue() == "Yes"):
			HC_OC0000 += 1
		if (product.Attr("FDM_Upgrade_Asset_Sentinel_integration_required").GetValue() == "Yes"):
			HC_IS0000 += 1
		HC_SM0000 += noOfExpTPSserver
		if noOfserNetLic < 25:
			HC_HM0000 += noOfserNetLic
		else:
			HC_HM0MX1 += 1
		if noOfHartLic < 25:
			HC_MM0000 += noOfHartLic
		else:
			HC_MM0MX1 += 1

		if noOfRemoPC < 25:
			HC_RI0000 += noOfRemoPC
		else:
			HC_RI0MX1 += 1
		HC_CLNT00 += fdmClients
		# FDM_Upgrade_2_Total_number_of_Server_Device_Points
		serRes = cal16k(serDevice)
		HC_SV0016 += serRes["016"]
		HC_SV0032 += serRes["032"]
		HC_SV0064 += serRes["064"]
		HC_SV0128 += serRes["128"]
		HC_SV0256 += serRes["256"]
		HC_SV0512 += serRes["512"]
		HC_SV1024 += serRes["1k"]
		HC_SV2048 += serRes["2k"]
		HC_SV4096 += serRes["4k"]
		HC_SV8192 += serRes["8k"]
		HC_SV016K += serRes["16k"]
		# Audit trail
		if (product.Attr("FDM_Upgrade_Audit_trail_file_required").GetValue() not in (" ", None, "No")):
			auditRes = cal16k(auditTrail)
			HC_AT0016 += auditRes["016"]
			HC_AT0032 += auditRes["032"]
			HC_AT0064 += auditRes["064"]
			HC_AT0128 += auditRes["128"]
			HC_AT0256 += auditRes["256"]
			HC_AT0512 += auditRes["512"]
			HC_AT1024 += auditRes["1k"]
			HC_AT2048 += auditRes["2k"]
			HC_AT4096 += auditRes["4k"]
			HC_AT8192 += auditRes["8k"]
			HC_AT016K += auditRes["16k"]
		# Fdm Hart
		if 2032 < FDMHartMulti <= 2048:
			Fh2048 = 1
		else:
			if 1008 < FDMHartMulti <= 1024:
				FH1024 = 1
			else:
				FH1024 = math.floor(FDMHartMulti / 1024)
				if 496 < FDMHartMulti <= 512 or 496 < (FDMHartMulti - FH1024 * 1024) <= 512:
					FH0512 = 1
				else:
					FH0512 = math.floor((FDMHartMulti - FH1024 * 1024) / 512)
					if 240 < FDMHartMulti <= 256 or 240 < (FDMHartMulti - FH1024 * 1024 - FH0512 * 512) <= 256:
						FH0256 = 1
					else:
						FH0256 = math.floor((FDMHartMulti - FH1024 * 1024 - FH0512 * 512) / 256)
						if 112 < FDMHartMulti <= 128 or 112 < (
								FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256) <= 128:
							FH0128 = 1
						else:
							FH0128 = math.floor(
								(FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256) / 128)
							if 48 < FDMHartMulti <= 64 or 48 < (
									FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256 - FH0128 * 128) <= 64:
								FH0064 = 1
							else:
								FH0064 = math.floor(
									(FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256 - FH0128 * 128) / 64)
								if 16 < FDMHartMulti <= 32 or 16 < (
										FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256 - FH0128 * 128 - FH0064 * 64) <= 32:
									FH0032 = 1
								else:
									FH0032 = math.floor((FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256 - FH0128 * 128 - FH0064 * 64) / 32)
									FH0016 = math.ceil((FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256 - FH0128 * 128 - FH0064 * 64 - FH0032 * 32) / 16)
		HC_FH0016 += FH0016
		HC_FH0032 += FH0032
		HC_FH0064 += FH0064
		HC_FH0128 += FH0128
		HC_FH0256 += FH0256
		HC_FH0512 += FH0512
		HC_FH1024 += FH1024
		HC_FH2048 += FH2048

		if (product.Attr("FDM_Upgrade_Is_Experion_Server_redundant_for_FDM").GetValue() not in (
				" ", None, "No")):
			# Experion Server process I/O point Redundancy adder licenses
			RedRes = cal10k(EXserIOLic)
			EP_RPR100 += RedRes["100"]
			EP_RPR01K += RedRes["1k"]
			EP_RPR02K += RedRes["2k"]
			EP_RPR05K += RedRes["5k"]
			EP_RPR10K += RedRes["10k"]
		# Experion Server process I/O point licenses
		IORes = cal10k(EXserIOLic)
		EP_DPR100 += IORes["100"]
		EP_DPR01K += IORes["1k"]
		EP_DPR02K += IORes["2k"]
		EP_DPR05K += IORes["5k"]
		EP_DPR10K += IORes["10k"]
		# PVST Planner Licenses
		if 992 < PVSTLic <= 1024:
			PV1024 = 1
		else:
			if 480 < PVSTLic <= 512:
				PV0512 = 1
			else:
				PV0512 = math.floor(PVSTLic / 512)
				if 224 < PVSTLic <= 256 or 224 < (PVSTLic - PV0512 * 512) <= 256:
					PV0256 = 1
				else:
					PV0256 = math.floor((PVSTLic - PV0512 * 512) / 256)
					if 96 < PVSTLic <= 128 or 96 < (PVSTLic - PV0512 * 512 - PV0256 * 256) <= 128:
						PV0128 += 1
					else:
						PV0128 = math.floor((PVSTLic - PV0512 * 512 - PV0256 * 256) / 128)
						if 32 < PVSTLic <= 64 or 32 < (PVSTLic - PV0512 * 512 - PV0256 * 256 - PV0128 * 128) <= 64:
							PV0064 = 1
						else:
							PV0064 = math.floor((PVSTLic - PV0512 * 512 - PV0256 * 256 - PV0128 * 128) / 64)
							PV0032 = math.ceil(
								(PVSTLic - PV0512 * 512 - PV0256 * 256 - PV0128 * 128 - PV0064 * 64) / 32)
		HC_PV0032 += PV0032
		HC_PV0064 += PV0064
		HC_PV0128 += PV0128
		HC_PV0256 += PV0256
		HC_PV0512 += PV0512
		HC_PV1024 += PV1024
		if (product.Attr("FDM HART IP DOWNLINK LICENSE").GetValue() == "Yes"):
			HC_HIP000 += 1
	d1=FDM_HartIP_License(product)
	attrValDict.update(d1)
	d2=FDM_Namur_Licence(product)
	attrValDict.update(d2)
	d3=FDM_OPC_UA_License(product)
	attrValDict.update(d3)
	d4=FDM_FF_License(product)
	attrValDict.update(d4)
	# FMD Upgrade Configuration-----------------------------------
	UPANR_FDM = 0
	q0 = q1 = q2 = q3 = 0
	if 1:
		if product.Attr("FDM_Upgrade_Do_you_want_to_upgrade_this_FDM").GetValue() == "Yes":
			q0 += 50
			# Trace.Write(row["FDM_Upgrade_Total_number_of_Server_Device_Points"])
			q1 += int(getFloat(product.Attr("Attr_FDM_Upg1ServerDevicePoints").GetValue()) * 0.22 + getFloat(
				product.Attr("Attr_FDMUpg1_AuditTrailDev").GetValue()) * 0.22)
			q2 += int(getFloat(product.Attr("Attr_FDMUpg1_RCIs_excExperion").GetValue()) * 31) + int(
				getFloat(product.Attr("Attr_FDM_Upg1_TotalFDMClients").GetValue()) * 17)
			q3 += int(getFloat(product.Attr("Attr_FDM_Upg_HdwareMultiplexer").GetValue()) * 14) + int(
				getFloat(product.Attr("Attr_FDM_Upg_Multiplexer").GetValue()) * 14)

	UPANR_FDM += (q0 + q1 + q2 + q3)

	attrValDict["UPANR_FDM_2"] = UPANR_FDM
	if UPANR_FDM >0:
		attrValDict["UPGCLN_FDM_2"]=1
	# -----------------------------------------------
	attrValDict["HC_SM0000_2"] = HC_SM0000
	attrValDict["HC_OC0000_2"] = HC_OC0000
	attrValDict["HC_HM0000_2"] = HC_HM0000
	attrValDict["HC_HM0MX1_2"] = HC_HM0MX1
	attrValDict["HC_MM0000_2"] = HC_MM0000
	attrValDict["HC_MM0MX1_2"] = HC_MM0MX1
	attrValDict["HC_RI0000_2"] = HC_RI0000
	attrValDict["HC_RI0MX1_2"] = HC_RI0MX1
	attrValDict["HC_IS0000_2"] = HC_IS0000
	attrValDict["HC_CLNT00_2"] = HC_CLNT00
	# server device
	attrValDict["HC_SV0016_2"]=HC_SV0016
	attrValDict["HC_SV0032_2"]=HC_SV0032
	attrValDict["HC_SV0064_2"]=HC_SV0064
	attrValDict["HC_SV0128_2"]=HC_SV0128
	attrValDict["HC_SV0256_2"]=HC_SV0256
	attrValDict["HC_SV0512_2"]=HC_SV0512
	attrValDict["HC_SV1024_2"]=HC_SV1024
	attrValDict["HC_SV2048_2"]=HC_SV2048
	attrValDict["HC_SV4096_2"]=HC_SV4096
	attrValDict["HC_SV8192_2"]=HC_SV8192
	attrValDict["HC_SV016K_2"]=HC_SV016K
	# Audit trail
	attrValDict["HC_AT0016_2"]=HC_AT0016
	attrValDict["HC_AT0032_2"]=HC_AT0032
	attrValDict["HC_AT0064_2"]=HC_AT0064
	attrValDict["HC_AT0128_2"]=HC_AT0128
	attrValDict["HC_AT0256_2"]=HC_AT0256
	attrValDict["HC_AT0512_2"]=HC_AT0512
	attrValDict["HC_AT1024_2"]=HC_AT1024
	attrValDict["HC_AT2048_2"]=HC_AT2048
	attrValDict["HC_AT4096_2"]=HC_AT4096
	attrValDict["HC_AT8192_2"]=HC_AT8192
	attrValDict["HC_AT016K_2"]=HC_AT016K
	#FDM HART Mutiplexer
	attrValDict["HC_FH0016_2"]=HC_FH0016
	attrValDict["HC_FH0032_2"]=HC_FH0032
	attrValDict["HC_FH0064_2"]=HC_FH0064
	attrValDict["HC_FH0128_2"]=HC_FH0128
	attrValDict["HC_FH0256_2"]=HC_FH0256
	attrValDict["HC_FH0512_2"]=HC_FH0512
	attrValDict["HC_FH1024_2"]=HC_FH1024
	attrValDict["HC_FH2048_2"]=HC_FH2048
	#Experion Server process I/O point licenses
	attrValDict["EP_DPR100_2"]=EP_DPR100
	attrValDict["EP_DPR01K_2"]=EP_DPR01K
	attrValDict["EP_DPR02K_2"]=EP_DPR02K
	attrValDict["EP_DPR05K_2"]=EP_DPR05K
	attrValDict["EP_DPR10K_2"]=EP_DPR10K
	#Experion Server process I/O point Redundancy adder licenses
	attrValDict["EP_RPR100_2"]=EP_RPR100
	attrValDict["EP_RPR01K_2"]=EP_RPR01K
	attrValDict["EP_RPR02K_2"]=EP_RPR02K
	attrValDict["EP_RPR05K_2"]=EP_RPR05K
	attrValDict["EP_RPR10K_2"]=EP_RPR10K
	#PVST Planner Licenses
	attrValDict["HC_PV0032_2"]=HC_PV0032
	attrValDict["HC_PV0064_2"]=HC_PV0064
	attrValDict["HC_PV0128_2"]=HC_PV0128
	attrValDict["HC_PV0256_2"]=HC_PV0256
	attrValDict["HC_PV0512_2"]=HC_PV0512
	attrValDict["HC_PV1024_2"]=HC_PV1024
	#Downlink Liscene
	attrValDict["HC_HIP000_2"]=HC_HIP000

def updateAttrDictWithCustomFDMUpgrade3(product, attrValDict):
	l = getFloat(product.Attr("Attr_FDM_Upg1_TotalFDMClients").GetValue())
	attrValDict["FDM_Upgrade_3_Total_FDM_Client_Count"] = l
	if float(attrValDict["FDM_Upgrade_3_Total_FDM_Client_Count"]) > 0:
		attrValDict["FDM_Upgrade_3_Total_FDM_Client_Count_grt_0"] = 'True'
	HC_SM0000 = 0
	HC_OC0000 = 0
	HC_HM0000 = 0
	HC_HM0MX1 = 0
	HC_MM0000 = 0
	HC_MM0MX1 = 0
	HC_RI0000 = 0
	HC_RI0MX1 = 0
	HC_IS0000 = 0
	HC_CLNT00 = 0
	#server device
	HC_SV0016 = 0
	HC_SV0032 = 0
	HC_SV0064 = 0
	HC_SV0128 = 0
	HC_SV0256 = 0
	HC_SV0512 = 0
	HC_SV1024 = 0
	HC_SV2048 = 0
	HC_SV4096 = 0
	HC_SV8192 = 0
	HC_SV016K = 0
	#Audit trail
	HC_AT0016 = 0
	HC_AT0032 = 0
	HC_AT0064 = 0
	HC_AT0128 = 0
	HC_AT0256 = 0
	HC_AT0512 = 0
	HC_AT1024 = 0
	HC_AT2048 = 0
	HC_AT4096 = 0
	HC_AT8192 = 0
	HC_AT016K = 0
	#FDM HART Multiplexer
	HC_FH0016 = 0
	HC_FH0032 = 0
	HC_FH0064 = 0
	HC_FH0128 = 0
	HC_FH0256 = 0
	HC_FH0512 = 0
	HC_FH1024 = 0
	HC_FH2048 = 0
	#Experion Server process I/O point licenses
	EP_DPR100 = 0
	EP_DPR01K = 0
	EP_DPR02K = 0
	EP_DPR05K = 0
	EP_DPR10K = 0
	#Experion Server process I/O point Redundancy adder licenses
	EP_RPR100 = 0
	EP_RPR01K = 0
	EP_RPR02K = 0
	EP_RPR05K = 0
	EP_RPR10K = 0
	#PVST Planner Licenses
	HC_PV0032 = 0
	HC_PV0064 = 0
	HC_PV0128 = 0
	HC_PV0256 = 0
	HC_PV0512 = 0
	HC_PV1024 = 0
	#Downlink Liscene
	HC_HIP000=0
	if 1:
		FH0016 = 0
		FH0032 = 0
		FH0064 = 0
		FH0128 = 0
		FH0256 = 0
		FH0512 = 0
		FH1024 = 0
		FH2048 = 0
		PV0032 = 0
		PV0064 = 0
		PV0128 = 0
		PV0256 = 0
		PV0512 = 0
		PV1024 = 0
		serDevice = getFloat(product.Attr('Attr_FDM_Upg_devmanaged').GetValue())
		auditTrail = getFloat(product.Attr('Attr_FDM_Upg_AuditTrailDev').GetValue())
		FDMHartMulti = getFloat(product.Attr('Attr_FDM_Upg_HARTdevvendors').GetValue())
		EXserIOLic = getFloat(product.Attr('Attr_ExpServer_processI/Opoint').GetValue())
		PVSTLic = getFloat(product.Attr('Attr_PVST_HARTESD').GetValue())
		noOfExpTPSserver = getFloat(product.Attr('Attr_Experion/TPS_Servers_FDMInt').GetValue())
		noOfserNetLic = getFloat(product.Attr('Attr_ServerNetInterfaceLic').GetValue())
		noOfHartLic = getFloat(product.Attr('Attr_HWMUX_Net_MonitoringLic').GetValue())
		noOfRemoPC = getFloat(product.Attr('Attr_remPCs_FDMServerviaLAN').GetValue())
		fdmClients = getFloat(product.Attr('Attr_FDMUpg_FDMClients').GetValue())
		if (product.Attr("FDM_Upgrade_HART_Devices_Offline_Configuration_req").GetValue() == "Yes"):
			HC_OC0000 += 1
		if (product.Attr("FDM_Upgrade_Asset_Sentinel_integration_required").GetValue() == "Yes"):
			HC_IS0000 += 1
		HC_SM0000 += noOfExpTPSserver
		if noOfserNetLic < 25:
			HC_HM0000 += noOfserNetLic
		else:
			HC_HM0MX1 += 1
		if noOfHartLic < 25:
			HC_MM0000 += noOfHartLic
		else:
			HC_MM0MX1 += 1

		if noOfRemoPC < 25:
			HC_RI0000 += noOfRemoPC
		else:
			HC_RI0MX1 += 1
		HC_CLNT00 += fdmClients
		# FDM_Upgrade_3_Total_number_of_Server_Device_Points
		serRes = cal16k(serDevice)
		HC_SV0016 += serRes["016"]
		HC_SV0032 += serRes["032"]
		HC_SV0064 += serRes["064"]
		HC_SV0128 += serRes["128"]
		HC_SV0256 += serRes["256"]
		HC_SV0512 += serRes["512"]
		HC_SV1024 += serRes["1k"]
		HC_SV2048 += serRes["2k"]
		HC_SV4096 += serRes["4k"]
		HC_SV8192 += serRes["8k"]
		HC_SV016K += serRes["16k"]
		# Audit trail
		if (product.Attr("FDM_Upgrade_Audit_trail_file_required").GetValue() not in (" ", None, "No")):
			auditRes = cal16k(auditTrail)
			HC_AT0016 += auditRes["016"]
			HC_AT0032 += auditRes["032"]
			HC_AT0064 += auditRes["064"]
			HC_AT0128 += auditRes["128"]
			HC_AT0256 += auditRes["256"]
			HC_AT0512 += auditRes["512"]
			HC_AT1024 += auditRes["1k"]
			HC_AT2048 += auditRes["2k"]
			HC_AT4096 += auditRes["4k"]
			HC_AT8192 += auditRes["8k"]
			HC_AT016K += auditRes["16k"]
		# Fdm Hart
		if 2032 < FDMHartMulti <= 2048:
			Fh2048 = 1
		else:
			if 1008 < FDMHartMulti <= 1024:
				FH1024 = 1
			else:
				FH1024 = math.floor(FDMHartMulti / 1024)
				if 496 < FDMHartMulti <= 512 or 496 < (FDMHartMulti - FH1024 * 1024) <= 512:
					FH0512 = 1
				else:
					FH0512 = math.floor((FDMHartMulti - FH1024 * 1024) / 512)
					if 240 < FDMHartMulti <= 256 or 240 < (FDMHartMulti - FH1024 * 1024 - FH0512 * 512) <= 256:
						FH0256 = 1
					else:
						FH0256 = math.floor((FDMHartMulti - FH1024 * 1024 - FH0512 * 512) / 256)
						if 112 < FDMHartMulti <= 128 or 112 < (
								FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256) <= 128:
							FH0128 = 1
						else:
							FH0128 = math.floor(
								(FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256) / 128)
							if 48 < FDMHartMulti <= 64 or 48 < (
									FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256 - FH0128 * 128) <= 64:
								FH0064 = 1
							else:
								FH0064 = math.floor(
									(FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256 - FH0128 * 128) / 64)
								if 16 < FDMHartMulti <= 32 or 16 < (
										FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256 - FH0128 * 128 - FH0064 * 64) <= 32:
									FH0032 = 1
								else:
									FH0032 = math.floor((FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256 - FH0128 * 128 - FH0064 * 64) / 32)
									FH0016 = math.ceil((FDMHartMulti - FH1024 * 1024 - FH0512 * 512 - FH0256 * 256 - FH0128 * 128 - FH0064 * 64 - FH0032 * 32) / 16)
		HC_FH0016 += FH0016
		HC_FH0032 += FH0032
		HC_FH0064 += FH0064
		HC_FH0128 += FH0128
		HC_FH0256 += FH0256
		HC_FH0512 += FH0512
		HC_FH1024 += FH1024
		HC_FH2048 += FH2048

		if (product.Attr("FDM_Upgrade_Is_Experion_Server_redundant_for_FDM").GetValue() not in (
				" ", None, "No")):
			# Experion Server process I/O point Redundancy adder licenses
			RedRes = cal10k(EXserIOLic)
			EP_RPR100 += RedRes["100"]
			EP_RPR01K += RedRes["1k"]
			EP_RPR02K += RedRes["2k"]
			EP_RPR05K += RedRes["5k"]
			EP_RPR10K += RedRes["10k"]
		# Experion Server process I/O point licenses
		IORes = cal10k(EXserIOLic)
		EP_DPR100 += IORes["100"]
		EP_DPR01K += IORes["1k"]
		EP_DPR02K += IORes["2k"]
		EP_DPR05K += IORes["5k"]
		EP_DPR10K += IORes["10k"]
		# PVST Planner Licenses
		if 992 < PVSTLic <= 1024:
			PV1024 = 1
		else:
			if 480 < PVSTLic <= 512:
				PV0512 = 1
			else:
				PV0512 = math.floor(PVSTLic / 512)
				if 224 < PVSTLic <= 256 or 224 < (PVSTLic - PV0512 * 512) <= 256:
					PV0256 = 1
				else:
					PV0256 = math.floor((PVSTLic - PV0512 * 512) / 256)
					if 96 < PVSTLic <= 128 or 96 < (PVSTLic - PV0512 * 512 - PV0256 * 256) <= 128:
						PV0128 += 1
					else:
						PV0128 = math.floor((PVSTLic - PV0512 * 512 - PV0256 * 256) / 128)
						if 32 < PVSTLic <= 64 or 32 < (PVSTLic - PV0512 * 512 - PV0256 * 256 - PV0128 * 128) <= 64:
							PV0064 = 1
						else:
							PV0064 = math.floor((PVSTLic - PV0512 * 512 - PV0256 * 256 - PV0128 * 128) / 64)
							PV0032 = math.ceil(
								(PVSTLic - PV0512 * 512 - PV0256 * 256 - PV0128 * 128 - PV0064 * 64) / 32)
		HC_PV0032 += PV0032
		HC_PV0064 += PV0064
		HC_PV0128 += PV0128
		HC_PV0256 += PV0256
		HC_PV0512 += PV0512
		HC_PV1024 += PV1024
		if (product.Attr("FDM HART IP DOWNLINK LICENSE").GetValue() == "Yes"):
			HC_HIP000 += 1
	d1=FDM_HartIP_License(product)
	attrValDict.update(d1)
	d2=FDM_Namur_Licence(product)
	attrValDict.update(d2)
	d3=FDM_OPC_UA_License(product)
	attrValDict.update(d3)
	d4=FDM_FF_License(product)
	attrValDict.update(d4)
	# FMD Upgrade Configuration-----------------------------------
	UPANR_FDM = 0
	q0 = q1 = q2 = q3 = 0
	if 1:
		if product.Attr("FDM_Upgrade_Do_you_want_to_upgrade_this_FDM").GetValue() == "Yes":
			q0 += 50
			# Trace.Write(row["FDM_Upgrade_Total_number_of_Server_Device_Points"])
			q1 += int(getFloat(product.Attr("Attr_FDM_Upg1ServerDevicePoints").GetValue()) * 0.22 + getFloat(
				product.Attr("Attr_FDMUpg1_AuditTrailDev").GetValue()) * 0.22)
			q2 += int(getFloat(product.Attr("Attr_FDMUpg1_RCIs_excExperion").GetValue()) * 31) + int(
				getFloat(product.Attr("Attr_FDM_Upg1_TotalFDMClients").GetValue()) * 17)
			q3 += int(getFloat(product.Attr("Attr_FDM_Upg_HdwareMultiplexer").GetValue()) * 14) + int(
				getFloat(product.Attr("Attr_FDM_Upg_Multiplexer").GetValue()) * 14)

	UPANR_FDM += (q0 + q1 + q2 + q3)

	attrValDict["UPANR_FDM_3"] = UPANR_FDM
	if UPANR_FDM >0:
		attrValDict["UPGCLN_FDM_3"]=1
	# -----------------------------------------------
	attrValDict["HC_SM0000_3"] = HC_SM0000
	attrValDict["HC_OC0000_3"] = HC_OC0000
	attrValDict["HC_HM0000_3"]=HC_HM0000
	attrValDict["HC_HM0MX1_3"]=HC_HM0MX1
	attrValDict["HC_MM0000_3"]=HC_MM0000
	attrValDict["HC_MM0MX1_3"]=HC_MM0MX1
	attrValDict["HC_RI0000_3"]=HC_RI0000
	attrValDict["HC_RI0MX1_3"]=HC_RI0MX1
	attrValDict["HC_IS0000_3"]=HC_IS0000
	attrValDict["HC_CLNT00_3"]=HC_CLNT00
	#server device
	attrValDict["HC_SV0016_3"]=HC_SV0016
	attrValDict["HC_SV0032_3"]=HC_SV0032
	attrValDict["HC_SV0064_3"]=HC_SV0064
	attrValDict["HC_SV0128_3"]=HC_SV0128
	attrValDict["HC_SV0256_3"]=HC_SV0256
	attrValDict["HC_SV0512_3"]=HC_SV0512
	attrValDict["HC_SV1024_3"]=HC_SV1024
	attrValDict["HC_SV2048_3"]=HC_SV2048
	attrValDict["HC_SV4096_3"]=HC_SV4096
	attrValDict["HC_SV8192_3"]=HC_SV8192
	attrValDict["HC_SV016K_3"]=HC_SV016K
	#Audit trail
	attrValDict["HC_AT0016_3"]=HC_AT0016
	attrValDict["HC_AT0032_3"]=HC_AT0032
	attrValDict["HC_AT0064_3"]=HC_AT0064
	attrValDict["HC_AT0128_3"]=HC_AT0128
	attrValDict["HC_AT0256_3"]=HC_AT0256
	attrValDict["HC_AT0512_3"]=HC_AT0512
	attrValDict["HC_AT1024_3"]=HC_AT1024
	attrValDict["HC_AT2048_3"]=HC_AT2048
	attrValDict["HC_AT4096_3"]=HC_AT4096
	attrValDict["HC_AT8192_3"]=HC_AT8192
	attrValDict["HC_AT016K_3"]=HC_AT016K
	#FDM HART Mutiplexer
	attrValDict["HC_FH0016_3"]=HC_FH0016
	attrValDict["HC_FH0032_3"]=HC_FH0032
	attrValDict["HC_FH0064_3"]=HC_FH0064
	attrValDict["HC_FH0128_3"]=HC_FH0128
	attrValDict["HC_FH0256_3"]=HC_FH0256
	attrValDict["HC_FH0512_3"]=HC_FH0512
	attrValDict["HC_FH1024_3"]=HC_FH1024
	attrValDict["HC_FH2048_3"]=HC_FH2048
	#Experion Server process I/O point licenses
	attrValDict["EP_DPR100_3"]=EP_DPR100
	attrValDict["EP_DPR01K_3"]=EP_DPR01K
	attrValDict["EP_DPR02K_3"]=EP_DPR02K
	attrValDict["EP_DPR05K_3"]=EP_DPR05K
	attrValDict["EP_DPR10K_3"]=EP_DPR10K
	#Experion Server process I/O point Redundancy adder licenses
	attrValDict["EP_RPR100_3"]=EP_RPR100
	attrValDict["EP_RPR01K_3"]=EP_RPR01K
	attrValDict["EP_RPR02K_3"]=EP_RPR02K
	attrValDict["EP_RPR05K_3"]=EP_RPR05K
	attrValDict["EP_RPR10K_3"]=EP_RPR10K
	#PVST Planner Licenses
	attrValDict["HC_PV0032_3"]=HC_PV0032
	attrValDict["HC_PV0064_3"]=HC_PV0064
	attrValDict["HC_PV0128_3"]=HC_PV0128
	attrValDict["HC_PV0256_3"]=HC_PV0256
	attrValDict["HC_PV0512_3"]=HC_PV0512
	attrValDict["HC_PV1024_3"]=HC_PV1024
	#Downlink Liscene
	attrValDict["HC_HIP000_3"]=HC_HIP000