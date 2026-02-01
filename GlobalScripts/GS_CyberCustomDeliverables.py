from GS_CyberProductModule import CyberProduct
cyber = CyberProduct(Quote, Product, TagParserQuote)

def getcontainer(container_name):
	return Product.GetContainerByName(container_name)

def updatechildproduct(configuredprdname):
	selectedproduct = getcontainer('Cyber Configurations')
	for row in selectedproduct.Rows:
		if row["Part Desc"] == configuredprdname:
			child_container = row.Product.GetContainerByName('Activities')
			return child_container

def loadcontainerdata(product_name, module_name, targetRow, sourceRow, child_update):
	fields_to_copy = [
		"Activity", "Execution Country", "Comments", "CostCurrency"]

	for field in fields_to_copy:
		targetRow[field] = sourceRow[field]

	if child_update:
		not_allowed = cyber.hide_year(module_name)
		targetRow.GetColumnByName('Execution_Year').ReferencingAttribute.SelectDisplayValue(sourceRow['Execution_Year'])
		targetRow.Product.DisallowAttrValues(product_name[module_name], *not_allowed)
		targetRow.GetColumnByName('Execution Country').SetAttributeValue(sourceRow['Execution Country'])
		#targetRow.GetColumnByName('PartNumber').SetAttributeValue(sourceRow['PartNumber'])

	# Default Fields
	targetRow['Hours'] = "0.00"
	targetRow['Edit Hours'] = "0"
	targetRow['Productivity'] = "1"
	targetRow['Activity_Type'] = 'Onsite' if sourceRow['Type'] == 'On-Site' else 'Offsite'
	targetRow['Error_Message'] = 'True'
	targetRow['Identifier'] = str(targetRow['Activity'])+'_'+str(targetRow['Activity_Type'])
	targetRow.Calculate()

def getContainerData(container):
	containerData = {}
	for row in container.Rows:
		containerData[row.RowIndex] = dict()
		for column in row.Columns:
			containerData[row.RowIndex][column.Name] = row[column.Name]
		containerData[row.RowIndex]["Select"] = row.IsSelected
	return containerData

def targetcontainerupdate(targetprdname, targetTable, sourceRow, alterCyberRow, childupdate):

	executionYear_context = {'SMX':'SMX_Execution_Year_Container',
							'MSS':'MSS_Execution_Year_Container',
							'Cyber App Control':'CAC_Execution_Year_Container',
							'Assessments':'Ass_Execution_Year_Container',
							'PCN Hardening':'PCN_Execution_Year_Container',
							'Cyber Generic System':'Generic_Execution_Year_Container'
							}
	
	deliverablePresent = False
	rowdeleteList = []
	for targetRow in targetTable.Rows:

		# If User add any Deliverable again, it will replace the existing
		if targetRow["Activity"] == sourceRow["Activity"] and targetRow["Activity_Type"].lower() == sourceRow["Type"].replace('-','').lower():
			loadcontainerdata(executionYear_context, targetprdname, targetRow, sourceRow, True)
			deliverablePresent = True

	if not deliverablePresent:
		if targetprdname == 'Cyber Generic System':
			first_header = getcontainer('Generic_System_Activities').Rows[1].Columns['Activity'].Value
			next_header = 'On-Site' if first_header == 'Off-Site' else 'Off-Site'
		else:
			first_header = 'Off-Site'
			next_header = 'On-Site'

		if alterCyberRow == '' or alterCyberRow == True:
			if sourceRow['Type'] == first_header:

				# Delete records in Target table if the record present is re-added with different Type
				if rowdeleteList:
					for rows_todelete in sorted(rowdeleteList, reverse=True):
						targetTable.DeleteRow(rows_todelete)

				containerData = getContainerData(targetTable)
				targetTable.Rows.Clear()
				if childupdate:
					childprdContext = updatechildproduct(targetprdname)
					childprdContext.Rows.Clear()


				for data in containerData:
					if containerData[data]["Identifier"] == next_header:
						addRow = targetTable.AddNewRow(False)
						loadcontainerdata(executionYear_context, targetprdname, addRow, sourceRow, True)
						if childupdate:
							childprdContext = updatechildproduct(targetprdname)
							addchildRow = childprdContext.AddNewRow(False)
							loadcontainerdata('', '', addchildRow, sourceRow, False)


					addRow = targetTable.AddNewRow(False)
					if childupdate:
						childprdContext = updatechildproduct(targetprdname)
						addchildRow = childprdContext.AddNewRow(False)
					for column in addRow.Columns:
						for key,value in containerData[data].items():
							if column.Name == key and (column.Name == 'Execution Country' or column.Name == 'Execution_Year' or column.Name == 'PartNumber'):
								addRow[column.Name] = value
								if column.Name == 'Execution_Year':
									not_allowed = cyber.hide_year(targetprdname)
									addRow.GetColumnByName(column.Name).ReferencingAttribute.SelectDisplayValue(value)
									addRow.Product.DisallowAttrValues(executionYear_context[targetprdname], *not_allowed)
								else:
									addRow.GetColumnByName(column.Name).SetAttributeValue(value) 
							else:
								if column.Name == key and column.Name != 'Select':
									addRow[column.Name] = value
							if childupdate and column.Name == key and column.Name != 'Select' and childupdate:
								addchildRow[column.Name] = value

							addRow.Calculate()
							if childupdate:
								addchildRow.Calculate()
			else:
				addRow = targetTable.AddNewRow(False)
				loadcontainerdata(executionYear_context, targetprdname, addRow, sourceRow, True)
				if childupdate:
					childprdContext = updatechildproduct(targetprdname)
					addchildRow = childprdContext.AddNewRow(False)
					loadcontainerdata('', '', addchildRow, sourceRow, False)
		else:
			addRow = targetTable.AddNewRow(False)
			loadcontainerdata(executionYear_context, targetprdname, addRow, sourceRow, True)
			if childupdate:
				childprdContext = updatechildproduct(targetprdname)
				addchildRow = childprdContext.AddNewRow(False)
				loadcontainerdata('', '', addchildRow, sourceRow, False)


