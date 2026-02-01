from GS_Migration_Labor_HelperFunctions import getExistingDeliverableRowsDict, deleteExistingDeliverableRows,getExistingDeliverablegraphicsRowsDict,deleteExistingDeliverablegraphicsrows

def getContainer(Product, Name):
	return Product.GetContainerByName(Name)

def getCfValue(Quote, Name):
	return Quote.GetCustomField(Name).Content

def getAttrValue(Product, Name):
	return Product.Attr(Name).GetValue()

def getFloat(Var):
	if Var:
		return float(Var)
	return 0

def getRowData(Product, container,column):
	Container = getContainer(Product, container)
	for row in Container.Rows:
		return row[column]

def getDefaultExecutionYear(Quote):
	executionYear = str(DateTime.Now.Year)
	yearsList = []
	currentYear = DateTime.Now.Year
	i = 0
	while i < 4:
		year = currentYear + i
		yearsList.append(year)
		i += 1
	if getCfValue(Quote, "EGAP_Contract_Start_Date") != '':
		year = UserPersonalizationHelper.CovertToDate(getCfValue(Quote, "EGAP_Contract_Start_Date")).Year
		if year in yearsList:
			executionYear = year
		else:
			executionYear = yearsList[-1] if len(yearsList) > 0 else str(DateTime.Now.Year)
	return executionYear
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
	
def addNewRow(Quote,container,productivity,mpaAvailable,activeServiceContract,excecutionCountry,entry,existing_deliverables,finalDeliverables,GES_location,GES_Valuecode):
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
		row["Execution_Year"] = str(getDefaultExecutionYear(Quote))
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


def getExecutionCountry(Quote):
	salesOrg = Quote.GetCustomField('Sales Area').Content
	currency = Quote.GetCustomField('Currency').Content
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
	if query is not None:
		return query.Execution_County
def populatelGraphicsLabCon(Quote,Product, LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename,GES_location,GES_Valuecode,msid_product):
	excecutionCountry = getExecutionCountry(Quote)
	queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = '{}'and Contract = '{}'".format(modulename,contractType))
	existing_deliverables = getExistingDeliverablegraphicsRowsDict(LabCon)
	finalDeliverables = []
	if not existing_deliverables.get(("Total", "Total")):
		row = LabCon.AddNewRow(False)
		row["Deliverable"] = "Total"
	finalDeliverables.append(("Total", "Total"))
	if not existing_deliverables.get(("Off-Site", "Offsite")):
		row = LabCon.AddNewRow(False)
		row["Deliverable"] = "Off-Site"
	finalDeliverables.append(("Off-Site", "Offsite"))
	if queryData is not None:
		for entry in queryData:
			deliverable_type = Product.ParseString(entry.Deliverable_Type)
			deliverable = entry.Deliverables
			key = (deliverable, deliverable_type)
			if deliverable_type == "Offsite":
				if existing_deliverables.get(key):
					row = existing_deliverables.get(key)
				else:
					row = LabCon.AddNewRow(False)
				finalDeliverables.append((deliverable,deliverable_type))
				Trace.Write("finalDeliverables"+str(finalDeliverables)+"entry"+str(entry.Deliverables)+"rowdeliverable"+str(row["Deliverable"]))
				row["Deliverable"] = deliverable
				row["Deliverable_Type"] = deliverable_type
				if row["Adjustment_Productivity"] == '':
					row["Adjustment_Productivity"] = AdjustmentProductivity
				if row["Execution_Year"] == '':
					row["Execution_Year"] = str(getDefaultExecutionYear(Quote))
				if row["FO_Eng"] == '':
					row["FO_Eng"] = entry.FO_Eng
				if GES_location :
					Trace.Write("GES_location"+str(GES_location)+"FO_Eng_Percentage_Split"+row["FO_Eng_Percentage_Split"])
					if row["FO_Eng_Percentage_Split"]  == '':
						Trace.Write("fovalue"+str(Product.ParseString(entry.FO_Eng_Split)))
						row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
					if row["GES_Eng_Percentage_Split"] == '':
						row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
					if row["GES_Eng"] == '':
						row["GES_Eng"] = "SVC_GES_P335B_{}".format(GES_Valuecode)
				else:
					if row["FO_Eng_Percentage_Split"] == '':
						row["FO_Eng_Percentage_Split"] = "100"
					if row["GES_Eng_Percentage_Split"] == '':
						row["GES_Eng_Percentage_Split"] = "0"
				if excecutionCountry:
					if row["Execution_Country"] == '':
						row["Execution_Country"] = excecutionCountry
		if not existing_deliverables.get(("On-Site", "Onsite")):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "On-Site"
		finalDeliverables.append(("On-Site","Onsite"))
		for entry in queryData:
			deliverable_type = Product.ParseString(entry.Deliverable_Type)
			deliverable = entry.Deliverables
			key = (deliverable, deliverable_type)
			if deliverable_type == "Onsite":
				if existing_deliverables.get(key):
					row = existing_deliverables.get(key)
				else:
					row = LabCon.AddNewRow(False)
				finalDeliverables.append((deliverable,deliverable_type))
				Trace.Write("finalDeliverables"+str(finalDeliverables)+"entry"+str(entry.Deliverables)+"rowdeliverable"+str(row["Deliverable"]))
				row["Deliverable"] = deliverable
				row["Deliverable_Type"] = deliverable_type
				if row["Adjustment_Productivity"] == '':
					row["Adjustment_Productivity"] = AdjustmentProductivity
				if row["Execution_Year"] == '':
					row["Execution_Year"] = str(getDefaultExecutionYear(Quote))
				if row["FO_Eng"] == '':
					row["FO_Eng"] = entry.FO_Eng
				if GES_location:
					if row["FO_Eng_Percentage_Split"] == '':
						row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
					if row["GES_Eng_Percentage_Split"] == '':
						row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
					if row["GES_Eng"] == '':
						row["GES_Eng"] = "SVC_GES_P335F_{}".format(GES_Valuecode)
				else:
					if row["FO_Eng_Percentage_Split"] == '':
						row["FO_Eng_Percentage_Split"] = "100"
					if row["GES_Eng_Percentage_Split"] == '':
						row["GES_Eng_Percentage_Split"] = "0"
				if excecutionCountry:
					if row["Execution_Country"] == '':
						row["Execution_Country"] = excecutionCountry
	deleteExistingDeliverablegraphicsrows(LabCon, finalDeliverables,msid_product)				

