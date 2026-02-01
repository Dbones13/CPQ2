import GS_HCI_PHD_Module
from System import DateTime
import math

Product.ResetAttr('AR_HCI_SELECTALL')
salesOrg = Quote.GetCustomField("Sales Area").Content
currency=Quote.GetCustomField("Currency").Content if Quote.GetCustomField("Currency").Content else 'USD'
alternate_execution_country = Quote.GetCustomField('R2Q_Alternate_Execution_Country').Content
R2Qexecution_year = Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content
Product.Attributes.GetByName('HCI_PHD_IsRequired').SelectDisplayValue('1')
def getExecutionCountry():
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
	if query is not None:
		return query.Execution_County

def addColumns(row,finalHrs,calcHrs,totalCost,totalListPrice,totalWTWCost):
	row['Deliverable']='Total'
	row['Final Hrs']=str(finalHrs)
	row['Calculated Hrs']=str(calcHrs)
	row['Eng Total Regional Cost']=str(totalCost)
	row['Eng Total List Price']=str(totalListPrice)
	row['Eng Total WTW Cost']=str(totalWTWCost)

def gesCostValues(cost, partNumber,currency):
	EACCost=GS_HCI_PHD_Module.getEACCost(partNumber,currency)
	reginoalCost=cost+EACCost
	w2wFactor=GS_HCI_PHD_Module.getW2WFactor(partNumber)
	w2wCost=reginoalCost/(1+w2wFactor)
	return reginoalCost,w2wCost 

laborquery=SqlHelper.GetList("select Labor,Service_Material from CT_HCI_PHD_LABORMATERIAL")
laborDetails={}
for lab in laborquery:
	laborDetails[lab.Labor]=lab.Service_Material
	
#Intialize all variables and calculate Technical scope values
totalInterfaceHours=0
Hrs_Tags=0
prjCmpSimple=0
prjCmpTypical=0
prjCmpComplex=0
No_Tags=0
No_Calcs=0
No_RDIs=0
No_Nodes=0
No_Monitor_Items=0
No_Honeywell_Nodes=0
No_Condition_Items=0
No_Historised_Monitor_Items=0
No_USM_Items=0
No_Displays=0
Hrs_Calcs=0
No_ERPandOther=0
Sum_ERPandOther=0
No_3rd_party_clients=0
contRows=Product.GetContainerByName('HCI_PHD_Tech_Scope').Rows
Trace.Write('tech scope')
for row in contRows:
	sysInterfaced=row['System to be interfaced to']
	Trace.Write('sysInterfaced--'+str(sysInterfaced))
	if sysInterfaced:
		sysDetails=SqlHelper.GetFirst("select * from CT_SYSINTERFACED where Value='{}'".format(sysInterfaced))
		Trace.Write('00000000000')
		if sysDetails.IsERP!='Yes':
			conComplexity=row['Interface Connectivity Complexity'] if row['Interface Connectivity Complexity'] else 'Simple'
			Trace.Write('complexity---'+str([sysDetails,conComplexity]))
			interfaceHrs = int(row['Number of Connections']) * float(getattr(sysDetails, conComplexity))
			totalInterfaceHours += interfaceHrs
			tagComplexity=row['Tag configuration Complexity'] + '_Tag' if row['Tag configuration Complexity'] else 'Simple_Tag'
			tagsHrs = 10 + (int(row['Number of Collected Tags']) * float(getattr(sysDetails, tagComplexity)))
			Hrs_Tags += tagsHrs
			No_Tags += int(row['Number of Collected Tags'])
			No_RDIs += int(row['Number of Connections'])
			if conComplexity=='Simple':
				prjCmpSimple += interfaceHrs
			if conComplexity=='Typical':
				prjCmpTypical += interfaceHrs
			if conComplexity=='Complex':
				prjCmpComplex += interfaceHrs
			if tagComplexity=='Simple_Tag':
				prjCmpSimple += tagsHrs
			if tagComplexity=='Typical_Tag':
				prjCmpTypical += tagsHrs
			if tagComplexity=='Complex_Tag':
				prjCmpComplex += tagsHrs
		else:
			conComplexity=row['Interface Connectivity Complexity']
			Sum_ERPandOther += int(row['Number of Connections']) * float(getattr(sysDetails, conComplexity))
			No_ERPandOther += int(row['Number of Connections'])
			

scopeDetails=SqlHelper.GetList("select Scope,Simple,Typical,Complex from CT_PHD_TECH_SCOPE")
scopeDict={}
for scope in scopeDetails:
	scopeDict[scope.Scope]=scope
	
scope='Virtual Calculations'
contCalcRow=Product.GetContainerByName('HCI_PHD_VirtualCalculations').Rows[0]
Hrs_Calcs=int(contCalcRow['Number of simple virtual calculations'])*float( getattr(scopeDict[scope], 'Simple')) + int(contCalcRow['Number of medium virtual calculations'])*float(getattr(scopeDict[scope], 'Typical')) + int(contCalcRow['Number of complex virtual calculations'])*float(getattr(scopeDict[scope], 'Complex'))

prjCmpSimple += int(contCalcRow['Number of simple virtual calculations'])*float( getattr(scopeDict[scope], 'Simple'))
prjCmpTypical += int(contCalcRow['Number of medium virtual calculations'])*float(getattr(scopeDict[scope], 'Typical'))
prjCmpComplex += int(contCalcRow['Number of complex virtual calculations'])*float(getattr(scopeDict[scope], 'Complex'))
No_Calcs = int(contCalcRow['Number of simple virtual calculations']) + int(contCalcRow['Number of medium virtual calculations']) + int(contCalcRow['Number of complex virtual calculations'])


