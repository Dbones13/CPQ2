conNames_map_hci = {
		'PHD_Labor': [
			"HCI_PHD_EngineeringLabour", 
			"HCI_PHD_ProjectManagement", 
			"HCI_PHD_ProjectManagement2",
			"HCI_PHD_AdditionalDeliverables"
		],
		'Uniformance_Insight_Labor': [
			"HCI_PHD_EngineeringLabour", 
			"HCI_PHD_ProjectManagement", 
			"HCI_PHD_ProjectManagement2",
			"HCI_PHD_AdditionalDeliverables"
		],
		'AFM_Labor': [
			"HCI_PHD_ProjectManagement", 
			"HCI_PHD_ProjectManagement2",
			"HCI_PHD_AdditionalDeliverables"
		]
	}

hci_materials_list = SqlHelper.GetList("SELECT Labor, Service_Material FROM CT_HCI_PHD_LABORMATERIAL")
service_material_dict = {hci.Labor: hci.Service_Material for hci in hci_materials_list}
CT_container=SqlHelper.GetList("SELECT * from CT_Container_Information")

def getFloat(val):
	if val:
		return round(float(val),2)
	return 0.0
def rowtotal(row):
	Split1=getFloat(row["FO Eng 1 % Split"])
	Split2=getFloat(row["FO Eng 2 % Split"])
	Split3=getFloat(row["FO Eng % Split"])
	Total_split_hrs = 0.0
	if row["Final Hrs"] not in ('',"0"):
		Split1_hrs = round(getFloat(row["Final Hrs"]) * (Split1) / 100) if str(Split1) != '0' else 0.0
		Split2_hrs = round(getFloat(row["Final Hrs"]) * (Split2) / 100) if str(Split2) != '0' else 0.0
		Split3_hrs = round(getFloat(row["Final Hrs"]) * (Split3) / 100) if str(Split3) != '0' else 0.0
		Total_split_hrs=Split1_hrs+Split2_hrs+Split3_hrs
		# Trace.Write("Total_split"+str(Total_split_hrs))
	Total_split = Split1+Split2+Split3
	return Total_split_hrs
def getWriteInProductType(quote):
	writeInProductType = dict()
	partNumberList = []
	for item in quote.Items:
		if item.IsOptional or (item.AsMainItem and len(list(item.AsMainItem.Children))):
			continue
		if item.ProductTypeName == 'Write-In':
			partNumberList.append(item.PartNumber)
	if len(partNumberList) > 0:
		strPartNubmers = ",".join(["'{0}'".format(x) for x in partNumberList])
		resProductType = SqlHelper.GetList("SELECT Product,ProductCategory FROM WriteInProducts WHERE Product in ({})".format(strPartNubmers))
		if resProductType:
			for row in resProductType:
				writeInProductType[row.Product] = row.ProductCategory
	return writeInProductType
def getDeliverableMappingDict(key, isGES):
	key ="EHPM HART IO" if key == "EHPM_HART_IO" else key
	query = (
		"select * from LSS_DELIVERABLES_MAPPING where Product_Module = '{}'"
		" and (SAP_Network_Name != 'LSS GES Activities' and SAP_Network_Name NOT LIKE 'PAS%')"
	).format(key)
	queryADC = (
		"select * from LSS_DELIVERABLES_MAPPING where Product_Module = 'Additional Custom Deliverables' and (SAP_Network_Name != 'LSS GES Activities' and SAP_Network_Name NOT LIKE 'PAS%')")
	if isGES :
		query = (
		"select * from LSS_DELIVERABLES_MAPPING where Product_Module = '{}'"
		" and (SAP_Network_Name = 'LSS GES Activities' and SAP_Network_Name NOT LIKE 'PAS%')"
	).format(key)
		queryADC = ("select * from LSS_DELIVERABLES_MAPPING where Product_Module ='Additional Custom Deliverables'  and (SAP_Network_Name = 'LSS GES Activities' and SAP_Network_Name NOT LIKE 'PAS%')")
	res = SqlHelper.GetList(query)
	res2 = SqlHelper.GetList(queryADC)
	dataDict = dict()
	ADCDict = dict()
	for r in res:
		dataDict[r.UI_Deliverables] = [
			r.SAP_Network_Name,
			r.SAP_Execution_Deliverable_Name,
		]
	for r in res2:
		ADCDict[r.UI_Deliverables] = [
			r.SAP_Network_Name,
			r.SAP_Execution_Deliverable_Name,
		]
	return dataDict, ADCDict
