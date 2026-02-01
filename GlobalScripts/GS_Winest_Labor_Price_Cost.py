import GS_Labor_Utils
import GS_GetPriceFromCPS as cps

service_material_map =  {"HPS_GES_P335F_CN": "SYS GES HMI Eng-FO-CN", "HPS_GES_P350B_RO": "SYS GES Eng-BO-RO", "HPS_GES_P335B_UZ": "SYS GES HMI Eng-BO-UZ", "HPS_SYS_PM1_P220": "SYS PM-Assoc Proj Manager", "HPS_SYS_PM1_P210": "SYS PM-Sr Project Manager", "HPS_GES_P335B_EG": "SYS GES HMI Eng-BO-EG", "HPS_GES_P350B_IN": "SYS GES Eng-BO-IN", "HPS_GES_P350B_CN": "SYS GES Eng-BO-CN", "HPS_SYS_SII_P345": "SYS SII-Design Eng", "HPS_GES_P350B_EG": "SYS GES Eng-BO-EG", "HPS_SYS_SII_P305": "SYS SII-Lead Eng", "HPS_GES_P215F_IN": "SYS GES PM-FO-IN", "HPS_SYS_SSE_P300": "SYS SSE-Prin Proj Eng", "HPS_SYS_SSE_P310": "SYS SSE-Sr Design Eng", "HPS_SYS_SSE_P350": "SYS SSE-Eng", "HPS_SYS_IND_P305": "SYS IND-Lead Eng", "HPS_GES_P335F_RO": "SYS GES HMI Eng-FO-RO", "HPS_GES_P215F_CN": "SYS GES PM-FO-CN", "HPS_SYS_IND_P345": "SYS IND-Design Eng", "HPS_SYS_QCS_P350": "SYS QCS-Eng", "HPS_SYS_QCS_P300": "SYS QCS-Prin Proj Eng", "HPS_SYS_QCS_P310": "SYS QCS-Sr Design Eng", "HPS_GES_P335F_UZ": "SYS GES HMI Eng-FO-UZ", "HPS_GES_P350F_UZ": "SYS GES Eng-FO-UZ", "HPS_GES_P335F_EG": "SYS GES HMI Eng-FO-EG", "HPS_SYS_SHE_P300": "SYS SHE-Prin Proj Eng", "HPS_SYS_SHE_P310": "SYS SHE-Sr Design Eng", "HPS_SYS_SHE_P350": "SYS SHE-Eng", "HPS_SYS_FIE_P350": "SYS FIE-Eng", "HPS_SYS_FIE_P310": "SYS FIE-Sr Design Eng", "HPS_SYS_FIE_P300": "SYS FIE-Prin Proj Eng", "HPS_SYS_SSE_P305": "SYS SSE-Lead Eng", "HPS_SYS_SSE_P345": "SYS SSE-Design Eng", "HPS_SYS_IND_P310": "SYS IND-Sr Design Eng", "HPS_SYS_IND_P300": "SYS IND-Prin Proj Eng", "HPS_SYS_IND_P350": "SYS IND-Eng", "HPS_GES_P215B_RO": "SYS GES PM-BO-RO", "HPS_SYS_BPA_P345": "SYS BPA-Design Eng", "HPS_SYS_BPA_P305": "SYS BPA-Lead Eng", "HPS_SYS_HMI_P350": "SYS HMI-Eng", "HPS_SYS_HMI_P310": "SYS HMI-Sr Design Eng", "HPS_SYS_HMI_P300": "SYS HMI-Prin Proj Eng", "HPS_SYS_BPA_P350": "SYS BPA-Eng", "HPS_SYS_BPA_P310": "SYS BPA-Sr Design Eng", "HPS_SYS_BPA_P300": "SYS BPA-Prin Proj Eng", "HPS_GES_P350B_UZ": "SYS GES Eng-BO-UZ", "HPS_SYS_HMI_P345": "SYS HMI-Design Eng", "HPS_SYS_HMI_P305": "SYS HMI-Lead Eng", "HPS_SYS_FIE_P345": "SYS FIE-Design Eng", "HPS_SYS_PCA_P605": "SYS PCA-Sr. Specialist", "HPS_SYS_PCA_P615": "SYS PCA-Asst. Specialis", "HPS_GES_P215B_EG": "SYS GES PM-BO-EG", "HPS_SYS_FIE_P305": "SYS FIE-Lead Eng", "HPS_GES_P215F_RO": "SYS GES PM-FO-RO", "HPS_SYS_SNC_P345": "SYS SNC-Design Eng", "HPS_SYS_PM1_P700": "SYS PM-Sr Project Admin", "HPS_SYS_SNC_P305": "SYS SNC-Lead Eng", "HPS_SYS_PCA_P620": "SYS PCA-Document Controller", "HPS_SYS_PCA_P610": "SYS PCA-Specialist", "HPS_SYS_PCA_P600": "SYS PCA-Lead", "HPS_GES_P215B_UZ": "SYS GES PM-BO-UZ", "HPS_GES_P215F_EG": "SYS GES PM-FO-EG", "HPS_GES_P335B_IN": "SYS GES HMI Eng-BO-IN", "HPS_GES_P335B_CN": "SYS GES HMI Eng-BO-CN", "HPS_GES_P350F_RO": "SYS GES Eng-FO-RO", "HPS_SYS_LE1_P310": "SYS LE1-Sr Design Eng", "HPS_SYS_LE1_P300": "SYS LE1-Prin Proj Eng", "HPS_SYS_SHE_P305": "SYS SHE-Lead Eng", "HPS_SYS_LE1_P350": "SYS LE1-Eng", "HPS_SYS_SHE_P345": "SYS SHE-Design Eng", "HPS_SYS_QCS_P345": "SYS QCS-Design Eng", "HPS_SYS_QCS_P305": "SYS QCS-Lead Eng", "HPS_GES_P350F_IN": "SYS GES Eng-FO-IN", "HPS_SYS_PM1_P215": "SYS PM-Project Manager", "HPS_SYS_PM1_P205": "SYS PM-Program Manager", "HPS_SYS_LE1_P305": "SYS LE1-Lead Eng", "HPS_GES_P350F_CN": "SYS GES Eng-FO-CN", "HPS_SYS_LE1_P345": "SYS LE1-Design Eng", "HPS_SYS_SNC_P350": "SYS SNC-Eng", "HPS_SYS_SNC_P300": "SYS SNC-Prin Proj Eng", "HPS_SYS_SNC_P310": "SYS SNC-Sr Design Eng", "HPS_GES_P350F_EG": "SYS GES Eng-FO-EG", "HPS_GES_P215B_IN": "SYS GES PM-BO-IN", "HPS_SYS_SII_P350": "SYS SII-Eng", "HPS_GES_P335B_RO": "SYS GES HMI Eng-BO-RO", "HPS_GES_P215B_CN": "SYS GES PM-BO-CN", "HPS_SYS_SII_P300": "SYS SII-Prin Proj Eng", "HPS_SYS_SII_P310": "SYS SII-Sr Design Eng", "HPS_SYS_CPA_P345": "SYS CPA-Design Eng", "HPS_SYS_CPA_P305": "SYS CPA-Lead Eng", "HPS_GES_P215F_UZ": "SYS GES PM-FO-UZ", "HPS_SYS_CPA_P350": "SYS CPA-Eng", "HPS_SYS_CPA_P300": "SYS CPA-Prin Proj Eng", "HPS_SYS_CPA_P310": "SYS CPA-Sr Design Eng", "HPS_GES_P335F_IN": "SYS GES HMI Eng-FO-IN","None":"None","SVC-ECON-ST":"SVC-ECON-ST Consultant","SVC-ECON-ST-NC":"SVC-ECON-ST-NC Consultant","SVC-ESSS-ST":"SVC-ESSS-ST Site Support Spec","SVC-ESSS-ST-NC":"SVC-ESSS-ST-NC Site Support Spec","SVC-EAPS-ST":"SVC-EAPS-ST Applications Support","SVC-EAPS-ST-NC":"SVC-EAPS-ST-NC Applications Support","SVC-EST1-ST":"SVC-EST1-ST System Svc Tech ","SVC-EST1-ST-NC":"SVC-EST1-ST-NC System Svc Tech ","SVC-NCOS-ST":"SVC-NCOS-ST Cyber Sr Consultant","SVC-NSER-ST":"SVC-NSER-ST Network Security Eng","SVC-NMON-ST":"SVC-NMON-ST Svcs Sec Spec","SVC-NRSC-ST":"SVC-NRSC-ST Cyber Security MSS","SVC-PADM-ST":"SVC-PADM-ST Project Administration","SVC-PADM-ST-NC":"SVC-PADM-ST-NC Project Administration","SVC-PLC-ST":"SVC-PLC-ST PLC SYSTEM SVC TECH","SVC-PLC-ST-NC":"SVC-PLC-ST-NC PLC SYSTEM SVC TECH","SVC-PMGT-ST":"SVC-PMGT-ST Project Management","SVC-PMGT-ST-NC":"SVC-PMGT-ST-NC Project Management","SVC-QCON-ST":"SVC-QCON-ST Consultant","SVC-QCON-ST-NC":"SVC-QCON-ST-NC Consultant","SVC-QST2-ST":"SVC-QST2-ST System Svc Spec","SVC-QST2-ST-NC":"SVC-QST2-ST-NC System Svc Spec","SVC-QAPS-ST":"SVC-QAPS-ST Application Support","SVC-QAPS-ST-NC":"SVC-QAPS-ST-NC Application Support","SVC-QST1-ST":"SVC-QST1-ST System Svc Tech","SVC-QST1-ST-NC":"SVC-QST1-ST-NC System Svc Tech","SVC-TCON-ST":"SVC-TCON-ST Consultant","SVC-TCON-ST-NC":"SVC-TCON-ST-NC Consultant","SVC-TSSS-ST":"SVC-TSSS-ST Site Support Spec","SVC-TSSS-ST-NC":"SVC-TSSS-ST-NC Site Support Spec","SVC-TAPS-ST":"SVC-TAPS-ST Application Support","SVC-TAPS-ST-NC":"SVC-TAPS-ST-NC Application Support","SVC-TST1-ST":"SVC-TST1-ST System Svc Tech","SVC-TST1-ST-NC":"SVC-TST1-ST-NC System Svc Tech","SVC_GES_P350B_CN":"LSS GES Eng-BO-CN","SVC_GES_P350F_CN":"LSS GES Eng-FO-CN","SVC_GES_P335B_CN":"LSS GES HMI Eng-BO-CN","SVC_GES_P335F_CN":"LSS GES HMI Eng-FO-CN","SVC_GES_PLCB_CN":"LSS GES PLC Eng-BO-CN","SVC_GES_P215B_CN":"LSS GES PM-BO-CN","SVC_GES_P215F_CN":"LSS GES PM-FO-CN","SVC_GES_P350B_EG":"LSS GES Eng-BO-EG","SVC_GES_P350F_EG":"LSS GES Eng-FO-EG","SVC_GES_P335B_EG":"LSS GES HMI Eng-BO-EG","SVC_GES_P335F_EG":"LSS GES HMI Eng-FO-EG","SVC_GES_PLCB_EG":"LSS GES PLC Eng-BO-EG","SVC_GES_P215B_EG":"LSS GES PM-BO-EG","SVC_GES_P215F_EG":"LSS GES PM-FO-EG","SVC_GES_P350B_IN":"LSS GES Eng-BO-IN","SVC_GES_P350F_IN":"LSS GES Eng-FO-IN","SVC_GES_P335B_IN":"LSS GES HMI Eng-BO-IN","SVC_GES_P335F_IN":"LSS GES HMI Eng-FO-IN","SVC_GES_PLCB_IN":"LSS GES PLC Eng-BO-IN","SVC_GES_P215B_IN":"LSS GES PM-BO-IN","SVC_GES_P215F_IN":"LSS GES PM-FO-IN","SVC_GES_P350B_RO":"LSS GES Eng-BO-RO","SVC_GES_P350F_RO":"LSS GES Eng-FO-RO","SVC_GES_P335B_RO":"LSS GES HMI Eng-BO-RO","SVC_GES_P335F_RO":"LSS GES HMI Eng-FO-RO","SVC_GES_PLCB_RO":"LSS GES PLC Eng-BO-RO","SVC_GES_P215B_RO":"LSS GES PM-BO-RO","SVC_GES_P215F_RO":"LSS GES PM-FO-RO","SVC_GES_P350B_UZ":"LSS GES Eng-BO-UZ","SVC_GES_P350F_UZ":"LSS GES Eng-FO-UZ","SVC_GES_P335B_UZ":"LSS GES HMI Eng-BO-UZ","SVC_GES_P335F_UZ":"LSS GES HMI Eng-FO-UZ","SVC_GES_PLCB_UZ":"LSS GES PLC Eng-BO-UZ","SVC_GES_P215B_UZ":"LSS GES PM-BO-UZ","SVC_GES_P215F_UZ":"LSS GES PM-FO-UZ","HPS_ADV_AMS_P310":"ADV AMS Prin Engineer","HPS_ADV_AMS_P345":"ADV AMS Sr Engineer","HPS_ADV_AMS_P350":"ADV AMS Engineer","HPS_ADV_AMS_P505":"ADV AMS Technician","HPS_ADV_AMS_P401":"ADV AMS Prin Consultant","HPS_ADV_AMS_P405":"ADV AMS Sr Consultant","HPS_ADV_AMS_P410":"ADV AMS Consultant","HPS_ADV_APC_P310":"ADV APC Prin Engineer","HPS_ADV_APC_P345":"ADV APC Sr Engineer","HPS_ADV_APC_P350":"ADV APC Engineer","HPS_ADV_APC_P505":"ADV APC Technician","HPS_ADV_APC_P401":"ADV APC Prin Consultant","HPS_ADV_APC_P405":"ADV APC Sr Consultant","HPS_ADV_APC_P410":"ADV APC Consultant","HPS_ADV_ASM_P310":"ADV ASM Prin Engineer","HPS_ADV_ASM_P345":"ADV ASM Sr Engineer","HPS_ADV_ASM_P350":"ADV ASM Engineer","HPS_ADV_ASM_P505":"ADV ASM Technician","HPS_ADV_ASM_P401":"ADV ASM Prin Consultant","HPS_ADV_ASM_P405":"ADV ASM Sr Consultant","HPS_ADV_ASM_P410":"ADV ASM Consultant","HPS_ADV_BMA_P310":"ADV BMA Prin Engineer","HPS_ADV_BMA_P345":"ADV BMA Sr Engineer","HPS_ADV_BMA_P350":"ADV BMA Engineer","HPS_ADV_BMA_P505":"ADV BMA Technician","HPS_ADV_BMA_P401":"ADV BMA Prin Consultant","HPS_ADV_BMA_P405":"ADV BMA Sr Consultant","HPS_ADV_BMA_P410":"ADV BMA Consultant","HPS_ADV_COR_P310":"ADV COR Prin Engineer","HPS_ADV_COR_P345":"ADV COR Sr Engineer","HPS_ADV_COR_P350":"ADV COR Engineer","HPS_ADV_COR_P505":"ADV COR Technician","HPS_ADV_COR_P401":"ADV COR Prin Consultant","HPS_ADV_COR_P405":"ADV COR Sr Consultant","HPS_ADV_COR_P410":"ADV COR Consultant","HPS_ADV_ECL_P310":"ADV ECL Prin Engineer","HPS_ADV_ECL_P345":"ADV ECL Sr Engineer","HPS_ADV_ECL_P350":"ADV ECL Engineer","HPS_ADV_ECL_P505":"ADV ECL Technician","HPS_ADV_ECL_P401":"ADV ECL Prin Consultant","HPS_ADV_ECL_P405":"ADV ECL Sr Consultant","HPS_ADV_ECL_P410":"ADV ECL Consultant","HPS_ADV_MES_P310":"ADV MES Prin Engineer","HPS_ADV_MES_P345":"ADV MES Sr Engineer","HPS_ADV_MES_P350":"ADV MES Engineer","HPS_ADV_MES_P505":"ADV MES Technician","HPS_ADV_MES_P401":"ADV MES Prin Consultant","HPS_ADV_MES_P405":"ADV MES Sr Consultant","HPS_ADV_MES_P410":"ADV MES Consultant","HPS_ADV_OPM_P310":"ADV OPM Prin Engineer","HPS_ADV_OPM_P345":"ADV OPM Sr Engineer","HPS_ADV_OPM_P350":"ADV OPM Engineer","HPS_ADV_OPM_P505":"ADV OPM Technician","HPS_ADV_OPM_P401":"ADV OPM Prin Consultant","HPS_ADV_OPM_P405":"ADV OPM Sr Consultant","HPS_ADV_OPM_P410":"ADV OPM Consultant","HPS_ADV_OPT_P310":"ADV OPT Prin Engineer","HPS_ADV_OPT_P345":"ADV OPT Sr Engineer","HPS_ADV_OPT_P350":"ADV OPT Engineer","HPS_ADV_OPT_P505":"ADV OPT Technician","HPS_ADV_OPT_P401":"ADV OPT Prin Consultant","HPS_ADV_OPT_P405":"ADV OPT Sr Consultant","HPS_ADV_OPT_P410":"ADV OPT Consultant","HPS_ADV_PHD_P310":"ADV PHD Prin Engineer","HPS_ADV_PHD_P345":"ADV PHD Sr Engineer","HPS_ADV_PHD_P350":"ADV PHD Engineer","HPS_ADV_PHD_P505":"ADV PHD Technician","HPS_ADV_PHD_P401":"ADV PHD Prin Consultant","HPS_ADV_PHD_P405":"ADV PHD Sr Consultant","HPS_ADV_PHD_P410":"ADV PHD Consultant","HPS_ADV_PM1_P700":"ADV PM1 Project Admin","HPS_ADV_PM1_P210":"ADV PM1 Senior Project Mgr","HPS_ADV_PM1_P215":"ADV PM1 Project Mgr","HPS_ADV_SIM_P310":"ADV SIM Prin Engineer","HPS_ADV_SIM_P345":"ADV SIM Sr Engineer","HPS_ADV_SIM_P350":"ADV SIM Engineer","HPS_ADV_SIM_P505":"ADV SIM Technician","HPS_ADV_SIM_P401":"ADV SIM Prin Consultant","HPS_ADV_SIM_P405":"ADV SIM Sr Consultant","HPS_ADV_SIM_P410":"ADV SIM Consultant","ADV_GES_P310B_IN":"ADV GES Prin Eng-BO-IN","ADV_GES_P345B_IN":"ADV GES Sr Eng-BO-IN","ADV_GES_P350B_IN":"ADV GES Eng-1-BO-IN","ADV_GES_P335B_IN":"ADV GES Eng-BO-IN","ADV_GES_P215B_IN":"ADV GES PM-BO-IN","ADV_GES_P310B_CN":"ADV GES Prin Eng-BO-CN","ADV_GES_P345B_CN":"ADV GES Sr Eng-BO-CN","ADV_GES_P350B_CN":"ADV GES Eng-1-BO-CN","ADV_GES_P335B_CN":"ADV GES Eng-BO-CN","ADV_GES_P215B_CN":"ADV GES PM-BO-CN","ADV_GES_P310B_UZ":"ADV GES Prin Eng-BO-UZ","ADV_GES_P345B_UZ":"ADV GES Sr Eng-BO-UZ","ADV_GES_P350B_UZ":"ADV GES Eng-1-BO-UZ","ADV_GES_P335B_UZ":"ADV GES Eng-BO-UZ","ADV_GES_P215B_UZ":"ADV GES PM-BO-UZ"}
service_material_map2={v:k for k, v in service_material_map.items()}