scope='Displays for Insight'
contCalcRow=Product.GetContainerByName('HCI_PHD_NewDisplaysforInsight').Rows[0]
dispInsightTotalHrs=int(contCalcRow['Number of simple displays'])*float( getattr(scopeDict[scope], 'Simple')) + int(contCalcRow['Number of medium displays'])*float(getattr(scopeDict[scope], 'Typical')) + int(contCalcRow['Number of complex displays'])*float(getattr(scopeDict[scope], 'Complex'))
No_Displays=int(contCalcRow['Number of simple displays'])+int(contCalcRow['Number of medium displays'])+int(contCalcRow['Number of complex displays'])

prjCmpSimple += int(contCalcRow['Number of simple displays'])*float( getattr(scopeDict[scope], 'Simple'))
prjCmpTypical += int(contCalcRow['Number of medium displays'])*float(getattr(scopeDict[scope], 'Typical'))
prjCmpComplex += int(contCalcRow['Number of complex displays'])*float(getattr(scopeDict[scope], 'Complex'))

scope='Migrated Displays for Insight'
contCalcRow=Product.GetContainerByName('HCI_PHD_MigratedDisplaysforInsight').Rows[0]
migrDispInsight=int(contCalcRow['Number of simple displays migrated from Experion'])*float( getattr(scopeDict[scope], 'Simple')) + int(contCalcRow['Number of typical displays migrated from Experion'])*float(getattr(scopeDict[scope], 'Typical')) + int(contCalcRow['Number of complex displays migrated from Experion'])*float(getattr(scopeDict[scope], 'Complex')) + int(contCalcRow['Number of simple displays migrated from Workcenter'])*float(0.1)
migrworkCenterInsight=int(contCalcRow['Number of simple displays migrated from Workcenter'])*float(0.1)

prjCmpSimple += int(contCalcRow['Number of simple displays migrated from Experion'])*float( getattr(scopeDict[scope], 'Simple'))
prjCmpTypical += int(contCalcRow['Number of typical displays migrated from Experion'])*float(getattr(scopeDict[scope], 'Typical'))
prjCmpComplex += int(contCalcRow['Number of complex displays migrated from Experion'])*float(getattr(scopeDict[scope], 'Complex'))
prjCmpSimple += int(contCalcRow['Number of simple displays migrated from Workcenter'])*float(0.1)

scope='Excel Reports'
contCalcRow=Product.GetContainerByName('HCI_PHD_ExcelReports').Rows[0]
exlReportTotalHrs=int(contCalcRow['Number of simple reports'])*float( getattr(scopeDict[scope], 'Simple')) + int(contCalcRow['Number of medium reports'])*float(getattr(scopeDict[scope], 'Typical')) + int(contCalcRow['Number of complex reports'])*float(getattr(scopeDict[scope], 'Complex'))

prjCmpSimple += int(contCalcRow['Number of simple reports'])*float( getattr(scopeDict[scope], 'Simple'))
prjCmpTypical += int(contCalcRow['Number of medium reports'])*float(getattr(scopeDict[scope], 'Typical'))
prjCmpComplex += int(contCalcRow['Number of complex reports'])*float(getattr(scopeDict[scope], 'Complex'))

scope='Crystal Reports'
contCalcRow=Product.GetContainerByName('HCI_PHD_CrystalReports').Rows[0]
cryReportTotalHrs=int(contCalcRow['Number of simple reports'])*float( getattr(scopeDict[scope], 'Simple')) + int(contCalcRow['Number of medium reports'])*float(getattr(scopeDict[scope], 'Typical')) + int(contCalcRow['Number of complex reports'])*float(getattr(scopeDict[scope], 'Complex'))

prjCmpSimple += int(contCalcRow['Number of simple reports'])*float( getattr(scopeDict[scope], 'Simple'))
prjCmpTypical += int(contCalcRow['Number of medium reports'])*float(getattr(scopeDict[scope], 'Typical'))
prjCmpComplex += int(contCalcRow['Number of complex reports'])*float(getattr(scopeDict[scope], 'Complex'))

scope='SQL SRS Reports'
contCalcRow=Product.GetContainerByName('HCI_PHD_SSRS_Reports').Rows[0]
ssrReportTotalHrs=int(contCalcRow['Number of simple reports'])*float( getattr(scopeDict[scope], 'Simple')) + int(contCalcRow['Number of medium reports'])*float(getattr(scopeDict[scope], 'Typical')) + int(contCalcRow['Number of complex reports'])*float(getattr(scopeDict[scope], 'Complex'))

totalReport = exlReportTotalHrs+cryReportTotalHrs+ssrReportTotalHrs
reportSaving = round(min((totalReport*0.1),60.0))
reportSaving=0
exlReportSaving = (reportSaving*exlReportTotalHrs)/totalReport if exlReportTotalHrs !=0 else 0
cryReportSaving = (reportSaving*cryReportTotalHrs)/totalReport if cryReportTotalHrs !=0 else 0
ssrReportSaving = (reportSaving*ssrReportTotalHrs)/totalReport if ssrReportTotalHrs !=0 else 0

prjCmpSimple += int(contCalcRow['Number of simple reports'])*float( getattr(scopeDict[scope], 'Simple'))
prjCmpTypical += int(contCalcRow['Number of medium reports'])*float(getattr(scopeDict[scope], 'Typical'))
prjCmpComplex += int(contCalcRow['Number of complex reports'])*float(getattr(scopeDict[scope], 'Complex'))