def getDeliverableMappingDict_PRJT(key, isGES, quote):
	lob = quote.GetCustomField('Booking LOB').Content if key in ['UOC','C300 System'] else 'PAS'
	other_lob = 'LSS' if lob == 'PAS' else 'PAS'
	query = ("select SAP_Network_Name,SAP_Execution_Deliverable_Name,UI_Deliverables from LSS_DELIVERABLES_MAPPING where Product_Module = '{}' and (SAP_Network_Name != '{} GES Activities' and SAP_Network_Name NOT LIKE '{}%')").format(key,lob,other_lob)
	queryADC = ("select SAP_Network_Name,SAP_Execution_Deliverable_Name,UI_Deliverables from LSS_DELIVERABLES_MAPPING where Product_Module = 'Additional Custom Deliverables' and (SAP_Network_Name != '{} GES Activities' and SAP_Network_Name NOT LIKE '{}%')".format(lob,other_lob))
	if isGES :
		query = ("select SAP_Network_Name,SAP_Execution_Deliverable_Name,UI_Deliverables from LSS_DELIVERABLES_MAPPING where Product_Module = '{}' and (SAP_Network_Name = '{} GES Activities' and SAP_Network_Name NOT LIKE '{}%')").format(key,lob,other_lob)
		queryADC = ("select SAP_Network_Name,SAP_Execution_Deliverable_Name,UI_Deliverables from LSS_DELIVERABLES_MAPPING where Product_Module ='Additional Custom Deliverables' and (SAP_Network_Name = '{} GES Activities' and SAP_Network_Name NOT LIKE '{}%')".format(lob,other_lob))
	res = SqlHelper.GetList(query)
	res2 = SqlHelper.GetList(queryADC)
	dataDict = dict()
	ADCDict = dict()
	for r in res:
		#dataDict[r.UI_Deliverables] =[r.SAP_Network_Name,r.SAP_Execution_Deliverable_Name,]
		a=[r.SAP_Network_Name,r.SAP_Execution_Deliverable_Name,]
		if dataDict.get(r.UI_Deliverables):
			dataDict[r.UI_Deliverables].append(a)
		else:
			dataDict[r.UI_Deliverables]=a
	for r in res2:
		#ADCDict[r.UI_Deliverables]=[r.SAP_Network_Name,r.SAP_Execution_Deliverable_Name,]
		b=[r.SAP_Network_Name,r.SAP_Execution_Deliverable_Name,]
		if ADCDict.get(r.UI_Deliverables):
			ADCDict[r.UI_Deliverables].append(b)
		else:
			ADCDict[r.UI_Deliverables]=b
	return dataDict, ADCDict

def getDeliverableMappingDict_Winest(key, isGES, quote, overlaps):
	query = ("select SAP_Network_Name,SAP_Execution_Deliverable_Name,UI_Deliverables from LSS_DELIVERABLES_MAPPING where Product_Module = 'Winest Labor Import' and SAP_Network_Name NOT LIKE '%GES Activities'")
	if isGES :
		query = ("select SAP_Network_Name,SAP_Execution_Deliverable_Name,UI_Deliverables from LSS_DELIVERABLES_MAPPING where Product_Module = 'Winest Labor Import' and SAP_Network_Name LIKE '%GES Activities'")
	res = SqlHelper.GetList(query)
	dataDict = dict()
	for r in res:
		if r.UI_Deliverables in overlaps:
			prefix = str(r.SAP_Network_Name).split(" ",1)[0]
			lobDict = dict()
			lobDict[prefix] = [r.SAP_Network_Name, r.SAP_Execution_Deliverable_Name]
			if dataDict.get(r.UI_Deliverables):
				(dataDict[r.UI_Deliverables]).update(lobDict)
			else:
				dataDict[r.UI_Deliverables] = lobDict
			dataDict[r.UI_Deliverables] = dataDict[r.UI_Deliverables]
		else:
			dataDict[r.UI_Deliverables] = [r.SAP_Network_Name, r.SAP_Execution_Deliverable_Name]
	return dataDict

def updateNetworkDataDict(item,networkDataDict, chinaDataDict, indiaDataDict,quote):
	groupingKey = "QI_ProductLine" if quote.GetCustomField('Booking Country').Content not in ['china','india','taiwan','hong kong'] else "QI_PLSG"
	networkName, executionName = "LSS Engineering Services", "Engineering Services"
	executionData = networkDataDict.get(networkName, dict())
	partsData = executionData.get(executionName, dict())
	plData = partsData.get(item[groupingKey].Value, dict())
	plData["hrs"] = plData.get("hrs", 0) + float(item.Quantity)
	plData["listPrice"] = plData.get("listPrice", 0) + float(
		item.ExtendedListPrice
	)
	plData["quoteSellPrice"] = plData.get("quoteSellPrice", 0) + float(
		item.ExtendedAmount
	)
	plData["cost"] = plData.get("cost", 0) + float(item.ExtendedCost)
	chinaData = chinaDataDict.get(item[groupingKey].Value)
	if chinaData:
		plData.update(chinaData)
	indiaData = indiaDataDict.get(item[groupingKey].Value)
	if indiaData:
		plData.update(indiaData)
	partsData[item[groupingKey].Value] = plData
	executionData[executionName] = partsData
	networkDataDict[networkName] = executionData
