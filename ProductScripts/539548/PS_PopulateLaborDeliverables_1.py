isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if not isR2Qquote:
	from System import DateTime
	from GS_Migration_Labor_HelperFunctions import getExistingDeliverableRowsDict, deleteExistingDeliverableRows

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
		salesOrg = Quote.GetCustomField('Sales Area').Content
		currency = Quote.GetCustomField('Currency').Content
		query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
		#query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))
		if query is not None:
			return query.Execution_County

	def populatelVirtualizationLabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
		#if LabCon.Rows.Count == 0:
		excecutionCountry = getExecutionCountry()
		queryData = SqlHelper.GetList("select * from VIRTUALIZATION_LABOR_DELIVERABLES")
		existing_deliverables = getExistingDeliverableRowsDict(LabCon)
		finalDeliverables = []
		if not existing_deliverables.get("Total"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Total"
		finalDeliverables.append("Total")
		#row = LabCon.AddNewRow(False)
		#row["Deliverable"] = "Off-Site"
		if not existing_deliverables.get("Off-Site"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Off-Site"
		finalDeliverables.append("Off-Site")
		if queryData is not None:
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Offsite":
					#row = LabCon.AddNewRow(False)
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
					if mpaAvailable or activeServiceContract == "Yes":
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng
					else:
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng + '-NC'
					if GES_Loc:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
						if row["GES_Eng"] == '':
							row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					else:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = "100"
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] == '':
							row["Execution_Country"] = excecutionCountry
			#row = LabCon.AddNewRow(False)
			#row["Deliverable"] = "On-Site"
			if not existing_deliverables.get("On-Site"):
				row = LabCon.AddNewRow(False)
				row["Deliverable"] = "On-Site"
			finalDeliverables.append("On-Site")
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Onsite":
					#row = LabCon.AddNewRow(False)
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
					if mpaAvailable or activeServiceContract == "Yes":
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng
					else:
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng + '-NC'
					if GES_Loc:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
						if row["GES_Eng"] == '':
							row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					else:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = "100"
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] == '':
							row["Execution_Country"] = excecutionCountry
		deleteExistingDeliverableRows(LabCon, finalDeliverables,msidnewproduct)

	def populatelGenericLabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
		#if LabCon.Rows.Count == 0:
		excecutionCountry = getExecutionCountry()
		queryData = SqlHelper.GetList("select * from GENERIC_LABOR_DELIVERABLES")
		existing_deliverables = getExistingDeliverableRowsDict(LabCon)
		finalDeliverables = []
		#row = LabCon.AddNewRow(False)
		#row["Deliverable"] = "Total"
		if not existing_deliverables.get("Total"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Total"
		finalDeliverables.append("Total")
		#row = LabCon.AddNewRow(False)
		#row["Deliverable"] = "Off-Site"
		if not existing_deliverables.get("Off-Site"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Off-Site"
		finalDeliverables.append("Off-Site")
		if queryData is not None:
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Offsite":
					#row = LabCon.AddNewRow(False)
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
					if mpaAvailable or activeServiceContract == "Yes":
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng
					else:
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng + '-NC'
					if GES_Loc:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
						if row["GES_Eng"] == '':
							row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					else:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = "100"
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] == '':
							row["Execution_Country"] = excecutionCountry
			#row = LabCon.AddNewRow(False)
			#row["Deliverable"] = "On-Site"
			if not existing_deliverables.get("On-Site"):
				row = LabCon.AddNewRow(False)
				row["Deliverable"] = "On-Site"
			finalDeliverables.append("On-Site")
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Onsite":
					#row = LabCon.AddNewRow(False)
					if existing_deliverables.get(entry.Deliverables):
						row = existing_deliverables.get(entry.Deliverables)
					else:
						row = LabCon.AddNewRow(False)
					finalDeliverables.append(entry.Deliverables)
					Trace.Write(entry.Deliverables)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Onsite"
					if row["Adjustment_Productivity"] == '':
						row["Adjustment_Productivity"] = AdjustmentProductivity
					if row["Execution_Year"] == '':
						row["Execution_Year"] = str(executionYear)
					if mpaAvailable or activeServiceContract == "Yes":
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng
					else:
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng + '-NC'
					if GES_Loc:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
						if row["GES_Eng"] == '':
							row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					else:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = "100"
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] == '':
							row["Execution_Country"] = excecutionCountry
		deleteExistingDeliverableRows(LabCon, finalDeliverables,msidnewproduct)

	def populatelQCSRAELabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
		#if LabCon.Rows.Count == 0:
		excecutionCountry = getExecutionCountry()
		queryData = SqlHelper.GetList("select * from QCS_RAE_UPGRADE_LABOR_DELIVERABLES_MSID")
		#row = LabCon.AddNewRow(False)
		#row["Deliverable"] = "Total"
		existing_deliverables = getExistingDeliverableRowsDict(LabCon)
		finalDeliverables = []
		if not existing_deliverables.get("Total"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Total"
		finalDeliverables.append("Total")
		#row = LabCon.AddNewRow(False)
		#row["Deliverable"] = "Off-Site"
		if not existing_deliverables.get("Off-Site"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Off-Site"
		finalDeliverables.append("Off-Site")
		if queryData is not None:
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Offsite":
					#row = LabCon.AddNewRow(False)
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
					if mpaAvailable or activeServiceContract == "Yes":
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng
					else:
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng + '-NC'
					if GES_Loc:
						#Trace.Write("ges_eng"+getAttrValue("MSID_GES_Location"))
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
						if row["Deliverable"] == "In-house Engineering MD-CD":
							if row["GES_Eng"] == '':
								row["GES_Eng"] = "SVC_GES_P350B_CN"
						else:
							if row["GES_Eng"] == '':
								row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					else:
						if row["Deliverable"] in ("In-house Engineering MD-CD","Server/Station Build"):
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
			#row = LabCon.AddNewRow(False)
			#row["Deliverable"] = "On-Site"
			if not existing_deliverables.get("On-Site"):
				row = LabCon.AddNewRow(False)
				row["Deliverable"] = "On-Site"
			finalDeliverables.append("On-Site")
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Onsite":
					#row = LabCon.AddNewRow(False)
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
					if mpaAvailable or activeServiceContract == "Yes":
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng
					else:
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng + '-NC'
					if GES_Loc:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
						if row["GES_Eng"] == '':
							row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					else:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = "100"
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] == '':
							row["Execution_Country"] = excecutionCountry
		deleteExistingDeliverableRows(LabCon, finalDeliverables,msidnewproduct)

	def populatelTPALabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename,msid_product):
		#if LabCon.Rows.Count == 0:
		excecutionCountry = getExecutionCountry()
		queryData = SqlHelper.GetList("select * from TPAPMD_MIGRATION_LABOR_DELIVERABLES")
		existing_deliverables = getExistingDeliverableRowsDict(LabCon)
		finalDeliverables = []
		#row = LabCon.AddNewRow(False)
		#row["Deliverable"] = "Total"
		if not existing_deliverables.get("Total"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Total"
		finalDeliverables.append("Total")
		#row = LabCon.AddNewRow(False)
		#row["Deliverable"] = "Off-Site"
		if not existing_deliverables.get("Off-Site"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Off-Site"
		finalDeliverables.append("Off-Site")
		if queryData is not None:
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Offsite":
					#row = LabCon.AddNewRow(False)
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
					if mpaAvailable or activeServiceContract == "Yes":
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng
					else:
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng + '-NC'
					if GES_Loc:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = msid_product.ParseString(entry.FO_Eng_Split)
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = msid_product.ParseString(entry.GES_Eng_Split)
						if row["GES_Eng"] == '':
							row["GES_Eng"] = "SVC_GES_P350B_{}".format(GES_VC)
					else:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = "100"
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] == '':
							row["Execution_Country"] = excecutionCountry
			#row = LabCon.AddNewRow(False)
			#row["Deliverable"] = "On-Site"
			if not existing_deliverables.get("On-Site"):
				row = LabCon.AddNewRow(False)
				row["Deliverable"] = "On-Site"
			finalDeliverables.append("On-Site")
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Onsite":
					#row = LabCon.AddNewRow(False)
					if entry.Deliverable_Type == "Onsite":
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
					if mpaAvailable or activeServiceContract == "Yes":
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng
					else:
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng + '-NC'
					if GES_Loc:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
						if row["GES_Eng_Percentage_Split"] == '':    
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
						if row["GES_Eng"] == '':  
							row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					else:
						if row["FO_Eng_Percentage_Split"] == '': 
							row["FO_Eng_Percentage_Split"] = "100"
						if row["GES_Eng_Percentage_Split"] == '': 
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] == '':
							row["Execution_Country"] = excecutionCountry
		deleteExistingDeliverableRows(LabCon, finalDeliverables,msidnewproduct) 

	# To have few common functionalities for Labor deliverables tab -- Janhavi Tanna : CXCPQ-60159 :start
	def populatelELEPIULabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
		#if LabCon.Rows.Count == 0:
		excecutionCountry = getExecutionCountry()
		queryData = SqlHelper.GetList("select * from ELEPIU_MIGRATION_LABOR_DELIVERABLES")
		existing_deliverables = getExistingDeliverableRowsDict(LabCon)
		finalDeliverables = []
		#row = LabCon.AddNewRow(False)
		#row["Deliverable"] = "Total"
		if not existing_deliverables.get("Total"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Total"
		finalDeliverables.append("Total")
		#row = LabCon.AddNewRow(False)
		#row["Deliverable"] = "Off-Site"
		if not existing_deliverables.get("Off-Site"):
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "Off-Site"
		finalDeliverables.append("Off-Site")
		if queryData is not None:
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Offsite":
					#row = LabCon.AddNewRow(False)
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
					if mpaAvailable or activeServiceContract == "Yes":
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng
					else:
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng + '-NC'
					if GES_Loc:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
						if row["GES_Eng"] == '':
							row["GES_Eng"] = "SVC_GES_P350B_{}".format(GES_VC)
					else:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = "100"
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] == '':
							row["Execution_Country"] = excecutionCountry
			#row = LabCon.AddNewRow(False)
			#row["Deliverable"] = "On-Site"
			if not existing_deliverables.get("On-Site"):
				row = LabCon.AddNewRow(False)
				row["Deliverable"] = "On-Site"
			finalDeliverables.append("On-Site")
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Onsite":
					#row = LabCon.AddNewRow(False)
					if entry.Deliverable_Type == "Onsite":
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
					if mpaAvailable or activeServiceContract == "Yes":
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng
					else:
						if row["FO_Eng"] == '':
							row["FO_Eng"] = entry.FO_Eng + '-NC'
					if GES_Loc:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
						if row["GES_Eng"] == '':
							row["GES_Eng"] = "SVC_GES_P350F_{}".format(GES_VC)
					else:
						if row["FO_Eng_Percentage_Split"] == '':
							row["FO_Eng_Percentage_Split"] = "100"
						if row["GES_Eng_Percentage_Split"] == '':
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						if row["Execution_Country"] == '':
							row["Execution_Country"] = excecutionCountry
		deleteExistingDeliverableRows(LabCon, finalDeliverables,msidnewproduct)
	#-- Janhavi Tanna : CXCPQ-60159 :end

	if Product.Attr('MIgration_Scope_Choices').GetValue() != "HW/SW":
		excecutionCountry = getExecutionCountry()
		executionYear = getDefaultExecutionYear()
		#foPartNumberCon = getContainer("MSID_Labor_FO_Part_Number")
		virtualizationCon = getContainer("MSID_Labor_Virtualization_con")
		virtualizationAdjustmentProductivity = getAttrValue("Virtualization_Adjustment_Productivity") if getAttrValue("Virtualization_Adjustment_Productivity") else "1"
		QCSRAECon = getContainer("MSID_Labor_QCS_RAE_Upgrade_con")
		QCSRAEAdjustmentProductivity = getAttrValue("QCS_RAE_Upgrade_Adjustment_Productivity")
		TPACon = getContainer("MSID_Labor_TPA_con")
		TPAAdjustmentProductivity = getAttrValue("TPA_Adjustment_Productivity")
		# To have few common functionalities for Labor deliverables tab -- Janhavi Tanna : CXCPQ-60159 :start
		ELEPIUCon = getContainer("MSID_Labor_ELEPIU_con")
		ELEPIUAdjustmentProductivity = getAttrValue("ELEPIU_Adjustment_Productivity")
		#-- Janhavi Tanna : CXCPQ-60159 :end
		mpaAvailable = checkForMPACustomer()
		activeServiceContract = getAttrValue("MSID_Active_Service_Contract")
		if activeServiceContract == 'Yes' or mpaAvailable:
			contractType = "Contract"
		else:
			contractType = "Non-Contract"

		#selectedProducts = Product.Attr('MSID_Selected_Products').GetValue().split('<br>')
		GES_Loc=getAttrValue("MSID_GES_Location") if getAttrValue("MSID_GES_Location") != 'None' else ''
		GES_VC=TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>')
		msidnewproduct = Product
		msidCont = Product.GetContainerByName("CONT_MSID_SUBPRD")
		gensyscount = 0
		for genrow in msidCont.Rows:
			if 'Generic System' in genrow['Product Name']:
				gensyscount = int(str(genrow['Product Name']).split()[-1])
				if genrow['Product Name'] == 'Generic System 1':
					Product.Attr('MSID_Labor_Generic_System1_Cont').LabelFormula = str(genrow['User_Define_Name']) if genrow['User_Define_Name'] else '<!-->'
				elif genrow['Product Name'] == 'Generic System 2' :
					Product.Attr('MSID_Labor_Generic_System2_Cont').LabelFormula = str(genrow['User_Define_Name']) if genrow['User_Define_Name'] else '<!-->'
				elif genrow['Product Name'] == 'Generic System 3':
					Product.Attr('MSID_Labor_Generic_System3_Cont').LabelFormula = str(genrow['User_Define_Name']) if genrow['User_Define_Name'] else '<!-->'
				elif genrow['Product Name'] == 'Generic System 4' :
					Product.Attr('MSID_Labor_Generic_System4_Cont').LabelFormula = str(genrow['User_Define_Name']) if genrow['User_Define_Name'] else '<!-->'
				elif genrow['Product Name'] == 'Generic System 5' :
					Product.Attr('MSID_Labor_Generic_System5_Cont').LabelFormula = str(genrow['User_Define_Name']) if genrow['User_Define_Name'] else '<!-->'

		for row in msidCont.Rows:
			selectedProducts = row.Product.Name
			Trace.Write("aaa::"+str(selectedProducts))
			msid_product = row.Product


		#if foPartNumberCon.Rows.Count == 0:
			#ScriptExecutor.Execute('PS_PopulatePartNumberContainer')

			populatelVirtualizationLabCon( virtualizationCon,virtualizationAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"Virtualization System") if "Virtualization System" in selectedProducts else 0
			populatelQCSRAELabCon( QCSRAECon,QCSRAEAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"QCS RAE Upgrade") if "QCS RAE Upgrade" in selectedProducts else 0
			populatelTPALabCon( TPACon,TPAAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"TPA/PMD Migration",msid_product) if "TPA/PMD Migration" in selectedProducts else 0
			populatelELEPIULabCon( ELEPIUCon,ELEPIUAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"ELEPIU ControlEdge RTU Migration Engineering") if "ELEPIU ControlEdge RTU Migration Engineering" in selectedProducts else 0
			if 'Generic System Migration' in selectedProducts:
				#prod_count = msid_product.GetContainerByName('MSID_Product_Container_Generic_hidden').Rows.Count
				#gensyscount = 1 #if prod_count == 0 else prod_count
				for i in range(1,gensyscount+1):
					cont_name = 'MSID_Labor_Generic_System'+str(i)+'_Cont'
					cont = getContainer(cont_name)
					#cont.Clear()
					populatelGenericLabCon( cont,str(1),mpaAvailable,activeServiceContract,contractType,"Generic System")