projectSize = totalInterfaceHours + Hrs_Tags + Hrs_Calcs + dispInsightTotalHrs + migrDispInsight + exlReportTotalHrs +  cryReportTotalHrs + ssrReportTotalHrs - reportSaving

prjCmpSimplePercent = round((prjCmpSimple/projectSize) * 100)
prjCmpTypicalPercent = round((prjCmpTypical/projectSize) * 100)
prjCmpComplexPercent = round((prjCmpComplex/projectSize) * 100)

scope='Project Complexity Factors'
projectComplexity= round(prjCmpSimplePercent*float(getattr(scopeDict[scope], 'Simple')) + prjCmpTypicalPercent*float(getattr(scopeDict[scope], 'Typical')) + prjCmpComplexPercent*float(getattr(scopeDict[scope], 'Complex')))
projectComplexity=projectComplexity/100

contCalcRow=Product.GetContainerByName('HCI_PHD_Hardware').Rows[0]
No_Nodes=contCalcRow['Total number of servers']
No_Honeywell_Nodes=contCalcRow['Numbers of servers provided by Honeywell']


contCalcRow=Product.GetContainerByName('HCI_PHD_USMConfiguration').Rows[0]
No_Monitor_Items = float(contCalcRow['Number of Monitor Items'])
No_Condition_Items = float(contCalcRow['Number of Condition Items'])
No_Historised_Monitor_Items = float(contCalcRow['Number of Historised Monitor Items'])
No_USM_Items=No_Monitor_Items+No_Condition_Items+No_Historised_Monitor_Items


No_3rd_party_clients=float(Product.Attributes.GetByName('HCI_NoOf3rdPartyClients').GetValue()) if Product.Attributes.GetByName('HCI_NoOf3rdPartyClients').GetValue() else 0


#Calculate Project scope values from Technical scope 
mainTaskDetails=SqlHelper.GetList("select * from CT_PHD_WBS where Indent=3 or Indent=4")
taskDetailsDict={}
for task in mainTaskDetails:
	taskDetailsDict[task.Task]=task
	

wbsDict={}
tempDict={'KOM type':'Face 2 Face','Travel Time':'8'}
parDictStr=Product.Attributes.GetByName('HCI_PHD_ParChildAttr').GetValue()
parDict=JsonHelper.Deserialize(parDictStr)
if parDict and parDict['scopeDict']:
	komType=parDict['scopeDict']['KOM type']
else:
	komType='Online'
noOfEngs=0
if parDict:
	headerScopeDict={}
	headerScopeDict=parDict['scopeDict']
	contRows=Product.GetContainerByName('AR_HCI_PHD_ProjectInputs1').Rows[0].Columns
	scopeDict2={}
	for col in contRows:
		if col.Name in ['Upgrade/Update-PHD','Upgrade/Update-Third Party Historian'] and col.Value == "":
			scopeDict2[col.Name] = Session[str(col.Name)] if Session[str(col.Name)] else ''
		else:
			scopeDict2[col.Name]=col.Value
	contRows=Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows[0].Columns
	for col in contRows:
		if col.Name in ['Graphics and Reports','Test Environment Installation and Setup','On-Site Installation'] and col.Value == "":
			scopeDict2[col.Name] = Session[str(col.Name)] if Session[str(col.Name)] else ''
		else:
			scopeDict2[col.Name]=col.Value
	headerScopeDict.update(scopeDict2)
	headerScopeDict['Uniformance Insight Implementation']='No'
	if headerScopeDict['Detailed Design']=='Yes' or headerScopeDict['USM Implementation']=='Yes':
		headerScopeDict['Detailed Design and USM Implementation']='Yes'
	if headerScopeDict['Detailed Design']=='No' or headerScopeDict['USM Implementation']=='No':
		headerScopeDict['Detailed Design and USM Implementation']='No'
	if headerScopeDict['Build and Configure']=='Yes' or headerScopeDict['USM Implementation']=='Yes':
		headerScopeDict['Build and Configure and USM Implementation']='Yes'
	if headerScopeDict['Build and Configure']=='No' or headerScopeDict['USM Implementation']=='No':
		headerScopeDict['Build and Configure and USM Implementation']='No'

	noOfEngs=parDict['noOfEngs']
	#Log.Info("---upgrade---recheck---"+str(headerScopeDict))


No_Tags=float(No_Tags)
No_Calcs=float(No_Calcs)
No_RDIs=float(No_RDIs)
No_ERPandOther=float(No_ERPandOther)
No_Nodes=float(No_Nodes)
No_Monitor_Items=float(No_Monitor_Items)
No_Condition_Items=float(No_Condition_Items)
No_Historised_Monitor_Items=float(No_Historised_Monitor_Items)
No_Honeywell_Nodes=float(No_Honeywell_Nodes)
Tag_Security=2
No_Displays=float(No_Displays)
No_USM_Items=float(No_USM_Items)
Hrs_Tags=float(Hrs_Tags)
Hrs_Calcs=float(Hrs_Calcs)
No_ofInductions=1 if headerScopeDict['On-Site Installation']=='Yes' else 0
No_of_Courses=1 if headerScopeDict['Client Training']=='Yes' else 0