def getLabourConData(msid, plDict, srvModulePriceMap,networkDataDict,isGES, chinaDataDict, indiaDataDict):
	conNames = {
		"OPM": "MSID_Labor_OPM_Engineering",
		"LCN": "MSID_Labor_LCN_One_Time_Upgrade_Engineering",
		"EBR": "MSID_Labor_EBR_Con",
		"ELCN": "MSID_Labor_ELCN_Con",
		"Orion Console": "MSID_Labor_Orion_Console_Con",
		"EHPM/EHPMX/ C300PM" : "MSID_Labor_EHPM_C300PM_Con",
		"TPS_to_EXP": "MSID_Labor_TPS_TO_EXPERION_Con",
		"TCMI": "MSID_Labor_TCMI_Con",
		"C200 Migration": "MSID_Labor_C200_Migration_Con",
		"EHPM_HART_IO": "MSID_Labor_EHPM_HART_IO_Con",
		"CB_EC_Upgrade_to_C300_UHIO": "MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con",
		"FSC to SM":"MSID_Labor_FSC_to_SM_con",
		"FSC to SM Audit": "MSID_Labor_FSC_to_SM_audit_Con",
		"FDM Upgrade":"MSID_Labor_FDM_Upgrade_Con",
		"LM_ELMM_ControlEdge_PLC":"MSID_Labor_LM_to_ELMM_Con",
		"xPM to C300 Migration":"MSID_Labor_xPM_to_C300_Migration_Con",
		"CD Actuator I-F Upgrade": "MSID_Labor_CD_Actuator_con",
		"Graphics Migration": "MSID_Labor_Graphics_Migration_con",
		"XP10 Actuator Upgrade": "MSID_Labor_XP10_Actuator_Upgrade_con",
		"Project Management": "MSID_Labor_Project_Management",
		"Generic System Migration 1": "MSID_Labor_Generic_System1_Cont",
		"Generic System Migration 2": "MSID_Labor_Generic_System2_Cont",
		"Generic System Migration 3": "MSID_Labor_Generic_System3_Cont",
		"Generic System Migration 4": "MSID_Labor_Generic_System4_Cont",
		"Generic System Migration 5": "MSID_Labor_Generic_System5_Cont",
		"3rd Party PLC to ControlEdge PLC/UOC": "3rd_Party_PLC_UOC_Labor",
		"QCS RAE Upgrade":"MSID_Labor_QCS_RAE_Upgrade_con",
		"CWS RAE Upgrade":"MSID_Labor_CWS_RAE_Upgrade_con",
		"TPA/PMD Migration":"MSID_Labor_TPA_con",
		"FSC to SM IO Migration":"MSID_Labor_FSCtoSM_IO_con",
		"FSC to SM IO Audit": "MSID_Labor_FSC_to_SM_IO_Audit_Con",
		# for Extending Logic to generate Migration Project - Excel Pull for Labor Document -- Boya YashwanthKumar : CXCPQ-60198 :start
		"ELEPIU ControlEdge RTU Migration Engineering":"MSID_Labor_ELEPIU_con",
		# for Extending Logic to generate Migration Project - Excel Pull for Labor Document -- Boya YashwanthKumar : CXCPQ-60198 :end
		"Virtualization System":"MSID_Labor_Virtualization_con",
        "Trace Software":"Trace_Software_Labor_con",
		}
	for key, conName in conNames.items():
		if key != "C200 Migration":
			delMapDict, adcMapDict = getDeliverableMappingDict(key, isGES)
		else:
			if msid.ProductName == 'MSID_New':
				for msid1 in msid.Children:
					if msid1.ProductName == "C200 Migration":
						if msid1.SelectedAttributes.GetContainerByName('C200_Migration_Scenario_Cont'):
							migrationScenarioCon = msid1.SelectedAttributes.GetContainerByName('C200_Migration_Scenario_Cont').Rows
							for row in migrationScenarioCon:
								migrationScenario = row['C200_Select_the_Migration_Scenario']
								break
							if migrationScenario in ['C200 to C300','']:
								delMapDict,adcMapDict = getDeliverableMappingDict("C200 C300 Migration", isGES)
							elif migrationScenario == 'C200 to ControlEdge UOC':
								delMapDict, adcMapDict = getDeliverableMappingDict(key, isGES)
						break
			else:
				if msid.SelectedAttributes.GetContainerByName('C200_Migration_Scenario_Cont'):
					migrationScenarioCon = msid.SelectedAttributes.GetContainerByName('C200_Migration_Scenario_Cont').Rows
					for row in migrationScenarioCon:
						migrationScenario = row['C200_Select_the_Migration_Scenario']
						break
					if migrationScenario in ['C200 to C300','']:
						delMapDict,adcMapDict = getDeliverableMappingDict("C200 C300 Migration", isGES)
					elif migrationScenario == 'C200 to ControlEdge UOC':
						delMapDict, adcMapDict = getDeliverableMappingDict(key, isGES)
		con = msid.SelectedAttributes.GetContainerByName(conName)
		if not con:
			continue
		for row in con.Rows:
			splitPer = row['FO_Eng_Percentage_Split']
			cost = row["Regional_Cost"]
			listPrice = row["FO_ListPrice"]
			partNumber = row["FO_Eng"]
			if isGES:
				splitPer = row['GES_Eng_Percentage_Split']
				cost = row["GES_Regional_Cost"]
				listPrice = row["GES_ListPrice"]
				partNumber = row["GES_Eng"]
			if not partNumber or not row["Final_Hrs"] or not getFloat(row["Final_Hrs"]) or getFloat(splitPer) <= 0:
				continue
			hrs = round((getFloat(row["Final_Hrs"])* getFloat(splitPer))/100)
			if hrs <1:
				continue;
			if row["Standard Deliverable selection"]:
				networkName, executionName = adcMapDict.get(row["Standard Deliverable selection"],("Unassigned Execution Deliverable","Unassigned Execution Deliverable") )
			else:
				networkName, executionName = delMapDict.get(row["Deliverable"],("Unassigned Execution Deliverable","Unassigned Execution Deliverable") )
			executionData = networkDataDict.get(networkName, dict())
			partsData = executionData.get(executionName, dict())
			# Trace.Write("-pldict-"+str(plDict))
			if partNumber in plDict:
				plData = partsData.get(plDict[partNumber], dict())
				plData["hrs"] = plData.get("hrs", 0) + getFloat(hrs)
				plData["listPrice"] = plData.get("listPrice", 0) + getFloat(
					listPrice
				)
				if key not in ("Generic System Migration 1","Generic System Migration 2","Generic System Migration 3","Generic System Migration 4","Generic System Migration 5"):
					# Trace.Write("-key--"+str(key)+"-partNumber--"+str(partNumber)+"-hrs-"+str(hrs))
					quoteSellPrice = srvModulePriceMap.get((key, partNumber), 0) * getFloat(hrs)
					# Trace.Write("-srvModulePriceMap-"+str(srvModulePriceMap))
					# Trace.Write("--quoteSellPrice-"+str(quoteSellPrice))
				else:
					quoteSellPrice = srvModulePriceMap.get(("Generic System Migration", partNumber), 0) * getFloat(
						hrs
					) 
				plData["quoteSellPrice"] = plData.get("quoteSellPrice", 0) + quoteSellPrice
				plData["cost"] = plData.get("cost", 0) + getFloat(cost)
				chinaData = chinaDataDict.get(plDict[partNumber])
				if chinaData:
					plData.update(chinaData)
				indiaData = indiaDataDict.get(plDict[partNumber])
				if indiaData:
					plData.update(indiaData)
				partsData[plDict[partNumber]] = plData
				executionData[executionName] = partsData
				networkDataDict[networkName] = executionData
				# Trace.Write("-networkDataDictnetworkDataDict-"+str(networkDataDict))
	#log(networkDataDict)
