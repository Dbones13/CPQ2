def addFinalHours_prjt(totalDict, key, value):
	totalDict[key] = getFloat_prjt(totalDict.get(key, 0)) + getFloat_prjt(value)
	return totalDict[key]
def getFloat_prjt(Var):
	if Var:
		return float(Var)
	return 0
def getExecutionCountry_prjt(Quote):
	marketCode = Quote.SelectedMarket.MarketCode
	salesOrg = Quote.GetCustomField('Sales Area').Content
	currency = Quote.GetCustomField('Currency').Content
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
	if query is not None:
		return query.Execution_County
def rowtotal(row):
	Split1=getFloat_prjt(row["FO Eng 1 % Split"])
	Split2=getFloat_prjt(row["FO Eng 2 % Split"])
	Split3=getFloat_prjt(row["FO Eng % Split"])
	Total_split_hrs = 0.0
	if row["Final Hrs"] not in ('',"0"):
		Split1_hrs = round(getFloat_prjt(row["Final Hrs"]) * (Split1) / 100) if str(Split1) != '0' else 0.0
		Split2_hrs = round(getFloat_prjt(row["Final Hrs"]) * (Split2) / 100) if str(Split2) != '0' else 0.0
		Split3_hrs = round(getFloat_prjt(row["Final Hrs"]) * (Split3) / 100) if str(Split3) != '0' else 0.0
		Total_split_hrs=Split1_hrs+Split2_hrs+Split3_hrs
		Trace.Write("Total_split"+str(Total_split_hrs))
	Total_split = Split1+Split2+Split3
	return Total_split,Total_split_hrs
