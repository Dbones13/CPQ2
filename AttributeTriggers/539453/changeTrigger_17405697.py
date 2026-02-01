gesLocation = Product.Attr("Experion_HS_Ges_Location_Labour").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
contList = []
sec=Product.Attr('Ges_Location_44925').GetValue()

laborCont = Product.GetContainerByName('HMI_Engineering_Labor_Container')
tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Execution_Country,FO_Eng_1_GES_Loc,FO_Eng_2_GES_Loc from HMI_ENGINEERING_LABOR_CONTAINER')
if laborCont.Rows.Count > 0:
	for new_row in laborCont.Rows:
		for row in tableLabor:
			if  new_row["Deliverable"]  ==  row.Deliverable:
				if gesLocation == "None" or gesLocation == '':
					Trace.Write("Deep")
					new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
					new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
					new_row['FO Eng 1']=row.FO_Eng_1_NoGES
					new_row['FO Eng 2']=row.FO_Eng_2_NoGES
					new_row["GES Eng % Split"]= row.GES_Eng_1_No
					new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
					new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
				else:
					Trace.Write('Test2')
					r2q = Quote.GetCustomField('R2QFlag').Content
					if (gesLocation !="None" and sec =="None") or (r2q == 'Yes' and gesLocation !="None") :
						Trace.Write('Test')
						Log.Info('GES Location1 --- '+str(gesLocation))
						new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_GES_Loc)
						new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_GES_Loc)
						new_row['FO Eng 1']=row.FO_Eng_1_GES_Loc
						new_row['FO Eng 2']=row.FO_Eng_2_GES_Loc
						new_row["GES Eng % Split"]= row.GES_Eng
						new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
						new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
						if new_row["Deliverable"] == 'HMI Operator Interface Workshop':
							new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES HMI Eng-BO-'+gesLocationVC)
	laborCont.Calculate()
	contList.append('HMI_Engineering_Labor_Container')

laborCont1 = Product.GetContainerByName('System_Network_Engineering_Labor_Container')
tableLabor1 = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Execution_Country,FO_Eng_1_LOC_GES from System_Network_ENGINEERING_LABOR')
if laborCont1.Rows.Count > 0:
	for new_row in laborCont1.Rows:
		for row in tableLabor1:
			if  new_row["Deliverable"]  ==  row.Deliverable:
				if gesLocation == "None" or gesLocation == '':
					new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
					new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
					new_row['FO Eng 1']=row.FO_Eng_1_NoGES
					new_row['FO Eng 2']=row.FO_Eng_2_NoGES
					new_row["GES Eng % Split"]= row.GES_Eng_1_No
					new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
					new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
				else:
					if gesLocation !="None" and sec =="None":
						new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_LOC_GES)
						new_row.GetColumnByName('FO Eng 2').SetAttributeValue('None')
						new_row['FO Eng 1']=row.FO_Eng_1_LOC_GES
						new_row['FO Eng 2']='None'
						new_row["GES Eng % Split"]= row.GES_Eng
						new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
						new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
	laborCont1.Calculate()
	contList.append('System_Network_Engineering_Labor_Container')

laborCont2 = Product.GetContainerByName('System_Interface_Engineering_Labor_Container')
tableLabor2 = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Execution_Country from System_Interface_Labor')
if laborCont2.Rows.Count > 0:
	for new_row in laborCont2.Rows:
		for row in tableLabor2:
			if  new_row["Deliverable"]  ==  row.Deliverable:
				if gesLocation == "None" or gesLocation == '':
					new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
					new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
					new_row['FO Eng 1']=row.FO_Eng_1_NoGES
					new_row['FO Eng 2']=row.FO_Eng_2_NoGES
					new_row["GES Eng % Split"]= row.GES_Eng_1_No
					new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
					new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
				else:
					if gesLocation !="None" and sec =="None":
						new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
						new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
						new_row['FO Eng 1']=row.FO_Eng_1_NoGES
						new_row['FO Eng 2']=row.FO_Eng_2_NoGES
						new_row["GES Eng % Split"]= row.GES_Eng
						new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
						new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
	laborCont2.Calculate()
	contList.append('System_Interface_Engineering_Labor_Container')

laborCont3 = Product.GetContainerByName('Hardware Engineering Labour Container')
tableLabor3 = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Execution_Country from HARDWARE_ENGINEERING_DELIVERABLE')
if laborCont3.Rows.Count > 0:
	for new_row in laborCont3.Rows:
		for row in tableLabor3:
			if  new_row["Deliverable"]  ==  row.Deliverable:
				if gesLocation == "None" or gesLocation == '':
					new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
					new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
					new_row['FO Eng 1']=row.FO_Eng_1_NoGES
					new_row['FO Eng 2']=row.FO_Eng_2_NoGES
					new_row["GES Eng % Split"]= row.GES_Eng_1_No
					new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
					new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
				else:
					if gesLocation !="None" and sec =="None":
						new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
						new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
						new_row['FO Eng 1']=row.FO_Eng_1_NoGES
						new_row['FO Eng 2']=row.FO_Eng_2_NoGES
						new_row["GES Eng % Split"]= row.GES_Eng
						new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
						new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
	laborCont3.Calculate()
	contList.append('Hardware Engineering Labour Container')

laborCont5 = Product.GetContainerByName('EBR_Engineering_Labor_Container')
tableLabor5 = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Execution_Country from EBR_ENGINEERING_LABOR_CONTAINER')
if laborCont5.Rows.Count > 0:
	for new_row in laborCont5.Rows:
		for row in tableLabor5:
			if  new_row["Deliverable"]  ==  row.Deliverable:
				if gesLocation == "None" or gesLocation == '':
					new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
					new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
					new_row['FO Eng 1']=row.FO_Eng_1_NoGES
					new_row['FO Eng 2']=row.FO_Eng_2_NoGES
					new_row["GES Eng % Split"]= row.GES_Eng_1_No
					new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
					new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
				else:
					Trace.Write('Test2')
					if gesLocation !="None" and sec =="None":
						Trace.Write('Test')
						new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
						new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
						new_row['FO Eng 1']=row.FO_Eng_1_NoGES
						new_row['FO Eng 2']=row.FO_Eng_2_NoGES
						new_row["GES Eng % Split"]= row.GES_Eng
						new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
						new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
	laborCont5.Calculate()
	contList.append('EBR_Engineering_Labor_Container')

laborCont4 = Product.GetContainerByName('Additional_CustomDev_Labour_Container')
if laborCont4.Rows.Count > 0:
	for new_row in laborCont4.Rows:
		if gesLocation == "None" or gesLocation == '':
			new_row['GES Eng'] = ''
			new_row["GES Eng % Split"]= '0'
			new_row["FO Eng % Split"]= '100'
		else:
			new_row['GES Location'] = gesLocationVC
			new_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
			new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
			new_row['GES Eng']=('SYS GES Eng-BO-'+gesLocationVC)
			#new_row["GES Eng % Split"]= '0'
			#new_row["FO Eng % Split"]= '100'
	laborCont4.Calculate()
	contList.append('Hardware Engineering Labour Container')

if len(contList) > 0:
	ScriptExecutor.Execute('PS_Labor_Part_Summary')
sec=Product.Attr('Ges_Location_44925').AssignValue(gesLocation)
Trace.Write('GES1Bottom= '+str(sec))