def partnumber_data(networkDataDict,networkName_ges,executionName_ges,partNumber,plDict,listPrice,hrs,chinaDataDict,indiaDataDict,cost,key,srvModulePriceMap):
	executionData = networkDataDict.get(networkName_ges, dict())
	# Trace.Write('partNumber=='+str(partNumber))
	# Trace.Write('executionData=='+str(executionData))
	partsData = executionData.get(executionName_ges, dict())
	plData = partsData.get(plDict[partNumber], dict())
	plData["hrs"] = plData.get("hrs", 0) + getFloat(hrs)
	plData["listPrice"] = plData.get("listPrice", 0) + getFloat(listPrice)
	quoteSellPrice = srvModulePriceMap.get((key, partNumber), 0) * getFloat(hrs)
	plData["quoteSellPrice"] = plData.get("quoteSellPrice", 0) + quoteSellPrice
	plData["cost"] = plData.get("cost", 0) + getFloat(cost)
	chinaData = chinaDataDict.get(plDict[partNumber])
	if chinaData and plData:
			plData.update(chinaData)
	indiaData = indiaDataDict.get(plDict[partNumber])
	if indiaData and plData:
		plData.update(indiaData)
	partsData[plDict[partNumber]] = plData
	executionData[executionName_ges] = partsData
	networkDataDict[networkName_ges] = executionData
def nonges_data(networkDataDict,networkName,executionName,partNumber1_sd,plDict,listPrice,hrs,chinaDataDict,indiaDataDict,cost,key,srvModulePriceMap):
	executionData = networkDataDict.get(networkName, dict())
	partsData = executionData.get(executionName, dict())
	plData = partsData.get(plDict[partNumber1_sd], dict())
	hours_pldata = plData.get("hrs", 0) + getFloat(hrs)
	plData["hrs"] = hours_pldata
	plData["listPrice"] = plData.get("listPrice", 0) + getFloat(listPrice)
	quoteSellPrice = srvModulePriceMap.get((key, partNumber1_sd), 0) * getFloat(hrs)
	plData["quoteSellPrice"] = plData.get("quoteSellPrice", 0) + quoteSellPrice
	plData["cost"] = plData.get("cost", 0) + getFloat(cost)
	# Trace.Write('nonges_dataplData["cost"]==='+str(plData["cost"]))
	chinaData = chinaDataDict.get(plDict[partNumber1_sd])
	if chinaData and plData:
		plData.update(chinaData)
	indiaData = indiaDataDict.get(plDict[partNumber1_sd])
	if indiaData and plData:
		plData.update(indiaData)
	partsData[plDict[partNumber1_sd]] = plData
	executionData[executionName] = partsData
	networkDataDict[networkName] = executionData
