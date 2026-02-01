gesLocation = Product.Attr("FDA GES Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
contList = []
laborCont = Product.GetContainerByName('FDA_Engineering_Labor_Container')
tableLabor = SqlHelper.GetList('select * from FIRE_DETECTION_AND_ALARM_ENGINEERING_LABOR_CUSTOM_TABLE')
if laborCont.Rows.Count > 0:
	for new_row in laborCont.Rows:
		for row in tableLabor:
			if  new_row["Deliverable"]  ==  row.Deliverable:
				if gesLocation == "None" or gesLocation == '':
					#Log.Write("None condition")
					new_row['GES Eng'] = ''
					new_row["FO Eng 1 % Split"] =  row.FO_Eng_1_GES_None
					new_row["FO Eng 2 % Split"] = row.FO_Eng_2_GES_None
					new_row["GES Eng % Split"] = "0"
					new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
					new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
					new_row['FO Eng 1'] = row.FO_Eng_1_NoGES
					new_row['FO Eng 2'] = row.FO_Eng_2_NoGES
				else:
					Trace.Write('Test2')
					if gesLocation !="None":
						#Log.Write("Not None condition")
						new_row["FO Eng 1 % Split"] = row.FO_Eng_1_GES
						new_row["FO Eng 2 % Split"] = row.FO_Eng_2_GES
						new_row["GES Eng % Split"] = row.GES_Eng_1
						new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
						new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
						new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
						new_row['FO Eng 1'] = row.FO_Eng_1_NoGES
						new_row['FO Eng 2'] = row.FO_Eng_2_NoGES
	laborCont.Calculate()
	contList.append('FDA_Engineering_Labor_Container')
laborCont4 = Product.GetContainerByName('FDA_Additional_Labor_Container')
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
			#new_row["GES Eng % Split"]= '0'
			#new_row["FO Eng % Split"]= '100'
	laborCont4.Calculate()
	contList.append('FDA_Additional_Labor_Container')
