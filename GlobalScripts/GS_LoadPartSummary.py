def fillcontainer(partsSummaryTable, attr_name, part_num, quantity, activities,product,exist_dict = None):
	partSummary = SqlHelper.GetList("SELECT A.PRODUCT_CATALOG_CODE, A.PRODUCT_NAME ,B.PARTNUMBER ,B.PLSG,B.PRODUCT_LINE_DESC,B.PRODUCT_LINE_SUBGROUP_DESC  FROM PRODUCTS A JOIN HPS_PRODUCTS_MASTER B ON A.PRODUCT_CATALOG_CODE=B.PARTNUMBER WHERE PRODUCT_CATALOG_CODE ='{}'".format(part_num))
	breakloop = 'False'
	for rows in partsSummaryTable.Rows:
		if product.PartNumber == 'MSS' and str(part_num) == 'CF-MSD000':
			if rows['PartNumber'] == 'CF-MSD000':
				breakloop = 'True'
	
	if breakloop == 'False':
		parts = partsSummaryTable.AddNewRow(False)
		parts['Attribute'] = attr_name
		parts['PartNumber'] = str(part_num)
		parts['Quantity'] = str(quantity) if quantity else '1'  # Use numeric if possible
		for sku_parts in partSummary:
			if parts['PartNumber'] == sku_parts.PARTNUMBER:
				parts['PartDescription'] = sku_parts.PRODUCT_NAME
				parts['PLSG'] = sku_parts.PLSG
				parts['plsgDescription'] = sku_parts.PRODUCT_LINE_DESC +"-"+ sku_parts.PRODUCT_LINE_SUBGROUP_DESC
				if exist_dict != None:
					parts['Adj Quantity'] = exist_dict.get(parts['PartNumber'], '')
				adj_quantity = 0 if parts['Adj Quantity'] == '' else round(float(parts['Adj Quantity']))
				parts['Final Quantity'] = str(int(float(parts['Quantity'])) + adj_quantity)


def get_attributeList(product, attributeName):
	val = product.Attr(attributeName)
	if val is not None and hasattr(val, 'SelectedValues'):
		# Assuming SelectedValues is a list-like structure
		part_num = [value.PartNumber for value in val.SelectedValues]
		quantity = [value.Quantity for value in val.SelectedValues]
		return part_num, quantity
	return [], []

def container_dataLoad(product, partsSummaryTable, attributeList, activities):
	for attr in attributeList:
		attributeName = attr.AttributeName
		part_nums, quantities = get_attributeList(product, attributeName)
		for part_num, quantity in zip(part_nums, quantities):
			fillcontainer(partsSummaryTable, attributeName, part_num, quantity, activities,product)

def labor_add_to_part_summary(product):
	if product.GetContainerByName('Activities').Rows.Count>0:
		part_qty_NMON_ST = 0
		part_qty_NSER_ST = 0
		part_qty_NCOS_ST = 0
		part_qty_NRSC_ST = 0
		hrs = 0
		for row in product.GetContainerByName('Activities').Rows:
			if row['Activity'] == 'Total':
				hrs = row['Edit Hours']
			if row['PartNumber'] == 'SVC-NMON-ST':
				part_qty_NMON_ST += int(float(row['Edit Hours'])) if row['Edit Hours'] !='' else 0.0
			if row['PartNumber'] == 'SVC-NSER-ST':
				part_qty_NSER_ST += int(float(row['Edit Hours'])) if row['Edit Hours'] !='' else 0.0
			if row['PartNumber'] == 'SVC-NCOS-ST':
				part_qty_NCOS_ST += int(float(row['Edit Hours'])) if row['Edit Hours'] else 0
			if row['PartNumber'] == 'SVC-NRSC-ST':
				part_qty_NRSC_ST += int(float(row['Edit Hours'])) if row['Edit Hours'] else 0

		part_qty_dict = {'SVC-NMON-ST':part_qty_NMON_ST,'SVC-NSER-ST':part_qty_NSER_ST,'SVC-NCOS-ST':part_qty_NCOS_ST,'SVC-NRSC-ST':part_qty_NRSC_ST}

		if product.PartNumber == 'ASSESSMENT':
			ass_part = product.Attr('Labour_Part_Number').GetValue()
			if ass_part == '':
				product.Attr('Labour_Part_Number').AssignValue('SVC-NSER-ST')
				ass_part = 'SVC-NSER-ST'
		else:
			ass_part = ''
		activities = {'SMX':'SVC-NMON-ST','MSS':'SVC-NMON-ST','ASSESSMENT':ass_part,'PCN':'SVC-NSER-ST','CYBER_APP_CNTRL':'SVC-NMON-ST'}
		partSummary = SqlHelper.GetFirst("SELECT A.PRODUCT_CATALOG_CODE, A.PRODUCT_NAME ,B.PARTNUMBER ,B.PLSG,B.PRODUCT_LINE_DESC,B.PRODUCT_LINE_SUBGROUP_DESC  FROM PRODUCTS A JOIN HPS_PRODUCTS_MASTER B ON A.PRODUCT_CATALOG_CODE=B.PARTNUMBER WHERE PRODUCT_CATALOG_CODE ='{}'".format(activities[product.PartNumber]))
		partsSummaryTable = product.GetContainerByName('AR_Cyber_PartsSummary')
		breakloop = 'False'
		rowstoDelete = []
		for row in partsSummaryTable.Rows:
			if (row['PartNumber']).StartsWith('SVC'):
				if row['PartNumber'] == str(activities[product.PartNumber]):
					if part_qty_dict[row['PartNumber']]>0:
						row['Quantity'] = str(part_qty_dict[row['PartNumber']])
						adj_quantity = 0 if row['Adj Quantity'] == '' else round(float(row['Adj Quantity']))
						row['Final Quantity'] = str(int(float(row['Quantity'])) + adj_quantity)
						breakloop = 'True'
					else:
						rowstoDelete.append(row.RowIndex)
						breakloop = 'True'
				else:
					if row['PartNumber'] in part_qty_dict.keys() and part_qty_dict[row['PartNumber']]>0:
						row['Quantity'] = str(part_qty_dict[row['PartNumber']])
						adj_quantity = 0 if row['Adj Quantity'] == '' else round(float(row['Adj Quantity']))
						row['Final Quantity'] = str(int(float(row['Quantity'])) + adj_quantity)
						breakloop = 'True'
					if row['PartNumber'] in part_qty_dict.keys() and part_qty_dict[row['PartNumber']]<1:
						rowstoDelete.append(row.RowIndex)
						breakloop = 'True'
		for row_index in sorted(rowstoDelete, reverse=True):
			partsSummaryTable.DeleteRow(row_index)
		if breakloop == 'False':
			if part_qty_dict[activities[product.PartNumber]]>0:
				parts = partsSummaryTable.AddNewRow()
				parts['Attribute'] = 'labor'
				parts['PartNumber'] = str(activities[product.PartNumber])
				parts['Quantity'] = str(part_qty_dict[activities[product.PartNumber]])
				parts['PartDescription'] = partSummary.PRODUCT_NAME
				parts['PLSG'] = partSummary.PLSG
				parts['plsgDescription'] = partSummary.PRODUCT_LINE_DESC +"-"+ partSummary.PRODUCT_LINE_SUBGROUP_DESC
				adj_quantity = 0 if parts['Adj Quantity'] == '' else round(float(parts['Adj Quantity']))
				parts['Final Quantity'] = str(int(float(parts['Quantity'])) + adj_quantity)
	else:
		partsSummaryTable = product.GetContainerByName('AR_Cyber_PartsSummary')
		rowstoDelete = []
		for row in partsSummaryTable.Rows:
			if (row['PartNumber']).StartsWith('SVC'):
				rowstoDelete.append(row.RowIndex)
		for row_index in sorted(rowstoDelete, reverse=True):
			partsSummaryTable.DeleteRow(row_index)