def getLabourConData_PRJT(item,quote,plDict,networkDataDict,isGES,srvModulePriceMap,chinaDataDict, indiaDataDict):

	if CT_container:
		for i in CT_container:
			conNames=i.Container_Name
			product_name=i.Product_Name
			if item.ProductName in product_name:
				key=item.QuoteItemGuid
				container_Name=i.Container_Name
				item_partNumber=item.PartNumber
				if item_partNumber=="MasterLogic-200 Generic" or item_partNumber =="Experion LX Generic" or item_partNumber =="MasterLogic-50 Generic" or item.ProductName == 'Generic System':
					item_partNumber="Generic"
				delMapDict, adcMapDict = getDeliverableMappingDict_PRJT(item_partNumber, isGES, quote)
				con = item.SelectedAttributes.GetContainerByName(conNames)
				# if item_partNumber == 'Process Safety Workbench Engineering':
					# Trace.Write('conNames-='+str(conNames))
				if not con:
					continue
				for row in con.Rows:
					if "additional" in conNames.lower() or item_partNumber=='Measurement IQ':
						partNumber_col = "FO Eng"
					else:
						partNumber_col="FO Eng 1"
					partNumber=''
					splitter_1=row['FO Eng 1 % Split']
					splitter_2=row['FO Eng 2 % Split']
					splitter_add=row['FO Eng % Split']
					splitPer=getFloat(splitter_1)+getFloat(splitter_2)+getFloat(splitter_add)
					cost = row["FO_Regional_Cost"]
					listPrice = row["FO_ListPrice"]
					partNumber_1 = row[partNumber_col]
					partNumber_2 = row["FO Eng 2"]
					if isGES:
						# Trace.Write('row["GES Eng"]-='+str( row["GES Eng"]))
						splitPer = row['GES Eng % Split']
						cost = row["GES_Regional_Cost"]
						listPrice = row["GES_ListPrice"]
						partNumber = row["GES Eng"]
					# Trace.Write('partNumber_1='+str(partNumber_1))
					# Trace.Write('row["Final Hrs"]='+str(row["Final Hrs"]))
					# Trace.Write('splitPer='+str(splitPer))
					if not partNumber_1 or row["Final Hrs"]=='' or not row["Final Hrs"] or not getFloat(row["Final Hrs"]) or getFloat(splitPer) <= 0:
						continue
					if isGES:
						hrs = round((getFloat(row["Final Hrs"])* getFloat(splitPer))/100)
					else:
						hrs = rowtotal(row)
					# Trace.Write('hrs==='+str(hrs))
					if hrs <=0:
						continue
					''' For Measurement IQ Product start'''
					if container_Name=="MIQ Engineering Labor Container":
						Add_Del=delMapDict.get(row['Deliverable'])
						if len(Add_Del) > 2:
							val=(Add_Del[0])
							vall=(Add_Del[1])
							networkName,executionName=val,vall
						else:
							val=(Add_Del[0])
							vall=(Add_Del[1])
							networkName,executionName=val,vall
						if len(Add_Del) > 2 and Add_Del[2][0]=='PAS GES Activities':
							val=Add_Del[2][0]
							vall=(Add_Del[2][1])
							networkName_ges,executionName_ges=val,vall
						else:
							val=(Add_Del[0])
							vall=(Add_Del[1])
							networkName_ges,executionName_ges=val,vall
						if isGES == True:
							partnumber_data(networkDataDict,networkName_ges,executionName_ges,partNumber,plDict,listPrice,hrs,chinaDataDict,indiaDataDict,cost,key,srvModulePriceMap)
						partNumber1_sd=partNumber_1
						if partNumber_1:
							if not partNumber_1.startswith("H"):
								get_value=SqlHelper.GetFirst("SELECT VALUE_CODE FROM CT_VALUECODE_MAPPING WHERE Value = '{}'".format(partNumber_1))
								if get_value:
									partNumber1_sd = get_value.VALUE_CODE
						if partNumber_1.startswith("H"):
							partNumber1_sd=partNumber_1
						if partNumber1_sd in plDict:
							if isGES == False:
								nonges_data(networkDataDict,networkName,executionName,partNumber1_sd,plDict,listPrice,hrs,chinaDataDict,indiaDataDict,cost,key,srvModulePriceMap)
					''' For Measurement IQ Product start'''
					if row["Standard Deliverable"] or row['Standard Deliverable selection']:
						Add_Del = adcMapDict.get(row["Standard Deliverable"] ) or (adcMapDict.get(row["Standard Deliverable selection"] ))
						if len(Add_Del) > 2:
							val=(Add_Del[0])
							vall=(Add_Del[1])
							networkName,executionName=val,vall
						else:
							val=(Add_Del[0])
							vall=(Add_Del[1])
							networkName,executionName=val,vall
						if len(Add_Del) > 2 and Add_Del[2][0]=='PAS GES Activities':
							val=Add_Del[2][0]
							vall=(Add_Del[2][1])
							networkName_ges,executionName_ges=val,vall
						else:
							val=(Add_Del[0])
							vall=(Add_Del[1])
							networkName_ges,executionName_ges=val,vall
						if isGES == True:
							partnumber_data(networkDataDict,networkName_ges,executionName_ges,partNumber,plDict,listPrice,hrs,chinaDataDict,indiaDataDict,cost,key,srvModulePriceMap)
						partNumber1_sd=partNumber_1
						if partNumber_1:
							if not partNumber_1.startswith("H"):
								get_value=SqlHelper.GetFirst("SELECT VALUE_CODE FROM CT_VALUECODE_MAPPING WHERE Value = '{}'".format(partNumber_1))
								if get_value:
									partNumber1_sd = get_value.VALUE_CODE
						if partNumber_1.startswith("H"):
							partNumber1_sd=partNumber_1
						if partNumber1_sd in plDict:
							if isGES == False:
								nonges_data(networkDataDict,networkName,executionName,partNumber1_sd,plDict,listPrice,hrs,chinaDataDict,indiaDataDict,cost,key,srvModulePriceMap)
					else:
						deli= str(row["Deliverable"]).strip()
						AA = delMapDict.get(deli,("Unassigned Execution Deliverable","Unassigned Execution Deliverable"))
						if len(AA) > 2:
							val=(AA[0])
							vall=(AA[1])
							networkName,executionName=val,vall
						else:
							val=(AA[0])
							vall=(AA[1])
							networkName,executionName=val,vall
						if len(AA) > 2 and AA[2][0]=='PAS GES Activities':
							val=AA[2][0]
							vall=(AA[2][1])
							networkName_ges,executionName_ges=val,vall
						else:
							val=(AA[0])
							vall=(AA[1])
							networkName_ges,executionName_ges=val,vall
						if isGES == True:
							if partNumber in plDict:
								partnumber_data(networkDataDict,networkName_ges,executionName_ges,partNumber,plDict,listPrice,hrs,chinaDataDict,indiaDataDict,cost,key,srvModulePriceMap)
						partNumber1_vc=partNumber_1
						partNumber2_vc=partNumber_2
						if not partNumber_1.startswith("H"):
							get_value=SqlHelper.GetFirst("SELECT VALUE_CODE FROM CT_VALUECODE_MAPPING WHERE Value = '{}'".format(partNumber_1))
							if get_value:
								partNumber1_vc = get_value.VALUE_CODE
						if not partNumber_2.startswith("H"):
							if partNumber_2:
								get_value=SqlHelper.GetFirst("SELECT VALUE_CODE FROM CT_VALUECODE_MAPPING WHERE Value = '{}'".format(partNumber_2))
								if get_value:
									partNumber2_vc = get_value.VALUE_CODE
						if partNumber1_vc in plDict:
							if isGES == False:
								splitter_1=row['FO Eng 1 % Split']
								hrs = round((getFloat(row["Final Hrs"])* getFloat(splitter_1))/100)
								cost =getFloat(row['FO_Eng_1_Unit_Regional_Cost'])*getFloat(hrs)
								nonges_data(networkDataDict,networkName,executionName,partNumber1_vc,plDict,listPrice,hrs,chinaDataDict,indiaDataDict,cost,key,srvModulePriceMap)
						if partNumber2_vc in plDict:
							if isGES == False:
								splitter_2=row['FO Eng 2 % Split']
								hrs = round((getFloat(row["Final Hrs"])* getFloat(splitter_2))/100)
								cost =getFloat(row['FO_Eng_2_Unit_Regional_Cost'])*getFloat(hrs)
								nonges_data(networkDataDict,networkName,executionName,partNumber2_vc,plDict,listPrice,hrs,chinaDataDict,indiaDataDict,cost,key,srvModulePriceMap)

