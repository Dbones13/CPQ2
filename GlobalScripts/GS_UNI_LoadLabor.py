import GS_HCI_PHD_Module
from System import DateTime

Product.ResetAttr('AR_HCI_SELECTALL')
salesOrg = Quote.GetCustomField("Sales Area").Content
currency=Quote.GetCustomField("Currency").Content if Quote.GetCustomField("Currency").Content else 'USD'
alternate_execution_country = Quote.GetCustomField('R2Q_Alternate_Execution_Country').Content
R2Qexecution_year = Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content
Product.Attributes.GetByName('HCI_PHD_IsRequiredUNI').SelectDisplayValue('1')
def getExecutionCountry():
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
	if query is not None:
		return query.Execution_County

parDictStr=Product.Attributes.GetByName('HCI_PHD_ParChildAttr').GetValue()
parDict=JsonHelper.Deserialize(parDictStr)
teamStr=parDict['teamStr']
Product.GetContainerByName('HCI_PHD_EngineeringLabour').Rows.Clear()
contRows=Product.GetContainerByName('HCI_PHD_EngineeringLabour')
engLst=['FO Eng 1','FO Eng 2','FO Eng 3','GES Eng 1','GES Eng 2']
labourFinalHrsDict={}
deliveralbeDict={'Insight Implementation & Configuration':40.00}

finalHrs=0
calcHrs=0
totalCost=0
totalListPrice=0
totalWTWCost=0
totalFinalhrs=0
salesCountry=getExecutionCountry()
productPrice={}
for task in deliveralbeDict.keys():
	for eng in engLst:
		if eng in teamStr.keys() and task!='Travel Time':
			row=contRows.AddNewRow(False)
			row['Deliverable']=task
			row['Calculated Hrs']=str(round(deliveralbeDict[task] * (float(teamStr[eng]['Participation'])/100)))
			row['Productivity']="1"
			row['Final Hrs']= str( round(deliveralbeDict[task] * (float(teamStr[eng]['Participation'])/100))* int(row['Productivity']))
			finalHrs+=float(row['Final Hrs'])
			calcHrs+=float(row['Calculated Hrs'])
			totalFinalhrs+=float(row['Final Hrs'])
			row['Eng']=teamStr[eng]['Activity Type']
			if 'GES' in row['Eng']:
				#row['Execution Country']=salesCountry
				row['Execution Country']='United States'
			else:
				row['Execution Country']=teamStr[eng]['Country']
			row['Execution Year']=str(DateTime.Now.Year)
			if Quote.GetCustomField('R2QFlag').Content == 'Yes':
				row['Execution Year'] = str(R2Qexecution_year)
			labor=row['Eng']
			laborDetails=SqlHelper.GetFirst("select * from CT_HCI_PHD_LABORMATERIAL where Labor='{}'".format(labor))
			serviceMaterial=str(laborDetails.Service_Material)
			if serviceMaterial not in productPrice.keys():
				Addproduct =ProductHelper.CreateProduct(laborDetails.Service_Material)
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
				partNumber=laborDetails.Service_Material
				EC_GES=row['Execution Country']
				if '_CN' in partNumber or '_UZ' in partNumber:
					EC_GES=''
				cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails.Service_Material,row['Execution Year'],currency)
				if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost) == 0.00:
					row["Execution Country"] = alternate_execution_country
					cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails.Service_Material,row['Execution Year'],currency)
				EACCost=GS_HCI_PHD_Module.getEACCost(partNumber,currency)
				reginoalCost=cost+EACCost
				w2wFactor=GS_HCI_PHD_Module.getW2WFactor(partNumber)
				w2wCost=reginoalCost/(1+w2wFactor)
				row['Eng Unit Regional Cost']=str(reginoalCost)
				row['Eng Total Regional Cost']=str(float(reginoalCost)*float(row['Final Hrs']))
				row['Eng Total WTW Cost']=str(float(w2wCost)*float(row['Final Hrs']))
			totalCost += float(row['Eng Total Regional Cost'])
			totalListPrice += float(row['Eng Total List Price'])
			totalWTWCost += float(row['Eng Total WTW Cost'])