def getYearPrice(power, partNumber, salesOrg, LOB, listPriceDict): #Needs the quote for the pricebook call
	query = "Select * from YOY_INFLATION_RATE where salesOrg = '{0}' and LOB = '{1}'".format(salesOrg,LOB)
	res = SqlHelper.GetFirst(query)
	price = listPriceDict.get(partNumber, 0)
	if power ==1 and res is not None:
		inflationRate1 = GS_Labor_Utils.getFloat(res.Inflation_Rate)
		price = GS_Labor_Utils.getFloat(price) * GS_Labor_Utils.getFloat((1 + inflationRate1 ))
	elif power == 2 and res is not None :
		inflationRate1 = GS_Labor_Utils.getFloat(res.Inflation_Rate)
		inflationRate2 = GS_Labor_Utils.getFloat(res.Inflation_Rate_Year2)
		price = GS_Labor_Utils.getFloat(price) * GS_Labor_Utils.getFloat((1 + inflationRate1 ))*GS_Labor_Utils.getFloat((1 + inflationRate2))
	elif power == 3 and res is not None:
		inflationRate1 = GS_Labor_Utils.getFloat(res.Inflation_Rate)
		inflationRate2 = GS_Labor_Utils.getFloat(res.Inflation_Rate_Year2)
		inflationRate3 = GS_Labor_Utils.getFloat(res.Inflation_Rate_Year3)
		price = GS_Labor_Utils.getFloat(price) * GS_Labor_Utils.getFloat((1 + inflationRate1 ))*GS_Labor_Utils.getFloat((1 + inflationRate2))*GS_Labor_Utils.getFloat((1 + inflationRate3))
	if price:
		return GS_Labor_Utils.getFloat(price)
	return 0.0