def populatelELCNCon(Product,Quote, elcnCon,elcnAdjustmentProductivity,mpaAvailable,activeServiceContract,GES_location,GES_Valuecode,msid_product):
	dataGatheringRequired = Product.Attr("MSID_FEL_Data_Gathering_Required").GetValue()
	offProcessSetup = Product.Attr("ELCN_Off_Process_Setup_Validation_Required").GetValue()
	willOpmandTPStoExperion = Product.Attr("ELCN_Will_OPM_or_TPS_to_Experion_be_performed").GetValue()
	elcnUpgradeNew = getContainer(Product, "ELCN_Upgrade_New_ELCN_Nodes")
	sum = migrationDDSCheck(elcnUpgradeNew)
	excecutionCountry = getExecutionCountry(Quote)
	queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = 'ELCN'")
	existing_deliverables = getExistingDeliverableRowsDict(elcnCon)
	finalDeliverables = []
	if not existing_deliverables.get("Total"):
		row = elcnCon.AddNewRow(False)
		row["Deliverable"] = "Total"
	finalDeliverables.append("Total")
	if not existing_deliverables.get("Off-Site"):
		row = elcnCon.AddNewRow(False)
		row["Deliverable"] = "Off-Site"
	finalDeliverables.append("Off-Site")
	if queryData is not None:
		for entry in queryData:
			if entry.Deliverable_Type == "Offsite":
				if (dataGatheringRequired == "NO" and entry.Deliverables == "FEL Site Visit Data Gathering") or (offProcessSetup in ('No','') and entry.Deliverables in ('Pre-FAT','FAT')) or (sum == 0 and entry.Deliverables == "Migration DDS"):
					continue
				finalDeliverables = addNewRow(Quote,elcnCon,elcnAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry,entry,existing_deliverables,finalDeliverables,GES_location,GES_Valuecode)
		if not existing_deliverables.get("On-Site"):
			row = elcnCon.AddNewRow(False)
			row["Deliverable"] = "On-Site"
		finalDeliverables.append("On-Site")
		for entry in queryData:
			if entry.Deliverable_Type == "Onsite":
				if willOpmandTPStoExperion == "Yes" and entry.Deliverables == "SAT":
					continue
				finalDeliverables = addNewRow(Quote,elcnCon,elcnAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry,entry,existing_deliverables,finalDeliverables,GES_location,GES_Valuecode)
	deleteExistingDeliverableRows(elcnCon, finalDeliverables,msid_product)

