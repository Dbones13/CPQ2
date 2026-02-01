from System import DateTime

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
	query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date < '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date > '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
	res = SqlHelper.GetList(query)
	if res and len(res) > 0:
		PricePlanPresent = True
	return PricePlanPresent

def getExecutionCountry():
	marketCode = Quote.SelectedMarket.MarketCode
	#salesOrg = marketCode.partition('_')[0]
	#Updated logic for Defect 27359
	#currency = marketCode.partition('_')[2]
	salesOrg = Quote.GetCustomField('Sales Area').Content
	currency = Quote.GetCustomField('Currency').Content
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
	#query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))
	if query is not None:
		return query.Execution_County

def populatelVirtualizationLabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
	if LabCon.Rows.Count == 0:
		excecutionCountry = getExecutionCountry()
		queryData = SqlHelper.GetList("select * from VIRTUALIZATION_LABOR_DELIVERABLES")
		row = LabCon.AddNewRow(False)
		row["Deliverable"] = "Total"
		row = LabCon.AddNewRow(False)
		row["Deliverable"] = "Off-Site"
		if queryData is not None:
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Offsite":
					row = LabCon.AddNewRow(False)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Offsite"
					row["Adjustment_Productivity"] = AdjustmentProductivity
					row["Execution_Year"] = str(executionYear)
					if mpaAvailable or activeServiceContract == "Yes":
						row["FO_Eng"] = entry.FO_Eng
					else:
						row["FO_Eng"] = entry.FO_Eng + '-NC'
					try:
						if getAttrValue("MSID_GES_Location") != 'None':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
							row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					except:
						row["FO_Eng_Percentage_Split"] = "100"
						row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						row["Execution_Country"] = excecutionCountry
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "On-Site"
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Onsite":
					row = LabCon.AddNewRow(False)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Onsite"
					row["Adjustment_Productivity"] = AdjustmentProductivity
					row["Execution_Year"] = str(executionYear)
					if mpaAvailable or activeServiceContract == "Yes":
						row["FO_Eng"] = entry.FO_Eng
					else:
						row["FO_Eng"] = entry.FO_Eng + '-NC'
					try:
						if getAttrValue("MSID_GES_Location") != 'None':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
							row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					except:
						row["FO_Eng_Percentage_Split"] = "100"
						row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						row["Execution_Country"] = excecutionCountry

def populatelGenericLabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
	if LabCon.Rows.Count == 0:
		excecutionCountry = getExecutionCountry()
		queryData = SqlHelper.GetList("select * from GENERIC_LABOR_DELIVERABLES")
		row = LabCon.AddNewRow(False)
		row["Deliverable"] = "Total"
		row = LabCon.AddNewRow(False)
		row["Deliverable"] = "Off-Site"
		if queryData is not None:
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Offsite":
					row = LabCon.AddNewRow(False)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Offsite"
					row["Adjustment_Productivity"] = AdjustmentProductivity
					row["Execution_Year"] = str(executionYear)
					if mpaAvailable or activeServiceContract == "Yes":
						row["FO_Eng"] = entry.FO_Eng
					else:
						row["FO_Eng"] = entry.FO_Eng + '-NC'
					try:
						if getAttrValue("MSID_GES_Location") != 'None':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
							row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					except:
						row["FO_Eng_Percentage_Split"] = "100"
						row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						row["Execution_Country"] = excecutionCountry
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "On-Site"
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Onsite":
					row = LabCon.AddNewRow(False)
					Trace.Write(entry.Deliverables)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Onsite"
					row["Adjustment_Productivity"] = AdjustmentProductivity
					row["Execution_Year"] = str(executionYear)
					if mpaAvailable or activeServiceContract == "Yes":
						row["FO_Eng"] = entry.FO_Eng
					else:
						row["FO_Eng"] = entry.FO_Eng + '-NC'
					try:
						if getAttrValue("MSID_GES_Location") != 'None':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
							row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					except:
						row["FO_Eng_Percentage_Split"] = "100"
						row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						row["Execution_Country"] = excecutionCountry

def populatelQCSRAELabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
	if LabCon.Rows.Count == 0:
		excecutionCountry = getExecutionCountry()
		queryData = SqlHelper.GetList("select * from QCS_RAE_UPGRADE_LABOR_DELIVERABLES_MSID")
		row = LabCon.AddNewRow(False)
		row["Deliverable"] = "Total"
		row = LabCon.AddNewRow(False)
		row["Deliverable"] = "Off-Site"
		if queryData is not None:
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Offsite":
					row = LabCon.AddNewRow(False)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Offsite"
					row["Adjustment_Productivity"] = AdjustmentProductivity
					row["Execution_Year"] = str(executionYear)
					if mpaAvailable or activeServiceContract == "Yes":
						row["FO_Eng"] = entry.FO_Eng
					else:
						row["FO_Eng"] = entry.FO_Eng + '-NC'
					try:
						if getAttrValue("MSID_GES_Location") != 'None':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
							if row["Deliverable"] == "In-house Engineering MD-CD":
								row["GES_Eng"] = "SVC_GES_P350B_CN"
							else:
								row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					except:
						if row["Deliverable"] in ("In-house Engineering MD-CD","Server/Station Build"):
							row["FO_Eng_Percentage_Split"] = "0"
							row["GES_Eng_Percentage_Split"] = "0"
						else:
							row["FO_Eng_Percentage_Split"] = "100"
							row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						row["Execution_Country"] = excecutionCountry
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "On-Site"
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Onsite":
					row = LabCon.AddNewRow(False)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Onsite"
					row["Adjustment_Productivity"] = AdjustmentProductivity
					row["Execution_Year"] = str(executionYear)
					if mpaAvailable or activeServiceContract == "Yes":
						row["FO_Eng"] = entry.FO_Eng
					else:
						row["FO_Eng"] = entry.FO_Eng + '-NC'
					try:
						if getAttrValue("MSID_GES_Location") != 'None':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
							row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					except:
						row["FO_Eng_Percentage_Split"] = "100"
						row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						row["Execution_Country"] = excecutionCountry

def populatelTPALabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
	if LabCon.Rows.Count == 0:
		excecutionCountry = getExecutionCountry()
		queryData = SqlHelper.GetList("select * from TPAPMD_MIGRATION_LABOR_DELIVERABLES")
		row = LabCon.AddNewRow(False)
		row["Deliverable"] = "Total"
		row = LabCon.AddNewRow(False)
		row["Deliverable"] = "Off-Site"
		if queryData is not None:
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Offsite":
					row = LabCon.AddNewRow(False)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Offsite"
					row["Adjustment_Productivity"] = AdjustmentProductivity
					row["Execution_Year"] = str(executionYear)
					if mpaAvailable or activeServiceContract == "Yes":
						row["FO_Eng"] = entry.FO_Eng
					else:
						row["FO_Eng"] = entry.FO_Eng + '-NC'
					try:
						if getAttrValue("MSID_GES_Location") != 'None':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
							row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					except:
						row["FO_Eng_Percentage_Split"] = "100"
						row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						row["Execution_Country"] = excecutionCountry
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "On-Site"
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Onsite":
					row = LabCon.AddNewRow(False)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Onsite"
					row["Adjustment_Productivity"] = AdjustmentProductivity
					row["Execution_Year"] = str(executionYear)
					if mpaAvailable or activeServiceContract == "Yes":
						row["FO_Eng"] = entry.FO_Eng
					else:
						row["FO_Eng"] = entry.FO_Eng + '-NC'
					try:
						if getAttrValue("MSID_GES_Location") != 'None':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
							row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					except:
						row["FO_Eng_Percentage_Split"] = "100"
						row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						row["Execution_Country"] = excecutionCountry
# To have few common functionalities for Labor deliverables tab -- Janhavi Tanna : CXCPQ-60159 :start
def populatelELEPIULabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
	Trace.Write("test:::")
	if LabCon.Rows.Count == 0:
		excecutionCountry = getExecutionCountry()
		queryData = SqlHelper.GetList("select * from ELEPIU_MIGRATION_LABOR_DELIVERABLES")
		row = LabCon.AddNewRow(False)
		row["Deliverable"] = "Total"
		row = LabCon.AddNewRow(False)
		row["Deliverable"] = "Off-Site"
		if queryData is not None:
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Offsite":
					row = LabCon.AddNewRow(False)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Offsite"
					row["Adjustment_Productivity"] = AdjustmentProductivity
					row["Execution_Year"] = str(executionYear)
					if mpaAvailable or activeServiceContract == "Yes":
						row["FO_Eng"] = entry.FO_Eng
					else:
						row["FO_Eng"] = entry.FO_Eng + '-NC'
					try:
						if getAttrValue("MSID_GES_Location") != 'None':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
							row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					except:

						row["FO_Eng_Percentage_Split"] = "100"
						row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						row["Execution_Country"] = excecutionCountry
			row = LabCon.AddNewRow(False)
			row["Deliverable"] = "On-Site"
			for entry in queryData:
				if Product.ParseString(entry.Deliverable_Type) == "Onsite":
					row = LabCon.AddNewRow(False)
					row["Deliverable"] = entry.Deliverables
					row["Deliverable_Type"] = "Onsite"
					row["Adjustment_Productivity"] = AdjustmentProductivity
					row["Execution_Year"] = str(executionYear)
					if mpaAvailable or activeServiceContract == "Yes":
						row["FO_Eng"] = entry.FO_Eng
					else:
						row["FO_Eng"] = entry.FO_Eng + '-NC'
					try:
						if getAttrValue("MSID_GES_Location") != 'None':
							row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
							row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
							row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
					except:
						row["FO_Eng_Percentage_Split"] = "100"
						row["GES_Eng_Percentage_Split"] = "0"
					if excecutionCountry:
						row["Execution_Country"] = excecutionCountry
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
	msidCont = Product.GetContainerByName("CONT_MSID_SUBPRD")
	for row in msidCont.Rows:
		#if row["Selected_Products"] == "OPM":
		Product = row.Product
		selectedProducts = row["Selected_Products"]

	#selectedProducts = Product.Attr('MSID_Selected_Products').GetValue().split('<br>')

	#if foPartNumberCon.Rows.Count == 0:
		#ScriptExecutor.Execute('PS_PopulatePartNumberContainer')

	populatelVirtualizationLabCon( virtualizationCon,virtualizationAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"Virtualization System") if "Virtualization System" in selectedProducts else 0
	populatelQCSRAELabCon( QCSRAECon,QCSRAEAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"QCS RAE Upgrade") if "QCS RAE Upgrade" in selectedProducts else 0
	populatelTPALabCon( TPACon,TPAAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"TPA/PMD Migration") if "TPA/PMD Migration" in selectedProducts else 0
	populatelELEPIULabCon( ELEPIUCon,ELEPIUAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"ELEPIU ControlEdge RTU Migration Engineering") if "ELEPIU ControlEdge RTU Migration Engineering" in selectedProducts else 0
	if 'Generic System' in selectedProducts:
		prod_count = Product.GetContainerByName('MSID_Product_Container_Generic_hidden').Rows.Count
		for i in range(1,prod_count+1):
			cont_name = 'MSID_Labor_Generic_System'+str(i)+'_Cont'
			cont = getContainer(cont_name)
			#cont.Clear()
			populatelGenericLabCon( cont,str(1),mpaAvailable,activeServiceContract,contractType,"Generic System")