def populateListPrice(Quote, row, listPriceDict): #sets List Price
	#salesOrg = Quote.SelectedMarket.MarketCode.split('_')[0]
	salesOrg = Quote.GetCustomField('Sales Area').Content
	LOB = Quote.GetCustomField("Booking LOB").Content
	serviceMaterial = row["Service Material"]
	finalHours = GS_Labor_Utils.getFloat(row["Final Hrs"])

	currentYear = DateTime.Now.Year
	year_diff = int(row["Execution Year"]) - currentYear

	if finalHours != 0 and serviceMaterial != "None":
		unitListPrice = getYearPrice(year_diff, serviceMaterial, salesOrg, LOB, listPriceDict)
		totalListPrice = round((finalHours * unitListPrice), 2)
		row["Unit_List_Price"] = str(unitListPrice)
		row["List_Price"] = str(totalListPrice)

def populateCost(Quote, row):
	different_salesOrg = False
	WTW_Markup_Factor = 0.00

	serviceMaterial = row["Service Material"]
	finalHours = GS_Labor_Utils.getFloat(row["Final Hrs"])
	salesOrg = GS_Labor_Utils.getSalesOrg(row["Execution Country"])

	if finalHours != 0 and serviceMaterial != 'None':
		unitRegionalCost = unitWTWCost = 0
		if 'GES'in serviceMaterial:  #GES parts
			#Trace.Write("Running GES Part Logic")
			non_salesOrg = ""
			if serviceMaterial.endswith("_IN") or serviceMaterial.endswith("_RO"):
				non_salesOrg = salesOrg
			gesTPSap, gesEAC1Sap = GS_Labor_Utils.getTPandEACValueParts(Quote, non_salesOrg, serviceMaterial, row["Execution Year"])
			#Trace.Write("gesTPSap --> "+str(gesTPSap))
			#Trace.Write("gesEAC1Sap --> "+str(gesEAC1Sap))
			if serviceMaterial in gesTPSap and gesTPSap[serviceMaterial]:
				unitRegionalCost = round(GS_Labor_Utils.getFloat(gesTPSap.get(serviceMaterial,0)) + GS_Labor_Utils.getFloat(gesEAC1Sap.get(serviceMaterial,0)), 2)
				try:
					WTW_Markup_Factor = SqlHelper.GetFirst("SELECT WTWMarkupFactorEstimated FROM LABOR_GES_WTW_MARKUP_FACTOR WHERE GES_Service_Material = '{}'".format(serviceMaterial)).WTWMarkupFactorEstimated
				except:
					pass
				unitWTWCost = round(unitRegionalCost / (1 + GS_Labor_Utils.getFloat(WTW_Markup_Factor)), 2)
		else:  #FO parts
			#Trace.Write("Running FO Part Logic")
			salesOrgCountry = GS_Labor_Utils.getExecutionCountry(Quote)
			if row["Execution Country"] != salesOrgCountry:
				different_salesOrg = True
				WTW_Markup_Factor = 0.1
			foPartsCost = GS_Labor_Utils.getFopartsCost(Quote, salesOrg, serviceMaterial, row["Execution Year"])
			#Trace.Write("foPartsCost --> "+str(foPartsCost))
			if serviceMaterial in foPartsCost and foPartsCost[serviceMaterial]:
				unitRegionalCost = round(GS_Labor_Utils.getFloat(foPartsCost.get(serviceMaterial,0)), 2)
				if different_salesOrg:
					add_10_percent = unitRegionalCost * 0.1
					unitRegionalCost = unitRegionalCost + add_10_percent
				unitWTWCost = round(unitRegionalCost / (1 + WTW_Markup_Factor), 2)

		totalCost = unitRegionalCost * finalHours
		totalWTWCost = unitWTWCost * finalHours
		row["Unit_Regional_Cost"] = str(unitRegionalCost)
		row["Regional_Cost"] = str(totalCost)
		row["Unit_WTW_Cost"] = str(unitWTWCost)
		row["WTW_Cost"] = str(totalWTWCost)
	else:
		row["Unit_Regional_Cost"] = row["Regional_Cost"] = row["WTW_Cost"] = "0"
	row.Calculate()