wbsCalcDict={}
wbsCalcDict['Kick Off Meeting']=8*noOfEngs if komType=='Face 2 Face' else 4*noOfEngs
wbsCalcDict['TravelTime']=float(tempDict['Travel Time'])
wbsCalcDict['FDS Travel Time']=float(tempDict['Travel Time'])*2
wbsCalcDict['Define Tags']=float(No_Tags)
wbsCalcDict['Define Virtual Tags']=float(No_Calcs)
wbsCalcDict['No_RDIs']=float(No_RDIs)
wbsCalcDict['Define ERP and other interfaces']=float(No_ERPandOther)
wbsCalcDict['No_Nodes']=float(No_Nodes)
wbsCalcDict['No_Monitor_Items']=float(No_Monitor_Items)
wbsCalcDict['No_Condition_Items']=float(No_Condition_Items)
wbsCalcDict['No_Historised_Monitor_Items']=float(No_Historised_Monitor_Items)
wbsCalcDict['Order Software']=1
wbsCalcDict['No_Honeywell_Nodes']=float(No_Honeywell_Nodes)
wbsCalcDict['Tag_Security']=float(Tag_Security)
wbsCalcDict['dispInsightTotalHrs']=float(dispInsightTotalHrs)
wbsCalcDict['migrDispInsight']=float(migrDispInsight)
wbsCalcDict['No_Displays']=float(No_Displays)
wbsCalcDict['Build Excel reports']=float(exlReportTotalHrs-exlReportSaving)
wbsCalcDict['Build Crystal reports']=float(cryReportTotalHrs-cryReportSaving)
wbsCalcDict['Build SQL Server Reporting Services reports']=float(ssrReportTotalHrs-ssrReportSaving)
wbsCalcDict['OnlyFactor']=1
wbsCalcDict['No_NodesXcomplx']=float(No_Nodes * projectComplexity)
wbsCalcDict['No_RDIsXcomplx']=float(No_RDIs * projectComplexity)
wbsCalcDict['No_ofInductions']=float(No_ofInductions)
wbsCalcDict['Hrs_Tags']=float(Hrs_Tags)
wbsCalcDict['Hrs_Calcs']=float(Hrs_Calcs)
wbsCalcDict['No_3rd_party_clients']=float(No_3rd_party_clients)
wbsCalcDict['projectComplexity']=float(projectComplexity)
wbsCalcDict['totalInterfaceHours']=float(totalInterfaceHours)
wbsCalcDict['No_USM_Items']=float(No_USM_Items)
wbsCalcDict['Sum_ERPandOther']=float(Sum_ERPandOther)
wbsCalcDict['reportSaving']=float(float(reportSaving))
wbsCalcDict['migrworkCenterInsight']=float(migrworkCenterInsight)
wbsCalcDict['No_of_Courses']=No_of_Courses
wbsCalcDict['Delivery_Support']=1

teamStr=parDict['teamStr']
participationPer=[]
for per in teamStr.keys():
	if teamStr[per]['Participation'] and teamStr[per]['Participation']>0:
		participationPer.append(float(teamStr[per]['Participation'])/100)

def calcWbsTotal(hrs):
	totalHrs=0
	for per in participationPer:
		totalHrs+=math.ceil(hrs*per)
	return(totalHrs)
#conditions for calculating total hours for each deliveralbe
for task in mainTaskDetails:
	if task.KeyName in wbsCalcDict.keys():
		hrs=round(wbsCalcDict[task.KeyName] * float(task.Factor))
		wbsDict[task.Task]=calcWbsTotal(hrs)
	elif task.ProjectSizeXComplexity=='Yes' and not task.MinHrs:
		hrs=round(projectSize * projectComplexity * float(task.Factor))
		wbsDict[task.Task]=calcWbsTotal(hrs)
	elif task.ProjectSizeXComplexity=='Yes' and  task.MinHrs:
		hrs=max(round(projectSize * projectComplexity * float(task.Factor)),float(task.MinHrs))
		wbsDict[task.Task]=calcWbsTotal(hrs)
	elif task.Task == 'Produce SAT Document':
		hrs=max(round(No_Nodes * projectComplexity * float(task.Factor)),float(task.MinHrs))
		wbsDict[task.Task]=calcWbsTotal(hrs)
 
 
integrationTestingTotal=0
for task in GS_HCI_PHD_Module.integrationTestingLst:
	if task in wbsDict.keys():
		integrationTestingTotal += wbsDict[task]
task='Internal application integration testing'
taskDetails=taskDetailsDict[task]
hrs=round(float(integrationTestingTotal)*float(taskDetails.Factor))
wbsDict[task]=calcWbsTotal(hrs)
 
satPunchList=['Validate scanning and data collection','Validate system and storage parameters','Validate engineering unit conversion','Validate calculations','Verify Uniformance Applications','Verify 3rd Party Clients (eg ERPs etc)','Verify PHD Clients','Test security model']
satPunchListTotal=0
for task in satPunchList:
	if task in wbsDict.keys():
		satPunchListTotal += wbsDict[task]
task='SAT Punch List Items'
taskDetails=taskDetailsDict[task]
hrs=round(float(satPunchListTotal)*float(taskDetails.Factor)) 
wbsDict[task]=calcWbsTotal(hrs)

task='Training Preparation'
taskDetails=taskDetailsDict[task]
trainPre=float(wbsDict['Administration Training (Site Specific)'])+float(wbsDict['User Training (Site Specific) (UPS & UI)'])
hrs=round(float(trainPre)*float(taskDetails.Factor))  
wbsDict[task]=calcWbsTotal(hrs)

Trace.Write(str(wbsDict))

