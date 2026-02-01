SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if SC_Product_Type == 'Renewal':
	SC_Pricing_Escalation = Product.Attr('SC_Pricing_Escalation').GetValue()
	if arg.NameOfCurrentTab == 'Scope Summary':
		Vcont = Product.GetContainerByName('SC_Honeywell_Scope_Summary_Pricing')
		cont = Product.GetContainerByName('HDP_OPB_Editable_Storage_Cont')
		hcont = Product.GetContainerByName('SC_RC_Honeywell_Scope_Summary_Pricing_Hidden')
		for row in cont.Rows:
			for ro in Vcont.Rows:
				if ro['Description'] == row['Description']:
					ro['PY_Quantity'] = row['PY_Quantity']
					ro['PY_ListPrice'] = row['PY_ListPrice']
			for row1 in hcont.Rows:
				if row1['Description'] == row['Description']:
					row1['PY_Quantity'] = row['PY_Quantity']
					row1['PY_ListPrice'] = row['PY_ListPrice']
	#cont.Rows.Clear()
	#Condition for OPB
	Vcont = Product.GetContainerByName('SC_Honeywell_Scope_Summary_Pricing')
	hcont = Product.GetContainerByName('SC_RC_Honeywell_Scope_Summary_Pricing_Hidden')
	ComparisonSummary = Product.GetContainerByName("ComparisonSummary")
	for row in Vcont.Rows:
		if row['PY_Quantity'] == "":
			row['PY_Quantity'] = "0"
		if float(row['PY_Quantity']) != 0:
			row['PY_UnitPrice'] = str((float(row['PY_ListPrice']) / float(row['PY_Quantity']))) if row['PY_ListPrice'] else 0
		else:
			row['PY_UnitPrice'] = "0"
	for row in hcont.Rows:
		if row['PY_Quantity'] == "":
			row['PY_Quantity'] = "0"
		if float(row['PY_Quantity']) != 0:
			row['PY_UnitPrice'] = str((float(row['PY_ListPrice']) / float(row['PY_Quantity']))) if row['PY_ListPrice'] else 0
		else:
			row['PY_UnitPrice'] = "0"

	'''for row in ComparisonSummary.Rows:
		if float(row['Configured_PY_List_Price']) == 0.0:
			row['Configured_PY_List_Price'] = row['PY_List_Price_SFDC']'''
	for row in hcont.Rows:
		if row['Description'] == "Base Package Experion":
			row['PY_Quantity'] = "1"
	for row in Vcont.Rows:
		if row['Description'] == "Base Package Experion":
			row['PY_Quantity'] = "1"
		if row['Description'] == "No of Concurrent Users or Stations":
			if int(row['PY_Quantity']) <0 or int(row['PY_Quantity']) > 99:
				row['PY_Quantity'] = "0"

	Vcont = Product.GetContainerByName('SC_Honeywell_Scope_Summary_Pricing')
	for row in Vcont.Rows:
		if int(row['R_Quantity']) > int(row['PY_Quantity']):
			row['SR_Quantity'] = '0'
			row['SA_Quantity'] = str(int(row['R_Quantity'])-int(row['PY_Quantity']))
			row['Comments'] = "Scope Addition"
		elif int(row['R_Quantity']) < int(row['PY_Quantity']):
			row['SR_Quantity'] = str(int(row['R_Quantity'])-int(row['PY_Quantity']))
			row['SA_Quantity'] = '0'
			row['Comments'] = "Scope Reduction"
		else:
			row['SR_Quantity'] = '0'
			row['SA_Quantity'] = '0'
			row['Comments'] = "No Scope Change"
		row['SR_Price'] = str (float(row['SR_Quantity']) * float(row['PY_UnitPrice']))
		row['SA_Price'] = str(float(row['SA_Quantity']) * float(row['HW_ListPrice']))

	hcont = Product.GetContainerByName('SC_RC_Honeywell_Scope_Summary_Pricing_Hidden')
	for row in hcont.Rows:
		if int(row['Quantity']) > int(row['PY_Quantity']):
			row['SR_Quantity'] = '0'
			row['SA_Quantity'] = str(int(row['Quantity'])-int(row['PY_Quantity']))
			row['Comments'] = "Scope Addition"
		elif int(row['Quantity']) < int(row['PY_Quantity']):
			row['SR_Quantity'] = str(int(row['Quantity'])-int(row['PY_Quantity']))
			row['SA_Quantity'] = '0'
			row['Comments'] = "Scope Reduction"
		else:
			row['SR_Quantity'] = '0'
			row['SA_Quantity'] = '0'
			row['Comments'] = "No Scope Change"
		row['SR_Price'] = str (float(row['SR_Quantity']) * float(row['PY_UnitPrice']))
		row['SA_Price'] = str(float(row['SA_Quantity']) * float(row['HW_ListPrice']))
		if SC_Pricing_Escalation == "Yes":
			if row['Comments'] == "Scope Reduction" or row['Comments'] == "No Scope Change":
				row['Escalation_Price'] = str(float(row['Quantity'])*float(row['PY_ListPrice'])/float(row['PY_Quantity'])) if row['PY_Quantity'] not in ('','0') else '0'
				row['Hidden_ListPrice'] = str(float(row['Quantity'])*float(row['PY_ListPrice'])/float(row['PY_Quantity'])) if row['PY_Quantity'] not in ('','0') else '0'
			elif row['Comments'] == "Scope Addition":
				row['Escalation_Price'] = str(float(row['PY_Quantity']) * float(row['PY_ListPrice']))
				row['Hidden_ListPrice'] = str(float(row['PY_ListPrice']) + ((float(row['Quantity']) - float(row['PY_Quantity']))*float(row['HW_ListPrice'])))
				Trace.Write(str((float(row['PY_Quantity']) * float(row['PY_ListPrice'])) + (float(row['Quantity']) * (float(row['HW_ListPrice'])))))
		else:
			row['Escalation_Price'] = '0'
			row['Hidden_ListPrice'] = str(float(row['Quantity']) * float(row['HW_ListPrice']))
	Vcont = Product.GetContainerByName('SC_Honeywell_Scope_Summary_Pricing')
	x = 0
	for i in Vcont.Rows:
		if i['PY_ListPrice'] == "":
			i['PY_ListPrice'] = "0"
		x =  float(i['PY_ListPrice']) + x
	for row in ComparisonSummary.Rows:
		#row['Configured_PY_List_Price'] = str(x)
		a = row['PY_List_Price_SFDC']
		b = row['Configured_PY_List_Price']
		if a == "":
			a = 0
		if b == "":
			b = 0
		row['List_Price_Delta'] = str(float(a) - float(b))

	if True:
		SummaryContHidden = Product.GetContainerByName('SC_RC_Honeywell_Scope_Summary_Pricing_Hidden')
		HW_Summary_Cont = Product.GetContainerByName('SC_Honeywell_Scope_Summary_Pricing')
		HW_Summary_Cont.Rows.Clear()
		x = Product.Attr("SC_HDP_RC_Selection").SelectedValues
		if SummaryContHidden.Rows.Count:
			for row in SummaryContHidden.Rows:
				for i in x:
					if i.Display == row["Comments"]:
						HW_summary_row = HW_Summary_Cont.AddNewRow(False)
						HW_summary_row['Description'] = row['Description']
						HW_summary_row['Quantity'] = row['Quantity']
						HW_summary_row['PY_Quantity'] = row['PY_Quantity']
						HW_summary_row['PY_UnitPrice'] = row['PY_UnitPrice']
						HW_summary_row['PY_ListPrice'] = row['PY_ListPrice']
						HW_summary_row['HW_ListPrice'] = row['HW_ListPrice']
						HW_summary_row['SR_Quantity'] = row['SR_Quantity']
						HW_summary_row['SA_Quantity'] = row['SA_Quantity']
						HW_summary_row['R_Quantity'] = row['Quantity']
						HW_summary_row['SR_Price'] = str(float(row['SR_Quantity']) * float(row['PY_UnitPrice']))
						HW_summary_row['SA_Price'] = str(float(row['SA_Quantity']) * float(row['HW_ListPrice']))
						HW_summary_row['Comments'] = row['Comments']
						HW_summary_row.Calculate()
				HW_Summary_Cont.Calculate()
	for row3 in hcont.Rows:
		row3['PY_Quantity_Backup'] = row3['Quantity']
	Vcont.Calculate()
	hcont.Calculate()
	Vcont.Calculate()
	ComparisonSummary.Calculate()