def getUniqueParts(laborCont, partList = []):
	for row in laborCont.Rows:
		if row['Service Material'] != '':
			if row['Service Material'] not in partList:
				partList.append(row['Service Material'])

	return partList

def updateLaborCostPrice(Product, Quote, TagParserQuote, conList, Session=dict()):
	#salesOrg = Quote.SelectedMarket.MarketCode.split('_')[0]
	salesOrg = Quote.GetCustomField('Sales Area').Content
	LOB = Quote.GetCustomField("Booking LOB").Content
	listPriceDict = dict()

	for cont in conList:
		laborCont = Product.GetContainerByName(cont)
		if laborCont.Rows.Count > 0:
			partList = getUniqueParts(laborCont)
			if len(partList) > 0:
				listPriceDict = cps.getPrice(Quote, {}, partList, TagParserQuote, Session)
				#Trace.Write("listPriceDict --> "+str(listPriceDict))

			for row in laborCont.Rows:
				try:
					populateCost(Quote, row)
				except Exception,e:
					msg = "Error when Calculating Cost: {0}, Line Number: {1}".format(e, '82')
					Trace.Write(msg)
				try:
					populateListPrice(Quote, row, listPriceDict)
				except Exception,e:
					msg = "Error when Calculating ListPice: {0}, Line Number: {1}".format(e, '87')
					Trace.Write(msg)
			laborCont.Calculate()

		#Populate Price Cost Container
		populatePriceCost(Product)

