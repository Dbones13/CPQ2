def pricing_summarytableUpdate(QT_pricing_summary, category, total, count, flag):
	new_row = QT_pricing_summary.AddNewRow()
	new_row['Pricing_Category'] = category
	new_row['Sell_Price'] = total
	new_row['Index_num'] = count
	new_row['Row_flag'] = flag

def pricing_summarytableUpdate_R2Q(QT_pricing_summary, value):
	new_row = QT_pricing_summary.AddNewRow()
	new_row['Product'] = value[0]
	new_row['Description'] = value[1]
	new_row['Sell_Price'] = value[2]
	new_row['Status'] = value[3]

def custom_field_update(item,support_care_ind,no_support_care_ind,custom_field_value):
	support_care = False
	for attr in item.SelectedAttributes:
		if attr.Name == "Enhanced Support-Cyber CARE":
			for data in attr.Values:
				if data.Display != '':
					support_care = True
					custom_field_value[support_care_ind] = item.ProductName+'_Care'
	if support_care == False:
		custom_field_value[no_support_care_ind] = item.ProductName+'_Hardening'

def populatecyberlooseparts(Quote, bomDict):
	table = Quote.QuoteTables["CYBER_BOM_Table"]
	table.Rows.Clear()
	counter = 1
	if bomDict:
		row = table.AddNewRow()
		row["Item_GUID"] = ""
		row["Part_Description"] = "Additional Parts"
	for part , partData in bomDict.items():
		if part != 'CYBER' and not part.startswith('Write-In') and (Quote.GetCustomField('cyberProductPresent').Content == 'Yes' or Quote.GetCustomField('cyberparts').Content == 'Yes'):
			row = table.AddNewRow()
			row["Item_Number"] = counter
			row["Part_Number"] = part
			row["Part_Description"] = partData[0]
			row["Qty"] = int(partData[1])
			counter += 1
	table.Save()