def getLabourConData_Winest(item,quote,plDict,networkDataDict,srvModulePriceMap,chinaDataDict, indiaDataDict):
	contList = ["Winest Labor Container", "Winest Additional Labor Container"]
	overlaps = ["LE Core & Duration Driven","PA Core & Duration Driven","PCO Core & Duration Driven","PM Core & Duration Driven","Travel Time","Create Test Protocols FAT-SAT-3rd Party","Internal & External training","Project Management","Engineering Services","Site Services"]
	for cont in contList:
		key = item.QuoteItemGuid
		item_partNumber = item.PartNumber
		delMapDict_GES = getDeliverableMappingDict_Winest(item_partNumber, True, quote, overlaps)
		delMapDict_NonGES = getDeliverableMappingDict_Winest(item_partNumber, False, quote, overlaps)
		con = item.SelectedAttributes.GetContainerByName(cont)
		if con:
			for row in con.Rows:
				cost = row["Regional_Cost"]
				listPrice = row["List_Price"]
				partNumber = row["Service Material"]
				finalHours = row["Final Hrs"]
				if partNumber == 'None' or getFloat(row["Final Hrs"]) <= 0:
					continue
				delMapDict = delMapDict_GES if "GES" in partNumber else delMapDict_NonGES
				deliverable = None
				if row["Deliverable"] in overlaps:
					if partNumber.startswith("HPS_SYS") or partNumber.startswith("HPS_GES"):
						deliverable = delMapDict.get(row["Deliverable"]).get("PAS")
						if not deliverable:
							deliverable = delMapDict.get(row["Deliverable"]).get("LSS")
					elif partNumber.startswith("SVC"):
						deliverable = delMapDict.get(row["Deliverable"]).get("LSS")
						if not deliverable:
							deliverable = delMapDict.get(row["Deliverable"]).get("PAS")
					elif partNumber.startswith("HPS_ADV") or partNumber.startswith("ADV_GES"):
						deliverable = delMapDict.get(row["Deliverable"]).get("AS")
				else:
					deliverable = delMapDict.get(row["Deliverable"])
				if deliverable:
					val = deliverable[0]
					vall = deliverable[1]
					networkName,executionName = val,vall
					partnumber_data(networkDataDict,networkName,executionName,partNumber,plDict,listPrice,finalHours,chinaDataDict,indiaDataDict,cost,key,srvModulePriceMap)

def getLabourConDataTrace(msid, plDict, srvModulePriceMap,networkDataDict,isGES, chinaDataDict, indiaDataDict):
	conNames = {
		"Trace Software": "Trace_Software_Labor_con",
		"Project Management": "Trace_Project_Management_Labor_con",
	}
	for key, conName in conNames.items():
		delMapDict, adcMapDict = getDeliverableMappingDict(key, isGES)

		con = msid.SelectedAttributes.GetContainerByName(conName)
		if not con:
			continue
		for row in con.Rows:
			splitPer = row['FO_Eng_Percentage_Split']
			cost = row["Regional_Cost"]
			listPrice = row["FO_ListPrice"]
			partNumber = row["FO_Eng"]
			if isGES:
				splitPer = row['GES_Eng_Percentage_Split']
				cost = row["GES_Regional_Cost"]
				listPrice = row["GES_ListPrice"]
				partNumber = row["GES_Eng"]
			if not partNumber or not row["Final_Hrs"] or not float(row["Final_Hrs"]) or float(splitPer) <= 0:
				continue
			hrs = round((getFloat(row["Final_Hrs"])* getFloat(splitPer))/100)
			if row["Standard Deliverable selection"]:
				networkName, executionName = adcMapDict.get(row["Standard Deliverable selection"],("Unassigned Execution Deliverable","Unassigned Execution Deliverable") )
			else:
				networkName, executionName = delMapDict.get(row["Deliverable"],("Unassigned Execution Deliverable","Unassigned Execution Deliverable") )
			executionData = networkDataDict.get(networkName, dict())
			partsData = executionData.get(executionName, dict())
			plData = partsData.get(plDict[partNumber], dict())
			plData["hrs"] = plData.get("hrs", 0) + getFloat(hrs)
			plData["listPrice"] = plData.get("listPrice", 0) + getFloat(
				listPrice
			)
			quoteSellPrice = srvModulePriceMap.get((key, partNumber), 0) * getFloat(
				hrs
			) 
			plData["quoteSellPrice"] = plData.get("quoteSellPrice", 0) + quoteSellPrice
			plData["cost"] = plData.get("cost", 0) + getFloat(cost)
			chinaData = chinaDataDict.get(plDict[partNumber])
			if chinaData:
				plData.update(chinaData)
			indiaData = indiaDataDict.get(plDict[partNumber])
			if indiaData:
				plData.update(indiaData)
			partsData[plDict[partNumber]] = plData
			executionData[executionName] = partsData
			networkDataDict[networkName] = executionData
	#log(networkDataDict)
