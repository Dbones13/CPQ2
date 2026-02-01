def FlexibleHoursValidation(tRow, cName):
	QT_SC_FlexibleHours = Quote.QuoteTables["QT_SC_FlexibleHours"]
	tRow["Totals"] = float(tRow["Flexible_Hours"]) + float(tRow["January"]) +  float(tRow["February"]) +  float(tRow["March"]) +  float(tRow["April"]) +  float(tRow["May"]) +	float(tRow["June"]) +  float(tRow["July"]) +  float(tRow["August"]) +  float(tRow["September"]) +  float(tRow["October"]) +	 float(tRow["November"]) +	float(tRow["December"])
	QT_SC_FlexibleHours.Save()
	if tRow['Service_Product'] in ('SESP Value Plus','SESP Value Remote Plus'):
		Country = Quote.GetCustomField('Opportunity Tab Booking Country').Content
		burdenRatePerHour = 0
		FlexiHours = 0
		query = SqlHelper.GetFirst("select Burden_Rate from CT_SC_LABOR_RESOURCETYPE where PartNumber='SVC-EST2-FD' and Country='{}'".format(Country))
		if query is not None:
			burdenRatePerHour = float(query.Burden_Rate)/8
		for record in filter(lambda y : y.PartNumber == 'Other cost details' and y.RolledUpQuoteItem.startswith("1.1"), Quote.MainItems):
			costPrice=float(record.QI_SC_CostPrice.Value.split()[1])
			if burdenRatePerHour == 0.00 :
				FlexiHours = 14
			else:
				FlexiHours=int(float(costPrice)/float(burdenRatePerHour))
				if FlexiHours==0:
					FlexiHours=14
		if tRow['Totals']!=FlexiHours:
			Quote.GetCustomField('SC_CF_QT_BookingInfo_Msg').Visible=True
			Quote.GetCustomField('SC_CF_QT_BookingInfo_Msg').Content = 'Total hours should be same as deliverable hours'
			tRow['Totals'] = FlexiHours
			QT_SC_FlexibleHours.Save()

	elif tRow['Service_Product'] in ('Service Contract Management', 'A360 Contract Management','Assessments','Preventive Maintenance','Requested Services'):
		LaborMap={}
		for item in Quote.MainItems:
			if item.ProductName == 'Labor' and item.QI_SC_ItemFlag.Value == 'Hidden':
				for row in item.SelectedAttributes.GetContainerByName('SC_Labor_Summary_Container').Rows:
					if row['Service_Product'].strip() == tRow['Service_Product'] and row['Entitlement'] == tRow['Entitlement'] and row['Resource_Type'] == tRow['Resource_Type'] :
						if row['Deliverable_Hours']:
							LaborMap[tRow['Service_Product'] + '_' + tRow['Entitlement'] + '_' + tRow['Resource_Type']]= LaborMap.get(tRow['Service_Product'] + '_' + tRow['Entitlement'] + '_' + tRow['Resource_Type'], 0) + (float(row['Deliverable_Hours'].strip()) if row['Deliverable_Hours'].strip() else 0)
						else:
							LaborMap[tRow['Service_Product'] + '_' + tRow['Entitlement'] + '_' + tRow['Resource_Type']]=0
		if tRow['Totals']!=float(LaborMap[tRow['Service_Product'] + '_' + tRow['Entitlement'] + '_' + tRow['Resource_Type']]): 
			Quote.GetCustomField('SC_CF_QT_BookingInfo_Msg').Visible=True
			Quote.GetCustomField('SC_CF_QT_BookingInfo_Msg').Content = 'Total hours should be same as deliverable hours'
			tRow['Totals'] = float(LaborMap[tRow['Service_Product'] + '_' + tRow['Entitlement'] + '_' + tRow['Resource_Type']])
			QT_SC_FlexibleHours.Save()

	for qRow in QT_SC_FlexibleHours.Rows:
		tot = sum(qRow[columnName] for columnName in ('Flexible_Hours', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'))
		if tot != qRow['Totals']:
			Quote.GetCustomField('SC_CF_QT_BookingInfo_Msg').Visible=True
			Quote.GetCustomField('SC_CF_QT_BookingInfo_Msg').Content = 'Total hours should be same as deliverable hours'
			break


if len(EventArgs.Cells)>0:
	columnName = EventArgs.Cells[0].ColumnName
	currentRow = EventArgs.Cells[0].Row
	QT_SC_FlexibleHours = Quote.QuoteTables["QT_SC_FlexibleHours"]
	Quote.GetCustomField('SC_CF_QT_BookingInfo_Msg').Content = ''
	Quote.GetCustomField('SC_CF_QT_BookingInfo_Msg').Visible=False
	if columnName in ('Flexible_Hours','January','February','March','April','May','June','July','August','September','October','November','December'):
		FlexibleHoursValidation(currentRow, columnName)