def labor_prjt(Quote,parentItem):
	product_name=['PMD System','Field Device Manager','ControlEdge RTU System','ControlEdge PLC System','Experion HS System','Virtualization System','3rd Party Devices/Systems Interface (SCADA)','eServer System','ARO, RESS & ERG System','Digital Video Manager','Electrical Substation Data Collector','Simulation System','MXProLine System','ControlEdge UOC System','ControlEdge CN900 System','Experion Enterprise System','New / Expansion Project','C300 System','Experion MX System','ControlEdge PCD System','Experion HS System','PlantCruise System','HC900 System',"Variable Frequency Drive System","Measurement IQ System","Safety Manager ESD","Safety Manager FGS","Safety Manager BMS","Safety Manager HIPPS","Terminal Manager","MasterLogic-50 Generic","MasterLogic-200 Generic","Experion LX Generic","One Wireless System","Fire and Gas Consultancy Service","Tank Gauging Engineering","Public Address General Alarm System","PRMS Skid Engineering","Metering Skid Engineering","Process Safety Workbench Engineering", "Fire Detection & Alarm Engineering","MS Analyser System Engineering","Gas MeterSuite Engineering - C300 Functions","Liquid MeterSuite Engineering - C300 Functions","Industrial Security (Access Control)","MeterSuite Engineering - MSC Functions","Generic System"]
	conNames = {
				"PMD System":["PMD Engineering Labor Container","PMD Labor Additional Custom Deliverable"],
				"Field Device Manager":["FDM Engineering Labor Container","FDM Additional Custom Deliverables"],
				"ControlEdge RTU System":["CE RTU Engineering Labor Container","CE RTU Additional Custom Deliverables"],
				"ControlEdge PLC System":["CE PLC Engineering Labor Container","CE PLC Additional Custom Deliverables"],
				"ControlEdge UOC System":["CE UOC Engineering Labor Container","CE UOC Additional Custom Deliverables"],
                "ControlEdge CN900 System":["CE CN900 Engineering Labor Container","CE CN900 Additional Custom Deliverables"],
				"Experion HS System":["Experion HS Engineering Labor Container","Experion HS Additional Custom Deliverables"],
				"Virtualization System":["Virtualization_Labor_Deliverable","Virtualization_Additional_Custom_Deliverables"],
				"3rd Party Devices/Systems Interface (SCADA)":["SCADA_Engineering_Labor_Container","SCADA_Additional_Custom_Deliverables_Container"],
				"eServer System":["eServer_Labor_Container","eServer_Labor_Additional_Cust_Deliverables_con"],
				"ARO, RESS & ERG System":["ARO_RESS_Engineering_Labor_Container","ARO_RESS_Additional_Labour_Container"],
				"Digital Video Manager":["DVM_Engineering_Labor_Container","DVM_Additional_Labour_Container"],
				"Electrical Substation Data Collector":["ESDC_Labor_Additional_Cust_Deliverables_con"],
				"Simulation System":["Simulation_Labor_Additional_Cust_Deliverables_con"],
				"MXProLine System":["MXPro_Labor_Container","MXPro_Labor_Additional_Cust_Deliverables_con"],
				"Experion Enterprise System":["Hardware Engineering Labour Container","System_Network_Engineering_Labor_Container","System_Interface_Engineering_Labor_Container","HMI_Engineering_Labor_Container","EBR_Engineering_Labor_Container","Additional_CustomDev_Labour_Container"],
				"C300 System":["C300_Engineering_Labor_Container","C300_Additional_Custom_Deliverables_Container"],
				"Experion MX System":["Experion_mx_Labor_Container","Experion_mx_labor_Additional_Cust_Deliverables_con"],
				"ControlEdge PCD System":["PCD Engineering Labor Container","PCD Additional Custom Deliverables"],
				"Experion HS System":["Experion HS Engineering Labor Container","Experion HS Additional Custom Deliverables"],
				"PlantCruise System":["PlantCruise Engineering Labor Container","PlantCruise Additional Custom Deliverables"],
				"HC900 System":["HC900 Engineering Labor Container","HC900 Additional Custom Deliverables"],
				"Variable Frequency Drive System":["VFD Engineering Labor Container","VFD Additional Custom Deliverables"],
				"Measurement IQ System":["MIQ Engineering Labor Container","MIQ Additional Custom Deliverables"],
				"Safety Manager ESD":["SM_SSE_Engineering_Labor_Container","SM_Additional_Custom_Deliverables_Labor_Container","SM Safety System - ESD/FGS/BMS/HIPPS Container"],
				"Safety Manager FGS":["SM_SSE_Engineering_Labor_Container","SM_Additional_Custom_Deliverables_Labor_Container","SM Safety System - ESD/FGS/BMS/HIPPS Container"],
				"Safety Manager BMS":["SM_SSE_Engineering_Labor_Container","SM_Additional_Custom_Deliverables_Labor_Container","SM Safety System - ESD/FGS/BMS/HIPPS Container"],
				"Safety Manager HIPPS":["SM_SSE_Engineering_Labor_Container","SM_Additional_Custom_Deliverables_Labor_Container","SM Safety System - ESD/FGS/BMS/HIPPS Container"],
				"Terminal Manager":["Terminal Engineering Labor Container","Terminal Additional Custom Deliverables"],
				"MasterLogic-50 Generic":["Generic Engineering Labor Container","Generic Additional Custom Deliverables"],
				"MasterLogic-200 Generic":["Generic Engineering Labor Container","Generic Additional Custom Deliverables"],
				"Experion LX Generic":["Generic Engineering Labor Container","Generic Additional Custom Deliverables"],
				"Public Address General Alarm System":["PAGA_Labor_Container","PAGA_Additional_Labour_Container"],
				"PRMS Skid Engineering":["PRMS_Engineering_Labor_Container","PRMS_Additional_Labor_Container"],
				"One Wireless System":["OWS_Engineering_Labor_Container","OWS_Additional_Labour_Container"],
				"Fire and Gas Consultancy Service":["FGC_Engineering_Labor_Container","FGC_Additional_Labour_Container"],
				"Tank Gauging Engineering":["TGE_Engineering_Labor_Container","TGE_Additional_Labour_Container"],
				"MS Analyser System Engineering":["MS_ASE_Engineering_Labor_Container","MS_ASE_Additional_Labour_Container"],
				"Metering Skid Engineering":["MSE_Engineering_Labor_Container","MSE_Additional_Labor_Container"],
				"Process Safety Workbench Engineering":["PSW_Labor_Container","PSW_Additional_Labor_Container"],
				"Fire Detection & Alarm Engineering":['FDA_Engineering_Labor_Container', 'FDA_Additional_Labor_Container'],
				"Liquid MeterSuite Engineering - C300 Functions":['LMS_Labor_Container','LMS_Additional_Labor_Container'],
				"Gas MeterSuite Engineering - C300 Functions":['Gas_MeterSuite_Engineering_Labor_Container', 'Gas_MeterSuite_Additional_Labor_Container'],
				"MeterSuite Engineering - MSC Functions":['MSC_Engineering_Labor_Container','MSC_Additional_Labour_Container'],
				"Industrial Security (Access Control)":['IS_Labor_Container','IS_Additional_Labor_Container'],
				"New / Expansion Project":["Labor_Container","PLE_Labor_Container","PM_Additional_Custom_Deliverables_Labor_Container","Project_management_Labor_Container"],"Generic System":["Generic Engineering Labor Container","Generic Additional Custom Deliverables"]
				}
	# To consider Additional Labor Container Labor Hours -- Janhavi Tanna : CXCPQ-67335 :start
	LaborHrs_Products=["PRMS Skid Engineering","Public Address General Alarm System","Tank Gauging Engineering","Metering Skid Engineering","Gas MeterSuite Engineering - C300 Functions","Industrial Security (Access Control)","Fire Detection & Alarm Engineering","MS Analyser System Engineering","MeterSuite Engineering - MSC Functions","One Wireless System","Fire and Gas Consultancy Service","Liquid MeterSuite Engineering - C300 Functions","Process Safety Workbench Engineering", "Virtualization","Digital Video Manager","ARO, RESS & ERG System","Experion Enterprise System"]
	# To consider Additional Labor Container Labor Hours -- Janhavi Tanna : CXCPQ-67335 :End
	laborHours = {}
	excecutionCountry=getExecutionCountry_prjt(Quote)
	for item in Quote.MainItems:
		txt=item.PartNumber
		'''if item.ProductTypeName =="Honeywell Labor" and txt.startswith("SVC-") and not txt.startswith("HPS_SYS_") and item.PartNumber=="SVC-EAPS-ST": #need to change the condition
			Trace.Write("----1st--aaaaaa-----"+str(item.Quantity))
			Quantity = item.Quantity'''
		#for key, conName in conNames.items():
		if item.ProductName in product_name and (item.RolledUpQuoteItem).startswith(parentItem.RolledUpQuoteItem):
			containers=conNames[item.ProductName]
			for conName in containers:
				con = item.SelectedAttributes.GetContainerByName(conName)
				# Trace.Write("---------con--------"+str(conName)+str(con))
				hours=0
				if con is not None:
					if "additional" in conName.lower():
						# To consider Additional Labor Container Labor Hours -- Janhavi Tanna : CXCPQ-67335 :start
						if item.PartNumber not in LaborHrs_Products:
							Deliverable="Standard Deliverable"
						else:
							Deliverable="Standard Deliverable selection"
						# To consider Additional Labor Container Labor Hours -- Janhavi Tanna : CXCPQ-67335 :End
					else:
						Deliverable="Deliverable"
					for row in con.Rows:
						if row[Deliverable] not in 'Total':
							TotalFOEngsplit, TotalFohours=rowtotal(row)
							if row["Execution Country"]== excecutionCountry and row["Final Hrs"] not in ('',"0") and TotalFOEngsplit != '0':
								# Trace.Write("inside if")
								addFinalHours_prjt(laborHours, "Local Labor", TotalFohours)
							elif row["Final Hrs"] not in ('',"0") and TotalFOEngsplit != '0':
								# Trace.Write("inside elif")
								addFinalHours_prjt(laborHours, "Cross Border Labor",TotalFohours)
							if row["Final Hrs"] not in ('',"0") and row["GES Eng"] != '' and row["GES Eng % Split"] != '0':
								GES_Eng=row["GES Eng"]
								if GES_Eng in ('HPS_GES_P350B_IN','HPS_GES_P350B_CN','HPS_GES_P350B_RO','HPS_GES_P350B_UZ','HPS_GES_P335B_IN','HPS_GES_P335B_CN','HPS_GES_P335B_RO','HPS_GES_P335B_UZ','HPS_GES_P215B_IN','HPS_GES_P215B_CN','HPS_GES_P215B_RO','HPS_GES_P215B_UZ','SVC_GES_P350B_IN','SVC_GES_P350B_CN','SVC_GES_P350B_RO','SVC_GES_P350B_UZ','SVC_GES_P335B_IN','SVC_GES_P335B_CN','SVC_GES_P335B_RO','SVC_GES_P335B_UZ','SVC_GES_P215B_IN','SVC_GES_P215B_CN','SVC_GES_P215B_RO','SVC_GES_P215B_UZ','HPS_GES_P350B_EG','HPS_GES_P335B_EG','HPS_GES_P215B_EG','SVC_GES_P350B_EG','SVC_GES_P335B_EG','SVC_GES_P215B_EG'):
									# Trace.Write("inside if if")
									addFinalHours_prjt(laborHours, "GES - Work @ GES Location", round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(row["GES Eng % Split"]) / 100))
								elif GES_Eng in ('HPS_GES_P350F_IN','HPS_GES_P350F_CN','HPS_GES_P350F_RO','HPS_GES_P350F_UZ','HPS_GES_P215F_CN','HPS_GES_P215F_IN','HPS_GES_P215F_RO','HPS_GES_P215F_UZ','HPS_GES_P335F_CN','HPS_GES_P335F_IN','HPS_GES_P335F_RO','HPS_GES_P335F_UZ','SVC_GES_P350F_IN','SVC_GES_P350F_CN','SVC_GES_P350F_RO','SVC_GES_P350F_UZ','SVC_GES_P215F_CN','SVC_GES_P215F_IN','SVC_GES_P215F_RO','SVC_GES_P215F_UZ','SVC_GES_P335F_CN','SVC_GES_P335F_IN','SVC_GES_P335F_RO','SVC_GES_P335F_UZ','HPS_GES_P350F_EG','HPS_GES_P335F_EG','HPS_GES_P215F_EG','SVC_GES_P350F_EG','SVC_GES_P335F_EG','SVC_GES_P215F_EG'):
									# Trace.Write("elsif ")
									addFinalHours_prjt(laborHours, "GES - Work @ Non GES Location", round(getFloat_prjt(row["Final Hrs"]) * getFloat_prjt(row["GES Eng % Split"]) / 100))
									#addFinalHours_prjt(laborHours, "Local Labor", round(getFloat_prjt(item.Quantity))
								elif item.ProductTypeName =="Honeywell Labor" :
									addFinalHours_prjt(laborHours, "Local Labor", round(getFloat_prjt(item.Quantity)))
			# Trace.Write(str(item.ProductName)+"----"+str(laborHours))
	# Trace.Write("----"+str(laborHours))
	return laborHours
#labor_prjt(Quote)