def getPartsDict(Product):
	parts_dict = dict()
	conList = ['Winest Labor Container', 'Winest Additional Labor Container']
	for contName in conList:
		cont = Product.GetContainerByName(contName)
		if cont:
			for row in cont.Rows:
				finalHours = GS_Labor_Utils.getFloat(row["Final Hrs"])
				serviceMaterial = row["Service Material"]
				if finalHours != 0 and serviceMaterial != 'None':
					year = row['Year']
					listPrice = GS_Labor_Utils.getFloat(row["List_Price"])
					regionalCost = GS_Labor_Utils.getFloat(row["Regional_Cost"])
					wtwCost = GS_Labor_Utils.getFloat(row["WTW_Cost"])
					parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, serviceMaterial + '|' + year, 'ListPrice', listPrice)
					parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, serviceMaterial + '|' + year, 'Qty', finalHours)
					parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, serviceMaterial + '|' + year, 'Cost', regionalCost)
					parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, serviceMaterial + '|' + year, 'WTWCost', wtwCost)
	return parts_dict

def populatePriceCost(Product): #Populates the pricing and costing container from the dictionary. This container will be used to add line items to cart
	price_cost_cont = Product.GetContainerByName('Winest_Labor_PriceCost_Cont')
	price_cost_cont.Clear()
	parts_dict = getPartsDict(Product)

	for part in parts_dict:
		part_info = parts_dict[part]
		if part and GS_Labor_Utils.getFloat(part_info.get("Qty",0)) != 0.0:
			new_row = price_cost_cont.AddNewRow()
			if new_row is not None:
				new_row['Part Number'] = part.split('|')[0]
				new_row['Qty']= str(part_info.get("Qty",0))
				new_row['Total Cost'] = (str(part_info['Cost'])) if 'Cost' in part_info else '0.0'
				new_row['Total List Price'] = (str(part_info['ListPrice'])) if 'ListPrice' in part_info else '0.0'
				new_row['Total WTW Cost'] = (str(part_info['WTWCost'])) if 'WTWCost' in part_info else '0.0'
				new_row['Year'] = part.split('|')[1]
				new_row.Calculate()
				new_row.IsSelected = True

