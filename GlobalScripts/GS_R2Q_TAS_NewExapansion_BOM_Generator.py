#salesOrg = Quote.SelectedMarket.MarketCode.partition('_')[0]
salesOrg = Quote.GetCustomField('Sales Area').Content
query = SqlHelper.GetList("Select Part_Number from HPS_LABOR_COST_DATA where Sales_Org='{}' ".format(salesOrg))
labor_parts = [x.Part_Number for x in query]
project = ""
for item in Quote.MainItems:
	if item.PartNumber == 'PRJT':
		project = item
		break

parts_dict = {}
sg_num = 0
names_dict = {}
for x in range(32):
	names_dict["CG_{0}".format(x+1)] = row = {}
	row["SG_1"] = row["SG_2"] = row["SG_3"] = row["SG_4"] = row["SG_5"] = row["SG_6"] = row["SG_7"] = row["SG_8"] = row["SG_9"] = row["SG_10"] = "Not Applicable"
	for y in range(16):
		names_dict["CG_{0}_RG_{1}".format(x+1,y+1)] = row = {}
		row["SG_1"] = row["SG_2"] = row["SG_3"] = row["SG_4"] = row["SG_5"] = row["SG_6"] = row["SG_7"] = row["SG_8"] = row["SG_9"] = row["SG_10"] = "Not Applicable"
area = {}
ioSum1=[]
cg_rg_map = {}
def PartsData(system):
    cg_num = Sr_Num=0
    for Tank_child in system.Children:
        if Tank_child.PartNumber not in labor_parts:
            if (Tank_child.PartNumber not in system_items) or (Tank_child.ProductName in ["WriteIn","Write-In"]): #New part needs to be added
                if Tank_child.ProductName in ["WriteIn","Write-In"]:
                    Sr_Num +=1
                    R2QWriteIn =str(Tank_child.PartNumber)+"|"+str(Sr_Num)
                    part = system_items[R2QWriteIn] = {}
                    part["Description"] = Tank_child.QI_ExtendedDescription.Value
                else:
                    part = system_items[Tank_child.PartNumber] = {}
                    part["Description"] = Tank_child.ProductName
                part["Product_Line"] = str(Tank_child.QI_PLSG.Value)
                part["Total"] = int(Tank_child.Quantity)
                part["System_Items"] = str(Tank_child.Quantity)
            else: #Product already exists
                part = system_items[Tank_child.PartNumber]
                part["Total"] += int(Tank_child.Quantity)
                part["System_Items"] = str(Tank_child.Quantity)
if project != "":
	for sys_group in project.Children:
		sg_num += 1
		gc = 0
		#system_group = parts_dict["{}".format(sg_num)] = {}
		system_group = parts_dict[sg_num] = {}
		system_group["SG_Name"] = sys_group.PartNumber
		for system in sys_group.Children:
			if system.ProductName in ["Tank Gauging Engineering"]:
				gc += 1
				if gc > 1:
					system_items = sample_dictionary
				else:
					system_items = system_group["{0}".format(system.ProductName)] = {}
			elif system.ProductName not in ['Skid and Instruments','Small Volume Prover','Tank Gauging Engineering']:
				system_items = system_group["{0}".format(system.ProductName)] = {}
			if system.ProductName in ['Tank Gauging Engineering']:
				PartsData(system)
				sample_dictionary = system_items
			elif system.ProductName in ['Industrial Security (Access Control)']:
				PartsData(system)
			elif system.ProductName in ['Fire Detection & Alarm Engineering']:
				PartsData(system)
		if sys_group.PartNumber in ['Skid and Instruments']:
			system_items = system_group["{0}".format(sys_group.PartNumber)] = {}
			PartsData(sys_group)
		if sys_group.PartNumber in ['Small Volume Prover']:
			system_items = system_group["{0}".format(sys_group.PartNumber)] = {}
			PartsData(sys_group)
for item in Quote.MainItems:
	vfdquery = SqlHelper.GetFirst("Select VFD_VC_Model from VFD_VC_Models where VFD_VC_Model = '{}'".format(item.PartNumber))
	vfdsparequery = SqlHelper.GetFirst("Select VFD_VC_Model from VFD_VC_Models where VFD_VC_Model = '{}'".format(item.QI_ParentVcModel.Value))
	if vfdquery is not None or vfdsparequery is not None:
		if area.get(item.QI_Area.Value):
			dict = {}
			dict["Model Number"] = item.PartNumber
			dict["Model Description"] = item.Description
			dict["Product Line"] = item.QI_PLSG.Value
			dict["Quantity"] = str(item.Quantity)

			for key in area[item.QI_Area.Value]:
				area[item.QI_Area.Value][key].append(dict)

Trace.Write("PAS BOM parts: {}".format(parts_dict))
#=============================================================
#Section that loops through dictionary and adds it to the quote table
quoteTable = Quote.QuoteTables["BOM_Table_for_Proposals"]
Tank_Gauging =Access_Control =Fire_Detection=Prover=Skid=0

for sg_id,sys_group in sorted(parts_dict.items()):
	for system_name in sys_group:
		if system_name == 'SG_Name': #Skips the name, because it isn't a system.
			continue
		system = sys_group[system_name]

		for part_num in system:
			part = system[part_num]
			row = quoteTable.AddNewRow()
			if system_name == 'Tank Gauging Engineering':
				Tank_Gauging += 1
				row['S_Number'] = Tank_Gauging
			elif system_name == 'Industrial Security (Access Control)':
				Access_Control += 1
				row['S_Number'] = Access_Control
			elif system_name == 'Fire Detection & Alarm Engineering':
				Fire_Detection += 1
				row['S_Number'] = Access_Control
			elif system_name == 'Skid and Instruments':
				Skid += 1
				row['S_Number'] = Skid
			elif system_name == 'Small Volume Prover':
				Prover += 1
				row['S_Number'] = Prover
			if "|" in part_num:
				ModName=part_num.split('|')
				part_num = ModName[0]
			row['Model_Number'] = part_num
			#Trace.Write("Result part_num {} system_name {} sys_group {}".format(part_num,system_name,sys_group['SG_Name']))
			row['Sys_Name'] = "Industrial Security" if system_name =='Industrial Security (Access Control)' else system_name
			row['SG_Name'] = sys_group['SG_Name']
			#Trace.Write(system_name)
			row['SG_ID'] = sg_id

			for entry in part:
				row[entry] = part.get(entry)

quoteTable.Save()

#Section to update names table
names_table = Quote.QuoteTables["PAS_BOM_Group_Names"]
for col_name, column_dict in sorted(names_dict.items()):
	column_dict = names_dict[col_name]
	test3 = repr(column_dict)
	test4 = col_name
	row = names_table.AddNewRow()
	row['Column_ID'] = col_name

	for entry in column_dict:
		row[entry] = column_dict.get(entry)

names_table.Save()