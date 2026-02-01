isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if not isR2Qquote:
	from System import DateTime
	from GS_Migration_Labor_HelperFunctions import getExistingDeliverableRowsDict, deleteExistingDeliverableRows
	from GS_Migration_Labor_populate import populatelGraphicsLabCon,populatelELCNCon,populatelCBECCon,populateLaborContainers,populateprojectManagementCon,populatelThirdpartyPLC_UOC_LabCon

	def getContainer(Name):
		return Product.GetContainerByName(Name)

	def getCfValue(Name):
		return Quote.GetCustomField(Name).Content

	def getAttrValue(Name):
		return Product.Attr(Name).GetValue()

	def getFloat(Var):
		if Var:
			return float(Var)
		return 0

	def getRowData(container,column):
		Container = getContainer(container)
		for row in Container.Rows:
			return row[column]

	def getDefaultExecutionYear():
		executionYear = str(DateTime.Now.Year)
		yearsList = []
		currentYear = DateTime.Now.Year
		i = 0
		while i < 4:
			year = currentYear + i
			yearsList.append(year)
			i += 1
		if getCfValue("EGAP_Contract_Start_Date") != '':
			year = UserPersonalizationHelper.CovertToDate(getCfValue("EGAP_Contract_Start_Date")).Year
			if year in yearsList:
				executionYear = year
			else:
				executionYear = yearsList[-1] if len(yearsList) > 0 else str(DateTime.Now.Year)
		return executionYear

	def checkForMPACustomer():
		PricePlanPresent = False
		query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Honeywell_Ref != '' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date < '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date > '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
		res = SqlHelper.GetList(query)
		if res and len(res) > 0:
			PricePlanPresent = True
		return PricePlanPresent

	def getExecutionCountry():
		#marketCode = Quote.SelectedMarket.MarketCode
		#salesOrg = marketCode.partition('_')[0]
		#Updated logic for Defect 27359
		#currency = marketCode.partition('_')[2]
		salesOrg = Quote.GetCustomField('Sales Area').Content
		currency = Quote.GetCustomField('Currency').Content
		query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
		if query is not None:
			return query.Execution_County

	def assignOPMParts(row,entry,mpaAvailable,activeServiceContract):
		if entry.Deliverables in ["OPM Pre-Migration Audit","OPM Plan Review & Migration Registration KOM","OPM Site Visit Data Gathering","OPM Pre-FAT & FAT","OPM Migration L2","OPM Migration L1","OPM SAT","OPM Post Migration Task","OPM Deployment L2 - AMT","Regional Migration Principal Efforts"]:
			if (mpaAvailable or activeServiceContract == "Yes"):
				if row["FO_Eng"] == '':
					row["FO_Eng"] = "SVC-ESSS-ST"
			else :
				if row["FO_Eng"] == '':
					row["FO_Eng"] = "SVC-ESSS-ST-NC"
		else:
			if (mpaAvailable or activeServiceContract == "Yes"):
				if row["FO_Eng"] == '':
					row["FO_Eng"] = "SVC-EST1-ST"
			else:
				if row["FO_Eng"] == '':
					row["FO_Eng"] = "SVC-EST1-ST-NC"

	def populateOpmCon(container,productModule,mpaAvailable,activeServiceContract,msid_product):
		existing_deliverables = getExistingDeliverableRowsDict(container)
		finalDeliverables = []
		opmBasicInfoCon = Product.GetContainerByName('OPM_Basic_Information')
		for row in opmBasicInfoCon.Rows:
			Trace.Write("remotemigration"+str(row['OPM_Is_this_is_a_Remote_Migration_Service_RMS']))
		amt = getRowData("OPM_Basic_Information","OPM_Is_this_is_a_Remote_Migration_Service_RMS")
		dataGatheringRequired =  msid_product.Attr('MSID_FEL_Data_Gathering_Required').GetValue()
		queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = '{}'".format(productModule))
		if queryData is not None:
			for entry in queryData:
				if entry.Deliverable_Type == "Onsite" and entry.Deliverables == 'OPM Deployment L2 - AMT' and amt in ('No',''):
					continue
				if entry.Deliverable_Type == "Offsite" and entry.Deliverables == 'OPM MCOE - AMT' and amt in ('No',''):
					continue
				if entry.Deliverable_Type == "Onsite" and entry.Deliverables == 'OPM Site Visit Data Gathering' and dataGatheringRequired in ('NO','','None'):
					continue
				if entry.Deliverable_Type == "Onsite" and entry.Deliverables == 'OPM Migration L2' and amt == 'Yes':
					continue
				if existing_deliverables.get(entry.Deliverables):
					row = existing_deliverables.get(entry.Deliverables)
				else:
					row = container.AddNewRow(False)
				finalDeliverables.append(entry.Deliverables)
				row["Deliverable"] = entry.Deliverables
				row["Deliverable_Type"] = entry.Deliverable_Type if entry.Deliverable_Type else ''
				if entry.Deliverables not in ('On-Site','Total','Off-Site'):
					if row["Execution_Year"] == '':
						row["Execution_Year"] = str(executionYear)
				if entry.Deliverables not in ('Total','Off-Site','On-Site'):
					if row["Adjustment_Productivity"] == '':
						row["Adjustment_Productivity"] = "1"
					assignOPMParts(row,entry,mpaAvailable,activeServiceContract)
					if GES_location:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = entry.FO_Eng_Split if entry.FO_Eng_Split else "100"
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = entry.GES_Eng_Split if entry.GES_Eng_Split else "0"
						if entry.Deliverable_Type == "Offsite":
							if row["GES_Eng"] == '':
								row["GES_Eng"] = "SVC_GES_P350B_{}".format(GES_Valuecode)
						elif entry.Deliverable_Type == "Onsite":
							if row["GES_Eng"] == '':
								row["GES_Eng"] = "SVC_GES_P350F_{}".format(GES_Valuecode)
					else:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = "100"
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] =='':
							row["Execution_Country"] = excecutionCountry
		deleteExistingDeliverableRows(container, finalDeliverables,msid_product)

	def populatelcnOneTimeUpgradeCon(lcnOneTimeUpgradeCon,lcnAdjustmentProductivity,mpaAvailable,activeServiceContract):
		existing_deliverables = getExistingDeliverableRowsDict(lcnOneTimeUpgradeCon)
		finalDeliverables = []
		excecutionCountry = getExecutionCountry()
		queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = 'LCN'")
		if not existing_deliverables.get("Total"):
			row = lcnOneTimeUpgradeCon.AddNewRow(False)
			row["Deliverable"] = "Total"
		finalDeliverables.append("Total")
		if not existing_deliverables.get("Off-Site"):
			row = lcnOneTimeUpgradeCon.AddNewRow(False)
			row["Deliverable"] = "Off-Site"
		finalDeliverables.append("Off-Site")
		if queryData is not None:
			for entry in queryData:
				if entry.Deliverable_Type == "Offsite":
					if existing_deliverables.get(entry.Deliverables):
						row = existing_deliverables.get(entry.Deliverables)
					else:
						row = lcnOneTimeUpgradeCon.AddNewRow(False)
					finalDeliverables.append(entry.Deliverables)
					row["Deliverable"] = entry.Deliverables
					if row["Adjustment_Productivity"] == '':
						row["Adjustment_Productivity"] = lcnAdjustmentProductivity
					row["Deliverable_Type"] = entry.Deliverable_Type
					if row["FO_Eng_Percentage_Split"] == '':
						row["FO_Eng_Percentage_Split"] = "100"
					if row["GES_Eng_Percentage_Split"] == '':
						row["GES_Eng_Percentage_Split"] = "0"
					if mpaAvailable or activeServiceContract == "Yes":
						if row["FO_Eng"] == '':
							row["FO_Eng"] = "SVC-EAPS-ST"
					else:
						if row["FO_Eng"] == '':
							row["FO_Eng"] = "SVC-EAPS-ST-NC"
					if row["Execution_Year"] =='':
						row["Execution_Year"] =str(executionYear)
					if GES_location:
						if row["GES_Eng"] == '':
							row["GES_Eng"] = "SVC_GES_P350B_{}".format(GES_Valuecode)
					else:
						Trace.Write("MSID_GES_Location not found in the product!!")
					if excecutionCountry:
						if row["Execution_Country"] == '':
							row["Execution_Country"] = excecutionCountry
		deleteExistingDeliverableRows(lcnOneTimeUpgradeCon, finalDeliverables,msid_product)

	def addNewRow(container,productivity,mpaAvailable,activeServiceContract,excecutionCountry,entry,existing_deliverables,finalDeliverables):
		if existing_deliverables.get(entry.Deliverables):
			row = existing_deliverables.get(entry.Deliverables)
		else:
			row = container.AddNewRow(False)
		finalDeliverables.append(entry.Deliverables)
		row["Deliverable"] = entry.Deliverables
		if row["Adjustment_Productivity"] == '':
			row["Adjustment_Productivity"] = productivity
		row["Deliverable_Type"] = entry.Deliverable_Type
		if row["FO_Eng_Percentage_Split"] == '':
			row["FO_Eng_Percentage_Split"] = "100"
		if row["GES_Eng_Percentage_Split"] == '':
			row["GES_Eng_Percentage_Split"] = "0"
		if entry.Deliverables=="Regional Migration Principal Efforts":
			if (mpaAvailable or activeServiceContract == "Yes"):
				if row["FO_Eng"] == '':
					row["FO_Eng"] = entry.FO_Eng
			else :
				if row["FO_Eng"] == '':
					row["FO_Eng"] = entry.FO_Eng+"-NC"
		elif mpaAvailable or activeServiceContract == "Yes":
			if row["FO_Eng"] == '':
				row["FO_Eng"] = "SVC-EAPS-ST"
		else:
			if row["FO_Eng"] == '':
				row["FO_Eng"] = "SVC-EAPS-ST-NC"
		if row["Execution_Year"] == '':
			row["Execution_Year"] = str(executionYear)
		if GES_location:
			if entry.Deliverable_Type == "Offsite":
				if row["GES_Eng"] =='':
					row["GES_Eng"] = "SVC_GES_P350B_{}".format(GES_Valuecode)
			else:
				if row["GES_Eng"] =='':
					row["GES_Eng"] = "SVC_GES_P350F_{}".format(GES_Valuecode)
		else:
			Trace.Write("MSID_GES_Location not found in the product!!")
		if excecutionCountry:
			if row["Execution_Country"] == '':
				row["Execution_Country"] = excecutionCountry
		return finalDeliverables

	def populatelEBRCon(ebrCon,ebrAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry):
		siteAccepTest = Product.Attr( "EBR_Site_Acceptance_Test_required").GetValue()
		queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = 'EBR'")

		existing_deliverables = getExistingDeliverableRowsDict(ebrCon)
		finalDeliverables = []
		if not existing_deliverables.get("Total"):
			row = ebrCon.AddNewRow(False)
			row["Deliverable"] = "Total"
		finalDeliverables.append("Total")
		if not existing_deliverables.get("Off-Site"):
			row = ebrCon.AddNewRow(False)
			row["Deliverable"] = "Off-Site"
		finalDeliverables.append("Off-Site")
		if queryData is not None:
			for entry in queryData:
				if entry.Deliverable_Type == "Offsite":
					finalDeliverables = addNewRow(ebrCon,ebrAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry,entry,existing_deliverables,finalDeliverables)
			if not existing_deliverables.get("On-Site"):
				row = ebrCon.AddNewRow(False)
				row["Deliverable"] = "On-Site"
			finalDeliverables.append("On-Site")
			for entry in queryData:
				if entry.Deliverable_Type == "Onsite":
					if siteAccepTest in ('No','') and entry.Deliverables == "SAT":
						continue
					finalDeliverables = addNewRow(ebrCon,ebrAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry,entry,existing_deliverables,finalDeliverables)
		deleteExistingDeliverableRows(ebrCon, finalDeliverables, msid_product)

	def migrationDDSCheck(elcnUpgradeNew):
		sum = 0
		rowIndex = 0
		for row in elcnUpgradeNew.Rows:
			if rowIndex < 2:
				for column in row.Columns:
					if row[column.Name] != '':
						sum += int(row[column.Name])
			rowIndex += 1
		if sum > 0:
			return sum
		else:
			return 0

	def populatelLabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
		excecutionCountry = getExecutionCountry()
		queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = '{}'and Contract = '{}'".format(modulename,contractType))
		existing_deliverables = getExistingDeliverableRowsDict(LabCon)
		finalDeliverables = []
		if not existing_deliverables.get("Total"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Total"
		finalDeliverables.append("Total")
		if not existing_deliverables.get("Off-Site"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Off-Site"
		finalDeliverables.append("Off-Site")
		if queryData is not None:
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Offsite":
					if existing_deliverables.get(entry.Deliverables):
						row = existing_deliverables.get(entry.Deliverables)
					else:
						row = LabCon.AddNewRow(False)
					finalDeliverables.append(entry.Deliverables)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Offsite"
					if row["Adjustment_Productivity"] =='':
						row["Adjustment_Productivity"] = AdjustmentProductivity
					if row["Execution_Year"] =='':
						row["Execution_Year"] = str(executionYear)
					if row["FO_Eng"] =='':
						row["FO_Eng"] = entry.FO_Eng
					if GES_location:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
						if row["GES_Eng"] == '':
							row["GES_Eng"] = "SVC_GES_P350B_{}".format(GES_Valuecode)
					else:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = "100"
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] =='':
							row["Execution_Country"] = excecutionCountry
			if not existing_deliverables.get("On-Site"):
				row = LabCon.AddNewRow(False)
				row["Deliverable"] = "On-Site"
			finalDeliverables.append("On-Site")
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Onsite":
					if existing_deliverables.get(entry.Deliverables):
						row = existing_deliverables.get(entry.Deliverables)
					else:
						row = LabCon.AddNewRow(False)
					finalDeliverables.append(entry.Deliverables)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Onsite"
					if row["Adjustment_Productivity"] == '':
						row["Adjustment_Productivity"] = AdjustmentProductivity
					if row["Execution_Year"] == '':
						row["Execution_Year"] = str(executionYear)
					if row["FO_Eng"] == '':
						row["FO_Eng"] = entry.FO_Eng
					if GES_location:
							if row["FO_Eng_Percentage_Split"] == '':
								row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
							if row["GES_Eng_Percentage_Split"] == '':
								row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
							if row["GES_Eng"] == '':
								row["GES_Eng"] = "SVC_GES_P350F_{}".format(GES_Valuecode)
					else:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = "100"
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] == '':
							row["Execution_Country"] = excecutionCountry
		deleteExistingDeliverableRows(LabCon, finalDeliverables,msid_product)

	def populatelCWSRAELabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
		excecutionCountry = getExecutionCountry()
		queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = '{}'and Contract = '{}'".format(modulename,contractType))
		existing_deliverables = getExistingDeliverableRowsDict(LabCon)
		finalDeliverables = []
		if not existing_deliverables.get("Total"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Total"
		finalDeliverables.append("Total")
		if not existing_deliverables.get("Off-Site"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Off-Site"
		finalDeliverables.append("Off-Site")
		if queryData is not None:
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Offsite":
					if existing_deliverables.get(entry.Deliverables):
						row = existing_deliverables.get(entry.Deliverables)
					else:
						row = LabCon.AddNewRow(False)
					finalDeliverables.append(entry.Deliverables)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Offsite"
					if row["Adjustment_Productivity"] == '':
						row["Adjustment_Productivity"] = AdjustmentProductivity
					if row["Execution_Year"] == '':
						row["Execution_Year"] = str(executionYear)
					if row["FO_Eng"] == '':
						row["FO_Eng"] = entry.FO_Eng
					if GES_location:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
						if row["Deliverable"] == "MD CD Configuration":
							if row["GES_Eng"] == '':
								row["GES_Eng"] = "SVC_GES_P350B_CN"
						else:
							if row["GES_Eng"] == '':
								row["GES_Eng"] = "SVC_GES_P350B_{}".format(GES_Valuecode)
					else:
						if row["Deliverable"] in ("MD CD Configuration","Server/Station Build"):
							if row["FO_Eng_Percentage_Split"] == '':
								row["FO_Eng_Percentage_Split"] = "0"
							if row["GES_Eng_Percentage_Split"] == '':
								row["GES_Eng_Percentage_Split"] = "0"
						else:
							if row["FO_Eng_Percentage_Split"] == '':
								row["FO_Eng_Percentage_Split"] = "100"
							if row["GES_Eng_Percentage_Split"] == '':
								row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] == '':
							row["Execution_Country"] = excecutionCountry
			if not existing_deliverables.get("On-Site"):
				row = LabCon.AddNewRow(False)
				row["Deliverable"] = "On-Site"
			finalDeliverables.append("On-Site")
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Onsite":
					if existing_deliverables.get(entry.Deliverables):
						row = existing_deliverables.get(entry.Deliverables)
					else:
						row = LabCon.AddNewRow(False)
					finalDeliverables.append(entry.Deliverables)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Onsite"
					if row["Adjustment_Productivity"] == '':
						row["Adjustment_Productivity"] = AdjustmentProductivity
					if row["Execution_Year"] == '':
						row["Execution_Year"] = str(executionYear)
					if row["FO_Eng"] == '':
						row["FO_Eng"] = entry.FO_Eng
					if GES_location:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
						if row["GES_Eng"] == '':
							row["GES_Eng"] = "SVC_GES_P350F_{}".format(GES_Valuecode)
					else:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = "100"
						if row["GES_Eng_Percentage_Split"] == '':    
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] == '':
							row["Execution_Country"] = excecutionCountry
		deleteExistingDeliverableRows(LabCon, finalDeliverables,msid_product)


	if Product.Attr('MIgration_Scope_Choices').GetValue() != "HW/SW":
		excecutionCountry = getExecutionCountry()
		executionYear = getDefaultExecutionYear()
		foPartNumberCon = getContainer("MSID_Labor_FO_Part_Number")
		opmEngineeringCon = getContainer("MSID_Labor_OPM_Engineering")
		lcnOneTimeUpgradeCon = getContainer("MSID_Labor_LCN_One_Time_Upgrade_Engineering")
		ebrCon = getContainer("MSID_Labor_EBR_Con")
		elcnCon = getContainer("MSID_Labor_ELCN_Con")
		orionConsoleCon = getContainer("MSID_Labor_Orion_Console_Con")
		ehpmCon = getContainer("MSID_Labor_EHPM_C300PM_Con")
		tpsCon = getContainer("MSID_Labor_TPS_TO_EXPERION_Con")
		tcmiCon = getContainer("MSID_Labor_TCMI_Con")
		c200MigrationCon = getContainer("MSID_Labor_C200_Migration_Con")
		ehpmhartioCon = getContainer("MSID_Labor_EHPM_HART_IO_Con")
		cbecCon = getContainer("MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con")
		fsctosmCon = getContainer("MSID_Labor_FSC_to_SM_con")
		fsctosmauditCon = getContainer("MSID_Labor_FSC_to_SM_audit_Con")
		fdmCon = getContainer("MSID_Labor_FDM_Upgrade_Con")
		xPMCon = getContainer("MSID_Labor_xPM_to_C300_Migration_Con")
		lmCon = getContainer("MSID_Labor_LM_to_ELMM_Con")
		XP10Con = getContainer("MSID_Labor_XP10_Actuator_Upgrade_con")
		CDActuatorCon = getContainer("MSID_Labor_CD_Actuator_con")
		fscsmioCon = getContainer("MSID_Labor_FSCtoSM_IO_con")
		fsctosmioauditCon = getContainer("MSID_Labor_FSC_to_SM_IO_Audit_Con")
		thirdPartyConPLC_UOC = getContainer("3rd_Party_PLC_UOC_Labor")
		projectManagementCon = getContainer("MSID_Labor_Project_Management")
		opmAdjustmentProductivity =getAttrValue("OPM_Adjustment_Productivity")
		lcnAdjustmentProductivity =getAttrValue("LCN_Adjustment_Productivity")
		ebrAdjustmentProductivity =getAttrValue("EBR_Adjustment_Productivity")
		elcnAdjustmentProductivity =getAttrValue("ELCN_Adjustment_Productivity")
		cbecAdjustmentProductivity =getAttrValue("CB-EC_Upgrade_to_C300-UHIO_Adjustment_Productivity")
		fsctosmAdjustmentProductivity = getAttrValue("FSC_to_SM_Adjustment_Productivity")
		fsctosmauditAdjustmentProductivity = getAttrValue("FSC_to_SM_audit_Adjustment_Productivity")
		fdmAdjustmentProductivity =getAttrValue("FDM_Upgrade_Adjustment_Productivity")
		xPMAdjustmentProductivity =getAttrValue("xPM_to_C300_Migration_Adjustment_Productivity")
		lmAdjustmentProductivity =getAttrValue("LM_to_ELMM_Adjustment_Productivity")
		XP10AdjustmentProductivity =getAttrValue("XP10_Actuator_Upgrade_Adjustment_Productivity")
		pmAdjustmentProductivity = getAttrValue("PM_Adjustment_Productivity")
		thirdPartyAdjustmentProductivity_PLC_UOC = getAttrValue("3rd_Party_PLC_UOC_Labor_Productivity") if getAttrValue("3rd_Party_PLC_UOC_Labor_Productivity") else "1"
		GraphicsCon = getContainer("MSID_Labor_Graphics_Migration_con")
		GraphicsAdjustmentProductivity = getAttrValue("Graphics_Migration_Adjustment_Productivity")
		CWSRAECon = getContainer("MSID_Labor_CWS_RAE_Upgrade_con")
		CWSRAEAdjustmentProductivity = getAttrValue("CWS_RAE_Upgrade_Adjustment_Productivity")
		CDActuatorAdjustmentProductivity = getAttrValue("CD_Actuator_Adjustment_Productivity")
		fscsmioAdjustmentProductivity = getAttrValue("FSCtoSM_IO_Adjustment_Productivity")
		fsctosmioauditAdjustmentProductivity = getAttrValue("MSID_Labor_Fsc_SM_IO_Audit_Productivity")
		mpaAvailable = checkForMPACustomer()
		activeServiceContract = getAttrValue("MSID_Active_Service_Contract")
		if activeServiceContract == 'Yes' or mpaAvailable:
			contractType = "Contract"
		else:
			contractType = "Non-Contract"
		msidCont = Product.GetContainerByName("CONT_MSID_SUBPRD")
		GES_location =Product.Attr('MSID_GES_Location').GetValue() if Product.Attr('MSID_GES_Location').GetValue() != 'None' else ''
		GES_Valuecode=TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>')
		msid_product = Product
		for row in msidCont.Rows:
			#if row["Selected_Products"] == "OPM":
			Product = row.Product
			selectedProducts = row["Selected_Products"]

			'''if foPartNumberCon.Rows.Count == 0 :#or (str(selectedProducts) != Product.Attr("MSID_Selected_Products_Flag").GetValue()):
				Trace.Write("populatecontainer")
				ScriptExecutor.Execute('PS_PopulatePartNumberContainer')
				Product.Attr("MSID_Selected_Products_Flag").AssignValue(str(selectedProducts))'''

			populateOpmCon(opmEngineeringCon,"OPM",mpaAvailable,activeServiceContract,msid_product) if "OPM" in selectedProducts else 0
			populatelcnOneTimeUpgradeCon(lcnOneTimeUpgradeCon,lcnAdjustmentProductivity,mpaAvailable,activeServiceContract) if "LCN One Time Upgrade" in selectedProducts else 0
			populatelEBRCon(ebrCon,ebrAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry) if "EBR" in selectedProducts else 0
			populatelELCNCon(Product,Quote,elcnCon,elcnAdjustmentProductivity,mpaAvailable,activeServiceContract,GES_location,GES_Valuecode,msid_product) if "ELCN" in selectedProducts else 0
			populatelCBECCon(Quote,Product, cbecCon,cbecAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,GES_location,GES_Valuecode,msid_product) if "CB-EC Upgrade to C300-UHIO" in selectedProducts else 0

			populatelLabCon(fdmCon,fdmAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"FDM Upgrade") if (("FDM Upgrade 1" in selectedProducts) or ("FDM Upgrade 2" in selectedProducts) or ("FDM Upgrade 3" in selectedProducts)) else 0
			populatelLabCon(XP10Con,XP10AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"XP10 Actuator Upgrade") if "XP10 Actuator Upgrade" in selectedProducts else 0
			populatelLabCon(fsctosmCon,fsctosmAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"FSC to SM") if selectedProducts == "FSC to SM" else 0
			populatelLabCon(fsctosmauditCon,fsctosmauditAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"FSC to SM Audit") if selectedProducts == "FSC to SM" else 0
			populatelLabCon(xPMCon,xPMAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"xPM to C300 Migration") if "xPM to C300 Migration" in selectedProducts else 0
			populatelLabCon(lmCon,lmAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"LM to ELMM ControlEdge PLC") if "LM to ELMM ControlEdge PLC" in selectedProducts else 0
			populatelGraphicsLabCon(Quote,Product,GraphicsCon,GraphicsAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"Graphics Migration",GES_location,GES_Valuecode,msid_product) if "Graphics Migration" in selectedProducts else 0

			populatelCWSRAELabCon(CWSRAECon,CWSRAEAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"CWS RAE Upgrade") if "CWS RAE Upgrade" in selectedProducts else 0
			populatelLabCon( CDActuatorCon,CDActuatorAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"CD Actuator I-F Upgrade") if "CD Actuator I-F Upgrade" in selectedProducts else 0
			populatelThirdpartyPLC_UOC_LabCon(Product, Quote,thirdPartyConPLC_UOC,thirdPartyAdjustmentProductivity_PLC_UOC,mpaAvailable,activeServiceContract,contractType,"3rd Party PLC to ControlEdge PLC/UOC",GES_location,GES_Valuecode,msid_product) if "3rd Party PLC to ControlEdge PLC/UOC" in selectedProducts else 0
			populatelLabCon(fscsmioCon,fscsmioAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"FSC to SM IO Migration") if  selectedProducts == "FSC to SM IO Migration" else 0
			populateprojectManagementCon(Quote,Product,projectManagementCon,pmAdjustmentProductivity,mpaAvailable,activeServiceContract,GES_location,GES_Valuecode,msid_product) 
			populateLaborContainers(Quote,Product,orionConsoleCon,"Orion Console",contractType,GES_location,GES_Valuecode,msid_product) if "Orion Console" in selectedProducts else 0
			populateLaborContainers(Quote,Product,ehpmCon,"EHPM/EHPMX/ C300PM",contractType,GES_location,GES_Valuecode,msid_product) if "EHPM/EHPMX/ C300PM" in selectedProducts else 0
			populateLaborContainers(Quote,Product,tpsCon,"TPS TO EXPERION",contractType,GES_location,GES_Valuecode,msid_product) if "TPS to Experion" in selectedProducts else 0
			populateLaborContainers(Quote,Product,tcmiCon,"TCMI",contractType,GES_location,GES_Valuecode,msid_product) if "TCMI" in selectedProducts else 0
			populateLaborContainers(Quote,Product,ehpmhartioCon,"EHPM HART IO",contractType,GES_location,GES_Valuecode,msid_product) if "EHPM HART IO" in selectedProducts else 0
			populatelLabCon(fsctosmioauditCon,fsctosmioauditAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"FSC to SM IO Audit") if selectedProducts == "FSC to SM IO Migration" else 0
			if "C200 Migration" in selectedProducts:
				migrationScenario =Product.Attr('C200_Select_Migration_Scenario').GetValue()
				if migrationScenario in ['C200 to C300','']:
					#c200MigrationCon.Clear()
					populateLaborContainers(Quote,Product,c200MigrationCon,"C200 C300 Migration",contractType,GES_location,GES_Valuecode,msid_product)
				elif migrationScenario == 'C200 to ControlEdge UOC':
					#c200MigrationCon.Clear()
					populateLaborContainers(Quote,Product,c200MigrationCon,"C200 Migration",contractType,GES_location,GES_Valuecode,msid_product)