def getChinaDataDict():
	results = SqlHelper.GetList("SELECT * FROM BOOKINGREPORT_CHINA")
	res = dict()
	for result in results:
		res[result.PLSG] = {
			"China_Supplier_1" : result.China_Supplier_1,
			"China_S1_Discount" : result.China_S1_Discount,
			"China_Supplier_2" : result.China_Supplier_2,
			"China_S2_Discount" : result.China_S2_Discount
		}
	return res
def getIndiaDataDict():
	results = SqlHelper.GetList("SELECT * FROM BOOKINGREPORT_INDIA")
	res = dict()
	for result in results:
		res[result.SG] = {
			"India_Discount_Percent" : result.Discount_Percent
		}
	return res

def getDeliverableMappingDictCyber(key):
	query = (
		"select UI_Deliverables,SAP_Network_Name,SAP_Execution_Deliverable_Name from LSS_DELIVERABLES_MAPPING where Product_Module = '{}'"
		" and (SAP_Network_Name != 'LSS GES Activities' and SAP_Network_Name NOT LIKE 'PAS%')"
	).format(key)
	res = SqlHelper.GetList(query)
	dataDict = dict()
	for r in res:
		dataDict[r.UI_Deliverables] = [
			r.SAP_Network_Name,
			r.SAP_Execution_Deliverable_Name,
		]
	# Trace.Write("-dataDict-"+str(dataDict))
	return dataDict

def getLabourConDataCyber(item, plDict, srvModulePriceMap,networkDataDict, chinaDataDict, indiaDataDict):
	conNames = {
		"Cyber Generic System":"Generic_System_Activities",
		"SMX": "AR_SMX_Activities",
		"ASSESSMENT": "AR_Assessment_Activities",
		"PCN": "AR_PCNH_Activities",
		"MSS": "AR_MSS_Activities",
		"CYBER_APP_CNTRL": "AR_CAC_Activities",
		"Project Management": "Cyber_Labor_Project_Management"
		}
	for key, conName in conNames.items():
		delMapDict  = getDeliverableMappingDictCyber(key)
		con = item.SelectedAttributes.GetContainerByName(conName)
		if not con:
			continue
		excluded_row = 'Identifier' if key != 'Project Management' else 'Deliverable'
		for row in con.Rows:
			if row[excluded_row] not in ['Total','On-Site','Off-Site']:
				if key != 'Project Management':
					cost = row["Regional_Cost"]
					listPrice = row["FO_List_Price"]
					partNumber = row["PartNumber"]
					hours_field = "Edit Hours"
				else:
					cost = row["Regional_Cost"]
					listPrice = row["FO_ListPrice"]
					partNumber = row["FO_Eng"]
					hours_field = "Final_Hrs"

				if not partNumber or not row[hours_field] or not float(row[hours_field]) :
					continue
				hrs = round(getFloat(row[hours_field]))
				if hrs<1:
					continue
				activity_key = "Activity" if key != 'Project Management' else "Deliverable"
				networkName, executionName = delMapDict.get(row[activity_key],("Unassigned Execution Deliverable","Unassigned Execution Deliverable") )
				executionData = networkDataDict.get(networkName, dict())
				partsData = executionData.get(executionName, dict())
				if partNumber in plDict:
					plData = partsData.get(plDict[partNumber], dict())
					plData["hrs"] = plData.get("hrs", 0) + getFloat(hrs)
					plData["listPrice"] = plData.get("listPrice", 0) + getFloat(listPrice)
					quoteSellPrice = srvModulePriceMap.get((key, partNumber), 0) * getFloat(hrs)
					plData["quoteSellPrice"] = plData.get("quoteSellPrice", 0) + quoteSellPrice
					plData["cost"] = plData.get("cost", 0) + getFloat(cost)
					chinaData = chinaDataDict.get(plDict[partNumber])
					if chinaData:
						plData.update(chinaData)
					indiaData = indiaDataDict.get(plDict[partNumber])
					if indiaData:
						plData.update(indiaData)
					partsData[plDict[partNumber]] = plData
					executionData[executionName] = partsData
					networkDataDict[networkName] = executionData

def getDeliverableMappingDicthcilabor(key):
	query = (
		"SELECT UI_Deliverables,SAP_Network_Name,SAP_Execution_Deliverable_Name FROM LSS_DELIVERABLES_MAPPING WHERE Product_Module = '{}' "
	).format(key)
	
	res = SqlHelper.GetList(query)
	dataDict = {}
	dataDictges = {}
	
	for r in res:
		target_dict = dataDictges if r.SAP_Network_Name == 'AS GES Activities' else dataDict
		target_dict[r.UI_Deliverables] = [r.SAP_Network_Name, r.SAP_Execution_Deliverable_Name]
	
	return dataDict, dataDictges

