def getExistingDeliverableRowsDict(container):
	existing_deliverables = {}
	for row in container.Rows:
		existing_deliverables[row['Deliverable']] = row
	return existing_deliverables

def deleteExistingDeliverableRows(container, finalDeliverables, Product=None):
	deleteRowsList = []
	try:
		if Product:
			additionalContainer = Product.GetContainerByName('MSID_Additional_Custom_Deliverables')
			for row in additionalContainer.Rows:
				finalDeliverables.append(row['Deliverable_Name'])
	except Exception as e:
		Trace.Write('MSID_Additional_Custom_Deliverables not available'+str(e))
	for row in container.Rows:
		if row["Deliverable"] not in finalDeliverables:
			deleteRowsList.append(row.RowIndex)
	deleteRowsList.reverse()
	for deleteRow in deleteRowsList:
		container.DeleteRow(deleteRow)
	onSiteHeaderRowIndex = None
	shouldReOrder = False
	for row in container.Rows:
		if row['Deliverable'] == 'On-Site':
			onSiteHeaderRowIndex = row.RowIndex
		elif row['Deliverable_Type'] == 'Offsite' and onSiteHeaderRowIndex and (row.RowIndex > onSiteHeaderRowIndex):
			shouldReOrder = True
	if shouldReOrder:
		offSiteList = []
		onSiteList = []
		deleteRowIndexes = []
		for row in container.Rows:
			if row['Deliverable_Type'] == 'Offsite' and row.RowIndex > onSiteHeaderRowIndex:
				rowData = {}
				rowData['IsSelected'] = row.IsSelected
				for col in row.Columns:
					rowData[col.Name] = col.Value
				offSiteList.append(rowData)
			elif row['Deliverable'] == 'On-Site' or row['Deliverable_Type'] == 'Onsite':
				rowData = {}
				rowData['IsSelected'] = row.IsSelected
				for col in row.Columns:
					rowData[col.Name] = col.Value
				onSiteList.append(rowData)
			if row.RowIndex >= onSiteHeaderRowIndex:
				deleteRowIndexes.append(row.RowIndex)
		deleteRowIndexes.reverse()
		for rowIndex in deleteRowIndexes:
			container.DeleteRow(rowIndex)
		for data in offSiteList:
			row = container.AddNewRow(False)
			for key, val in data.items():
				if key == 'IsSelected':
					row.IsSelected = val
				else:
					row[key] = val
		for data in onSiteList:
			row = container.AddNewRow(False)
			for key, val in data.items():
				if key == 'IsSelected':
					row.IsSelected = val
				else:
					row[key] = val
					
def getExistingDeliverablegraphicsRowsDict(container):
	existing_deliverables = {}
	for row in container.Rows:
		deliverable = row["Deliverable"].strip()
		deliverable_type = row["Deliverable_Type"].strip()
		if not deliverable_type:
			if deliverable == 'Total':
				deliverable_type = 'Total'
			elif deliverable == 'Off-Site':
				deliverable_type = 'Offsite'
			elif deliverable == 'On-Site':
				deliverable_type = 'Onsite'
		key = (deliverable, deliverable_type)
		existing_deliverables[key] = row
		Trace.Write("existing_deliverables: " + str(existing_deliverables))
	return existing_deliverables

def deleteExistingDeliverablegraphicsrows(container, finalDeliverables, Product=None):
	deleteRowsList = []

	try:
		if Product:
			Trace.Write("productname" + str(Product.Name))
			additionalContainer = Product.GetContainerByName('MSID_Additional_Custom_Deliverables')
			for row in additionalContainer.Rows:
				finalDeliverables.append((row['Deliverable_Name'], row['Type']))
	except Exception as e:
		Trace.Write('MSID_Additional_Custom_Deliverables not available' + str(e))
	finalDeliverables_set = set(finalDeliverables)
	for row in container.Rows:
		Trace.Write("deliverable"+str(row["Deliverable"])+"deliverable_type"+str(row["Deliverable_Type"])+"finaldeliverable"+str(finalDeliverables))
		deliverable = row["Deliverable"].strip()
		deliverable_type = row["Deliverable_Type"].strip()
		if not deliverable_type:
			if deliverable == 'Total':
				deliverable_type = 'Total'
			elif deliverable == 'Off-Site':
				deliverable_type = 'Offsite'
			elif deliverable == 'On-Site':
				deliverable_type = 'Onsite'
		Trace.Write("deliverable: {}, deliverable_type: {}".format(deliverable, deliverable_type))
		Trace.Write("finalDeliverables_set"+str(finalDeliverables_set))
		if (deliverable,deliverable_type) not in finalDeliverables_set:
			Trace.Write("deliverable_delete: {}, deliverable_type_delete: {}".format(deliverable, deliverable_type))
			deleteRowsList.append(row.RowIndex)

	deleteRowsList.reverse()
	for deleteRow in deleteRowsList:
		container.DeleteRow(deleteRow)

	onSiteHeaderRowIndex = None
	shouldReOrder = False

	for row in container.Rows:
		if row['Deliverable'] == 'On-Site':
			onSiteHeaderRowIndex = row.RowIndex
		elif row['Deliverable_Type'] == 'Offsite' and onSiteHeaderRowIndex and (row.RowIndex > onSiteHeaderRowIndex):
			shouldReOrder = True

	if shouldReOrder:
		offSiteList = []
		onSiteList = []
		deleteRowIndexes = []

		for row in container.Rows:
			rowData = {}
			rowData['IsSelected'] = row.IsSelected

			for col in row.Columns:
				rowData[col.Name] = col.Value

			if row['Deliverable_Type'] == 'Offsite' and row.RowIndex > onSiteHeaderRowIndex:
				offSiteList.append(rowData)
			elif row['Deliverable'] == 'On-Site' or row['Deliverable_Type'] in ('Onsite', 'On-Site'):
				onSiteList.append(rowData)

			if row.RowIndex >= onSiteHeaderRowIndex:
				deleteRowIndexes.append(row.RowIndex)

		deleteRowIndexes.reverse()
		for rowIndex in deleteRowIndexes:
			container.DeleteRow(rowIndex)

		for data in offSiteList:
			row = container.AddNewRow(False)
			for key, val in data.items():
				if key == 'IsSelected':
					row.IsSelected = val
				else:
					row[key] = val

		for data in onSiteList:
			row = container.AddNewRow(False)
			for key, val in data.items():
				if key == 'IsSelected':
					row.IsSelected = val
				else:
					row[key] = val