def createItemDataDict(item):
	qDiscDict = {}
	for child in item.Children:
		qDiscDict[str(child.PartNumber) + "|" + str(child.QI_Year.Value)] = {"Additional_Discount_Percent": child.QI_Additional_Discount_Percent.Value, "MPA_Discount_Percent": child.QI_MPA_Discount_Percent.Value, "Sell_Price": child.ExtendedAmount, "List_Price": child.ExtendedListPrice, "Target_Sell_Price": child.QI_Target_Sell_Price.Value, "No_Discount_Allowed": child.QI_No_Discount_Allowed.Value, "Product Name": child.ProductName, "Project Type": child.ProductTypeName, "Min Order Qty": child.QI_MinOrderQty.Value, "Lead Time": child.LeadTime, "PLSG": child.QI_PLSG.Value, "PLSG Description": child.QI_PLSGDesc.Value, "PL": child.QI_ProductLine.Value, "PL Description": child.QI_ProductLineDesc.Value, "User Comments": child.QI_UserComments.Value, "UOM": child.QI_UoM.Value, "ERP Text": child.QI_SalesText.Value, "Extended Description": child.QI_ExtendedDescription.Value, "Product Category": child.QI_ProductCostCategory.Value}
	return qDiscDict

def transferQuoteDataToContainer(cont, qDiscDict):
	for row in cont.Rows:
		year = row["Year"] if row["Year"] != "No Multi-year" else ""
		itemData = qDiscDict.get(str(row["Material Number"]) + "|" + str(year), "")
		listPriceFactor = GS_Labor_Utils.getFloat(row["List_Price"]) / GS_Labor_Utils.getFloat(itemData["List_Price"])
		row["Sell_Price"] = str(GS_Labor_Utils.getFloat(itemData["Sell_Price"]) * listPriceFactor)
		row["Unit_Sell_Price"] = str(GS_Labor_Utils.getFloat(row["Sell_Price"]) / GS_Labor_Utils.getFloat(row["Final Hrs"]))
		row["Additional_Discount_Amount"] = str((itemData["Additional_Discount_Percent"] /100) * GS_Labor_Utils.getFloat(row["List_Price"]))
		row["Additional_Discount_Percent"] = str(itemData["Additional_Discount_Percent"])
		row["MPA_Discount_Amount"] = str((itemData["MPA_Discount_Percent"] /100) * GS_Labor_Utils.getFloat(row["List_Price"]))
		row["MPA_Discount_Percent"] = str(itemData["MPA_Discount_Percent"])
		row["Target_Sell_Price"] = str(GS_Labor_Utils.getFloat(itemData["Target_Sell_Price"]) * listPriceFactor)
		row["No_Discount_Allowed"] = str(itemData["No_Discount_Allowed"])
		row["Regional_Margin"] = str(GS_Labor_Utils.getFloat(row["Sell_Price"]) - GS_Labor_Utils.getFloat(row["Regional_Cost"]))
		row["WTW_Margin"] = str(GS_Labor_Utils.getFloat(row["Sell_Price"]) - GS_Labor_Utils.getFloat(row["WTW_Cost"]))
		row["Regional_Margin_Percent"] = str((GS_Labor_Utils.getFloat(row["Regional_Margin"]) / GS_Labor_Utils.getFloat(row["Sell_Price"])) * 100)
		row["WTW_Margin_Percent"] = str((GS_Labor_Utils.getFloat(row["WTW_Margin"]) / GS_Labor_Utils.getFloat(row["Sell_Price"])) * 100)
		row["Product Name"] = str(itemData["Product Name"])
		row["Project Type"] = str(itemData["Project Type"])
		row["Min Order Qty"] = str(itemData["Min Order Qty"])
		row["Lead Time"] = str(itemData["Lead Time"])
		row["PLSG"] = str(itemData["PLSG"])
		row["PLSG Description"] = str(itemData["PLSG Description"])
		row["PL"] = str(itemData["PL"])
		row["PL Description"] = str(itemData["PL Description"])
		row["User Comments"] = str(itemData["User Comments"])
		row["UOM"] = str(itemData["UOM"])
		row["ERP Text"] = str(itemData["ERP Text"])
		row["Extended Description"] = str(itemData["Extended Description"])
		row["Product Category"] = str(itemData["Product Category"])
	cont.Calculate()

def updateReportsContainer(prod, reportCont):
	contList = ["Winest Labor Container", "Winest Additional Labor Container"]
	contColumns = ["Deliverable","Service Material","Material Number","Area","WBS Code","Year","Calculated Hrs","Productivity","Final Hrs","Execution Country","Execution Year","Unit_Regional_Cost","Regional_Cost","Unit_List_Price","List_Price","Unit_WTW_Cost","WTW_Cost"]
	for contName in contList:
		cont = prod.GetContainerByName(contName)
		if cont:
			for row in cont.Rows:
				if GS_Labor_Utils.getFloat(row['Final Hrs']) != 0 and row['Material Number'] != 'None':
					newRow = reportCont.AddNewRow()
					for col in contColumns:
						if 'Additional' in contName and col in ("Calculated Hrs","Productivity"):
							continue
						if col == "Service Material":
							newRow[col] = row.GetColumnByName(col).DisplayValue
						else:
							newRow[col] = row[col]