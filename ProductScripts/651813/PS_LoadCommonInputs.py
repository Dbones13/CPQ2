prd_Family=Product.Attributes.GetByName('HCI_PHD_Prd_Family').GetValue()
if not prd_Family:
	Product.DisallowAttr('HCI_PHD_AddSelected')
	Product.DisallowAttrValues('HCI_Product_Choices', 'PHD_Labor', 'Uniformance_Insight_Labor', 'AFM_Labor')
else:
	Product.AllowAttr('HCI_PHD_AddSelected')
	Product.AllowAttrValues('HCI_Product_Choices', 'PHD_Labor', 'Uniformance_Insight_Labor', 'AFM_Labor')
Session['PHDCommonInputs']={}
teamStr={}
contRows=Product.GetContainerByName('HCI_PHD_Fo_Eng').Rows
for row in contRows:
	if row['Participation'] and  float(row['Participation']) != float(0):
		teamStr[row['Engineer']]={}
		teamStr[row['Engineer']]['Activity Type']=row['Activity Type']
		teamStr[row['Engineer']]['Participation']=row['Participation']
		teamStr[row['Engineer']]['Country']=row['Execution Country']
		teamStr[row['Engineer']]['NoOfEng']=row['Number of trips per engineer']
		teamStr[row['Engineer']]['Travel Time']=row['Hours per trip']
contRows=Product.GetContainerByName('HCI_PHD_GES_Eng').Rows
gesEngContry=Product.Attributes.GetByName('HCI_PHD_GES_Location').GetValue()
for row in contRows:
	if row['Participation'] and  float(row['Participation']) != float(0):
		teamStr[row['Engineer']]={}
		teamStr[row['Engineer']]['Activity Type']=row['Activity Type']
		teamStr[row['Engineer']]['Participation']=row['Participation']
		teamStr[row['Engineer']]['Country']=gesEngContry
		teamStr[row['Engineer']]['NoOfEng']=row['Number of trips per engineer']
		teamStr[row['Engineer']]['Travel Time']=row['Hours per trip']
Trace.Write(str(teamStr))
Session['PHDCommonInputs']['teamStr']=teamStr
scopeDict={}
if Product.GetContainerByName("HCI_Labor_common_prj_input1").Rows.Count != 0:
	contRows=Product.GetContainerByName("HCI_Labor_common_prj_input1").Rows[0].Columns
	for col in contRows:
		scopeDict[col.Name ]=col.DisplayValue
if Product.GetContainerByName("HCI_Labor_common_prj_input2").Rows.Count != 0:
	contRows=Product.GetContainerByName("HCI_Labor_common_prj_input2").Rows[0].Columns
	for col in contRows:
		scopeDict[col.Name ]=col.DisplayValue
Session['PHDCommonInputs']['scopeDict']=scopeDict
if Product.GetContainerByName('HCI_PHD_Fo_Eng').Rows.Count>0 and Quote.GetCustomField('R2QFlag').Content == 'Yes':
	prjLbr_country = str(Product.GetContainerByName('HCI_PHD_Fo_Eng').Rows[0]['Execution Country'])
	Trace.Write('in R2Q--'+str(Product.GetContainerByName('HCI_PHD_Fo_Eng').Rows[0]['Execution Country']))
	Product.Attr('AR_HCI_FO_ENG_Executioncountry').SelectDisplayValue(prjLbr_country)
	for i in Product.GetContainerByName('HCI_Labor_prj_mng_lbr_input').Rows:
		i.GetColumnByName('Execution Country').ReferencingAttribute.SelectDisplayValue(prjLbr_country)
pmLaborDict={}
particpationhours = 0
contRows=Product.GetContainerByName('HCI_Labor_prj_mng_lbr_input').Rows
for row in contRows:
	if row['Percentage'] and  float(row['Percentage']) != float(0):
		pmLaborDict[row['Role']]={}
		pmLaborDict[row['Role']]['Percentage']=row['Percentage']
		pmLaborDict[row['Role']]['Activity_Type']=row['Activity_Type']
		pmLaborDict[row['Role']]['Country']=row['Execution Country']
if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
	if Product.GetContainerByName('HCI_PHD_Fo_Eng').Rows.Count>0:
		contRowsEng=Product.GetContainerByName('HCI_PHD_Fo_Eng').Rows[0]
		particpationhours = 100 - int(Product.Attributes.GetByName('AR_HCI_GES Participation %').GetValue() or 0)
		contRowsEng.SetColumnValue('Participation',str(particpationhours))
		Trace.Write('particpationhours---2-'+str(particpationhours))
	if Product.GetContainerByName('HCI_PHD_GES_Eng').Rows.Count>0:
		contRowsGES=Product.GetContainerByName('HCI_PHD_GES_Eng').Rows[0]
		contRowsGES.SetColumnValue('Participation',str(Product.Attributes.GetByName('AR_HCI_GES Participation %').GetValue() or 0))

particpationhours = int(float(Product.ParseString('<*CTX(Container(HCI_PHD_Fo_Eng).Sum("Participation"))*>'))) + int(float(Product.ParseString('<*CTX(Container(HCI_PHD_GES_Eng).Sum("Participation"))*>')))
Trace.Write(str(float(Product.ParseString('<*CTX(Container(HCI_PHD_Fo_Eng).Sum("Participation"))*>')))+'---Str---flag -'+str(particpationhours))
if particpationhours == 100:
	Product.Attributes.GetByName('AR_HCI_ParticipationFlag').AssignValue('True')
else:
	Product.Attributes.GetByName('AR_HCI_ParticipationFlag').AssignValue('False')

FoEngs=int(Product.Attributes.GetByName('AR_HCI_No_FO_ENG').GetValue()) if Product.Attributes.GetByName('AR_HCI_No_FO_ENG').GetValue() else 0
GAESEngs=int(Product.Attributes.GetByName('AR_HCI_No_GES_ENG').GetValue()) if Product.Attributes.GetByName('AR_HCI_No_GES_ENG').GetValue() else 0
noOfEngs=FoEngs+GAESEngs
Session['PHDCommonInputs']['noOfEngs']=noOfEngs
Session['PHDCommonInputs']['pmLaborDict']=pmLaborDict
json=Session['PHDCommonInputs']
jsonStr=JsonHelper.Serialize(json)
Log.Write(str(jsonStr)+'=jsonStr----hci--'+str(json))
Product.Attributes.GetByName('HCI_PHD_ParChildAttr').AssignValue(jsonStr)
Product.ApplyRules()
if Quote.GetCustomField('R2QFlag').Content == 'Yes':
	if Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows.Count>0:
		if Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows[0]['Graphics and Reports'] == 'Yes':
			Product.Attributes.GetByName('HCI_PHD_IsReports').AssignValue('True')
			Product.AllowAttr('HCI_PHD_NewDisplaysforInsight')
			Product.AllowAttr('HCI_PHD_ExcelReports')
		else:
			Product.Attributes.GetByName('HCI_PHD_IsReports').AssignValue('False')
			Product.DisallowAttr('HCI_PHD_NewDisplaysforInsight')
			Product.DisallowAttr('HCI_PHD_ExcelReports')
	'''if Product.Attributes.GetByName('HCI_PHD_GES_Location').GetValue():
		Product.AllowAttr('HCI_PHD_GES_Eng')
	else:
		Product.DisallowAttr('HCI_PHD_GES_Eng')'''