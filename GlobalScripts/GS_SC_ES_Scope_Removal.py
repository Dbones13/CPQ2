#GS_SC_ES_Scope_Removal
if Product.Name != "Service Contract Products":
	Product_type = Product.Attr('SC_Product_Type').GetValue()
	if Product_type == 'Renewal':
		from GS_EanbledServices_functions import assets_container_update

		def ResetValue(partCont, backupColumnMapping, ES_Asset_Summary):
			for row in partCont.Rows:
				for backupColumn in backupColumnMapping.keys():
					column = backupColumnMapping[backupColumn]
					row[column] = row[backupColumn] if str(row[backupColumn]).strip() != '' else '0'
				row.Calculate()
			row_cont = partCont.Rows.Count
			for row1 in ES_Asset_Summary.Rows:
				row1["CY_List_Price"] = row1["CY_List_Price_Backup"] if str(row1["CY_List_Price_Backup"]).strip() != '' else '0'
				row1["No_MSID_CY"] = str(row_cont)
				row1.Calculate()

		partCont = Product.GetContainerByName("Asset_details_ServiceProd")
		ES_Asset_Summary = Product.GetContainerByName("ES_Asset_Summary")
		#container = Product.GetContainerByName("ESComparisonSummary")
		changedRow = None
		pyServiceProduct = ""
		container = Product.GetContainerByName("ESComparisonSummary")
		if container.Rows.Count > 0:
			contRows = container.Rows
			changedRow = contRows[0]
			pyServiceProduct = changedRow['Service_Product']
		#contRows = container.Rows
		#changedRow = contRows[0]
		cyServiceProduct = Product.Attr('EnabledServices_servprod').GetValue()
		#pyServiceProduct = changedRow['Service_Product']
		backupColumnMapping = {'Servers_Backup': 'Servers', 'Workstations_Backup': 'Workstations', 'Windows - Other_Backup': 'Windows - Other', 'TPN Nodes_Backup': 'TPN Nodes', 'Controllers_Backup': 'Controllers', 'Switches_Backup': 'Switches', 'SCADA Servers_Backup': 'SCADA Servers', 'Safety Manager_Backup': 'Safety Manager', 'List Price_Backup': 'List Price'}
		totalListPrice = partCont.TotalRow.Columns['List Price'].Value
		exchange_rate = 1
		if Quote:
			exchange_rate = float(Quote.GetCustomField('Exchange Rate').Content)
		if changedRow and changedRow.IsSelected:
			if cyServiceProduct == pyServiceProduct:
				for row in partCont.Rows:
					for backupColumn in backupColumnMapping.keys():
						column = backupColumnMapping[backupColumn]
						columnValue = int(float(row[column])) if str(row[column]).strip() != '' else 0
						if columnValue > 0:
							row[backupColumn] = row[column]
						row[column] = '0'
					row.Calculate()
				for row1 in ES_Asset_Summary.Rows:
					row1["CY_List_Price_Backup"] = row1["CY_List_Price"]
					row1["CY_List_Price"] = "0"
					row1.Calculate()
					row1["No_MSID_CY"] = "0"
				"""Matrix_Lic = float(Product.Attr('SC_ES_Matrikon_License').GetValue()) if Product.Attr('SC_ES_Matrikon_License').GetValue() != '' else 0
				changedRow['Configured_PY_List_Price'] = str(float(Product.GetContainerByName('ES_PY_Asset_Details').TotalRow.Columns['List Price'].Value) + Matrix_Lic)
				discount_percent = ((float(changedRow['PY_List_Price_SFDC']) - float(changedRow['PY_Sell_Price_SFDC']))/float(changedRow['PY_List_Price_SFDC']) if float(changedRow['PY_List_Price_SFDC']) != '' else 0)
				changedRow['Configured_PY_Sell_Price'] = str(float(changedRow['Configured_PY_List_Price']) - (float(changedRow['Configured_PY_List_Price']) * discount_percent))
				changedRow['List_Price_Delta'] = str(float(changedRow['PY_List_Price_SFDC']) - float(changedRow['Configured_PY_List_Price']))
				changedRow['Sell_Price_Delta'] = str(float(changedRow['PY_Sell_Price_SFDC']) - float(changedRow['Configured_PY_Sell_Price']))"""
			else:
				if float(totalListPrice) == 0.0:
					ResetValue(partCont, backupColumnMapping, ES_Asset_Summary)
				for row1 in ES_Asset_Summary.Rows:
					row1["PY_List_Price"] = "0"
					row1["PY_ListPrice"] = row1["PY_List_Price"]
					row1["PY_SellPrice"] = "0"
					row1.Calculate()
					row1["No_MSID_PY"] = "0"
				changedRow['Configured_PY_List_Price'] = '0'
				changedRow['List_Price_Delta'] = changedRow['PY_List_Price_SFDC']
				changedRow['Configured_PY_Sell_Price'] = '0'
				changedRow['Sell_Price_Delta'] = changedRow['PY_Sell_Price_SFDC']
				#changedRow.Calculate()
		else:
			if float(totalListPrice) == 0.0:
				ResetValue(partCont, backupColumnMapping, ES_Asset_Summary)
		assets_container_update(partCont,cyServiceProduct,exchange_rate,Product.Attr('SC_Service_Product').GetValue())
		partCont.Calculate()