def process_containers(cont_name, con, key, plDict, srvModulePriceMap, networkDataDict, chinaDataDict, indiaDataDict, delMapDict, delMapDictges):
	for row in con.Rows:
		if cont_name == "AR_HCI_LABOR_CONTAINER":
			cost = row["TransferCost"]
			listPrice = row["TotalListPrice"]
			partNumber = row["LaborResource"]
			hours_field = "FinalHours"
		else:
			cost = row["Eng Total Regional Cost"]
			listPrice = row["Eng Total List Price"]
			partNumber = service_material_dict[row['Eng']] if row['Eng'] !='' and row['Eng'] != 'None' else ''
			hours_field = "Final Hrs"

		if not partNumber or not row[hours_field] or not float(row[hours_field]) :
			continue
		hrs = round(getFloat(row[hours_field]))
		if hrs<1:
			continue
		if 'GES' in partNumber:
			networkName, executionName = delMapDictges.get(row['Deliverable'],("Unassigned Execution Deliverable","Unassigned Execution Deliverable") )
		else:
			networkName, executionName = delMapDict.get(row['Deliverable'],("Unassigned Execution Deliverable","Unassigned Execution Deliverable") )
		executionData = networkDataDict.get(networkName, dict())
		partsData = executionData.get(executionName, dict())
		if partNumber in plDict:
			plData = partsData.get(plDict[partNumber], dict())
			plData["hrs"] = plData.get("hrs", 0) + getFloat(hrs)
			plData["listPrice"] = plData.get("listPrice", 0) + getFloat(listPrice)
			quoteSellPrice = srvModulePriceMap.get((key, partNumber), 0) * getFloat(hrs)
			plData["quoteSellPrice"] = plData.get("quoteSellPrice", 0) + quoteSellPrice
			plData["cost"] = plData.get("cost", 0) + getFloat(cost)
			chinaData = chinaDataDict.get(plDict[partNumber])
			if chinaData:
				plData.update(chinaData)
			indiaData = indiaDataDict.get(plDict[partNumber])
			if indiaData:
				plData.update(indiaData)
			partsData[plDict[partNumber]] = plData
			executionData[executionName] = partsData
			networkDataDict[networkName] = executionData

def getMigrationLaborData(quote, srvModulePriceMap,plDict):
	writeInProductTypes = getWriteInProductType(quote)
	chinaDataDict = getChinaDataDict()
	indiaDataDict = getIndiaDataDict()
	networkDataDict = {}
	product_N=[i.Product_Name for i in CT_container if CT_container]
	for item in quote.MainItems:
		if item.ProductName in product_N:
			getLabourConData_PRJT(item, quote, plDict, networkDataDict, False, srvModulePriceMap, chinaDataDict, indiaDataDict)
			getLabourConData_PRJT(item, quote, plDict, networkDataDict, True, srvModulePriceMap, chinaDataDict, indiaDataDict)
		elif item.PartNumber == "Migration":
			for msid in item.Children:
				getLabourConData(msid, plDict, srvModulePriceMap, networkDataDict, False, chinaDataDict, indiaDataDict)
				getLabourConData(msid, plDict, srvModulePriceMap, networkDataDict, True, chinaDataDict, indiaDataDict)
			continue
		elif item.ProductName == "Winest Labor Import":
			getLabourConData_Winest(item, quote, plDict, networkDataDict, srvModulePriceMap, chinaDataDict, indiaDataDict)
		elif item.PartNumber == "Trace Software" and quote.GetCustomField('R2Q_Save').Content=='':
			getLabourConDataTrace(item, plDict, srvModulePriceMap, networkDataDict, False, chinaDataDict, indiaDataDict)
			getLabourConDataTrace(item, plDict, srvModulePriceMap, networkDataDict, True, chinaDataDict, indiaDataDict)
			continue
		elif item.PartNumber == "CYBER":
			getLabourConDataCyber(item, plDict, srvModulePriceMap, networkDataDict, chinaDataDict, indiaDataDict)
			continue
		elif item.PartNumber == "HCI_LABOR":
			delMapDict,delMapDictges  = getDeliverableMappingDicthcilabor('Import')
			con = item.SelectedAttributes.GetContainerByName("AR_HCI_LABOR_CONTAINER")
			if con:
				process_containers("AR_HCI_LABOR_CONTAINER", con, "HCI_LABOR", plDict, srvModulePriceMap, networkDataDict, chinaDataDict, indiaDataDict, delMapDict, delMapDictges)
			continue
		elif item.PartNumber == "HCI_Labor_config":
			for child in item.Children:
				delMapDict,delMapDictges  = getDeliverableMappingDicthcilabor(child.PartNumber)
				for cont in conNames_map_hci.get(child.PartNumber):
					if cont == 'HCI_PHD_AdditionalDeliverables':
						delMapDict,delMapDictges  = getDeliverableMappingDicthcilabor('HCI Additional Custom Deliverable')
					con = child.SelectedAttributes.GetContainerByName(cont)
					if con:
						process_containers(cont, con, child.PartNumber, plDict, srvModulePriceMap, networkDataDict, chinaDataDict, indiaDataDict, delMapDict, delMapDictges)
			continue
		elif item.ParentItemGuid != "":
			continue
		elif item.ProductTypeName == "Honeywell Labor" and item.PartNumber not in ["HCI_LABOR","CYBER","HCI_Labor_config"]:
			updateNetworkDataDict(item, networkDataDict, chinaDataDict, indiaDataDict,quote)
			continue
		elif item.ProductTypeName == "Write-In" and writeInProductTypes.get(item.PartNumber) == "Honeywell Labor":
			updateNetworkDataDict(item, networkDataDict, chinaDataDict, indiaDataDict,quote)
			continue
	return networkDataDict