def populatelCBECCon(Quote,Product, cbecCon,cbecAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,GES_location,GES_Valuecode,msid_product):
	excecutionCountry = getExecutionCountry(Quote)
	queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = 'CB-EC Upgrade to C300-UHIO'and Contract = '{}'".format(contractType))
	existing_deliverables = getExistingDeliverableRowsDict(cbecCon)
	finalDeliverables = []
	if not existing_deliverables.get("Total"):
		row = cbecCon.AddNewRow(False)
		row["Deliverable"] = "Total"
	finalDeliverables.append("Total")
	if not existing_deliverables.get("Off-Site"):
		row = cbecCon.AddNewRow(False)
		row["Deliverable"] = "Off-Site"
	finalDeliverables.append("Off-Site")
	if queryData is not None:
		for entry in queryData:
			if entry.Deliverable_Type == "Offsite":
				finalDeliverables = addNewRow(Quote, cbecCon,cbecAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry,entry,existing_deliverables,finalDeliverables,GES_location,GES_Valuecode)
		if not existing_deliverables.get("On-Site"):
			row = cbecCon.AddNewRow(False)
			row["Deliverable"] = "On-Site"
		finalDeliverables.append("On-Site")
		for entry in queryData:
			if entry.Deliverable_Type == "Onsite":
				finalDeliverables = addNewRow(Quote, cbecCon,cbecAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry,entry,existing_deliverables,finalDeliverables,GES_location,GES_Valuecode)
	deleteExistingDeliverableRows(cbecCon, finalDeliverables,msid_product)

def populateLaborContainers(Quote,Product, container,productModule,activeServiceContract,GES_location,GES_Valuecode,msid_product):
	excecutionCountry = getExecutionCountry(Quote)
	queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = '{}' and Contract = '{}'".format(productModule,activeServiceContract))
	existing_deliverables = getExistingDeliverableRowsDict(container)
	finalDeliverables = []
	if queryData is not None:
		for entry in queryData:
			if existing_deliverables.get(entry.Deliverables):
				row = existing_deliverables.get(entry.Deliverables)
			else:
				row = container.AddNewRow(False)
			finalDeliverables.append(entry.Deliverables)
			row["Deliverable"] = entry.Deliverables
			row["Deliverable_Type"] = entry.Deliverable_Type if entry.Deliverable_Type else ''
			if row["FO_Eng"] == '':
				row["FO_Eng"] = entry.FO_Eng if entry.FO_Eng else ''
			if entry.Deliverables not in ('On-Site','Total','Off-Site'):
				if row["Execution_Year"] == '':
					row["Execution_Year"] = str(getDefaultExecutionYear(Quote))
			if entry.Deliverables not in ('Total','Off-Site','On-Site'):
				if row["Adjustment_Productivity"] == '':
					row["Adjustment_Productivity"] = "1"
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
					if row["Execution_Country"] == '':
						row["Execution_Country"] = excecutionCountry
	deleteExistingDeliverableRows(container, finalDeliverables,msid_product)