#Calculate Labour deliveralbe values 
if parDict:
	totalFinalhrs=0
	deliveralbeDict={}
	for task in mainTaskDetails:
		if task.Task in wbsDict.keys():
			subGroup=task.SubGroup
			mainGroup=task.MainGroup
			visibilityGrp=task.HeaderPhase
			if mainGroup and subGroup:
				if mainGroup not in deliveralbeDict.keys() and visibilityGrp in headerScopeDict.keys() and headerScopeDict[visibilityGrp]=='Yes':
					totalFinalhrs+=float(wbsDict[task.Task])
					deliveralbeDict[mainGroup]={}
					deliveralbeDict[mainGroup]['total']=float(wbsDict[task.Task])
					deliveralbeDict[mainGroup]['subGroup']={}
					deliveralbeDict[mainGroup]['subGroup'][subGroup] = float(wbsDict[task.Task])
				elif mainGroup in deliveralbeDict.keys() and visibilityGrp in headerScopeDict.keys() and headerScopeDict[visibilityGrp]=='Yes':
					totalFinalhrs+=float(wbsDict[task.Task])
					if subGroup not in deliveralbeDict[mainGroup]['subGroup'].keys():
						deliveralbeDict[mainGroup]['subGroup'][subGroup] = float(wbsDict[task.Task])
					else:
						deliveralbeDict[mainGroup]['subGroup'][subGroup] += float(wbsDict[task.Task])
					deliveralbeDict[mainGroup]['total'] += float(wbsDict[task.Task])
			 
	Trace.Write(str(deliveralbeDict))
	
	teamStr=parDict['teamStr']
	Trace.Write(str(teamStr))
	Product.GetContainerByName('HCI_PHD_EngineeringLabour').Rows.Clear()
	contRows=Product.GetContainerByName('HCI_PHD_EngineeringLabour')
	engLst=['FO Eng 1','FO Eng 2','FO Eng 3','GES Eng 1','GES Eng 2']
	labourFinalHrsDict={}
	salesCountry=getExecutionCountry()
	productPrice={}
	headerTotal={}
	costTotalDict={}
	ListPriceTotalDict={}
	WTWCostTotalDict={}
	mainWbsList=['Project Set Up and Scope of Work','User Requirements','Functional and Detailed Design','Order, Build and Configure','Uniformance Insight Implementation','Graphics and Reports','Upgrade/Update','Installation, Setup and FAT','On-Site Installation and SAT','Post-Go-Live Activities and Documentation','Client Training','Post Delivery Support']
	subWbsDict={'Project Set Up and Scope of Work':['Kick Off Meeting','Prepare, Review and Update Scope of Work Document'],'User Requirements':['Site Survey and Data Collection','Prepare, Review & Approve User Requirements Document'],'Functional and Detailed Design':['Prepare, Review and Update Functional Design Specification Document','Define System Parameters, Eng Units','Define Tags, Virtual Tags, RDIs','Define ERP and other interfaces','Define USM Architecture (Slaves Nodes, Master Nodes, Communications)','Define Monitor, Condition and Historised Monitor Items','Prepare, Review and Update Detailed Design Document'],'Order, Build and Configure':['Order Software & Hardware','Build Base Infrastructure','Install and Configure Software','Configure and load PHD tag definitions','Configure/setup RDIs, ERP and other interfaces','Define and test virtual tag calculations','Define user profiles and tag security','Implement TagSync','Configure USM Software','Configure USM Monitor, Condition and Historised Monitor Items','Verify PHD Collection and Communication','Internal application integration testing'],'Uniformance Insight Implementation':['Insight Implementation & Configuration'],'Graphics and Reports':['Build new displays','Migrate Experion and Workcenter displays','Build graphic navigation hierarchy','Build Excel, Crystal and SQL Server Reporting Services reports'],'Upgrade/Update':['Upgrade PHD DB R215 to R3xx','Upgrade PHD DB R300 to R340/R321','Archieve File Migration-PHD','DB Upgrade','Archieve File Migration Third Party Historian'],'Installation, Setup and FAT':['Install Base Software','Test Environment Installation, Setup & pre-FAT testing','Test Environment Installation, Setup for USM (as required) & pre-FAT testing','Produce FAT Document','Perform FAT and Post FAT Activities (including Punch List Items)','System Backup efforts, Engineering System De-Assembly, pack & shipping'],'On-Site Installation and SAT':['Site Inductions and DCS Activities','Production Environment and Client Software Installation','Produce SAT Document','Validate scanning and data collection','Validate system and storage parameters','Validate engineering unit conversion and calculations','Verify Uniformance Applications, 3rd Party Clients (eg ERPs etc) and PHD Clients','Test security model','SAT Punch List Items','Performance/Stress Test'],'Post-Go-Live Activities and Documentation':['Go-Live Support','Post Go-Live System Checks','As-Built Documentation','Operator Manual Development/Review/Update','System Admin Manual Development/Review/Update'],'Client Training':['Training Preparation','Administration Training (Site Specific)','User Training (Site Specific) (UPS & UI)'],'Post Delivery Support':['Off-Site/On-Site Maintenance','Standard Warranty']}
	for mainGroup in mainWbsList:
		if mainGroup in deliveralbeDict.keys():
			row=contRows.AddNewRow(False)
			row['Deliverable']=mainGroup
			row['Calculated Hrs']=str(deliveralbeDict[mainGroup]['total'])
			row['Productivity']="1"
			row['Final Hrs']=str(deliveralbeDict[mainGroup]['total'])
			row['Header']="Header"
			deliveralbeDict[mainGroup]['localTotal']=0
			for task in  subWbsDict[mainGroup]:
				if task in deliveralbeDict[mainGroup]['subGroup']:
					for eng in engLst:
						hrs=deliveralbeDict[mainGroup]['subGroup'][task]
						#if eng in teamStr.keys() and task!='Travel Time' and hrs and int(hrs)!=0:
						if eng in teamStr.keys() and task!='Travel Time':
							row=contRows.AddNewRow(False)
							row['Header']=mainGroup
							row['Deliverable']=task
							row['Calculated Hrs']=str(round(deliveralbeDict[mainGroup]['subGroup'][task] * (float(teamStr[eng]['Participation'])/100)))
							if row['Header'] not in headerTotal.keys():
								headerTotal[row['Header']]=float(row['Calculated Hrs'])
							else:
								headerTotal[row['Header']]+=float(row['Calculated Hrs'])
							row['Productivity']="1"
							row['Final Hrs']=str(round(deliveralbeDict[mainGroup]['subGroup'][task] * (float(teamStr[eng]['Participation'])/100)))
							row['Eng']=teamStr[eng]['Activity Type']
							if 'GES' in eng:
								#row['Execution Country']=salesCountry
								row['Execution Country']='United States'
							else:
								row['Execution Country']=teamStr[eng]['Country']
							row['Execution Year']=str(DateTime.Now.Year)
							if Quote.GetCustomField('R2QFlag').Content == 'Yes':
								row['Execution Year'] = str(R2Qexecution_year)
							labor=row['Eng']
							serviceMaterial=str(laborDetails[labor])
							if serviceMaterial not in productPrice.keys():
								Addproduct =ProductHelper.CreateProduct(laborDetails[labor])
								productPrice[serviceMaterial]=float(Addproduct.TotalPrice)
							listPrice=productPrice[serviceMaterial]
							#Log.Info(str(serviceMaterial)+"---GS_PHD_CalculateLabour----000-->"+str(listPrice))
							Log.Info(str(serviceMaterial)+"---GS_PHD_CalculateLabour----000-->"+str(listPrice)+"---salesOrg-->"+str(salesOrg)+"-->"+str(currency))
							row['Eng Unit List Price']= str(GS_HCI_PHD_Module.getCalculateListPrice(salesOrg,float(listPrice),row['Execution Year']))
							row['Eng Total List Price']=str(float(row['Eng Unit List Price'])*float(row['Final Hrs']))
							if 'GES' not in eng:
								cost=GS_HCI_PHD_Module.getLaborCost(row['Execution Country'],serviceMaterial,row['Execution Year'],currency)
								if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost) == 0.00:
									row["Execution Country"] = alternate_execution_country
									cost=GS_HCI_PHD_Module.getLaborCost(row['Execution Country'],serviceMaterial,row['Execution Year'],currency)
								if salesCountry!=row['Execution Country']:
									cost=cost*1.1 if cost else 0
								w2wCost=cost
								if salesCountry!=row['Execution Country']:
									w2wCost=w2wCost/1.1 if w2wCost else 0
								Log.Info(str(serviceMaterial)+"---GS_PHD_CalculateLabour--COST--000-->"+str(cost)+"---salesOrg-->"+str(salesOrg)+"-->"+str(currency))
								row['Eng Unit Regional Cost']=str(cost)
								row['Eng Total Regional Cost']=str(float(cost)*float(row['Final Hrs']))
								row['Eng Total WTW Cost']=str(float(w2wCost)*float(row['Final Hrs']))
							else:
								partNumber=laborDetails[labor]
								EC_GES=row['Execution Country']
								if '_CN' in partNumber or '_UZ' in partNumber:
									EC_GES=''
								cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails[labor],row['Execution Year'],currency)
								if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost) == 0.00:
									row["Execution Country"] = alternate_execution_country
									EC_GES=row['Execution Country']
									if '_CN' in partNumber or '_UZ' in partNumber:
										EC_GES=''
									cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails[labor],row['Execution Year'],currency)
								reginoalCost, w2wCost=gesCostValues(cost,partNumber,currency)
								row['Eng Unit Regional Cost']=str(reginoalCost)
								row['Eng Total Regional Cost']=str(float(reginoalCost)*float(row['Final Hrs']))
								row['Eng Total WTW Cost']=str(float(w2wCost)*float(row['Final Hrs']))
							if row['Header'] not in costTotalDict.keys():
								costTotalDict[row['Header']]=float(row['Eng Total Regional Cost'])
							else:
								costTotalDict[row['Header']]+=float(row['Eng Total Regional Cost'])
							if row['Header'] not in ListPriceTotalDict.keys():
								ListPriceTotalDict[row['Header']]=float(row['Eng Total List Price'])
							else:
								ListPriceTotalDict[row['Header']]+=float(row['Eng Total List Price'])
							if row['Header'] not in WTWCostTotalDict.keys():
								WTWCostTotalDict[row['Header']]=float(row['Eng Total WTW Cost'])
							else:
								WTWCostTotalDict[row['Header']]+=float(row['Eng Total WTW Cost'])
							
	totalTravelTime=0
	for eng in teamStr.keys():
		if teamStr[eng]['NoOfEng'] and teamStr[eng]['Travel Time']:
			totalTravelTime+=float(teamStr[eng]['NoOfEng']) * float(teamStr[eng]['Travel Time'])
	if totalTravelTime>0:
		row=contRows.AddNewRow(False)
		row['Deliverable']='Total Travel Time'
		row['Calculated Hrs']=str(totalTravelTime)
		row['Productivity']="1"
		row['Final Hrs']=str(totalTravelTime)
		row['Header']="Header"
	finalHrs=0
	calcHrs=0
	totalCost=0
	totalListPrice=0
	totalWTWCost=0
	travelTimeTotalCost=0
	travelTimeTotalListPrice=0
	travelTimeTotalWTWCost=0
	for eng in engLst:
		if eng in teamStr.keys() and teamStr[eng]['NoOfEng'] and teamStr[eng]['Travel Time']:
			hrs=float(teamStr[eng]['NoOfEng']) * float(teamStr[eng]['Travel Time'])
			totalFinalhrs+=float(hrs)
			row=contRows.AddNewRow(False)
			row['Header']='Total Travel Time'
			task='Travel Time'
			row['Deliverable']=task
			row['Calculated Hrs']=str(hrs)
			calcHrs+=float(row['Calculated Hrs'])
			row['Productivity']="1"
			row['Final Hrs']= str( hrs * int(row['Productivity']))
			finalHrs+=float(row['Final Hrs'])
			row['Eng']=teamStr[eng]['Activity Type']
			if 'GES' in eng:
				#row['Execution Country']=salesCountry
				row['Execution Country']='United States'
			else:
				row['Execution Country']=teamStr[eng]['Country']
			row['Execution Year']=str(DateTime.Now.Year)
			if Quote.GetCustomField('R2QFlag').Content == 'Yes':
				row['Execution Year'] = str(R2Qexecution_year)
			labor=row['Eng']
			serviceMaterial=str(laborDetails[labor])
			if serviceMaterial not in productPrice.keys():
				Addproduct =ProductHelper.CreateProduct(laborDetails[labor])
				productPrice[serviceMaterial]=float(Addproduct.TotalPrice)
			listPrice=productPrice[serviceMaterial]
			row['Eng Unit List Price']=str(GS_HCI_PHD_Module.getCalculateListPrice(salesOrg,float(listPrice),row['Execution Year']))
			row['Eng Total List Price']=str(float(row['Eng Unit List Price'])*float(row['Final Hrs']))
			if 'GES' not in eng:
				cost=GS_HCI_PHD_Module.getLaborCost(row['Execution Country'],serviceMaterial,row['Execution Year'],currency)
				if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost) == 0.00:
					row["Execution Country"] = alternate_execution_country
					cost=GS_HCI_PHD_Module.getLaborCost(row['Execution Country'],serviceMaterial,row['Execution Year'],currency)
				if salesCountry!=row['Execution Country']:
					cost=cost*1.1 if cost else 0
				w2wCost=cost
				if salesCountry!=row['Execution Country']:
					w2wCost=w2wCost/1.1 if w2wCost else 0
				row['Eng Unit Regional Cost']=str(cost)
				row['Eng Total Regional Cost']=str(float(cost)*float(row['Final Hrs']))
				row['Eng Total WTW Cost']=str(float(w2wCost)*float(row['Final Hrs']))
			else:
				partNumber=laborDetails[labor]
				EC_GES=row['Execution Country']
				if '_CN' in partNumber or '_UZ' in partNumber:
					EC_GES=''
				cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails[labor],row['Execution Year'],currency)
				if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost) == 0.00:
					row["Execution Country"] = alternate_execution_country
					EC_GES=row['Execution Country']
					if '_CN' in partNumber or '_UZ' in partNumber:
						EC_GES=''
					cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails[labor],row['Execution Year'],currency)
				reginoalCost, w2wCost=gesCostValues(cost, partNumber,currency)
				row['Eng Unit Regional Cost']=str(reginoalCost)
				row['Eng Total Regional Cost']=str(float(reginoalCost)*float(row['Final Hrs']))
				row['Eng Total WTW Cost']=str(float(w2wCost)*float(row['Final Hrs']))
			travelTimeTotalCost += float(row['Eng Total Regional Cost'])
			travelTimeTotalListPrice += float(row['Eng Total List Price'])
			travelTimeTotalWTWCost += float(row['Eng Total WTW Cost'])
			totalCost += float(row['Eng Total Regional Cost'])
			totalListPrice += float(row['Eng Total List Price'])
			totalWTWCost += float(row['Eng Total WTW Cost'])
				
	contRows=Product.GetContainerByName('HCI_PHD_EngineeringLabour').Rows                
	for row in contRows:
		if row['Header']=='Header' and row['Deliverable'] in headerTotal.keys() :
			row['Final Hrs']=str(headerTotal[row['Deliverable']])
			finalHrs+=float(row['Final Hrs'])
			row['Calculated Hrs']=str(headerTotal[row['Deliverable']])
			calcHrs+=float(row['Calculated Hrs'])
			row['Eng Total Regional Cost']=str(costTotalDict[row['Deliverable']])
			totalCost+=float(row['Eng Total Regional Cost'])
			row['Eng Total List Price']=str(ListPriceTotalDict[row['Deliverable']])
			totalListPrice+=float(row['Eng Total List Price'])
			row['Eng Total WTW Cost']=str(WTWCostTotalDict[row['Deliverable']])
			totalWTWCost+=float(row['Eng Total WTW Cost'])
		if row['Deliverable']=='Total Travel Time':
			row['Eng Total Regional Cost']=str(travelTimeTotalCost)
			row['Eng Total List Price']=str(travelTimeTotalListPrice)
			row['Eng Total WTW Cost']=str(travelTimeTotalWTWCost)
	row=Product.GetContainerByName('HCI_PHD_EngineeringLabour').AddNewRow(False)
	addColumns(row,finalHrs,calcHrs,totalCost,totalListPrice,totalWTWCost)
	
	contRows=Product.GetContainerByName('HCI_PHD_AdditionalDeliverables').Rows
	for row in contRows:
		if row['Final Hrs'] and row['Hidden_lable']!='Total':
			totalFinalhrs+=float(row['Final Hrs'])
			finalHrs+=float(row['Final Hrs'])
	
	
	leadEngFinalHrs=0
	leadEngCalcHrs=0
	leadEngTotalCost=0
	leadEngTotalLP=0
	leadEngTotalWTW=0
	pmFinalHrs=0
	pmCalcHrs=0
	pmTotalCost=0
	pmTotalLP=0
	pmTotalWTW=0
	pmLaborDict=parDict['pmLaborDict']
	Product.GetContainerByName('HCI_PHD_ProjectManagement').Rows.Clear()
	Product.GetContainerByName('HCI_PHD_ProjectManagement2').Rows.Clear()
	contRows=Product.GetContainerByName('HCI_PHD_ProjectManagement')
	contRows2=Product.GetContainerByName('HCI_PHD_ProjectManagement2')
	pmDeliverableDict={'Project Management':'PM Core & Duration Driven','Project Management - GES':'PM Core & Duration Driven','Project Administration':'PM Core & Duration Driven','Project Controls':'PCO Core & Duration Driven','Lead Engineering':'LE Core & Duration Driven'}
	for eng in pmLaborDict.keys():
		if eng !='Lead Engineering':
			row=contRows.AddNewRow(False)
		else:
			row=contRows2.AddNewRow(False)
		row['Deliverable']=pmDeliverableDict[eng]
		row['Calculated Hrs']=str(round(finalHrs * (float(pmLaborDict[eng]['Percentage'])/100)))
		row['Productivity']="1"
		row['Final Hrs']= str( round(finalHrs * (float(pmLaborDict[eng]['Percentage'])/100))* int(row['Productivity']))
		row['PM_Percentage']=eng
		
		row['Eng']=pmLaborDict[eng]['Activity_Type']
		if 'GES' in eng:
			#row['Execution Country']=salesCountry
			row['Execution Country']='United States'
		else:
			row['Execution Country']=pmLaborDict[eng]['Country']
		row['Execution Year']=str(DateTime.Now.Year)
		if Quote.GetCustomField('R2QFlag').Content == 'Yes':
			row['Execution Year'] = str(R2Qexecution_year)
		labor=pmLaborDict[eng]['Activity_Type']
		Addproduct =ProductHelper.CreateProduct(laborDetails[labor])
		listPrice=Addproduct.TotalPrice
		row['Eng Unit List Price']=str(GS_HCI_PHD_Module.getCalculateListPrice(salesOrg,float(listPrice),row['Execution Year']))
		row['Eng Total List Price']=str(float(row['Eng Unit List Price'])*float(row['Final Hrs']))
		if 'GES' not in eng:
			cost=GS_HCI_PHD_Module.getLaborCost(row['Execution Country'],laborDetails[labor],row['Execution Year'],currency)
			if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost) == 0.00:
				row["Execution Country"] = alternate_execution_country
				cost=GS_HCI_PHD_Module.getLaborCost(row['Execution Country'],laborDetails[labor],row['Execution Year'],currency)
			if salesCountry!=row['Execution Country']:
				cost=cost*1.1 if cost else 0
			w2wCost=cost
			if salesCountry!=row['Execution Country']:
				w2wCost=w2wCost/1.1 if w2wCost else 0
			row['Eng Unit Regional Cost']=str(cost)
			row['Eng Total Regional Cost']=str(float(cost)*float(row['Final Hrs']))
			row['Eng Total WTW Cost']=str(float(w2wCost)*float(row['Final Hrs']))
		else:
			partNumber=laborDetails[labor]
			EC_GES=row['Execution Country']
			if '_CN' in partNumber or '_UZ' in partNumber:
				EC_GES=''
			cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails[labor],row['Execution Year'],currency)
			if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost) == 0.00:
				row["Execution Country"] = alternate_execution_country
				EC_GES=row['Execution Country']
				if '_CN' in partNumber or '_UZ' in partNumber:
					EC_GES=''
				cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails[labor],row['Execution Year'],currency)
			reginoalCost, w2wCost=gesCostValues(cost, partNumber,currency)
			row['Eng Unit Regional Cost']=str(reginoalCost)
			row['Eng Total Regional Cost']=str(float(reginoalCost)*float(row['Final Hrs']))
			row['Eng Total WTW Cost']=str(float(w2wCost)*float(row['Final Hrs']))
		if eng =='Lead Engineering':
			leadEngFinalHrs+=float(row['Final Hrs'])
			leadEngCalcHrs+=float(row['Calculated Hrs'])
			leadEngTotalCost+=float(row['Eng Total Regional Cost'])
			leadEngTotalLP+=float(row['Eng Total List Price'])
			leadEngTotalWTW+=float(row['Eng Total WTW Cost'])
		else:
			pmFinalHrs+=float(row['Final Hrs'])
			pmCalcHrs+=float(row['Calculated Hrs'])
			pmTotalCost+=float(row['Eng Total Regional Cost'])
			pmTotalLP+=float(row['Eng Total List Price'])
			pmTotalWTW+=float(row['Eng Total WTW Cost'])
			
			
	row=contRows.AddNewRow(False)
	addColumns(row,pmFinalHrs,pmCalcHrs,pmTotalCost,pmTotalLP,pmTotalWTW)    
	row=contRows2.AddNewRow(False)
	addColumns(row,leadEngFinalHrs,leadEngCalcHrs,leadEngTotalCost,leadEngTotalLP,leadEngTotalWTW)
if Product.GetContainerByName('HCI_PHD_AdditionalDeliverables') and Product.GetContainerByName('HCI_PHD_AdditionalDeliverables').Rows.Count < 1:
	Product.GetContainerByName('HCI_PHD_AdditionalDeliverables').AddNewRow(False)