def cyber_proposal(Quote):
	productpricing_dict = {}
	BomDict = dict()
	additionalparts_sellprice = 0

	#R2Q
	new_dict = {}
	rolledupvalue = ''
	rolledup_dict = {}
	productorder = {'Assessments':1,'PCN Hardening':2,'MSS':3,'SMX':4,'Cyber App Control':5}
	productpricing_dict_R2Q = {}
	#R2Q

	# Mapping of product names to their corresponding index positions in the custom field value
	product_mapping = {
		'Assessments': 0,  # Replace the first value ('1') with 'Assessments'
		'PCN Hardening': 2,  # Replace the second value ('2') with 'PCN Hardening'
		'MSS': 4,  # Replace the third value ('3') with 'MSS'
		'SMX': 5,  # Replace the fourth value ('4') with 'SMX'
		'Cyber App Control': 6  # Replace the fifth value ('5') with 'Cyber App Control'
	}

	# Initial custom field value (starting with '1||2||3||4||5')
	custom_field_value = ['1', '2', '3', '4', '5', '6', '7', '8']

	key_list = set()
	CF_CyberBOMflag = ''

	product_counts = {prd: 0 for prd in ['Cyber','SMX','MSS','PCN Hardening','Assessments','Cyber App Control','Cyber Generic System']}

	# Loop through items in the quote only if the cyber part numbers is present in the quote
	for item in Quote.Items:

		# R2Q
		if item.ProductName in ['SMX','PCN Hardening','Cyber App Control','MSS','Assessments']:
			rolledupvalue = item.RolledUpQuoteItem
			if item.ProductName == 'Assessments':
				for attr in item.SelectedAttributes:
					if attr.Name == "Assessment Type":
						for data in attr.Values:
							prd_name = 'Cybersecurity Vulnerability Assessment' if str(data.Display) == 'Cyber' else 'ICS Network Assessment'
							break
				rolledup_dict[rolledupvalue] = prd_name
			else:
				rolledup_dict[rolledupvalue] = item.ProductName
		if rolledupvalue and rolledupvalue in item.RolledUpQuoteItem:
			if rolledup_dict[rolledupvalue] in productpricing_dict_R2Q.keys():
				productpricing_dict_R2Q[rolledup_dict[rolledupvalue]][item.PartNumber] = item.ExtendedAmount
			else:
				productpricing_dict_R2Q[rolledup_dict[rolledupvalue]] = {item.PartNumber:item.ExtendedAmount}
		else:
			if item.PartNumber in productpricing_dict_R2Q.keys():
				productpricing_dict_R2Q[item.PartNumber][item.PartNumber] = productpricing_dict_R2Q.get(item.PartNumber, {}).get(item.PartNumber, 0) + item.ExtendedAmount
			productpricing_dict_R2Q[item.PartNumber] = {item.PartNumber:item.ExtendedAmount}
		# R2Q

		if item.ProductName in product_counts:
			product_counts[item.ProductName] += 1
		# Add part numbers and their extended amounts to the dictionary
		productpricing_dict[item.PartNumber] = productpricing_dict.get(item.PartNumber, 0) + item.ExtendedAmount

		if '.' not in item.RolledUpQuoteItem:
			partData = BomDict.get(item.PartNumber , ["" , 0,""])
			partData[0] = item.Description
			partData[1] += item.Quantity
			partData[2] = item.ProductTypeName
			BomDict[item.PartNumber] = partData

		if item.ProductName in product_mapping:
			CF_CyberBOMflag = (CF_CyberBOMflag + item.ProductName).join("||")
			key_list.add(item.ProductName)
			if item.ProductName == 'Assessments':
				for attr in item.SelectedAttributes:
					if attr.Name == "Assessment Type":
						for data in attr.Values:
							index = 0 if str(data.Display) == 'Cyber' else 1
							custom_field_value[index] = data.Display+' Assessments'
							key_list.add(str(data.Display)+'_Assessments')
			elif item.ProductName == 'PCN Hardening':
				custom_field_update(item,2,3,custom_field_value)
				key_list.add('SAT')
				for attr in item.SelectedAttributes:
					if attr.Name == "FDS & DDS Documentation Required":
						for data in attr.Values:
							if data.Display != '':
								CF_CyberBOMflag = (CF_CyberBOMflag + 'PCN_FDS').join("||")
					elif attr.Name == "FAT Document Verification and Execution":
						for data in attr.Values:
							if data.Display != '':
								CF_CyberBOMflag = (CF_CyberBOMflag + 'PCN_FAT').join("||")
								key_list.add('FAT')
					elif attr.Name == 'Domain':
						for row in item.SelectedAttributes.GetContainerByName('Domain').Rows:
							if row.RowIndex == 1 and (int(row['Domain_1']) > 0 or int(row['Domain_2']) > 0 or int(row['Domain_3']) > 0):
								key_list.add('Window_System')
							elif row.RowIndex == 2 and (int(row['Domain_1']) > 0 or int(row['Domain_2']) > 0 or int(row['Domain_3']) > 0):
								key_list.add('Network_Device')
							elif row.RowIndex == 3 and (int(row['Domain_1']) > 0 or int(row['Domain_2']) > 0 or int(row['Domain_3']) > 0):
								key_list.add('Firewall')
			elif item.ProductName == 'Cyber App Control':
				custom_field_update(item,6,7,custom_field_value)
				for data in item.SelectedAttributes:
					if data.Name == "SAT Document Verification and Execution":
						for val in data.Values:
							if val.Display != '':
								CF_CyberBOMflag = (CF_CyberBOMflag + 'CAC_SAT').join("||")
								key_list.add('SAT')
					elif data.Name == "FDS & DDS Documentation Required":
						for val in data.Values:
							if val.Display != '':
								CF_CyberBOMflag = (CF_CyberBOMflag + 'CAC_FDS').join("||")
					elif data.Name == "FAT Document Verification and Execution":
						for val in data.Values:
							if val.Display != '':
								CF_CyberBOMflag = (CF_CyberBOMflag + 'CAC_FAT').join("||")
								key_list.add('FAT')
			elif item.ProductName == 'MSS':
				index = product_mapping[item.ProductName]
				custom_field_value[index] = item.ProductName
				for data in item.SelectedAttributes:
					if data.Name == "Patching and Anti-Virus Required":
						for val in data.Values:
							if val.Display != '':
								CF_CyberBOMflag = (CF_CyberBOMflag + 'PATCH').join("||")
								key_list.add('Patch_Antivirus')
					elif data.Name == "SAT Document Verification and Execution":
						for val in data.Values:
							if val.Display != '':
								CF_CyberBOMflag = (CF_CyberBOMflag + 'MSS_SAT').join("||")
								key_list.add('SAT')
					elif data.Name == "FDS & DDS Documentation Required":
						for val in data.Values:
							if val.Display != '':
								CF_CyberBOMflag = (CF_CyberBOMflag + 'MSS_FDS').join("||")
					elif data.Name == "FAT Document Verification and Execution":
						for val in data.Values:
							if val.Display != '':
								CF_CyberBOMflag = (CF_CyberBOMflag + 'MSS_FAT').join("||")
								key_list.add('FAT')
					elif data.Name == "Onsite Support Implementation Services":
						for val in data.Values:
							if val.Display != '':
								key_list.add('OnSite_Support')
					elif data.Name == "Number of Windows Assets":
						for val in data.Values:
							if val.Display != '' and int(val.Display)>0:
								CF_CyberBOMflag = (CF_CyberBOMflag + 'NumberofWindowsAssets').join("||")
			elif item.ProductName == 'SMX':
				index = product_mapping[item.ProductName]
				custom_field_value[index] = item.ProductName
				for data in item.SelectedAttributes:
					if data.Name == "Include Services":
						for val in data.Values:
							if val.Display != '':
								CF_CyberBOMflag = (CF_CyberBOMflag + 'SMX_Include_Services').join("||")
								key_list.add('Onsite_Configuration')

	# Join the modified list back into a string with '||' as the separator
	custom_field_value_str = '||'.join(custom_field_value)

	# Assign the resulting content to the Cyberproposalorder custom field
	Quote.GetCustomField("CF_Cyberproposalorder").Content = custom_field_value_str

	for product, count in product_counts.items():
		if count > 1 and product != 'Cyber':
			CF_CyberBOMflag = (CF_CyberBOMflag + 'proceed_flag_bundle_True').join("||")
			break
	Quote.GetCustomField('CF_CyberBOMflag').Content = CF_CyberBOMflag

	has_other_products = any(product != 'SMX' and not product.isdigit() for product in Quote.GetCustomField("CF_Cyberproposalorder").Content.split('||'))
	if has_other_products == True and Quote.GetCustomField("Opportunity Type").Content == 'Project':
		Quote.GetCustomField("CF_CyberDoc_AppendixH").Content = 'True'
	else:
		Quote.GetCustomField("CF_CyberDoc_AppendixH").Content = ''

	# Query for pricing summary categories for part numbers
	pricing_summarytable_query = SqlHelper.GetList(
		"SELECT Pricing_SummaryCategory, Part_Number FROM CT_CYBER_PRICINGLISTTYPE WHERE Part_Number IN ({})".format(
			', '.join("'"+str(part)+"'" for part in productpricing_dict.keys())
		)
	)

	# Dictionary to map part numbers to their pricing categories
	productcategory_dict = {data.Part_Number: data.Pricing_SummaryCategory for data in pricing_summarytable_query}

	# Initialize categories
	categories = {
		'Hardware & Licenses': 0,
		'Cybersecurity Services': 0,
		'Product - Enhanced Support': 0,
		'Product Subscription - Software, Support and Services': 0,
		'Travel & Living': 0,
		'Additional Parts': 0
	}
	main_product = ['SMX','PCN','CYBER_APP_CNTRL','MSS','ASSESSMENT','Cyber Generic System','CYBER']

	# Group parts into categories or additional parts - Non R2Q
	if Quote.GetCustomField('IsR2QRequest').Content == '':
		for partnumber, sellprice in productpricing_dict.items():
			if partnumber in productcategory_dict:
				category = productcategory_dict[partnumber]
				if category in categories:
					categories[category] += productpricing_dict[partnumber]
			else:
				# Group as additional parts if not in the pricing list
				if partnumber not in main_product:
					categories['Additional Parts'] += productpricing_dict[partnumber]
					additionalparts_sellprice += productpricing_dict[partnumber]
	# Group parts into categories or additional parts - Non R2Q

	# R2Q
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
		for prd_name, val in productpricing_dict_R2Q.items():
			for partnumber, sellprice in val.items():
				if partnumber in productcategory_dict:
					category = productcategory_dict.get(partnumber)
					if category in categories:
						if prd_name and prd_name in new_dict:
							if category in new_dict.get(prd_name, {}):
								existing_price = new_dict[prd_name][category][2]
								new_dict[prd_name][category][2] = existing_price + sellprice                        
							else:
								new_dict[prd_name][category] = [prd_name, category, sellprice, 'Child', productorder.get(prd_name)]
						else:
							new_dict[prd_name] = {category:[prd_name, category, sellprice, 'Parent', productorder.get(prd_name)]}
				else:
					additional_parts_category = 'Additional Parts'
					if partnumber not in main_product:
						if additional_parts_category in new_dict.get('Additional Parts', {}):
							existing_price = new_dict['Additional Parts'][additional_parts_category][2]
							new_dict['Additional Parts'][additional_parts_category][2] = existing_price + productpricing_dict[partnumber]
						else:
							new_dict['Additional Parts'] = {additional_parts_category: [additional_parts_category,"", productpricing_dict[partnumber], 'Total', 6]}
		
	grand_total = 0
	for product in new_dict:
		total_price = 0  
		for category in new_dict[product]:
			total_price += new_dict[product][category][2]
		
		if product != 'Additional Parts':
			new_dict[product][product+"_Total"] = [product+" Total","", total_price, "Total", new_dict[product][category][4]]
		
		grand_total += total_price
		
	new_dict["Grand Total"] = ["Grand Total","", grand_total, "Total", 7]
	# R2Q

	# Prepare summary table
	QT_pricing_summary = Quote.QuoteTables['QT_Cyber_Doc_PricingSummary']
	QT_pricing_summary.Rows.Clear()

	# Non R2Q
	if Quote.GetCustomField('IsR2QRequest').Content == '':
		count = 0
		for category, total in categories.items():
			if total != 0:
				count += 1
				pricing_summarytableUpdate(QT_pricing_summary, category, total, count, '')

		# Add total row
		pricing_summarytableUpdate(QT_pricing_summary, 'Proposal Total', sum(categories.values()), count + 1, 'Footer')
	# Non R2Q

	# R2Q
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
		order = ['ICS Network Assessment', 'Cybersecurity Vulnerability Assessment', 'PCN Hardening', 'MSS', 'SMX', 'Cyber App Control', 'Additional Parts', 'Grand Total']

		ordered_keys = [key for key in order if key in new_dict]

		def process_items(QT_pricing_summary,items):

			parent_items = {k: v for k, v in items.items() if v[3] == 'Parent'}
			child_items = {k: v for k, v in items.items() if v[3] == 'Child'}
			total_items = {k: v for k, v in items.items() if v[3] == 'Total'}
			
			for sub_key, sub_value in parent_items.items():
				if int(sub_value[2])>0:
					pricing_summarytableUpdate_R2Q(QT_pricing_summary, sub_value)
				
			for sub_key, sub_value in child_items.items():
				if int(sub_value[2])>0:
					pricing_summarytableUpdate_R2Q(QT_pricing_summary, sub_value)
				
			for sub_key, sub_value in total_items.items():
				if int(sub_value[2])>0:
					pricing_summarytableUpdate_R2Q(QT_pricing_summary, sub_value)

		QT_pricing_summary = Quote.QuoteTables['QT_Cyber_Doc_PricingSummary']
		QT_pricing_summary.Rows.Clear()

		for key in ordered_keys:
			value = new_dict[key]

			if isinstance(value, dict):
				process_items(QT_pricing_summary,value)
			else:
				if int(value[2])>0:
					pricing_summarytableUpdate_R2Q(QT_pricing_summary, value)
	#R2Q

	populatecyberlooseparts(Quote, BomDict)

	if Quote.GetCustomField('IsR2QRequest').Content == '':
		# obtaining all the Keyresponsibilities from Custom table
		key_resp = SqlHelper.GetList("SELECT Product, Data, Sub_Header, Customer, Honeywell FROM CT_CYBER_PROPOSAL_CUSTOMERRESPONSIBILITES WHERE Proposal_Section = 'Key_Responsibilities'")

		# Assign to Quote Table - QT_Cyber_Doc_KeyResponsibilities
		QT_KeyResp = Quote.QuoteTables['QT_Cyber_Doc_KeyResponsibilities']
		QT_KeyResp.Rows.Clear()
		for data in key_resp:
			if data.Product in key_list or data.Product == '':
				if data.Sub_Header in key_list or data.Sub_Header == '':
					new_row = QT_KeyResp.AddNewRow()
					new_row['Key_Responsibilities'] = data.Data
					new_row['Customer'] = data.Customer
					new_row['Honeywell'] = data.Honeywell
# Cyber changes completed