def populateprojectManagementCon(Quote, Product,projectManagementCon,pmAdjustmentProductivity,mpaAvailable,activeServiceContract,GES_location,GES_Valuecode,msid_product):
	excecutionCountry = getExecutionCountry(Quote)
	queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = 'PM'")
	existing_deliverables = getExistingDeliverableRowsDict(projectManagementCon)
	finalDeliverables = []
	if not existing_deliverables.get("Total"):
		row = projectManagementCon.AddNewRow(False)
		row["Deliverable"] = "Total"
	finalDeliverables.append("Total")
	if queryData is not None:
		for entry in queryData:
			if entry.Deliverable_Type == "Offsite":
				if existing_deliverables.get(entry.Deliverables):
					row = existing_deliverables.get(entry.Deliverables)
				else:
					row = projectManagementCon.AddNewRow(False)
				finalDeliverables.append(entry.Deliverables)
				row["Deliverable"] = entry.Deliverables
				if row["Adjustment_Productivity"] == '':
					row["Adjustment_Productivity"] = pmAdjustmentProductivity
				row["Deliverable_Flag"] = entry.Deliverable_Flag
				row["Deliverable_Type"] = entry.Deliverable_Type
				if row["FO_Eng_Percentage_Split"] == '':
					row["FO_Eng_Percentage_Split"] = "100"
				if row["GES_Eng_Percentage_Split"] == '':
					row["GES_Eng_Percentage_Split"] = "0"
				if row["Deliverable_Flag"] == "PM":
					if mpaAvailable or activeServiceContract == "Yes":
						if row["FO_Eng"] == '':
							row["FO_Eng"] = "SVC-PMGT-ST"
					else:
						if row["FO_Eng"] == '':
							row["FO_Eng"] = "SVC-PMGT-ST-NC"
				elif row["Deliverable_Flag"] == "PA":
					if mpaAvailable or activeServiceContract == "Yes":
						if row["FO_Eng"] == '':
							row["FO_Eng"] = "SVC-PADM-ST"
					else:
						if row["FO_Eng"] == '':
							row["FO_Eng"] = "SVC-PADM-ST-NC"
				if row["Execution_Year"] == '':
					row["Execution_Year"] = str(getDefaultExecutionYear(Quote))
				if GES_location:
					if row["GES_Eng"] == '':
						row["GES_Eng"] = "SVC_GES_P215B_{}".format(GES_Valuecode)
				else:
					Trace.Write("MSID_GES_Location not found in the product!!")
				if excecutionCountry:
					if row["Execution_Country"] == '':
						row["Execution_Country"] = excecutionCountry
	deleteExistingDeliverableRows(projectManagementCon, finalDeliverables,msid_product)
	
def populatelThirdpartyPLC_UOC_LabCon(Product,Quote, LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename,GES_location,GES_Valuecode,msid_product):
	excecutionCountry = getExecutionCountry(Quote)
	queryData = SqlHelper.GetList("select * from TABLE_3RD_PARTY_PLC_UOC_LABOR_DELIVERABLES")
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
					row["Execution_Year"] = str(getDefaultExecutionYear(Quote))
				if mpaAvailable or activeServiceContract == "Yes":
					if row["FO_Eng"] == '':
						row["FO_Eng"] = entry.FO_Eng
				else:
					if row["FO_Eng"] == '':
						row["FO_Eng"] = str(entry.FO_Eng) + '-NC'
				if GES_location :
					if row["FO_Eng_Percentage_Split"] == '':
						row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
					if row["GES_Eng_Percentage_Split"] == '':
						row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
					if row["GES_Eng"] == '':
						row["GES_Eng"] = "SVC_GES_PLCB_{}".format(GES_Valuecode)
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
					row["Execution_Year"] = str(getDefaultExecutionYear(Quote))
				if mpaAvailable or activeServiceContract == "Yes":
					if row["FO_Eng"] == '':
						row["FO_Eng"] = entry.FO_Eng
				else:
					if row["FO_Eng"] == '':
						row["FO_Eng"] = entry.FO_Eng + '-NC'
				if GES_location:
					if row["FO_Eng_Percentage_Split"] == '':
						row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
					if row["GES_Eng_Percentage_Split"] == '':
						row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
					if row["GES_Eng"] == '':
						row["GES_Eng"] = "SVC_GES_PLCB_{}".format(GES_Valuecode)
				else:
					if row["FO_Eng_Percentage_Split"] == '':
						row["FO_Eng_Percentage_Split"] = "100"
					if row["GES_Eng_Percentage_Split"] == '':
						row["GES_Eng_Percentage_Split"] = "0"
				if excecutionCountry:
					if row["Execution_Country"] == '':
						row["Execution_Country"] = excecutionCountry
	deleteExistingDeliverableRows(LabCon, finalDeliverables,msid_product)