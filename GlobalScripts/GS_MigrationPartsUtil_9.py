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


def populateWriteInsCBBCtoC300(product):
	writeInData = dict()
	msid= product.Attr('Migration_MSID_Choices').GetValue()
	sysNumber= product.Attr('Migration_MSID_System_Number').GetValue()
	area = msid +" - "+ sysNumber
	thirdPartyCost = 0
	thirdPartyPrice = 0
	writeInData["Write-in Third Party Hardware Misc"] = [str(thirdPartyPrice), str(thirdPartyCost), "", area]
	con = getContainer(product, "CB_EC_Third_party_items_Cont")
	for row in con.Rows:
		writeInData[row["WriteInProduct"]] = [row["Price"] if row["Price"] else "0", row["Cost"] if row["Cost"] else "0",row["ExtendedDescription"], area]
	productContainer = product.GetContainerByName("MSID_Product_Container")
	productRow = productContainer.Rows.GetByColumnName("Product Name", "CB-EC Upgrade to C300-UHIO")
	prod = productRow.Product
	con = prod.GetContainerByName("WriteInProduct")
	con.Clear()
	for wi, wiData in writeInData.items():
		if (wiData[0] and getFloat(wiData[0])) or (wiData[1] and getFloat(wiData[1])):
			row = con.Rows.GetByColumnName("WriteInProducts", wi)
			row = con.AddNewRow()
			#if not row:
				#row = con.AddNewRow()
			row.Product.Attr("Selected_WriteIn").AssignValue(wi)
			row.Product.Attr("Price").AssignValue(wiData[0])
			row.Product.Attr("Cost").AssignValue(wiData[1])
			row.Product.Attr("Area").AssignValue(wiData[3])
			row.Product.Attr("ItemQuantity").AssignValue("1")
			row.Product.Attr("Extended Description").AssignValue(wiData[2])
			row.Product.ApplyRules()
			row.ApplyProductChanges()
			row.Calculate()
	con.Calculate()

