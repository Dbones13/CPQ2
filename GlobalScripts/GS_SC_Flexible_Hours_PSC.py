def hideQuoteTable(table):
	table.AccessLevel = table.AccessLevel.Hidden

def clearTable(table):
	table.Rows.Clear()
	table.Save()

def ContractNew(QT_SC_FlexibleHours):
	for record in Quote.MainItems:
		if len(record.QI_PartNumber.Value) > 1 and record.RolledUpQuoteItem.startswith("1.1") and record.QI_SC_ItemFlag.Value != 'Hidden' :
			row = QT_SC_FlexibleHours.AddNewRow()
			if record.PartNumber == 'SESP':
				row["Module_Name"] = record.Description
				row["Flexible_Hours"]= FlexiHours
				row["Totals"]=FlexiHours
			elif record.PartNumber == 'Service Product' and record.Description in ('Service Contract Management','A360 Contract Management','Assessments','Preventive Maintenance','Requested Services'):
				for key in LaborMap:
					if key == record.Description:
						row["Module_Name"] = record.Description
						row["Flexible_Hours"]= LaborMap[key]
						row["Totals"]=LaborMap[key]
			else :
				row["Module_Name"] = record.Description
				row['Flexible_Hours'] =0
				row["Totals"]=0
	QT_SC_FlexibleHours.Save()
	for row in QT_SC_FlexibleHours.Rows:
		if  len(row["Module_Name"]) <1:
			QT_SC_FlexibleHours.DeleteRow(row.Id)
	QT_SC_FlexibleHours.Save()

def ContractRenew(QT_PSC_FlexibleHours,NewModules):
	ExistingModules = set()
	for row in QT_PSC_FlexibleHours.Rows:
		ExistingModules.add(row["Service_Product"]+"__"+row["Resource_Type"])
	NewlyAddedItems = NewModules.difference(ExistingModules)
	RemovedItems = ExistingModules.difference(NewModules)
	RetainedItems = NewModules & ExistingModules
	if RemovedItems:
		for name in RemovedItems:
			service = name.split("__")[0] if len(name.split("__")) > 1 else name
			resource_type = name.split("__")[1] if len(name.split("__")) > 1 else ""
			for row in QT_PSC_FlexibleHours.Rows:
				if row["Service_Product"] == service and row["Resource_Type"] == resource_type:
					QT_PSC_FlexibleHours.DeleteRow(row.Id)
		QT_PSC_FlexibleHours.Save()
	if NewlyAddedItems:
		for name in NewlyAddedItems:
			if name == 'SESP':
				row = QT_PSC_FlexibleHours.AddNewRow()
				row["Service_Product"] = name
				row["Flexible_Hours"]= FlexiHours
				row["Totals"]=FlexiHours
			elif name in ('Service Contract Management','A360 Contract Management','Assessments','Preventive Maintenance','Requested Services'):
				for key in LaborMap:
					if name in key:
						row = QT_PSC_FlexibleHours.AddNewRow()
						row["Service_Product"] = name
						row["Resource_Type"] = str(key).split("__")[1] if len(str(key).split("__")) > 0 else ""
						row["Flexible_Hours"]= LaborMap[key]
						row["Totals"]=LaborMap[key]
			else:
				row = QT_PSC_FlexibleHours.AddNewRow()
				row["Service_Product"] = name
				row["Resource_Type"] = ""
				row['Flexible_Hours'] =0
				row["Totals"]=0
		QT_PSC_FlexibleHours.Save()
	if RetainedItems:
		for name in RetainedItems:
			service = name.split("__")[0] if len(name.split("__")) > 1 else name
			resource_type = name.split("__")[1] if len(name.split("__")) > 1 else ""
			for row in QT_PSC_FlexibleHours.Rows:
				if row["Service_Product"] == service  and 'SESP' in service:
					if FlexiHours != row['Totals']:
						row["Flexible_Hours"]= FlexiHours
						row["Totals"]=FlexiHours
				elif row["Service_Product"] == service  and service in ('Service Contract Management','A360 Contract Management','Assessments','Preventive Maintenance','Requested Services') and row["Resource_Type"] == resource_type:
					if float(LaborMap[name]) != row['Totals']:
						row["Flexible_Hours"]= LaborMap[name]
						row["Totals"]= LaborMap[name]
		QT_PSC_FlexibleHours.Save()