def main(product):

	if product.PartNumber not in ['ASSESSMENT','PCN']:
		partsSummaryTable = product.GetContainerByName('AR_Cyber_PartsSummary')

		attributeList = SqlHelper.GetList("SELECT * FROM CT_VARIANT_ITEMS_TO_CART_MAPPING WHERE Product = '{}'".format(product.PartNumber))
		partSummary = ''
		activities = product.GetContainerByName('Activities')

		command = 'Load Data' if partsSummaryTable is None else 'Modify Data'

		if command == 'Load Data':
			container_dataLoad(product, partsSummaryTable, attributeList, activities)

		elif command == 'Modify Data':
			container_attributeList = [row['Attribute'] for row in partsSummaryTable.Rows]
			newAttributes = [attr.AttributeName for attr in attributeList if attr.AttributeName not in container_attributeList and product.Attr(attr.AttributeName).SelectedValue is not None]
			invalid_attributeList = [attr.AttributeName for attr in attributeList if product.Attr(attr.AttributeName).SelectedValue is None]
			if (product.PartNumber == 'SMX' and product.Attr('Include Services').GetValue() != 'Yes') or (product.PartNumber == 'MSS' and product.Attr('Onsite Support Implementation Services').GetValue() != 'Yes'):
				invalid_attributeList.append('labor')
			exist_partnumber = {row['PartNumber']:row['Quantity'] for row in partsSummaryTable.Rows}
			new_partnumber = []
			for attr in attributeList:
				selected_value = product.Attr(attr.AttributeName).SelectedValue
				if selected_value is not None:
					for value in product.Attr(attr.AttributeName).SelectedValues:
						if value.PartNumber not in exist_partnumber:
							new_partnumber.append(value.PartNumber)
						elif value.PartNumber in exist_partnumber:
							if value.Quantity != int(exist_partnumber[value.PartNumber]):
								new_partnumber.append(value.PartNumber)
			# Iterate in reverse order
			deletelist = []
			exist_dict = {}
			for row in partsSummaryTable.Rows:
				if row['Attribute'] in invalid_attributeList:
					deletelist.append(row.RowIndex)
					exist_dict[row['PartNumber']] = str(round(float(row['Adj Quantity']))) if row['Adj Quantity'] !='' else '0'
				elif new_partnumber and row['PartNumber'] in new_partnumber:
					if row['Attribute'] not in newAttributes:
						newAttributes.append(row['Attribute'])

			for rows in partsSummaryTable.Rows:
				if rows['Attribute'] in newAttributes:
					deletelist.append(rows.RowIndex)
					exist_dict[rows['PartNumber']] = str(round(float(rows['Adj Quantity']))) if rows['Adj Quantity'] !='' else '0'

			if len(deletelist) > 0:
				for row_index in sorted(deletelist, reverse=True):
					partsSummaryTable.DeleteRow(row_index)
			for attr in newAttributes:
				part_nums, quantities = get_attributeList(product, attr)
				for part_num, quantity in zip(part_nums, quantities):
					fillcontainer(partsSummaryTable, attr, part_num, quantity, partSummary,product,exist_dict)

	if (product.PartNumber == 'SMX' and product.Attr('Include Services').GetValue() == 'Yes') or (product.PartNumber == 'MSS' and product.Attr('Onsite Support Implementation Services').GetValue() == 'Yes') or product.PartNumber not in ['SMX','MSS']:
		labor_add_to_part_summary(product)