def updateAttrDictWithCustomFDMUpgrade2(product, attrValDict):
	l = 0
	con = getContainer(product, "FDM_Upgrade_2_Configuration")
	for row in con.Rows:
		l = getFloat(row["FDM_Upgrade_2_Total_FDM_Clients"])
	attrValDict["FDM_Upgrade_2_Total_FDM_Client_Count"] = float(l)
	if float(attrValDict["FDM_Upgrade_2_Total_FDM_Client_Count"]) > 0:
		attrValDict["FDM_Upgrade_2_Total_FDM_Client_Count_grt_0"] = 'True'
	con1 = getContainer(product, 'FDM_Upgrade_2_Additional_Configuration')
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
	for row in con1.Rows:
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
		serDevice = getFloat(row['FDM_Upgrade_2_How_many_devices_will_be_managed'])
		auditTrail = getFloat(row['FDM_Upgrade_2_Number_of_Audit_Trail_Devices'])
		FDMHartMulti = getFloat(row['FDM_Upgrade_2_Number_of_HART_devices_from_device_vendors'])
		EXserIOLic = getFloat(row['FDM_Upgrade_2_Number_of_Experion_Server_process_IO_point_licenses'])
		PVSTLic = getFloat(row['FDM_Upgrade_2_Number_of_PVST_Planner_Licenses_for_supported_HART_ESD_Devices'])
		noOfExpTPSserver = getFloat(row['FDM_Upgrade_2_Number_of_Experion_TPS_Servers_for_FDM_Integration'])
		noOfserNetLic = getFloat(row['FDM_Upgrade_2_Number_of_Server_Network_Interface_Licenses_Add'])
		noOfHartLic = getFloat(row['FDM_Upgrade_2_Number_of_HART_Hardware_MUX_Network_Monitoring_Licenses'])
		noOfRemoPC = getFloat(row['FDM_Upgrade_2_Number_of_remote_PCs_connecting_to_FDM_Serve_ via_LAN'])
		fdmClients = getFloat(row['FDM_Upgrade_2_Number_of_FDM_Clients'])
		if (row["FDM_Upgrade_2_HART_Devices_Offline_Configuration_required"] == "Yes"):
			HC_OC0000 += 1
		if (row["FDM_Upgrade_2_Asset_Sentinel_integration_required"] == "Yes"):
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
		if (row["FDM_Upgrade_2_Audit_trail_file_required"] not in (" ", None, "No")):
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

		if (row["FDM_Upgrade_2_Is_Experion_Server_redundant_for_FDM_Multiplexer_Monitoring"] not in (
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
		if (row["FDM 2 HART IP DOWNLINK LICENSE"] == "Yes"):
			HC_HIP000 += 1
	# FMD Upgrade Configuration-----------------------------------
	UPANR_FDM = 0
	q0 = q1 = q2 = q3 = 0
	for row in con.Rows:
		if row["FDM_Upgrade_2_Do_you_want_to_upgrade_this_FDM"] == "Yes":
			q0 += 50
			q1 += int(getFloat(row["FDM_Upgrade_2_Total_number_of_Server_Device_Points"]) * 0.22 + getFloat(
				row["FDM_Upgrade_2_Total_number_of_Audit_Trail_Devices"]) * 0.22)
			q2 += int(getFloat(row["FDM_Upgrade_2_Total_RCIs_excluding_Experion_PKS_Server_Interfaces"]) * 31) + int(
				getFloat(row["FDM_Upgrade_2_Total_FDM_Clients"]) * 17)
			q3 += int(getFloat(row["FDM_Upgrade_2_Total_Server_Hardware_Multiplexer_Licenses"]) * 14) + int(
				getFloat(row["FDM_Upgrade_2_Total_Multiplexer_Monitoring_Network_Licenses"]) * 14)

	UPANR_FDM += (q0 + q1 + q2 + q3)

	attrValDict["UPANR_FDM_2"] = UPANR_FDM
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
	l = 0
	con = getContainer(product, "FDM_Upgrade_3_Configuration")
	for row in con.Rows:
		l = getFloat(row["FDM_Upgrade_3_Total_FDM_Clients"])
	attrValDict["FDM_Upgrade_3_Total_FDM_Client_Count"] = float(l)
	if float(attrValDict["FDM_Upgrade_3_Total_FDM_Client_Count"]) > 0:
		attrValDict["FDM_Upgrade_3_Total_FDM_Client_Count_grt_0"] = 'True'
	con1 = getContainer(product, 'FDM_Upgrade_3_Additional_Configuration')
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
	for row in con1.Rows:
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
		serDevice = getFloat(row['FDM_Upgrade_3_How_many_devices_will_be_managed'])
		auditTrail = getFloat(row['FDM_Upgrade_3_Number_of_Audit_Trail_Devices'])
		FDMHartMulti = getFloat(row['FDM_Upgrade_3_Number_of_HART_devices_from_device_vendors'])
		EXserIOLic = getFloat(row['FDM_Upgrade_3_Number_of_Experion_Server_process_IO_point_licenses'])
		PVSTLic = getFloat(row['FDM_Upgrade_3_Number_of_PVST_Planner_Licenses_for_supported_HART_ESD_Devices'])
		noOfExpTPSserver = getFloat(row['FDM_Upgrade_3_Number_of_Experion_TPS_Servers_for_FDM_Integration'])
		noOfserNetLic = getFloat(row['FDM_Upgrade_3_Number_of_Server_Network_Interface_Licenses_Add'])
		noOfHartLic = getFloat(row['FDM_Upgrade_3_Number_of_HART_Hardware_MUX_Network_Monitoring_Licenses'])
		noOfRemoPC = getFloat(row['FDM_Upgrade_3_Number_of_remote_PCs_connecting_to_FDM_Serve_ via_LAN'])
		fdmClients = getFloat(row['FDM_Upgrade_3_Number_of_FDM_Clients'])
		if (row["FDM_Upgrade_3_HART_Devices_Offline_Configuration_required"] == "Yes"):
			HC_OC0000 += 1
		if (row["FDM_Upgrade_3_Asset_Sentinel_integration_required"] == "Yes"):
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
		if (row["FDM_Upgrade_3_Audit_trail_file_required"] not in (" ", None, "No")):
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

		if (row["FDM_Upgrade_3_Is_Experion_Server_redundant_for_FDM_Multiplexer_Monitoring"] not in (
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
		if (row["FDM 3 HART IP DOWNLINK LICENSE"] == "Yes"):
			HC_HIP000 += 1
	# FMD Upgrade Configuration-----------------------------------
	UPANR_FDM = 0
	q0 = q1 = q2 = q3 = 0
	for row in con.Rows:
		if row["FDM_Upgrade_3_Do_you_want_to_upgrade_this_FDM"] == "Yes":
			q0 += 50
			q1 += int(getFloat(row["FDM_Upgrade_3_Total_number_of_Server_Device_Points"]) * 0.22 + getFloat(
				row["FDM_Upgrade_3_Total_number_of_Audit_Trail_Devices"]) * 0.22)
			q2 += int(getFloat(row["FDM_Upgrade_3_Total_RCIs_excluding_Experion_PKS_Server_Interfaces"]) * 31) + int(
				getFloat(row["FDM_Upgrade_3_Total_FDM_Clients"]) * 17)
			q3 += int(getFloat(row["FDM_Upgrade_3_Total_Server_Hardware_Multiplexer_Licenses"]) * 14) + int(
				getFloat(row["FDM_Upgrade_3_Total_Multiplexer_Monitoring_Network_Licenses"]) * 14)

	UPANR_FDM += (q0 + q1 + q2 + q3)

	attrValDict["UPANR_FDM_3"] = UPANR_FDM
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