if Quote.GetCustomField('Quote Type').Content in ['Contract New','Contract Renewal'] and Quote.GetGlobal('EditFlag') == '1' :
	Trace.Write("SCRIPT CHECK EXECUTION")
	QT_SC_FlexibleHours = Quote.QuoteTables["QT_SC_FlexibleHours"]
	QT_PSC_FlexibleHours = Quote.QuoteTables["QT_SC_PSC_Labor_Details"]
	Country             = Quote.GetCustomField('Opportunity Tab Booking Country').Content
	query               = SqlHelper.GetFirst("select Burden_Rate from CT_SC_LABOR_RESOURCETYPE where PartNumber='SVC-EST2-FD' and Country='{}'".format(Country))
	burdenRatePerHour = 0
	FlexiHours = 0
	NewModules = set()
	if query is not None:
		burdenRatePerHour   = float(query.Burden_Rate)/8
	LaborMap={}
	for item in Quote.MainItems:
		if item.PartNumber == 'Other cost details' and item.RolledUpQuoteItem.startswith("1.1"):
			costPrice=float(item.QI_SC_Cost.Value)
			if burdenRatePerHour == 0.00 :
				FlexiHours = 0
			else:
				FlexiHours=int(float(costPrice)/float(burdenRatePerHour))
				if FlexiHours==0:
					FlexiHours=14
		if  item.ProductName == 'Labor' and item.QI_SC_ItemFlag.Value == 'Hidden':
			for row in item.SelectedAttributes.GetContainerByName('SC_Labor_Summary_Container').Rows:
				if Quote.GetCustomField('Quote Type').Content == 'Contract New':
					if row['Deliverable_Hours']:
						LaborMap[row['Service_Product'].strip()]=row['Deliverable_Hours'].strip()
					else :
						LaborMap[row['Service_Product'].strip()]=0
				else:
					if row['Deliverable_Hours']:
						LaborMap[str(row['Service_Product']).strip()+"__"+str(row['Resource_Type']).strip()]= str(int(row['Deliverable_Hours'].strip() or 0)+int(LaborMap.get(str(row['Service_Product']).strip()+"__"+str(row['Resource_Type']).strip(),0))) if LaborMap.get(str(row['Service_Product']).strip()+"__"+str(row['Resource_Type']).strip()) else row['Deliverable_Hours'].strip()
						#LaborMap[str(row['Service_Product']).strip()+"__"+str(row['Resource_Type']).strip()]=row['Deliverable_Hours'].strip()
					else :
						LaborMap[str(row['Service_Product']).strip()+"__"+str(row['Resource_Type']).strip()]=0
		if len(item.QI_PartNumber.Value) > 1 and  item.RolledUpQuoteItem.startswith("1.1") and item.QI_SC_ItemFlag.Value != 'Hidden':
			NewModules.add(item.Description)
	
	if Quote.GetCustomField('Quote Type').Content == 'Contract New':
		clearTable(QT_SC_FlexibleHours)
		hideQuoteTable(QT_PSC_FlexibleHours)
		ContractNew(QT_SC_FlexibleHours)
		
	elif Quote.GetCustomField('Quote Type').Content == 'Contract Renewal':
		hideQuoteTable(QT_SC_FlexibleHours)
		ContractRenew(QT_PSC_FlexibleHours,NewModules)
	Quote.SetGlobal('EditFlag','0')
	Quote.Save(False)

if Quote.GetCustomField('Quote Type').Content in ['Contract New','Contract Renewal']:
	QT_LineItemDetails  = Quote.QuoteTables["QT_PROJECT_BOOKING_LINE_ITEM_DETAILS"]
	hideQuoteTable(QT_LineItemDetails)