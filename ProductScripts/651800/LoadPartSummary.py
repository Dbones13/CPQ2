if (Product.Attr('R2QRequest').GetValue() == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == "Submit") or Product.Attr('R2QRequest').GetValue() != 'Yes':

	from System import DateTime
	import GS_UTILITY_CONTAINER_SORT as con
	from GS_CyberProductModule import CyberProduct
	cyber = CyberProduct(Quote, Product, TagParserQuote)

	def fill_partSummarytable(child_partsContainer, selectedproduct):
		# key:value = Product:PartSummaryContainer_Name
		partSummaryDict = { 'SMX':'AR_Cyber_PartsSummary',
							'MSS':'AR_MSS_PartsSummary',
							'PCN Hardening':'AR_PCNH_PartsSummary',
							'Assessments':'AR_Assessments_PartsSummary',
							'Cyber App Control':'AR_CAC_PartsSummary'
							}
		
		parent_partSummary = Product.GetContainerByName(partSummaryDict[selectedproduct])
		parent_partSummary.Rows.Clear()
		count = 0
		# Assigning individual Parent Level PartSummary containers with values
		for row in child_partsContainer.Rows:
			parent_partRow = parent_partSummary.AddNewRow()
			parent_partRow["PartNumber"] = row["PartNumber"]
			parent_partRow["Quantity"] = row["Quantity"]
			parent_partRow["PartDescription"] = row["PartDescription"]
			parent_partRow["PLSG"] = row["PLSG"]
			parent_partRow["plsgDescription"] = row["plsgDescription"]
			parent_partRow["Adj Quantity"] = row["Adj Quantity"]
			qty = round(float(row["Quantity"])) if row["Quantity"] !='' else 0
			adj_qty = round(float(row["Adj Quantity"])) if row["Adj Quantity"] !='' else 0
			parent_partRow["Final Quantity"] =  str(qty + adj_qty)
			parent_partRow["Comments"] = row["Comments"]
			parent_partRow["Attribute"] = row["Attribute"]
			if row["Attribute"] != 'labor' and parent_partRow["Final Quantity"] != '0':
				count += 1
				parent_partRow["container_index"] = str(count)

	def fill_labortable(currentYear, child_laborContainer, selectedproduct):
		attribute_dict = {'SMX':'SMX_Execution_Year_Container','Assessments':'Ass_Execution_Year_Container','PCN Hardening':'PCN_Execution_Year_Container','MSS':'MSS_Execution_Year_Container','Cyber App Control':'CAC_Execution_Year_Container'}
		activitiesDict = {  'SMX':['AR_SMX_Activities','SMX_Execution_Country','SMX_Execution_Year','Sales_Org_SMX'],
							'MSS':['AR_MSS_Activities','MSS_Execution_Country','MSS_Execution_Year','Sales_Org_MSS'],
							'PCN Hardening':['AR_PCNH_Activities','PCNH_Execution_Country','PCNH_Execution_Year','Sales_Org_PCN'],
							'Assessments':['AR_Assessment_Activities','Assessments_Execution_Country','Assessments_Execution_Year','Sales_Org_Assessments'],
							'Cyber App Control':['AR_CAC_Activities','CAC_Execution_Country','CAC_Execution_Year','Sales_Org_CAC']
							}
		
		parent_laborDeliverable = Product.GetContainerByName(activitiesDict[selectedproduct][0])
		parent_laborDeliverable.Rows.Clear()

		for labordata in child_laborContainer.Rows:
			parent_laborRow = parent_laborDeliverable.AddNewRow()
			parent_laborRow["Activity_Type"] = labordata["Activity_Type"]
			parent_laborRow["Activity"] = labordata["Activity"]
			parent_laborRow["Hours"] = labordata["Hours"]
			parent_laborRow["Edit Hours"] = labordata["Edit Hours"]
			parent_laborRow["List_Price"] = labordata["List_Price"]
			parent_laborRow["FO_List_Price"] = labordata["FO_List_Price"]
			parent_laborRow["Productivity"] = labordata["Productivity"]
			parent_laborRow["Comments"] = labordata["Comments"]
			parent_laborRow["FOWTWCost"] = labordata["FOWTWCost"]
			parent_laborRow["Regional_Cost"] = labordata["Regional_Cost"]
			parent_laborRow["FO_MPA_Price"] = labordata["FO_MPA_Price"]
			parent_laborRow["Identifier"] = labordata["Identifier"]
			parent_laborRow["Error_Message"] = labordata["Error_Message"]
			parent_laborRow["Rank"] = labordata["Rank"]
			parent_laborRow["Pricing"] = labordata["Pricing"]
			if labordata["Identifier"] not in ['Total','On-Site','Off-Site']:
				parent_laborRow["PartNumber"] = labordata["PartNumber"]
				parent_laborRow.GetColumnByName('PartNumber').SetAttributeValue(labordata["PartNumber"])
				parent_laborRow["Currency"] = labordata["Currency"]
				parent_laborRow["CostCurrency"] = labordata["CostCurrency"]
				parent_laborRow["Execution Country"] = labordata["Execution Country"]
				parent_laborRow.GetColumnByName('Execution Country').SetAttributeValue(labordata["Execution Country"])
				parent_laborRow["Execution_Year"] = labordata["Execution_Year"]
				parent_laborRow.GetColumnByName('Execution_Year').ReferencingAttribute.SelectDisplayValue(labordata["Execution_Year"])
				not_allowed = cyber.hide_year(selectedproduct)
				parent_laborRow.Product.DisallowAttrValues(attribute_dict[selectedproduct], *not_allowed)
				parent_laborRow.Calculate()

	def update_selected_products():
		cyberproducts = '<br>'.join(row["Part Desc"] for row in Product.GetContainerByName('Cyber Configurations').Rows)
		Product.Attr('AR_Cyber_SelectedProducts').AssignValue(cyberproducts)

	def process_selected_products():
		SelectedProducts = Product.GetContainerByName('Cyber Configurations')
		order_dict = { 'Assessments' : 0,
						'PCN Hardening' : 1,
						'MSS' : 2,
						'SMX' : 3,
						'Cyber App Control' : 4,
						'Project Management': 5
		}
		orderadjustment = []
		for row in SelectedProducts.Rows:
			if row['Part Desc'] not in ['Project Management','Cyber Generic System']:
				if row.Product.Attr('CyberChildFlag').GetValue() == 'True':
					row.Product.Attr('CyberChildFlag').AssignValue('')
					selectedproduct = row['Part Desc']
					currentYear = DateTime.Now.Year
					fill_labortable(currentYear, row.Product.GetContainerByName('Activities'), selectedproduct)
					fill_partSummarytable(row.Product.GetContainerByName('AR_Cyber_PartsSummary'), selectedproduct)
					row['Rank'] = str(order_dict[row['Part Desc']])
				else:
					selectedproduct = row['Part Desc']
					attribute_dict = {'SMX':'SMX_Execution_Year_Container','Assessments':'Ass_Execution_Year_Container','PCN Hardening':'PCN_Execution_Year_Container','MSS':'MSS_Execution_Year_Container','Cyber App Control':'CAC_Execution_Year_Container','Cyber Generic System':'Generic_Execution_Year_Container'}
					activitiesDict = {  'SMX':['AR_SMX_Activities','SMX_Execution_Country','SMX_Execution_Year','Sales_Org_SMX'],
										'MSS':['AR_MSS_Activities','MSS_Execution_Country','MSS_Execution_Year','Sales_Org_MSS'],
										'PCN Hardening':['AR_PCNH_Activities','PCNH_Execution_Country','PCNH_Execution_Year','Sales_Org_PCN'],
										'Assessments':['AR_Assessment_Activities','Assessments_Execution_Country','Assessments_Execution_Year','Sales_Org_Assessments'],
										'Cyber App Control':['AR_CAC_Activities','CAC_Execution_Country','CAC_Execution_Year','Sales_Org_CAC']
										}
					not_allowed = cyber.hide_year(selectedproduct)
					parent_laborDeliverable = Product.GetContainerByName(activitiesDict[selectedproduct][0])
					for row in parent_laborDeliverable.Rows:
						row.Product.DisallowAttrValues(attribute_dict[selectedproduct], *not_allowed)
						row.Calculate()

			orderadjustment.append((SelectedProducts,row['Rank'],row.RowIndex))
		for container, rank, rowindex in orderadjustment:
			con.sortRow(container,rank,rowindex)

	# Execute main functions

	update_selected_products()
	process_selected_products()

	def hide_column(container, Column):
		Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(container, Column))
	def show_column(container, Column):
		Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(container, Column))
	if Product.ParseString('[LIKE](<*CTX ( Container(Cyber Configurations).UniqueValues(Part Desc).Separator(,) )*>,Cyber Generic System)') == '1':
		show_column('Cyber Configurations','Product Name')
		show_column('Cyber Configurations','User_Define_Name')
	else:
		hide_column('Cyber Configurations','Product Name')
		hide_column('Cyber Configurations','User_Define_Name')
#Product.Attr('calculate_value_set').AssignValue('')