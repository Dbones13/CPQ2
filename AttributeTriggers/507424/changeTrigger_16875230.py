gesLocation = Product.Attr("PSW_GES_Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
contList = []
sec=Product.Attr('Ges_Location_44925').GetValue()
laborCont = Product.GetContainerByName('PSW_Labor_Container')
tableLabor = SqlHelper.GetList('select * from Process_Safety_Workbench_Engineering_Custom_Table')
if laborCont.Rows.Count > 0:
	for new_row in laborCont.Rows:
		for row in tableLabor:
			if  new_row["Deliverable"]  ==  row.Deliverable:
				if gesLocation == "None" or gesLocation == '':
					Log.Write("None condition")
					new_row['GES Eng'] = ''
					new_row["FO Eng 1 % Split"] =  row.FO_Eng_1_Split_GES_None
					new_row["FO Eng 2 % Split"] = row.FO_Eng_2_Split_GES_None
					new_row["GES Eng % Split"] = "0"
					new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_Ges_None)
					new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2)
					new_row['FO Eng 1'] = row.FO_Eng_1_Ges_None
					new_row['FO Eng 2'] = row.FO_Eng_2
				else:
					Trace.Write('Test2')
					if gesLocation !="None" and sec =="None":
						Log.Write("Not None condition")
						new_row["FO Eng 1 % Split"] = row.FO_Eng_1_GES
						new_row["FO Eng 2 % Split"] = row.FO_Eng_2_GES
						new_row["GES Eng % Split"] = row.GES_Eng_Split
						new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
						new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1)
						new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2)
						new_row['FO Eng 1'] = row.FO_Eng_1
						new_row['FO Eng 2'] = row.FO_Eng_2
	laborCont.Calculate()
	contList.append('PSW_Labor_Container')
laborCont4 = Product.GetContainerByName('PSW_Additional_Labor_Container')
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
	contList.append('PSW_Additional_Labor_Container')
if len(contList) > 0:
	ScriptExecutor.Execute('PS_PSW_Update_Labor_Cost')
sec=Product.Attr('Ges_Location_44925').AssignValue(gesLocation)