for eng in engLst:
	if eng in teamStr.keys() and teamStr[eng]['NoOfEng'] and teamStr[eng]['Travel Time']:
		task='Travel Time'
		row=contRows.AddNewRow(False)
		row['Deliverable']=task
		row['Calculated Hrs']=str( float(teamStr[eng]['NoOfEng']) * float(teamStr[eng]['Travel Time']))
		row['Productivity']="1"
		row['Final Hrs']= str( float(teamStr[eng]['NoOfEng']) * float(teamStr[eng]['Travel Time'])* int(row['Productivity']))
		finalHrs+=float(row['Final Hrs'])
		calcHrs+=float(row['Calculated Hrs'])
		totalFinalhrs+=float(row['Final Hrs'])
		row['Eng']=teamStr[eng]['Activity Type']
		if 'GES' in row['Eng']:
			#row['Execution Country']=salesCountry
			row['Execution Country']='United States'
		else:
			row['Execution Country']=teamStr[eng]['Country']
		row['Execution Year']=str(DateTime.Now.Year)
		if Quote.GetCustomField('R2QFlag').Content == 'Yes':
			row['Execution Year'] = str(R2Qexecution_year)
		labor=row['Eng']
		laborDetails=SqlHelper.GetFirst("select * from CT_HCI_PHD_LABORMATERIAL where Labor='{}'".format(labor))
		serviceMaterial=str(laborDetails.Service_Material)
		if serviceMaterial not in productPrice.keys():
			Addproduct =ProductHelper.CreateProduct(laborDetails.Service_Material)
			productPrice[serviceMaterial]=float(Addproduct.TotalPrice)
		listPrice=productPrice[serviceMaterial]
		row['Eng Unit List Price']=str(GS_HCI_PHD_Module.getCalculateListPrice(salesOrg,float(listPrice),row['Execution Year']))
		row['Eng Total List Price']=str(float(row['Eng Unit List Price'])*float(row['Final Hrs']))
		if 'GES' not in eng:
			cost=GS_HCI_PHD_Module.getLaborCost(row['Execution Country'],serviceMaterial,row['Execution Year'],currency)
			if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost) == 0.00:
				row["Execution Country"] = alternate_execution_country
				GS_HCI_PHD_Module.getLaborCost(row['Execution Country'],serviceMaterial,row['Execution Year'],currency)
			if salesCountry!=row['Execution Country']:
				cost=cost*1.1 if cost else 0
			w2wCost=cost
			if salesCountry!=row['Execution Country']:
				w2wCost=w2wCost/1.1 if w2wCost else 0
			row['Eng Unit Regional Cost']=str(cost)
			row['Eng Total Regional Cost']=str(float(cost)*float(row['Final Hrs']))
			row['Eng Total WTW Cost']=str(float(w2wCost)*float(row['Final Hrs']))
		else:
			partNumber=laborDetails.Service_Material
			EC_GES=row['Execution Country']
			if '_CN' in partNumber or '_UZ' in partNumber:
				EC_GES=''
			cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails.Service_Material,row['Execution Year'],currency)
			if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost) == 0.00:
				row["Execution Country"] = alternate_execution_country
				cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails.Service_Material,row['Execution Year'],currency)
			EACCost=GS_HCI_PHD_Module.getEACCost(partNumber,currency)
			reginoalCost=cost+EACCost
			w2wFactor=GS_HCI_PHD_Module.getW2WFactor(partNumber)
			w2wCost=reginoalCost/(1+w2wFactor)
			row['Eng Unit Regional Cost']=str(reginoalCost)
			row['Eng Total Regional Cost']=str(float(reginoalCost)*float(row['Final Hrs']))
			row['Eng Total WTW Cost']=str(float(w2wCost)*float(row['Final Hrs']))
		totalCost += float(row['Eng Total Regional Cost'])
		totalListPrice += float(row['Eng Total List Price'])
		totalWTWCost += float(row['Eng Total WTW Cost'])

row=Product.GetContainerByName('HCI_PHD_EngineeringLabour').AddNewRow(False)
row['Deliverable']='Total'
row['Final Hrs']=str(finalHrs)
row['Calculated Hrs']=str(calcHrs)
row['Eng Total Regional Cost']=str(totalCost)
row['Eng Total List Price']=str(totalListPrice)
row['Eng Total WTW Cost']=str(totalWTWCost)


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
contRows=Product.GetContainerByName('HCI_PHD_AdditionalDeliverables').Rows
for row in contRows:
	if row['Final Hrs'] and row['Hidden_lable']!='Total' :
		totalFinalhrs+=float(row['Final Hrs'])

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
	row['Calculated Hrs']=str(round(totalFinalhrs * (float(pmLaborDict[eng]['Percentage'])/100)))
	row['Productivity']="1"
	row['Final Hrs']= str( round(totalFinalhrs * (float(pmLaborDict[eng]['Percentage'])/100))* int(row['Productivity']))
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
	labor=row['Eng']
	laborDetails=SqlHelper.GetFirst("select * from CT_HCI_PHD_LABORMATERIAL where Labor='{}'".format(labor))
	serviceMaterial=str(laborDetails.Service_Material)
	if serviceMaterial not in productPrice.keys():
		Addproduct =ProductHelper.CreateProduct(laborDetails.Service_Material)
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
		partNumber=laborDetails.Service_Material
		EC_GES=row['Execution Country']
		if '_CN' in partNumber or '_UZ' in partNumber:
			EC_GES=''
		cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails.Service_Material,row['Execution Year'],currency)
		if Quote.GetCustomField('R2QFlag').Content == 'Yes' and float(cost)== 0.00:
			row["Execution Country"] = alternate_execution_country
			cost=GS_HCI_PHD_Module.getLaborCost(EC_GES,laborDetails.Service_Material,row['Execution Year'],currency)
		'''if salesCountry!=row['Execution Country']:
			cost=cost*1.1 if cost else 0'''
		EACCost=GS_HCI_PHD_Module.getEACCost(partNumber,currency)
		reginoalCost=cost+EACCost
		w2wFactor=GS_HCI_PHD_Module.getW2WFactor(partNumber)
		w2wCost=reginoalCost/(1+w2wFactor)
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
row['Deliverable']='Total'
row['Final Hrs']=str(pmFinalHrs)
row['Calculated Hrs']=str(pmCalcHrs)
row['Eng Total Regional Cost']=str(pmTotalCost)
row['Eng Total List Price']=str(pmTotalLP)
row['Eng Total WTW Cost']=str(pmTotalWTW)
row=contRows2.AddNewRow(False)
row['Deliverable']='Total'
row['Final Hrs']=str(leadEngFinalHrs)
row['Calculated Hrs']=str(leadEngCalcHrs)
row['Eng Total Regional Cost']=str(leadEngTotalCost)
row['Eng Total List Price']=str(leadEngTotalLP)
row['Eng Total WTW Cost']=str(leadEngTotalWTW)
if Product.GetContainerByName('HCI_PHD_AdditionalDeliverables') and Product.GetContainerByName('HCI_PHD_AdditionalDeliverables').Rows.Count < 1:
	Product.GetContainerByName('HCI_PHD_AdditionalDeliverables').AddNewRow(False)