productDict = {'SMX':'AR_SMX_Activities',
			   'MSS':'AR_MSS_Activities',
			   'Cyber App Control':'AR_CAC_Activities',
			   'Assessments':'AR_Assessment_Activities',
			   'PCN Hardening':'AR_PCNH_Activities',
			   'Cyber Generic System':'Generic_System_Activities'
			   }

source_deliverableTable = getcontainer('AR_Cyber_AdditionalCustomDeliverable')
alterCyberRow = False
if source_deliverableTable.Rows.Count > 0:
	for row in source_deliverableTable.Rows:
		target_deliverableTable = getcontainer(productDict[row['Product_Module']])

		# Update Cyber Generic Container -->>
		if row['Product_Module'] == 'Cyber Generic System':
			cyberExistingtypes = [parentrow['Activity'] for parentrow in target_deliverableTable.Rows]

			# To check if both On-Site and Off-Site Header present in Cyber Generic product
			if 'On-Site' in cyberExistingtypes and 'Off-Site' in cyberExistingtypes:
				alterCyberRow = True

			count = getcontainer(productDict[row['Product_Module']]).Rows.Count
			if count == 0:
				addtotalheader = target_deliverableTable.AddNewRow()
				addtotalheader['Activity'] = 'Total'
				addtotalheader['Identifier'] = 'Total'
				addtotalheader['Error_Message'] = 'True'
				addtypeheader = target_deliverableTable.AddNewRow()
				addtypeheader['Activity'] = row['Type']
				addtypeheader['Identifier'] = row['Type']
				addtypeheader['Error_Message'] = 'True'
				targetcontainerupdate(row['Product_Module'], target_deliverableTable, row, alterCyberRow, False)
			else:
				if row['Type'] in cyberExistingtypes:
					targetcontainerupdate(row['Product_Module'], target_deliverableTable, row, alterCyberRow, False)
				else:
					# If either Header ('Off-Site', 'On-Site') not present in Cyber container
					addnewRow = target_deliverableTable.AddNewRow()
					addnewRow['Activity'] = row['Type']
					addnewRow['Identifier'] = row['Type']
					addnewRow['Error_Message'] = 'True'
					targetcontainerupdate(row['Product_Module'], target_deliverableTable, row, alterCyberRow, False)

		# Update Containers except Cyber Generic -->>
		else:
			targetcontainerupdate(row['Product_Module'], target_deliverableTable, row, '', True)

source_deliverableTable.Rows.Clear()